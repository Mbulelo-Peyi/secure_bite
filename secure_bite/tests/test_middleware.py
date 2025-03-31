from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from unittest.mock import patch
from secure_bite.middleware import RefreshTokenMiddleware
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class RefreshTokenMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.middleware = RefreshTokenMiddleware(lambda req: HttpResponse())

    @patch('secure_bite.middleware.RefreshToken.for_user')
    def test_process_request_valid_refresh_token(self, mock_for_user):
        # Mocking RefreshToken.for_user to return a mock token
        mock_token = RefreshToken.for_user(self.user)
        mock_for_user.return_value = mock_token

        request = self.factory.get('/')
        request.COOKIES['refresh_token'] = str(mock_token)

        response = self.middleware(request)

        # Check if the access token cookie is set in the response
        self.assertIn('access_token', response.cookies)
        self.assertEqual(response.cookies['access_token'].value, str(mock_token.access_token))

    def test_process_request_no_refresh_token(self):
        request = self.factory.get('/')
        response = self.middleware(request)

        # Ensure no access token is set if there's no refresh token
        self.assertNotIn('access_token', response.cookies)
