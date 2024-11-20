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
        logger.info("Fetching portfolio queryset")
        queryset = Portfolio.objects.prefetch_related("technologies", "images")
        count = queryset.count()
        logger.info(f"Found {count} portfolio items")
        return queryset

    def list(self, request, *args, **kwargs):
        logger.info("Portfolio list endpoint called")
        response = super().list(request, *args, **kwargs)
        logger.info(f"Portfolio list response data: {response.data}")
        return response
    
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Portfolio retrieve called with kwargs: {kwargs}")
        response = super().retrieve(request, *args, **kwargs)
        logger.info(f"Portfolio retrieve response data: {response.data}")
        return response

    def perform_create(self, serializer):
        logger.info("Creating new portfolio item")
        instance = serializer.save()
        if instance.featured_image:
            try:
                path = ImageHandler.save_and_optimize_image(
                    instance.featured_image, "portfolio/images"
                )
                logger.info(f"Image saved at: {path}")
            except Exception as e:
                logger.error(
                    f"Error optimizing image for portfolio {instance.title}: {str(e)}"
                )

    def perform_update(self, serializer):
        logger.info("Updating portfolio item")
        instance = serializer.save()
        if instance.featured_image:
            try:
                path = ImageHandler.save_and_optimize_image(
                    instance.featured_image, "portfolio/images"
                )
                logger.info(f"Image updated at: {path}")
            except Exception as e:
                logger.error(
                    f"Error optimizing image for portfolio {instance.title}: {str(e)}"
                )


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
                logger.error(f"Error optimizing portfolio image: {str(e)}")

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.image, "portfolio/gallery"
                )
            except Exception as e:
                logger.error(f"Error optimizing portfolio image: {str(e)}")
