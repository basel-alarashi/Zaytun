from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("api/v1/", include("farmer.urls")),
    path("api/v1/", include("catalog.urls")),
]

# Requests that don't match any URL pattern at all (so they never reach a
# DRF view, e.g. GET /api/v1/does-not-exist/) still return the canonical
# JSON error envelope instead of Django's default HTML 404 page.
handler404 = "api.views.not_found"
