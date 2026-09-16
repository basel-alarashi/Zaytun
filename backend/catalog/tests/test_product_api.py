from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Category, Unit, Product
from farmer.models import FarmerProfile

User = __import__("django.contrib.auth", fromlist=["get_user_model"]).get_user_model()


class ProductOwnershipTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Vegetables")
        self.unit = Unit.objects.create(code=Unit.Code.KG)

        self.farmer_a_user = User.objects.create_user(
            username="farmerA", email="a@example.com", password="pass1234", role="FARMER"
        )
        self.farmer_a = FarmerProfile.objects.create(
            user=self.farmer_a_user, storefront_name="Farm A",
            city="Bucharest", region="B", is_public=True,
        )

        self.farmer_b_user = User.objects.create_user(
            username="farmerB", email="b@example.com", password="pass1234", role="FARMER"
        )
        self.farmer_b = FarmerProfile.objects.create(
            user=self.farmer_b_user, storefront_name="Farm B",
            city="Cluj", region="CJ", is_public=True,
        )

        self.consumer_user = User.objects.create_user(
            username="consumer1", email="c@example.com", password="pass1234", role="CONSUMER"
        )

        self.product_a = Product.objects.create(
            farmer=self.farmer_a, category=self.category, unit=self.unit,
            name="Tomatoes", price=Decimal("2.50"), stock_quantity=10,
        )

    def test_farmer_can_create_own_product(self):
        self.client.force_authenticate(self.farmer_a_user)
        url = reverse("farmer-product-list-create")
        payload = {
            "name": "Cucumbers", "price": "1.75", "stock_quantity": 20,
            "category": self.category.id, "unit": self.unit.id,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Product.objects.get(name="Cucumbers")
        self.assertEqual(created.farmer_id, self.farmer_a.id)

    def test_client_supplied_farmer_id_is_ignored(self):
        """API spec §13: never trust client-supplied ownership."""
        self.client.force_authenticate(self.farmer_a_user)
        url = reverse("farmer-product-list-create")
        payload = {
            "name": "Spinach", "price": "3.00", "stock_quantity": 5,
            "category": self.category.id, "unit": self.unit.id,
            "farmer": self.farmer_b.id,  # attempted spoof
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Product.objects.get(name="Spinach")
        self.assertEqual(created.farmer_id, self.farmer_a.id)  # not farmer_b

    def test_farmer_cannot_edit_another_farmers_product(self):
        self.client.force_authenticate(self.farmer_b_user)
        url = reverse("farmer-product-detail", kwargs={"pk": self.product_a.id})
        response = self.client.patch(url, {"price": "0.01"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.product_a.refresh_from_db()
        self.assertEqual(self.product_a.price, Decimal("2.50"))  # unchanged

    def test_farmer_cannot_delete_another_farmers_product(self):
        self.client.force_authenticate(self.farmer_b_user)
        url = reverse("farmer-product-detail", kwargs={"pk": self.product_a.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.product_a.refresh_from_db()
        self.assertTrue(self.product_a.is_active)  # unchanged

    def test_delete_is_soft_deactivation_not_destructive(self):
        self.client.force_authenticate(self.farmer_a_user)
        url = reverse("farmer-product-detail", kwargs={"pk": self.product_a.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.product_a.refresh_from_db()
        self.assertFalse(self.product_a.is_active)
        self.assertTrue(Product.objects.filter(pk=self.product_a.id).exists())

    def test_consumer_cannot_access_farmer_product_endpoints(self):
        self.client.force_authenticate(self.consumer_user)
        url = reverse("farmer-product-list-create")
        response = self.client.post(url, {
            "name": "X", "price": "1.00", "stock_quantity": 1,
            "category": self.category.id, "unit": self.unit.id,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_access_farmer_endpoints(self):
        url = reverse("farmer-product-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_negative_price_rejected(self):
        self.client.force_authenticate(self.farmer_a_user)
        url = reverse("farmer-product-list-create")
        response = self.client.post(url, {
            "name": "Bad", "price": "-1.00", "stock_quantity": 1,
            "category": self.category.id, "unit": self.unit.id,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)

    def test_negative_stock_rejected(self):
        self.client.force_authenticate(self.farmer_a_user)
        url = reverse("farmer-product-list-create")
        response = self.client.post(url, {
            "name": "Bad", "price": "1.00", "stock_quantity": -5,
            "category": self.category.id, "unit": self.unit.id,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("stock_quantity", response.data)


class ProductPublicListTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fruits")
        self.unit = Unit.objects.create(code=Unit.Code.PIECE)

        user = User.objects.create_user(
            username="farmerC", email="c2@example.com", password="pass1234", role="FARMER"
        )
        self.public_farmer = FarmerProfile.objects.create(
            user=user, storefront_name="Public Farm", city="Iasi", region="IS", is_public=True
        )

        unpublished_user = User.objects.create_user(
            username="farmerD", email="d@example.com", password="pass1234", role="FARMER"
        )
        self.unpublished_farmer = FarmerProfile.objects.create(
            user=unpublished_user, storefront_name="Hidden Farm",
            city="Iasi", region="IS", is_public=False,
        )

        self.visible_product = Product.objects.create(
            farmer=self.public_farmer, category=self.category, unit=self.unit,
            name="Apples", price=Decimal("2.00"), stock_quantity=5, is_active=True,
        )
        self.inactive_product = Product.objects.create(
            farmer=self.public_farmer, category=self.category, unit=self.unit,
            name="Old Pears", price=Decimal("2.00"), stock_quantity=5, is_active=False,
        )
        self.hidden_farmer_product = Product.objects.create(
            farmer=self.unpublished_farmer, category=self.category, unit=self.unit,
            name="Secret Grapes", price=Decimal("2.00"), stock_quantity=5, is_active=True,
        )

    def test_public_list_excludes_inactive_products(self):
        url = reverse("product-list")
        response = self.client.get(url)
        names = [p["name"] for p in response.data["results"]] if "results" in response.data else [p["name"] for p in response.data]
        self.assertIn("Apples", names)
        self.assertNotIn("Old Pears", names)

    def test_public_list_excludes_unpublished_farmers(self):
        url = reverse("product-list")
        response = self.client.get(url)
        names = [p["name"] for p in response.data["results"]] if "results" in response.data else [p["name"] for p in response.data]
        self.assertNotIn("Secret Grapes", names)

    def test_search_filters_by_name(self):
        url = reverse("product-list")
        response = self.client.get(url, {"q": "apple"})
        results = response.data["results"] if "results" in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Apples")

    def test_inactive_product_detail_returns_404(self):
        url = reverse("product-detail", kwargs={"pk": self.inactive_product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)