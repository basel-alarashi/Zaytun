from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from accounts.permissions import IsFarmer
from .models import Category, Unit, Product
from .serializers import (
    CategorySerializer, UnitSerializer,
    ProductPublicSerializer, ProductWriteSerializer,
)


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.filter(is_active=True)


class UnitListView(generics.ListAPIView):
    serializer_class = UnitSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Unit.objects.filter(is_active=True)


class ProductListView(generics.ListAPIView):
    """GET /products/ — public discovery. Supports ?q= &category= &farmer= &available=.
    Server owns filtering/pagination (API spec §5)."""

    serializer_class = ProductPublicSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Product.objects.select_related("category", "unit", "farmer").filter(
            is_active=True, farmer__is_public=True
        )

        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category_id=category)

        farmer = self.request.query_params.get("farmer")
        if farmer:
            qs = qs.filter(farmer_id=farmer)

        available = self.request.query_params.get("available")
        if available is not None:
            wants_available = available.lower() in ("1", "true", "yes")
            qs = qs.filter(stock_quantity__gt=0) if wants_available else qs.filter(stock_quantity=0)

        return qs.order_by("name")


class ProductDetailView(generics.RetrieveAPIView):
    """GET /products/{id}/ — public detail; hidden if inactive or farmer unpublished."""

    serializer_class = ProductPublicSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        try:
            return Product.objects.select_related("category", "unit", "farmer").get(
                pk=self.kwargs["pk"], is_active=True, farmer__is_public=True
            )
        except Product.DoesNotExist:
            raise NotFound("Product not found.")


class FarmerProductListCreateView(generics.ListCreateAPIView):
    """GET/POST /farmer/products/ — farmer sees & creates only their own products."""

    permission_classes = [permissions.IsAuthenticated, IsFarmer]

    def get_serializer_class(self):
        return ProductWriteSerializer

    def get_queryset(self):
        return Product.objects.select_related("category", "unit").filter(
            farmer__user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        # Ownership derived from authenticated identity — never from client input.
        farmer_profile = self.request.user.farmer_profile
        serializer.save(farmer=farmer_profile)


class FarmerProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /farmer/products/{id}/ — scoped to the requesting farmer.

    DELETE performs a soft-deactivation (is_active=False), not a destructive
    delete, per DB design §5 (history/order integrity)."""

    serializer_class = ProductWriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsFarmer]

    def get_queryset(self):
        # Non-owned products are excluded from the queryset entirely, so a
        # farmer attempting to touch another farmer's product gets 404, not 403 —
        # this avoids confirming the object's existence to a non-owner.
        return Product.objects.filter(farmer__user=self.request.user)

    def get_object(self):
        try:
            return self.get_queryset().get(pk=self.kwargs["pk"])
        except Product.DoesNotExist:
            raise NotFound("Product not found.")

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])