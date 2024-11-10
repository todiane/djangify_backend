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
    """
    API endpoint for managing blog categories.

    Provides read-only access to blog categories with search capabilities.
    Includes post count for each category.

    list:
        Return a paginated list of all categories.

    retrieve:
        Return the details of a specific category by slug.

    search:
        Filter categories by title or description using the search parameter.
        Example: ?search=python
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]
    http_method_names = ["get"]  # Read-only operations

    def get_queryset(self):
        return super().get_queryset().prefetch_related("posts")


class TagViewSet(BaseViewSet):
    """
    API endpoint for managing blog tags.

    Provides read-only access to blog tags with search capabilities.
    Includes post count for each tag.

    list:
        Return a paginated list of all tags.

    retrieve:
        Return the details of a specific tag by slug.

    search:
        Filter tags by title using the search parameter.
        Example: ?search=django
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]
    http_method_names = ["get"]  # Read-only operations

    def get_queryset(self):
        return super().get_queryset().prefetch_related("posts")


class PostViewSet(BaseViewSet):
    """
    API endpoint for managing blog posts.

    Provides full CRUD operations for authenticated staff users and read-only access for others.
    Includes filtering, searching, and ordering capabilities.

    list:
        Return a paginated list of published posts (all posts for staff users).

    retrieve:
        Return the details of a specific post by slug.

    create:
        Create a new blog post (staff only).
        Handles automatic image optimization for featured images.

    update:
        Update an existing blog post (staff only).
        Handles automatic image optimization for featured images.

    partial_update:
        Partially update a blog post (staff only).

    delete:
        Delete a blog post (staff only).

    filters:
        - category__slug: Filter by category slug
        - tags__slug: Filter by tag slug
        - status: Filter by post status (published/draft)
        - is_featured: Filter featured posts
        Example: ?category__slug=python&is_featured=true

    search:
        Search in title, content, and excerpt
        Example: ?search=django

    ordering:
        Order by created_at, published_date, or title
        Example: ?ordering=-published_date
    """

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
