from django.test import TestCase, RequestFactory
from rest_framework.exceptions import AuthenticationFailed
from secure_bite.authentication import CookieJWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()


class CookieJWTAuthenticationTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.authenticator = CookieJWTAuthentication()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_authenticate_valid_token(self):
        token = AccessToken.for_user(self.user)
        request = self.factory.get('/')
        request.COOKIES['authToken'] = str(token)

        user, validated_token = self.authenticator.authenticate(request)
        self.assertEqual(user, self.user)
        self.assertEqual(str(validated_token), str(token))

    def test_authenticate_no_token(self):
        request = self.factory.get('/')
        result = self.authenticator.authenticate(request)
        self.assertIsNone(result)

    def test_authenticate_invalid_token(self):
        """Invalid tokens should simply return None, not raise AuthenticationFailed"""
        request = self.factory.get("/")
        request.COOKIES["authToken"] = "invalidtoken"

        result = self.authenticator.authenticate(request)
        self.assertIsNone(result)
