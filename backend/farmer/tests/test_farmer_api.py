from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from farmer.models import FarmerProfile

User = get_user_model()


class FarmerStorefrontTests(APITestCase):
    def setUp(self):
        self.farmer_user = User.objects.create_user(
            email="f1@example.com", password="pass1234", role="FARMER"
        )
        self.profile = FarmerProfile.objects.create(
            user=self.farmer_user, storefront_name="My Farm",
            city="Brasov", region="BV", is_public=False,
        )
        self.other_farmer_user = User.objects.create_user(
            email="f2@example.com", password="pass1234", role="FARMER"
        )

    def test_farmer_can_view_own_storefront(self):
        self.client.force_authenticate(self.farmer_user)
        url = reverse("farmer-me-storefront")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["storefront_name"], "My Farm")

    def test_farmer_can_update_own_storefront(self):
        self.client.force_authenticate(self.farmer_user)
        url = reverse("farmer-me-storefront")
        response = self.client.patch(url, {"storefront_name": "Renamed Farm", "is_public": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.storefront_name, "Renamed Farm")
        self.assertTrue(self.profile.is_public)

    def test_farmer_without_profile_gets_404_not_500(self):
        self.client.force_authenticate(self.other_farmer_user)
        url = reverse("farmer-me-storefront")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unpublished_storefront_hidden_from_public_list(self):
        url = reverse("farmer-list")
        response = self.client.get(url)
        names = [f["storefront_name"] for f in response.data["results"]] if "results" in response.data else [f["storefront_name"] for f in response.data]
        self.assertNotIn("My Farm", names)

    def test_blank_storefront_name_rejected(self):
        self.client.force_authenticate(self.farmer_user)
        url = reverse("farmer-me-storefront")
        response = self.client.patch(url, {"storefront_name": "   "})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)