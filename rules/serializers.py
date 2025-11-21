"""
Serializers for the rules API.
"""

from rest_framework import serializers
from .engine import RuleRegistry


class RuleCheckRequestSerializer(serializers.Serializer):
    """
    Serializer for rule check requests.

    Validates that the order_id and rules are provided correctly.
    """
    order_id = serializers.IntegerField(
        min_value=1,
        help_text="ID of the order to validate"
    )
    rules = serializers.ListField(
        child=serializers.CharField(max_length=100),
        min_length=1,
        help_text="List of rule names to apply"
    )

    def validate_rules(self, value):
        """
        Validate that all requested rules exist in the registry.

        Args:
            value: List of rule names

        Returns:
            The validated list of rule names

        Raises:
            serializers.ValidationError: If any rule is not found
        """
        invalid_rules = []
        for rule_name in value:
            if not RuleRegistry.rule_exists(rule_name):
                invalid_rules.append(rule_name)

        if invalid_rules:
            available_rules = list(RuleRegistry.get_all_rules().keys())
            raise serializers.ValidationError(
                f"Invalid rule(s): {', '.join(invalid_rules)}. "
                f"Available rules: {', '.join(available_rules)}"
            )

        return value


class RuleCheckResponseSerializer(serializers.Serializer):
    """
    Serializer for rule check responses.

    This is primarily used for API documentation.
    """
    passed = serializers.BooleanField(
        help_text="True if all rules passed, False otherwise"
    )
    details = serializers.DictField(
        child=serializers.BooleanField(),
        help_text="Dictionary mapping rule names to their evaluation results"
    )


class RuleInfoSerializer(serializers.Serializer):
    """
    Serializer for rule information.
    """
    name = serializers.CharField(help_text="Unique identifier for the rule")
    description = serializers.CharField(help_text="Human-readable description of the rule")
