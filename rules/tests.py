"""
Comprehensive test suite for the rules engine.
"""

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal

from orders.models import Order
from .engine import BaseRule, RuleRegistry, RuleEngine


class TestRuleRegistry(TestCase):
    """Tests for the RuleRegistry."""

    def test_rules_are_registered(self):
        """Test that rules are auto-registered."""
        self.assertIn('min_total_100', RuleRegistry.get_all_rules())
        self.assertIn('min_items_2', RuleRegistry.get_all_rules())
        self.assertIn('divisible_by_5', RuleRegistry.get_all_rules())

    def test_get_rule(self):
        """Test retrieving a rule by name."""
        rule_class = RuleRegistry.get_rule('min_total_100')
        self.assertIsNotNone(rule_class)
        self.assertEqual(rule_class.name, 'min_total_100')

    def test_get_nonexistent_rule_raises_error(self):
        """Test that getting a non-existent rule raises KeyError."""
        with self.assertRaises(KeyError):
            RuleRegistry.get_rule('nonexistent_rule')

    def test_rule_exists(self):
        """Test checking if a rule exists."""
        self.assertTrue(RuleRegistry.rule_exists('min_total_100'))
        self.assertFalse(RuleRegistry.rule_exists('nonexistent_rule'))


class TestOrderRules(TestCase):
    """Tests for individual order rules."""

    def setUp(self):
        """Create test orders."""
        self.order_high_total = Order.objects.create(
            total=Decimal('152.00'),
            items_count=3
        )
        self.order_low_total = Order.objects.create(
            total=Decimal('73.00'),
            items_count=1
        )
        self.order_divisible = Order.objects.create(
            total=Decimal('200.00'),
            items_count=5
        )

    def test_min_total_100_rule(self):
        """Test the min_total_100 rule."""
        rule_class = RuleRegistry.get_rule('min_total_100')
        rule = rule_class()

        self.assertTrue(rule.evaluate(self.order_high_total))
        self.assertFalse(rule.evaluate(self.order_low_total))
        self.assertTrue(rule.evaluate(self.order_divisible))

    def test_min_items_2_rule(self):
        """Test the min_items_2 rule."""
        rule_class = RuleRegistry.get_rule('min_items_2')
        rule = rule_class()

        self.assertTrue(rule.evaluate(self.order_high_total))
        self.assertFalse(rule.evaluate(self.order_low_total))
        self.assertTrue(rule.evaluate(self.order_divisible))

    def test_divisible_by_5_rule(self):
        """Test the divisible_by_5 rule."""
        rule_class = RuleRegistry.get_rule('divisible_by_5')
        rule = rule_class()

        self.assertFalse(rule.evaluate(self.order_high_total))
        self.assertFalse(rule.evaluate(self.order_low_total))
        self.assertTrue(rule.evaluate(self.order_divisible))


class TestRuleEngine(TestCase):
    """Tests for the RuleEngine."""

    def setUp(self):
        """Create test orders."""
        self.order = Order.objects.create(
            total=Decimal('152.00'),
            items_count=3
        )
        self.engine = RuleEngine()

    def test_evaluate_single_rule(self):
        """Test evaluating a single rule."""
        result = self.engine.evaluate_rules(self.order, ['min_total_100'])

        self.assertTrue(result['passed'])
        self.assertEqual(result['details']['min_total_100'], True)

    def test_evaluate_multiple_rules_all_pass(self):
        """Test evaluating multiple rules where all pass."""
        order = Order.objects.create(total=Decimal('200.00'), items_count=5)
        result = self.engine.evaluate_rules(
            order,
            ['min_total_100', 'min_items_2', 'divisible_by_5']
        )

        self.assertTrue(result['passed'])
        self.assertEqual(result['details']['min_total_100'], True)
        self.assertEqual(result['details']['min_items_2'], True)
        self.assertEqual(result['details']['divisible_by_5'], True)

    def test_evaluate_multiple_rules_some_fail(self):
        """Test evaluating multiple rules where some fail."""
        result = self.engine.evaluate_rules(
            self.order,
            ['min_total_100', 'divisible_by_5']
        )

        self.assertFalse(result['passed'])
        self.assertEqual(result['details']['min_total_100'], True)
        self.assertEqual(result['details']['divisible_by_5'], False)

    def test_evaluate_nonexistent_rule_raises_error(self):
        """Test that evaluating a non-existent rule raises an error."""
        with self.assertRaises(KeyError):
            self.engine.evaluate_rules(self.order, ['nonexistent_rule'])


class TestRuleCheckAPI(APITestCase):
    """Tests for the Rule Check API endpoint."""

    def setUp(self):
        """Create test orders."""
        self.order_high_total = Order.objects.create(
            total=Decimal('150.00'),
            items_count=3
        )
        self.order_low_total = Order.objects.create(
            total=Decimal('75.50'),
            items_count=1
        )

    def test_rule_check_success(self):
        """Test successful rule check."""
        url = '/rules/check/'
        data = {
            'order_id': self.order_high_total.id,
            'rules': ['min_total_100', 'min_items_2']
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['passed'])
        self.assertEqual(response.data['details']['min_total_100'], True)
        self.assertEqual(response.data['details']['min_items_2'], True)

    def test_rule_check_some_fail(self):
        """Test rule check where some rules fail."""
        url = '/rules/check/'
        data = {
            'order_id': self.order_low_total.id,
            'rules': ['min_total_100', 'min_items_2']
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['passed'])
        self.assertEqual(response.data['details']['min_total_100'], False)
        self.assertEqual(response.data['details']['min_items_2'], False)

    def test_rule_check_order_not_found(self):
        """Test rule check with non-existent order."""
        url = '/rules/check/'
        data = {
            'order_id': 99999,
            'rules': ['min_total_100']
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_rule_check_invalid_rule(self):
        """Test rule check with invalid rule name."""
        url = '/rules/check/'
        data = {
            'order_id': self.order_high_total.id,
            'rules': ['invalid_rule']
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_rule_check_missing_fields(self):
        """Test rule check with missing required fields."""
        url = '/rules/check/'
        data = {'order_id': self.order_high_total.id}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rule_check_invalid_order_id(self):
        """Test rule check with invalid order_id."""
        url = '/rules/check/'
        data = {
            'order_id': -1,
            'rules': ['min_total_100']
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestRuleListAPI(APITestCase):
    """Tests for the Rule List API endpoint."""

    def test_list_rules(self):
        """Test listing all available rules."""
        url = '/rules/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 3)

        rule_names = [rule['name'] for rule in response.data]
        self.assertIn('min_total_100', rule_names)
        self.assertIn('min_items_2', rule_names)
        self.assertIn('divisible_by_5', rule_names)

        # Check that each rule has required fields
        for rule in response.data:
            self.assertIn('name', rule)
            self.assertIn('description', rule)
