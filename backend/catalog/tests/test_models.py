from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.utils import DataError
from django.test import TestCase

from catalog.models import Category, Product, Unit
from farmer.models import FarmerProfile

User = get_user_model()


class ProductCatalogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="f1@example.com", password="pass1234", role="FARMER"
        )
        self.farmer_profile = FarmerProfile.objects.create(
            user=self.user, storefront_name="Green Fields", city="Rotterdam", region="ZH"
        )
        self.category = Category.objects.create(name="Vegetables")
        self.unit = Unit.objects.create(code=Unit.Code.KG)

    def test_product_belongs_to_one_farmer(self):
        product = Product.objects.create(
            farmer=self.farmer_profile,
            category=self.category,
            unit=self.unit,
            name="Tomatoes",
            price=Decimal("2.50"),
            stock_quantity=10,
        )
        self.assertEqual(product.farmer_id, self.farmer_profile.id)

    def test_stock_cannot_be_negative_at_db_level(self):
        product = Product(
            farmer=self.farmer_profile,
            category=self.category,
            unit=self.unit,
            name="Tomatoes",
            price=Decimal("2.50"),
            stock_quantity=-1,
        )
        # MySQL raises DataError (out of range) for PositiveIntegerField when negative values are passed
        with self.assertRaises(DataError):
            with transaction.atomic():
                product.save()

    def test_price_must_be_positive(self):
        product = Product(
            farmer=self.farmer_profile,
            category=self.category,
            unit=self.unit,
            name="Tomatoes",
            price=Decimal("0.00"),
            stock_quantity=5,
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_is_available_requires_active_and_in_stock(self):
        in_stock = Product.objects.create(
            farmer=self.farmer_profile,
            category=self.category,
            unit=self.unit,
            name="Apples",
            price=Decimal("3.00"),
            stock_quantity=5,
            is_active=True,
        )
        out_of_stock = Product.objects.create(
            farmer=self.farmer_profile,
            category=self.category,
            unit=self.unit,
            name="Pears",
            price=Decimal("3.00"),
            stock_quantity=0,
            is_active=True,
        )
        inactive = Product.objects.create(
            farmer=self.farmer_profile,
            category=self.category,
            unit=self.unit,
            name="Plums",
            price=Decimal("3.00"),
            stock_quantity=5,
            is_active=False,
        )
        self.assertTrue(in_stock.is_available)
        self.assertFalse(out_of_stock.is_available)
        self.assertFalse(inactive.is_available)

    def test_farmer_profile_requires_farmer_role(self):
        consumer = User.objects.create_user(
            email="c1@example.com", password="pass1234", role="CONSUMER"
        )
        profile = FarmerProfile(
            user=consumer, storefront_name="Bad Profile", city="X", region="Y"
        )
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_category_name_is_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Category.objects.create(name="Vegetables")
