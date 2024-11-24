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

logger = logging.getLogger('apps.portfolio')

class TechnologyViewSet(BaseViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    http_method_names = ["get"]  # Read-only operations

class PortfolioViewSet(BaseViewSet):
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
        instance = serializer.save()
        if instance.featured_image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.featured_image, "portfolio/images"
                )
            except Exception as e:
                print(f"Error optimizing image for portfolio {instance.title}: {str(e)}")

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.featured_image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.featured_image, "portfolio/images"
                )
            except Exception as e:
                print(f"Error optimizing image for portfolio {instance.title}: {str(e)}")

def get_queryset(self):
        logger.info("Fetching portfolio queryset")
        queryset = Portfolio.objects.prefetch_related("technologies", "images")
        count = queryset.count()
        logger.info(f"Found {count} portfolio items")
        return queryset

def perform_create(self, serializer):
        """Handle image optimization during portfolio creation."""
        logger.info("Creating new portfolio item")
        instance = serializer.save()
        if instance.featured_image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.featured_image, "portfolio/images"
                )
                logger.info(f"Successfully created portfolio item: {instance.title}")
            except Exception as e:
                logger.error(
                    f"Error optimizing image for portfolio {instance.title}: {str(e)}"
                )
                raise
            try:
                ImageHandler.save_and_optimize_image(
                    instance.featured_image, "portfolio/images"
                )
                logger.info(f"Successfully created portfolio item: {instance.title}")
            except Exception as e:
                logger.error(
                    f"Error optimizing image for portfolio {instance.title}: {str(e)}"
                )
                raise

def perform_update(self, serializer):
        """Handle image optimization during portfolio update."""
        logger.info("Updating portfolio item")
        instance = serializer.save()
        if instance.featured_image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.featured_image, "portfolio/images"
                )
                logger.info(f"Successfully updated portfolio item: {instance.title}")
            except Exception as e:
                logger.error(
                    f"Error optimizing image for portfolio {instance.title}: {str(e)}"
                )
                raise

def perform_destroy(self, instance):
        """Log portfolio deletion."""
        logger.info(f"Deleting portfolio item: {instance.title}")
        super().perform_destroy(instance)
        logger.info(f"Successfully deleted portfolio item: {instance.title}")

class PortfolioImageViewSet(BaseViewSet):
    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageSerializer
    ordering_fields = ["order"]
    ordering = ["order"]

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.image, "portfolio/gallery"
                )
            except Exception as e:
                print(f"Error optimizing portfolio image: {str(e)}")

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.image, "portfolio/gallery"
                )
            except Exception as e:
                print(f"Error optimizing portfolio image: {str(e)}")
