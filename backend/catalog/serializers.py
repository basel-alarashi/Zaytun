from rest_framework import serializers
from .models import Category, Unit, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        read_only_fields = fields


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["id", "code"]
        read_only_fields = fields


class ProductPublicSerializer(serializers.ModelSerializer):
    """Read-only representation for consumers (GET /products/, /products/{id}/)."""

    category = CategorySerializer(read_only=True)
    unit = UnitSerializer(read_only=True)
    farmer_id = serializers.IntegerField(source="farmer.id", read_only=True)
    farmer_name = serializers.CharField(source="farmer.storefront_name", read_only=True)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "description", "price", "stock_quantity",
            "is_active", "is_available", "category", "unit",
            "farmer_id", "farmer_name",
        ]
        read_only_fields = fields


class ProductWriteSerializer(serializers.ModelSerializer):
    """Farmer create/update. `farmer` is never accepted from the client —
    it is set server-side from request.user in the view (API spec §13)."""

    class Meta:
        model = Product
        fields = [
            "id", "name", "description", "price", "stock_quantity",
            "category", "unit", "is_active",
        ]
        read_only_fields = ["id"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value

    def validate_category(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Category is not active.")
        return value

    def validate_unit(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Unit is not active.")
        return value