from django.conf import settings
from django.db import models

from api.models import TimeStampedModel


class FarmerProfile(TimeStampedModel):
    """One storefront profile per Farmer-role User (ADR-006, DB design §2)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="farmer_profile",
    )
    storefront_name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    # Location fields kept flat for V1 single-country scope (ADR-005).
    city = models.CharField(max_length=80)
    region = models.CharField(max_length=80)

    is_public = models.BooleanField(
        default=False,
        help_text="Storefront is visible to consumers only when public.",
    )

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return self.storefront_name

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.user_id and getattr(self.user, "role", None) != "FARMER":
            raise ValidationError("Only Farmer-role users may own a FarmerProfile.")