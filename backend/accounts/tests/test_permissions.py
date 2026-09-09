from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from accounts.models import User
from accounts.permissions import IsAdminRole, IsConsumer, IsFarmer, IsOwner


class RolePermissionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.consumer = User.objects.create_user(
            email="consumer@example.com", password="pw", role=User.Role.CONSUMER
        )
        self.farmer = User.objects.create_user(
            email="farmer@example.com", password="pw", role=User.Role.FARMER
        )
        self.admin = User.objects.create_user(
            email="admin@example.com", password="pw", role=User.Role.ADMIN
        )

    def _request_as(self, user):
        request = self.factory.get("/")
        request.user = user
        return request

    def test_is_consumer_allows_only_consumers(self):
        perm = IsConsumer()
        self.assertTrue(perm.has_permission(self._request_as(self.consumer), None))
        self.assertFalse(perm.has_permission(self._request_as(self.farmer), None))
        self.assertFalse(perm.has_permission(self._request_as(self.admin), None))

    def test_is_farmer_allows_only_farmers(self):
        perm = IsFarmer()
        self.assertTrue(perm.has_permission(self._request_as(self.farmer), None))
        self.assertFalse(perm.has_permission(self._request_as(self.consumer), None))
        self.assertFalse(perm.has_permission(self._request_as(self.admin), None))

    def test_is_admin_role_allows_only_admin_role(self):
        perm = IsAdminRole()
        self.assertTrue(perm.has_permission(self._request_as(self.admin), None))
        self.assertFalse(perm.has_permission(self._request_as(self.farmer), None))
        self.assertFalse(perm.has_permission(self._request_as(self.consumer), None))

    def test_role_permission_denies_anonymous_user(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()

        self.assertFalse(IsConsumer().has_permission(request, None))
        self.assertFalse(IsFarmer().has_permission(request, None))
        self.assertFalse(IsAdminRole().has_permission(request, None))


class IsOwnerPermissionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(email="owner@example.com", password="pw")
        self.other = User.objects.create_user(email="other@example.com", password="pw")

    def _request_as(self, user):
        request = self.factory.get("/")
        request.user = user
        return request

    def test_has_permission_only_requires_authentication(self):
        perm = IsOwner()
        self.assertTrue(perm.has_permission(self._request_as(self.owner), None))

        anon_request = self.factory.get("/")
        anon_request.user = AnonymousUser()
        self.assertFalse(perm.has_permission(anon_request, None))

    def test_has_object_permission_allows_only_the_owner(self):
        class DummyResource:
            def __init__(self, user):
                self.user = user

        perm = IsOwner()
        resource = DummyResource(user=self.owner)

        self.assertTrue(
            perm.has_object_permission(self._request_as(self.owner), None, resource)
        )
        self.assertFalse(
            perm.has_object_permission(self._request_as(self.other), None, resource)
        )

    def test_owner_field_is_configurable_for_other_resource_shapes(self):
        class ConsumerOwnedPermission(IsOwner):
            owner_field = "consumer"

        class DummyAddress:
            def __init__(self, consumer):
                self.consumer = consumer

        perm = ConsumerOwnedPermission()
        address = DummyAddress(consumer=self.owner)

        self.assertTrue(
            perm.has_object_permission(self._request_as(self.owner), None, address)
        )
        self.assertFalse(
            perm.has_object_permission(self._request_as(self.other), None, address)
        )