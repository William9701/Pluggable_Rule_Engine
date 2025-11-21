"""
Order validation rules.

This module contains concrete rule implementations for order validation.
Each rule is automatically registered with the RuleRegistry when imported.
"""

from .engine import BaseRule
from decimal import Decimal


class MinimumTotalRule(BaseRule):
    """
    Rule that checks if order total exceeds a minimum threshold.

    Default threshold: 100
    """
    name = "min_total_100"
    description = "Validates that order total is greater than 100"

    def evaluate(self, order) -> bool:
        """
        Check if order total is greater than 100.

        Args:
            order: Order instance with a 'total' attribute

        Returns:
            True if total > 100, False otherwise
        """
        threshold = self.config.get('threshold', Decimal('100.00'))
        return order.total > threshold


class MinimumItemsRule(BaseRule):
    """
    Rule that checks if order has a minimum number of items.

    Default threshold: 2
    """
    name = "min_items_2"
    description = "Validates that order has at least 2 items"

    def evaluate(self, order) -> bool:
        """
        Check if order has at least 2 items.

        Args:
            order: Order instance with an 'items_count' attribute

        Returns:
            True if items_count >= 2, False otherwise
        """
        threshold = self.config.get('threshold', 2)
        return order.items_count >= threshold


class DivisibleByFiveRule(BaseRule):
    """
    Rule that checks if order total is divisible by 5.
    """
    name = "divisible_by_5"
    description = "Validates that order total is divisible by 5"

    def evaluate(self, order) -> bool:
        """
        Check if order total is divisible by 5.

        Args:
            order: Order instance with a 'total' attribute

        Returns:
            True if total is divisible by 5, False otherwise
        """
        # Convert to Decimal for precise division check
        return order.total % Decimal('5.00') == Decimal('0.00')
