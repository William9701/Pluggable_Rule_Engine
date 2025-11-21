from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""

    class Meta:
        model = Order
        fields = ['id', 'total', 'items_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_total(self, value):
        """Validate that total is non-negative."""
        if value < 0:
            raise serializers.ValidationError("Total must be non-negative.")
        return value

    def validate_items_count(self, value):
        """Validate that items_count is positive."""
        if value < 1:
            raise serializers.ValidationError("Items count must be at least 1.")
        return value
