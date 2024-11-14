from django.db import models  # Path: apps/blog/models.py

from django.db import models
from django.core.validators import FileExtensionValidator
from apps.core.models import TimeStampedModel, SEOModel, SluggedModel, optimize_image
from django.conf import settings
import os


class PostManager(models.Manager):
    """
    Custom manager for Post model providing common query operations.
    """

    def get_queryset(self):
        return (
            super().get_queryset().select_related("category").prefetch_related("tags")
        )

    def published(self):
        return (
            self.get_queryset().filter(status="published").order_by("-published_date")
        )

    def featured(self):
        return self.published().filter(is_featured=True)

    def by_category(self, category_slug):
        return self.published().filter(category__slug=category_slug)

    def by_tag(self, tag_slug):
        return self.published().filter(tags__slug=tag_slug)


class Category(TimeStampedModel, SluggedModel):
    """Category model for organizing blog posts."""

    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['title', '-created_at']

    def __str__(self):
        return self.title


class Tag(TimeStampedModel, SluggedModel):
    """Tag model for labeling blog posts."""

    class Meta:
        ordering = ['title', '-created_at']

    def __str__(self):
        return self.title


class Post(TimeStampedModel, SluggedModel, SEOModel):
    """Blog post model with SEO and timestamp capabilities."""

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    content = models.TextField()
    excerpt = models.TextField(blank=True, help_text="A short summary of the post")
    featured_image = models.ImageField(
        upload_to="blog",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"]),
        ],
        help_text="Image should be optimized before upload",
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="posts"
    )
    tags = models.ManyToManyField(Tag, related_name="posts")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    published_date = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    objects = PostManager()

    class Meta:
        ordering = ["-published_date", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Optimize image after save if it exists
        if self.featured_image:
            optimize_image(
                self.featured_image.path,
                max_size=getattr(settings, "BLOG_IMAGE_SIZE", (800, 800)),
                quality=getattr(settings, "BLOG_IMAGE_QUALITY", 85),
            )

    def get_absolute_url(self):
        """Returns the full URL to the post."""
        from django.conf import settings

        base_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
        return f"{base_url.rstrip('/')}/blog/{self.slug}"



