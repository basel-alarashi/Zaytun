from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("units/", views.UnitListView.as_view(), name="unit-list"),
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("farmer/products/", views.FarmerProductListCreateView.as_view(), name="farmer-product-list-create"),
    path("farmer/products/<int:pk>/", views.FarmerProductDetailView.as_view(), name="farmer-product-detail"),
]