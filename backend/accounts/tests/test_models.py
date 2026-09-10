from django.db import IntegrityError, transaction
from django.test import TestCase

from accounts.models import User


class UserManagerTests(TestCase):
    def test_create_user_sets_normalized_email_and_hashed_password(self):
        user = User.objects.create_user(email="Consumer@Example.com", password="s3cret-pass")

        self.assertEqual(user.email, "Consumer@example.com")
        self.assertTrue(user.check_password("s3cret-pass"))
        self.assertNotEqual(user.password, "s3cret-pass")

    def test_create_user_defaults_to_consumer_role(self):
        user = User.objects.create_user(email="consumer@example.com", password="s3cret-pass")

        self.assertEqual(user.role, User.Role.CONSUMER)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_user_without_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="s3cret-pass")

    def test_create_superuser_sets_admin_role_and_staff_flags(self):
        admin = User.objects.create_superuser(email="admin@example.com", password="s3cret-pass")

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, User.Role.ADMIN)

    def test_create_superuser_rejects_is_staff_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@example.com", password="s3cret-pass", is_staff=False
            )


class UserModelTests(TestCase):
    def test_email_is_unique(self):
        User.objects.create_user(email="dup@example.com", password="s3cret-pass")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(email="dup@example.com", password="another-pass")

    def test_string_representation_is_email(self):
        user = User.objects.create_user(email="consumer@example.com", password="s3cret-pass")

        self.assertEqual(str(user), "consumer@example.com")

    def test_role_helper_properties(self):
        farmer = User.objects.create_user(
            email="farmer@example.com", password="s3cret-pass", role=User.Role.FARMER
        )

        self.assertTrue(farmer.is_farmer)
        self.assertFalse(farmer.is_consumer)
        self.assertFalse(farmer.is_admin_role)