# Path: apps/portfolio/views.py

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.views import BaseViewSet
from apps.portfolio.models import Technology, Portfolio, PortfolioImage
from apps.portfolio.serializers import (
    TechnologySerializer,
    PortfolioSerializer,
    PortfolioImageSerializer,
)
from apps.core.utils import ImageHandler
import logging
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class TechnologyViewSet(BaseViewSet):
    """
    API endpoint for managing technology/skill entries.

    Provides read-only access to technologies used in portfolio projects.

    list:
        Return a paginated list of all technologies.

    retrieve:
        Return the details of a specific technology by slug.

    search:
        Search technologies by name.
        Example: ?search=python
    """

    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name", "-created_at"]
    http_method_names = ["get"]

@method_decorator(csrf_exempt, name='dispatch')
class PortfolioViewSet(BaseViewSet):
    """
    API endpoint for managing portfolio projects.

    Provides full CRUD operations for authenticated staff users and read-only access for others.
    Includes filtering, searching, and ordering capabilities.

    list:
        Return a paginated list of portfolio projects.

    retrieve:
        Return the details of a specific project by slug.

    create:
        Create a new portfolio project (staff only).
        Handles automatic image optimization for featured images.

    update:
        Update an existing portfolio project (staff only).
        Handles automatic image optimization for featured images.

    partial_update:
        Partially update a portfolio project (staff only).

    delete:
        Delete a portfolio project (staff only).

    toggle_featured:
        Toggle the featured status of a portfolio project (staff only).

    filters:
        - technologies__slug: Filter by technology slug
        - is_featured: Filter featured projects
        Example: ?technologies__slug=python&is_featured=true

    search:
        Search in title, description, and short_description
        Example: ?search=django

    ordering:
        Order by order, created_at
        Example: ?ordering=order
    """

    serializer_class = PortfolioSerializer
    lookup_field = "slug"
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["technologies__slug", "is_featured"]
    search_fields = ["title", "description", "short_description"]
    ordering_fields = ["order", "created_at"]
    ordering = ["order"]

    def get_queryset(self):
        return Portfolio.objects.prefetch_related("technologies", "images")

    def perform_create(self, serializer):
        """Handle image optimization during portfolio creation."""
        instance = serializer.save()
        if instance.featured_image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.featured_image, "portfolio/images"
                )
            except Exception as e:
                logger.error(
                    f"Error optimizing image for portfolio {instance.title}: {str(e)}"
                )

    def perform_update(self, serializer):
        """Handle image optimization during portfolio update."""
        instance = serializer.save()
        if instance.featured_image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.featured_image, "portfolio/images"
                )
            except Exception as e:
                logger.error(
                    f"Error optimizing image for portfolio {instance.title}: {str(e)}"
                )

    @action(detail=True, methods=["post"])
    def toggle_featured(self, request, slug=None):
        """
        Toggle featured status of a portfolio project.

        Requires staff user authentication.
        Returns updated portfolio data.
        """
        try:
            portfolio = self.get_object()
            portfolio.is_featured = not portfolio.is_featured
            portfolio.save()
            return self.success_response(
                data=self.get_serializer(portfolio).data,
                message=f"Portfolio {'featured' if portfolio.is_featured else 'unfeatured'} successfully",
            )
        except Exception as e:
            logger.error(f"Error toggling featured status: {str(e)}")
            return self.error_response(str(e))


class PortfolioImageViewSet(BaseViewSet):
    """
    API endpoint for managing portfolio gallery images.

    Provides operations for managing additional images associated with portfolio projects.
    Handles automatic image optimization.

    list:
        Return a paginated list of portfolio images.

    create:
        Add a new image to a portfolio project (staff only).
        Handles automatic image optimization.

    update:
        Update an existing portfolio image (staff only).
        Handles automatic image optimization.

    delete:
        Delete a portfolio image (staff only).

    ordering:
        Order by image order
        Example: ?ordering=order
    """

    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageSerializer
    ordering_fields = ["order", "created_at"]
    ordering = ["order", "-created_at"]

    def perform_create(self, serializer):
        """Handle image optimization during image creation."""
        instance = serializer.save()
        if instance.image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.image, "portfolio/gallery"
                )
            except Exception as e:
                logger.error(f"Error optimizing portfolio image: {str(e)}")

    def perform_update(self, serializer):
        """Handle image optimization during image update."""
        instance = serializer.save()
        if instance.image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.image, "portfolio/gallery"
                )
            except Exception as e:
                logger.error(f"Error optimizing portfolio image: {str(e)}")

def get_queryset(self):
    queryset = Portfolio.objects.prefetch_related("technologies", "images")
    logger.debug(f"Portfolio queryset count: {queryset.count()}")
    return queryset
