from django.contrib import admin
from .models import Category, Unit, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("code", "is_active")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "farmer", "category", "unit", "price", "stock_quantity", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "farmer__storefront_name")