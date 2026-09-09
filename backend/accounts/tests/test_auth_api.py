from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User


class RegisterViewTests(APITestCase):
    url = "/api/v1/auth/register/"

    def test_register_creates_user_and_establishes_session(self):
        response = self.client.post(
            self.url,
            {"email": "new@example.com", "password": "Str0ng-Passw0rd!", "first_name": "New"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "new@example.com")
        self.assertNotIn("password", response.data)
        self.assertTrue(User.objects.filter(email="new@example.com").exists())

        me_response = self.client.get("/api/v1/auth/me/")
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)

    def test_register_rejects_duplicate_email(self):
        User.objects.create_user(email="dup@example.com", password="Str0ng-Passw0rd!")

        response = self.client.post(
            self.url, {"email": "dup@example.com", "password": "Str0ng-Passw0rd!"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "VALIDATION_ERROR")

    def test_register_rejects_weak_password(self):
        response = self.client.post(self.url, {"email": "weak@example.com", "password": "123"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_cannot_self_assign_admin_role(self):
        response = self.client.post(
            self.url,
            {"email": "sneaky@example.com", "password": "Str0ng-Passw0rd!", "role": "ADMIN"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email="sneaky@example.com").exists())


class LoginViewTests(APITestCase):
    url = "/api/v1/auth/login/"

    def setUp(self):
        self.user = User.objects.create_user(
            email="consumer@example.com", password="Str0ng-Passw0rd!"
        )

    def test_login_with_valid_credentials_establishes_session(self):
        response = self.client.post(
            self.url, {"email": "consumer@example.com", "password": "Str0ng-Passw0rd!"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        me_response = self.client.get("/api/v1/auth/me/")
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)

    def test_login_with_wrong_password_returns_generic_error(self):
        response = self.client.post(
            self.url, {"email": "consumer@example.com", "password": "wrong"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("exist", str(response.data).lower())

    def test_login_with_unknown_email_returns_same_generic_error(self):
        response = self.client.post(
            self.url, {"email": "nobody@example.com", "password": "whatever"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "VALIDATION_ERROR")

    def test_login_rejects_inactive_user(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])

        response = self.client.post(
            self.url, {"email": "consumer@example.com", "password": "Str0ng-Passw0rd!"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(email="consumer@example.com", password="Str0ng-Passw0rd!")

    def test_logout_requires_authentication(self):
        response = self.client.post("/api/v1/auth/logout/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_ends_session(self):
        self.client.login(email="consumer@example.com", password="Str0ng-Passw0rd!")

        response = self.client.post("/api/v1/auth/logout/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        me_response = self.client.get("/api/v1/auth/me/")
        self.assertEqual(me_response.status_code, status.HTTP_401_UNAUTHORIZED)


class MeViewTests(APITestCase):
    def test_me_requires_authentication(self):
        response = self.client.get("/api/v1/auth/me/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["code"], "UNAUTHENTICATED")

    def test_me_returns_current_user_without_password(self):
        User.objects.create_user(email="consumer@example.com", password="Str0ng-Passw0rd!")
        self.client.login(email="consumer@example.com", password="Str0ng-Passw0rd!")

        response = self.client.get("/api/v1/auth/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("password", response.data)


class CsrfEnforcementTests(APITestCase):
    """
    APITestCase's default client disables CSRF checks for convenience (used
    in every test above). This class uses a CSRF-enforcing client instead,
    to prove the protection ADR-007 promises actually exists.
    """

    def setUp(self):
        self.csrf_client = Client(enforce_csrf_checks=True)

    def test_login_without_csrf_token_is_rejected(self):
        User.objects.create_user(email="consumer@example.com", password="Str0ng-Passw0rd!")

        response = self.csrf_client.post(
            "/api/v1/auth/login/",
            {"email": "consumer@example.com", "password": "Str0ng-Passw0rd!"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_with_csrf_token_succeeds(self):
        User.objects.create_user(email="consumer@example.com", password="Str0ng-Passw0rd!")

        self.csrf_client.get("/api/v1/auth/csrf/")
        csrf_token = self.csrf_client.cookies["csrftoken"].value

        response = self.csrf_client.post(
            "/api/v1/auth/login/",
            {"email": "consumer@example.com", "password": "Str0ng-Passw0rd!"},
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)