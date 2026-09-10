from rest_framework.test import APITestCase

from accounts.models import User


class PasswordSecurityTests(APITestCase):
    url = "/api/v1/auth/register/"

    def test_same_password_produces_different_hashes_for_different_users(self):
        first = User.objects.create_user(email="a@example.com", password="Str0ng-Passw0rd!")
        second = User.objects.create_user(email="b@example.com", password="Str0ng-Passw0rd!")

        self.assertNotEqual(first.password, second.password)

    def test_registration_rejects_common_password(self):
        response = self.client.post(
            self.url, {"email": "common@example.com", "password": "password123"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], "VALIDATION_ERROR")

    def test_registration_rejects_entirely_numeric_password(self):
        response = self.client.post(
            self.url, {"email": "numeric@example.com", "password": "18273645"}
        )

        self.assertEqual(response.status_code, 400)

    def test_registration_rejects_password_too_similar_to_email(self):
        response = self.client.post(
            self.url,
            {"email": "basel2026@example.com", "password": "basel2026"},
        )

        self.assertEqual(response.status_code, 400)


class SessionCookieSecurityTests(APITestCase):
    def test_session_cookie_is_httponly(self):
        User.objects.create_user(email="consumer@example.com", password="Str0ng-Passw0rd!")

        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": "consumer@example.com", "password": "Str0ng-Passw0rd!"},
        )

        session_cookie = response.cookies.get("sessionid")
        self.assertIsNotNone(session_cookie)
        self.assertTrue(session_cookie["httponly"])

    def test_csrf_cookie_is_not_httponly(self):
        # Must be JS-readable — the frontend reads it to send X-CSRFToken (ADR-007).
        response = self.client.get("/api/v1/auth/csrf/")

        csrf_cookie = response.cookies.get("csrftoken")
        self.assertIsNotNone(csrf_cookie)
        self.assertFalse(csrf_cookie["httponly"])