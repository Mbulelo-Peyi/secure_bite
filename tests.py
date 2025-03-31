from django.test import TestCase, Client
from django.urls import reverse

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_sets_cookies(self):
        response = self.client.post(reverse("secure_bite:login"))
        self.assertIn("authToken", response.cookies)

    def test_logout_clears_cookies(self):
        self.client.post(reverse("secure_bite:login"))
        response = self.client.post(reverse("secure_bite:logout"))
        self.assertNotIn("authToken", response.cookies)

    def test_protected_route_requires_authentication(self):
        response = self.client.get(reverse("secure_bite:protected"))
        self.assertEqual(response.status_code, 403)
