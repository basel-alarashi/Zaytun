from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from accounts.permissions import IsFarmer
from .models import FarmerProfile
from .serializers import FarmerProfilePublicSerializer, FarmerProfileSelfSerializer


class FarmerListView(generics.ListAPIView):
    """GET /farmers/ — public list of published storefronts only."""

    serializer_class = FarmerProfilePublicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = FarmerProfile.objects.filter(is_public=True).order_by("storefront_name")


class FarmerDetailView(generics.RetrieveAPIView):
    """GET /farmers/{id}/ — public detail; unpublished storefronts 404."""

    serializer_class = FarmerProfilePublicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = FarmerProfile.objects.filter(is_public=True)

    def get_object(self):
        try:
            return self.get_queryset().get(pk=self.kwargs["pk"])
        except FarmerProfile.DoesNotExist:
            raise NotFound("Storefront not found.")


class FarmerStorefrontDetailView(FarmerDetailView):
    """GET /farmers/{id}/storefront/ — alias kept distinct for future divergence
    (e.g. embedding product counts) without breaking /farmers/{id}/."""
    pass


class FarmerMeStorefrontView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /farmers/me/storefront/ — farmer manages only their own profile."""

    serializer_class = FarmerProfileSelfSerializer
    permission_classes = [permissions.IsAuthenticated, IsFarmer]

    def get_object(self):
        try:
            return self.request.user.farmer_profile
        except FarmerProfile.DoesNotExist:
            raise NotFound("Farmer profile does not exist for this account.")