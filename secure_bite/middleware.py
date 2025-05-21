from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import logging

logger = logging.getLogger(__name__)

class RefreshTokenMiddleware(MiddlewareMixin):
    """Middleware to automatically refresh JWT tokens when expired."""

    def process_request(self, request):
        request.new_access_token = None  # Default: No new token

        refresh_token = request.COOKIES.get("refreshToken")
        if not refresh_token:
            return None  # No refresh token, continue request

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            # Store the new token to be set in the response
            request.new_access_token = new_access_token
        except TokenError:
            logger.warning("Invalid or expired refresh token.")
            request.new_access_token = None
        
    def process_response(self, request, response):
        """If a new token was generated, set it in cookies."""
        if request.new_access_token:
            response.set_cookie(
                settings.SIMPLE_JWT["AUTH_COOKIE"],
                request.new_access_token,
                max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],  # 15 minutes
                httponly=True,
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
        return response