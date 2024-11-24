from django.http import JsonResponse
import logging

logger = logging.getLogger('django')

class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f'Error processing request: {request.path}', exc_info=True)
        if request.path.startswith('/admin/'):
            return None  # Let Django's admin handle its own errors
        return JsonResponse({
            'error': 'An error occurred processing your request',
            'detail': str(exception)
        }, status=500)
  