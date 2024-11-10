# Path: apps/blog/views.py

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.views import BaseViewSet
from apps.blog.models import Post, Category, Tag
from apps.blog.serializers import PostSerializer, CategorySerializer, TagSerializer
from apps.core.utils import ImageHandler
import logging

logger = logging.getLogger(__name__)


class CategoryViewSet(BaseViewSet):
    """ViewSet for Category model providing list and retrieve operations."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]
    http_method_names = ["get"]  # Read-only operations

    def get_queryset(self):
        return super().get_queryset().prefetch_related("posts")


class TagViewSet(BaseViewSet):
    """ViewSet for Tag model providing list and retrieve operations."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]
    http_method_names = ["get"]  # Read-only operations

    def get_queryset(self):
        return super().get_queryset().prefetch_related("posts")


class PostViewSet(BaseViewSet):
    """ViewSet for Post model providing full CRUD operations."""

    serializer_class = PostSerializer
    lookup_field = "slug"
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title", "content", "excerpt"]
    filterset_fields = ["category__slug", "tags__slug", "status", "is_featured"]
    ordering_fields = ["created_at", "published_date", "title"]
    ordering = ["-published_date"]

    def get_queryset(self):
        """Returns published posts for non-staff users, all posts for staff."""
        queryset = Post.objects.select_related("category").prefetch_related("tags")

        if not self.request.user.is_staff:
            queryset = queryset.filter(status="published")

        return queryset

    def perform_create(self, serializer):
        """Handle image optimization during post creation."""
        instance = serializer.save()
        if instance.featured_image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.featured_image, "blog/images"
                )
            except Exception as e:
                logger.error(
                    f"Error optimizing image for post {instance.title}: {str(e)}"
                )

    def perform_update(self, serializer):
        """Handle image optimization during post update."""
        instance = serializer.save()
        if instance.featured_image:
            try:
                ImageHandler.save_and_optimize_image(
                    instance.featured_image, "blog/images"
                )
            except Exception as e:
                logger.error(
                    f"Error optimizing image for post {instance.title}: {str(e)}"
                )
