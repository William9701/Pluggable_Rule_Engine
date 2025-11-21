from django.core.management.base import BaseCommand
from orders.models import Order
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seeds the database with example orders'

    def handle(self, *args, **kwargs):
        # Clear existing orders
        Order.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing orders'))

        # Create example orders
        orders_data = [
            {'total': Decimal('150.00'), 'items_count': 3},
            {'total': Decimal('75.50'), 'items_count': 1},
            {'total': Decimal('200.00'), 'items_count': 5},
        ]

        orders = []
        for data in orders_data:
            order = Order.objects.create(**data)
            orders.append(order)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created order #{order.id}: Total=${order.total}, Items={order.items_count}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {len(orders)} orders')
        )
