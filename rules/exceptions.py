"""
Custom exception handlers for the rules API.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides detailed error responses.

    Args:
        exc: The exception instance
        context: The context in which the exception occurred

    Returns:
        Response object with error details
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # If response is None, it's not a DRF exception
    if response is None:
        # Log the unexpected exception
        logger.error(
            f"Unhandled exception: {type(exc).__name__}: {str(exc)}",
            exc_info=True
        )

        # Handle KeyError (e.g., rule not found)
        if isinstance(exc, KeyError):
            return Response(
                {
                    'error': 'Invalid rule name',
                    'detail': str(exc),
                    'status_code': status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generic error response for other exceptions
        return Response(
            {
                'error': 'Internal server error',
                'detail': 'An unexpected error occurred. Please try again later.',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Add custom fields to DRF error responses
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
