# backend/apps/catalog/models.py
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

from api.models import TimeStampedModel
from farmer.models import FarmerProfile


class Category(TimeStampedModel):
    """Controlled product classification (DB design §2)."""

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Unit(TimeStampedModel):
    """Controlled measurement unit catalogue (ADR-003)."""

    class Code(models.TextChoices):
        KG = "kg", "Kilogram"
        G = "g", "Gram"
        L = "l", "Liter"
        ML = "ml", "Milliliter"
        PIECE = "piece", "Piece"
        DOZEN = "dozen", "Dozen"
        BUNCH = "bunch", "Bunch"
        BOX = "box", "Box"
        PACKAGE = "package", "Package"

    code = models.CharField(max_length=10, choices=Code.choices, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_code_display()


class Product(TimeStampedModel):
    """A sellable organic item belonging to exactly one farmer (DB design §4.1)."""

    farmer = models.ForeignKey(
        FarmerProfile, on_delete=models.CASCADE, related_name="products"
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    unit = models.ForeignKey(
        Unit, on_delete=models.PROTECT, related_name="products"
    )

    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    stock_quantity = models.PositiveIntegerField(default=0)

    # Farmer-controlled toggle; product is orderable only if active AND stock > 0.
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["farmer"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(stock_quantity__gte=0),
                name="product_stock_non_negative",
            ),
        ]

    def __str__(self):
        return self.name

    @property
    def is_available(self):
        """Availability = active AND in stock (Glossary §2: don't conflate the two)."""
        return self.is_active and self.stock_quantity > 0

    def clean(self):
        if self.price is not None and self.price <= 0:
            raise ValidationError(
                {"price": "Price must be greater than zero."})
