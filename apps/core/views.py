# Path: apps/core/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@require_GET
def health_check(request):
    """Basic health check endpoint for Railway deployment"""
    return JsonResponse(
        {"status": "healthy", "service": "djangify_backend", "version": "1.0.0"}
    )


class BaseViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet class with simplified response handling.
    Other ViewSets in the application will inherit from this.
    """

    def success_response(self, data=None, message=None, status_code=status.HTTP_200_OK):
        """Create a standardized success response"""
        response = {"status": "success", "data": data}
        if message:
            response["message"] = message
        return Response(response, status=status_code)

    def error_response(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        """Create a standardized error response"""
        return Response({"status": "error", "message": message}, status=status_code)

    def handle_exception(self, exc):
        """Global exception handler"""
        logger.error(f"Error in {self.__class__.__name__}: {str(exc)}")
        return self.error_response(
            message=str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
