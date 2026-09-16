from django.urls import path
from . import views

urlpatterns = [
    path("farmers/", views.FarmerListView.as_view(), name="farmer-list"),
    path("farmers/me/storefront/", views.FarmerMeStorefrontView.as_view(), name="farmer-me-storefront"),
    path("farmers/<int:pk>/storefront/", views.FarmerStorefrontDetailView.as_view(), name="farmer-storefront-detail"),
    path("farmers/<int:pk>/", views.FarmerDetailView.as_view(), name="farmer-detail"),
]