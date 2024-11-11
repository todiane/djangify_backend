# apps/core/middleware.py
from time import time
import logging
from django.db import connection
from django.conf import settings

performance_logger = logging.getLogger("performance")
api_logger = logging.getLogger("api")


class PerformanceMonitoringMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.slow_query_threshold = getattr(
            settings, "SLOW_QUERY_THRESHOLD", 1.0
        )  # seconds

    def __call__(self, request):
        # Start timing
        start_time = time()

        # Count queries before request
        initial_queries = len(connection.queries)

        response = self.get_response(request)

        # Calculate request processing time
        duration = time() - start_time

        # Log slow requests
        if duration > self.slow_query_threshold:
            performance_logger.warning(
                f"Slow request: {request.method} {request.path} took {duration:.2f}s"
            )

        # Log database query statistics if DEBUG is True
        if settings.DEBUG:
            queries_count = len(connection.queries) - initial_queries
            if queries_count > 0:
                total_query_time = sum(
                    float(query.get("time", 0))
                    for query in connection.queries[initial_queries:]
                )
                performance_logger.info(
                    f"Request: {request.method} {request.path} | "
                    f"Queries: {queries_count} | "
                    f"Query time: {total_query_time:.2f}s | "
                    f"Total time: {duration:.2f}s"
                )

        return response


class APIMonitoringMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only monitor API endpoints
        if not request.path.startswith("/api/"):
            return self.get_response(request)

        start_time = time()
        response = self.get_response(request)
        duration = time() - start_time

        # Log API request details
        api_logger.info(
            f"API Request | "
            f"Method: {request.method} | "
            f"Path: {request.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {duration:.2f}s | "
            f"User: {request.user.username if request.user.is_authenticated else 'anonymous'}"
        )

        # Log rate limit hits
        if response.status_code == 429:  # Too Many Requests
            api_logger.warning(
                f"Rate limit exceeded | "
                f"Path: {request.path} | "
                f"User: {request.user.username if request.user.is_authenticated else 'anonymous'}"
            )

        return response
