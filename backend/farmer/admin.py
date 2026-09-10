from django.contrib import admin
from .models import FarmerProfile


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ("storefront_name", "user", "city", "region", "is_public")
    list_filter = ("is_public", "region")
    search_fields = ("storefront_name", "user__email")