from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a user to ensure login works
        User = get_user_model()
        self.user = User.objects.create_user(username="testUser", password="Testing321")
        self.credentials = {
            "user_field": "testUser",
            "password": "Testing321"
        }

    def test_login_sets_cookies(self):
        # Login request
        response = self.client.post(
            path=reverse("secure_bite:login"),
            data=self.credentials,
            content_type="application/json"
        )
        # Check if 'authToken' is in the response cookies
        self.assertIn("authToken", response.cookies)
        self.assertIn("refreshToken", response.cookies)
        

    def test_logout_clears_cookies(self):
        # Login first
        self.client.post(reverse("secure_bite:login"), content_type="application/json")
        # Logout request
        response = self.client.post(reverse("secure_bite:logout"))
        # Check if the cookie is cleared
        self.assertNotIn("authToken", response.cookies)
        self.assertNotIn("refreshToken", response.cookies)

    def test_protected_route_requires_authentication(self):
        # Try to access the protected route without being authenticated
        response = self.client.get(reverse("secure_bite:protected"))
        # Expect 401 Unauthorized as the user is not authenticated
        self.assertEqual(response.status_code, 401)
