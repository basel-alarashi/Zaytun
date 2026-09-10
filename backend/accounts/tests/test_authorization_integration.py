from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework.views import APIView

from accounts.models import User
from accounts.permissions import IsAdminRole, IsConsumer, IsFarmer, IsOwner


# --- Throwaway views, defined only for this test module ------------------
# Not registered in any urls.py. They exist purely to exercise the
# permission classes through DRF's real request -> permission ->
# exception-handling pipeline, since no production endpoint attaches
# role/ownership checks yet (deferred to Sprint 3 — see Stage C's note).

class _ConsumerOnlyView(APIView):
    permission_classes = [IsConsumer]

    def get(self, request):
        return Response({"ok": True})


class _FarmerOnlyView(APIView):
    permission_classes = [IsFarmer]

    def get(self, request):
        return Response({"ok": True})


class _AdminOnlyView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        return Response({"ok": True})


class _OwnedResource:
    """Minimal stand-in for a real owned model (Product, Address, ...)."""

    def __init__(self, user):
        self.user = user


class _OwnerOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, owner_id):
        resource = _OwnedResource(user=User.objects.get(pk=owner_id))
        self.check_object_permissions(request, resource)
        return Response({"ok": True})


class RoleProtectedViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.consumer = User.objects.create_user(
            email="consumer@example.com", password="pw", role=User.Role.CONSUMER
        )
        self.farmer = User.objects.create_user(
            email="farmer@example.com", password="pw", role=User.Role.FARMER
        )
        self.admin = User.objects.create_user(
            email="admin@example.com", password="pw", role=User.Role.ADMIN
        )

    def test_anonymous_request_is_401_not_403(self):
        request = self.factory.get("/fake-consumer-only/")
        response = _ConsumerOnlyView.as_view()(request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], "UNAUTHENTICATED")

    def test_authenticated_wrong_role_is_403_not_401(self):
        request = self.factory.get("/fake-consumer-only/")
        force_authenticate(request, user=self.farmer)
        response = _ConsumerOnlyView.as_view()(request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["code"], "PERMISSION_DENIED")

    def test_correct_role_is_allowed(self):
        request = self.factory.get("/fake-consumer-only/")
        force_authenticate(request, user=self.consumer)
        response = _ConsumerOnlyView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_farmer_only_view_rejects_consumer_and_admin(self):
        for other_user in (self.consumer, self.admin):
            request = self.factory.get("/fake-farmer-only/")
            force_authenticate(request, user=other_user)
            response = _FarmerOnlyView.as_view()(request)
            self.assertEqual(response.status_code, 403)

        request = self.factory.get("/fake-farmer-only/")
        force_authenticate(request, user=self.farmer)
        response = _FarmerOnlyView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_admin_only_view_rejects_consumer_and_farmer(self):
        for other_user in (self.consumer, self.farmer):
            request = self.factory.get("/fake-admin-only/")
            force_authenticate(request, user=other_user)
            response = _AdminOnlyView.as_view()(request)
            self.assertEqual(response.status_code, 403)

        request = self.factory.get("/fake-admin-only/")
        force_authenticate(request, user=self.admin)
        response = _AdminOnlyView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class OwnershipProtectedViewTests(APITestCase):
    """
    Proves the generic IsOwner mechanism end-to-end. The real acceptance
    criterion ("farmer cannot modify another farmer's product") gets its
    own test using this same permission class once Product exists in
    Sprint 3 — this is the reusable machinery that test will rely on.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.owner = User.objects.create_user(email="owner@example.com", password="pw")
        self.other = User.objects.create_user(email="other@example.com", password="pw")

    def test_owner_can_access_own_resource(self):
        request = self.factory.get(f"/fake-owner-only/{self.owner.pk}/")
        force_authenticate(request, user=self.owner)
        response = _OwnerOnlyView.as_view()(request, owner_id=self.owner.pk)

        self.assertEqual(response.status_code, 200)

    def test_non_owner_is_denied_with_403(self):
        request = self.factory.get(f"/fake-owner-only/{self.owner.pk}/")
        force_authenticate(request, user=self.other)
        response = _OwnerOnlyView.as_view()(request, owner_id=self.owner.pk)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["code"], "PERMISSION_DENIED")

    def test_anonymous_is_denied_with_401_not_403(self):
        request = self.factory.get(f"/fake-owner-only/{self.owner.pk}/")
        response = _OwnerOnlyView.as_view()(request, owner_id=self.owner.pk)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], "UNAUTHENTICATED")