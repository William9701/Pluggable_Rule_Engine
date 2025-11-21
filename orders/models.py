from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Order(models.Model):
    """
    Order model representing a customer order.

    Attributes:
        total: The total amount of the order (must be non-negative)
        items_count: The number of items in the order (must be positive)
        created_at: Timestamp when the order was created
        updated_at: Timestamp when the order was last updated
    """
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Total amount of the order"
    )
    items_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of items in the order"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['total']),
        ]

    def __str__(self):
        return f"Order #{self.id} - Total: ${self.total}, Items: {self.items_count}"

    def __repr__(self):
        return f"<Order(id={self.id}, total={self.total}, items_count={self.items_count})>"
