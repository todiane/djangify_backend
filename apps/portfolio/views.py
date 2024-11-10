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

logger = logging.getLogger(__name__)


class TechnologyViewSet(BaseViewSet):
    """ViewSet for Technology model providing list and retrieve operations."""

    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    http_method_names = ["get"]  # Read-only operations


class PortfolioViewSet(BaseViewSet):
    """ViewSet for Portfolio model providing full CRUD operations."""

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
    ordering = ["order", "-created_at"]

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
        """Toggle featured status of a portfolio item."""
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
    """ViewSet for PortfolioImage model."""

    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageSerializer
    ordering_fields = ["order"]
    ordering = ["order"]

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
