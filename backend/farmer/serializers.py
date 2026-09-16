from rest_framework import serializers
from .models import FarmerProfile


class FarmerProfilePublicSerializer(serializers.ModelSerializer):
    """Read-only representation shown to consumers/public."""

    class Meta:
        model = FarmerProfile
        fields = ["id", "storefront_name", "description", "city", "region"]
        read_only_fields = fields


class FarmerProfileSelfSerializer(serializers.ModelSerializer):
    """Farmer's own view/edit of their storefront (PATCH /farmers/me/storefront/)."""

    class Meta:
        model = FarmerProfile
        fields = ["id", "storefront_name", "description", "city", "region", "is_public"]
        read_only_fields = ["id"]

    def validate_storefront_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Storefront name cannot be blank.")
        return value.strip()