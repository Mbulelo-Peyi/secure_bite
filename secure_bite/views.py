from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from secure_bite.authentication import CookieJWTAuthentication
from secure_bite.utils import clear_cookie
from django.conf import settings

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """Authenticates the user using the dynamic username field and password and sets JWT tokens in cookies."""
        
        # Get identifier (username, email or phone) and password from request
        identifier = request.data.get("user_field")  # Expecting "username_or_email_or_phone" as the input field
        password = request.data.get("password")
        
        if not identifier or not password:
            return Response({"error": "Both 'user_field' and 'password' are required."}, status=400)

        # Get the custom user model dynamically
        User = get_user_model()

        # Get the USERNAME_FIELD from the user model (it could be 'username', 'email', or another custom field)
        username_field = User.USERNAME_FIELD
        
        # Create a dictionary to authenticate with the correct username field
        credentials = {username_field: identifier, 'password': password}
        
        # Attempt authentication with the provided username field and password
        user = authenticate(**credentials)
        
        # If user is not found or password doesn't match
        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Prepare the response
        response = Response({"message": "Login successful"})

        # Set the access token in a cookie
        response.set_cookie(
            settings.SIMPLE_JWT["AUTH_COOKIE"],
            access_token,
            max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            httponly=True,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        # Set the refresh token in a cookie
        response.set_cookie(
            "refreshToken",
            refresh_token,
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            httponly=True,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        return response

class LogoutView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """Clears JWT cookies on logout."""
        response = Response({"message": "Logged out"}, status=status.HTTP_200_OK)
        
        # Delete the JWT cookies with the same attributes used to set them from utils clear_cookie
        clear_cookie(response=response,name=settings.SIMPLE_JWT["AUTH_COOKIE"])
        clear_cookie(response=response,name="refreshToken")
        return response


class UserDetails(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = settings.SIMPLE_JWT["TOKEN_OBTAIN_SERIALIZER"] if "TOKEN_OBTAIN_SERIALIZER" in settings.SIMPLE_JWT else TokenObtainPairSerializer

    def get(self, request, *args, **kwargs):
        """Get the current user"""
        user = request.user
        # Serialize the user data using your custom serializer (without including 'id')
        serializer = self.serializer_class(user)

        # Pop the tokens from the serialized data to avoid including them in the response
        serializer.data.pop('access', None)
        serializer.data.pop('refresh', None)

        # Check if 'id' is in the serialized data
        # Manually add the 'id' field if it's missing
        if len(serializer.data.items()) == 0:
            data = {"id":user.id}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProtectedView(APIView):
    """
    Protected endpoint requiring authentication.
    """
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"message": "You are authenticated"}, status=status.HTTP_200_OK)