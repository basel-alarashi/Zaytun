from django.core.management.base import BaseCommand
from catalog.models import Category, Unit


DEFAULT_CATEGORIES = ["Vegetables", "Fruits", "Grains", "Dairy", "Herbs", "Honey & Preserves"]


class Command(BaseCommand):
    help = "Seed baseline categories and units (idempotent)."

    def handle(self, *args, **options):
        for name in DEFAULT_CATEGORIES:
            Category.objects.get_or_create(name=name)

        for code, _ in Unit.Code.choices:
            Unit.objects.get_or_create(code=code)

        self.stdout.write(self.style.SUCCESS("Catalog seeded."))