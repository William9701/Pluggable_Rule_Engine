"""
Pluggable Rule Engine with Auto-Registration.

This module provides a base class for rules and a registry system that automatically
discovers and registers all rule classes. New rules can be added without modifying
existing code - simply create a new class that inherits from BaseRule.
"""

import logging
from abc import ABCMeta, abstractmethod
from typing import Dict, Type, Any

logger = logging.getLogger(__name__)


class RuleRegistry:
    """
    Registry for auto-discovering and managing rule classes.

    Rules are automatically registered when their class is defined,
    thanks to the metaclass used in BaseRule.
    """
    _rules: Dict[str, Type['BaseRule']] = {}

    @classmethod
    def register(cls, name: str, rule_class: Type['BaseRule']) -> None:
        """
        Register a rule class with a given name.

        Args:
            name: Unique identifier for the rule
            rule_class: The rule class to register
        """
        if name in cls._rules:
            logger.warning(f"Rule '{name}' is being overridden")
        cls._rules[name] = rule_class
        logger.info(f"Registered rule: {name}")

    @classmethod
    def get_rule(cls, name: str) -> Type['BaseRule']:
        """
        Retrieve a rule class by name.

        Args:
            name: The rule identifier

        Returns:
            The rule class

        Raises:
            KeyError: If the rule is not found
        """
        if name not in cls._rules:
            raise KeyError(f"Rule '{name}' not found. Available rules: {list(cls._rules.keys())}")
        return cls._rules[name]

    @classmethod
    def get_all_rules(cls) -> Dict[str, Type['BaseRule']]:
        """Get all registered rules."""
        return cls._rules.copy()

    @classmethod
    def rule_exists(cls, name: str) -> bool:
        """Check if a rule is registered."""
        return name in cls._rules


class RuleMeta(ABCMeta):
    """
    Metaclass that auto-registers rule classes.

    When a class using this metaclass is defined, it automatically
    registers itself with the RuleRegistry using its 'name' attribute.

    Inherits from ABCMeta to be compatible with ABC.
    """
    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        cls = super().__new__(mcs, name, bases, attrs)

        # Don't register the base class itself
        if name != 'BaseRule' and 'name' in attrs and attrs['name']:
            RuleRegistry.register(attrs['name'], cls)

        return cls


class BaseRule(metaclass=RuleMeta):
    """
    Abstract base class for all rules.

    To create a new rule:
    1. Inherit from this class
    2. Set the 'name' class attribute (must be unique)
    3. Optionally set 'description'
    4. Implement the 'evaluate' method

    The rule will be automatically registered and available for use.

    Example:
        class MyCustomRule(BaseRule):
            name = "my_custom_rule"
            description = "Checks if order meets custom criteria"

            def evaluate(self, order) -> bool:
                return order.total > 50
    """

    name: str = None
    description: str = ""

    def __init__(self, **kwargs):
        """
        Initialize the rule with optional parameters.

        Args:
            **kwargs: Additional parameters for rule configuration
        """
        self.config = kwargs

    @abstractmethod
    def evaluate(self, order: Any) -> bool:
        """
        Evaluate the rule against an order.

        Args:
            order: The order object to evaluate

        Returns:
            True if the order passes the rule, False otherwise
        """
        pass

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}')>"


class RuleEngine:
    """
    Engine for evaluating multiple rules against an order.

    This class orchestrates the evaluation of rules and provides
    detailed results for each rule.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def evaluate_rules(self, order: Any, rule_names: list) -> dict:
        """
        Evaluate multiple rules against an order.

        Args:
            order: The order to evaluate
            rule_names: List of rule names to evaluate

        Returns:
            Dictionary containing:
                - passed: True if all rules passed
                - details: Dictionary mapping rule names to their results

        Raises:
            KeyError: If a rule name is not found in the registry
        """
        results = {}

        for rule_name in rule_names:
            try:
                # Get the rule class from registry
                rule_class = RuleRegistry.get_rule(rule_name)

                # Instantiate and evaluate
                rule_instance = rule_class()
                result = rule_instance.evaluate(order)
                results[rule_name] = result

                self.logger.debug(
                    f"Rule '{rule_name}' evaluated for order {order.id}: {result}"
                )

            except KeyError as e:
                self.logger.error(f"Rule not found: {rule_name}")
                raise
            except Exception as e:
                self.logger.error(
                    f"Error evaluating rule '{rule_name}': {str(e)}",
                    exc_info=True
                )
                raise

        # All rules must pass for overall success
        passed = all(results.values())

        return {
            'passed': passed,
            'details': results
        }
