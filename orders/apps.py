from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self):
        from decimal import Decimal
        from django.db import connection
        from django.db.utils import OperationalError

        # Only seed if table exists (avoid issues during migrations)
        try:
            from .models import Order
            if not Order.objects.exists():
                orders_data = [
                    {'total': Decimal('150.00'), 'items_count': 3},
                    {'total': Decimal('75.50'), 'items_count': 1},
                    {'total': Decimal('200.00'), 'items_count': 5},
                ]
                for data in orders_data:
                    Order.objects.create(**data)
        except (OperationalError, Exception):
            # Table doesn't exist yet, skip seeding
            pass
