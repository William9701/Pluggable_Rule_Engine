"""
API views for rule evaluation.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from orders.models import Order
from .engine import RuleEngine, RuleRegistry
from .serializers import (
    RuleCheckRequestSerializer,
    RuleCheckResponseSerializer,
    RuleInfoSerializer
)

logger = logging.getLogger(__name__)


class RuleCheckView(APIView):
    """
    API endpoint to evaluate rules against an order.

    POST /rules/check/
    """

    @swagger_auto_schema(
        operation_description="Evaluate multiple rules against an order",
        request_body=RuleCheckRequestSerializer,
        responses={
            200: RuleCheckResponseSerializer,
            400: openapi.Response('Bad Request', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING),
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            404: openapi.Response('Order Not Found', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING),
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
        },
        tags=['Rules']
    )
    def post(self, request):
        """
        Evaluate rules against an order.

        Request body:
        {
            "order_id": 1,
            "rules": ["min_total_100", "min_items_2"]
        }

        Response:
        {
            "passed": true,
            "details": {
                "min_total_100": true,
                "min_items_2": false
            }
        }
        """
        # Validate request data
        serializer = RuleCheckRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid request data: {serializer.errors}")
            return Response(
                {
                    'error': 'Invalid request',
                    'detail': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        order_id = validated_data['order_id']
        rule_names = validated_data['rules']

        # Retrieve the order
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            logger.warning(f"Order {order_id} not found")
            return Response(
                {
                    'error': 'Order not found',
                    'detail': f'Order with id {order_id} does not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Evaluate rules
        try:
            engine = RuleEngine()
            result = engine.evaluate_rules(order, rule_names)

            logger.info(
                f"Rules evaluated for order {order_id}: "
                f"Passed={result['passed']}, Details={result['details']}"
            )

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error evaluating rules: {str(e)}", exc_info=True)
            raise


class RuleListView(APIView):
    """
    API endpoint to list all available rules.

    GET /rules/
    """

    @swagger_auto_schema(
        operation_description="Get a list of all available rules",
        responses={
            200: RuleInfoSerializer(many=True)
        },
        tags=['Rules']
    )
    def get(self, request):
        """
        Get all available rules.

        Response:
        [
            {
                "name": "min_total_100",
                "description": "Validates that order total is greater than 100"
            },
            ...
        ]
        """
        rules = RuleRegistry.get_all_rules()
        rules_info = [
            {
                'name': rule_class.name,
                'description': rule_class.description
            }
            for rule_class in rules.values()
        ]

        logger.info(f"Retrieved {len(rules_info)} available rules")
        return Response(rules_info, status=status.HTTP_200_OK)
