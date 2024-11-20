# Path: apps/core/models.py

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import logging


logger = logging.getLogger(__name__)


class TimeStampedModel(models.Model):
    """
    Abstract base model providing automatic timestamps.
    """

    created_at = models.DateTimeField(
        default=timezone.now, help_text="The datetime this object was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="The datetime this object was last updated"
    )

    class Meta:
        abstract = True
        ordering = ['-created_at'] 


class SEOModel(models.Model):
    """
    Abstract base model providing SEO fields.
    """

    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="Maximum 60 characters. Should be unique and descriptive.",
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Maximum 160 characters. Provide a concise summary.",
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords. Maximum 10 keywords.",
    )

    class Meta:
        abstract = True


class SluggedModel(models.Model):
    """
    Abstract base model providing slug functionality.
    """

    title = models.CharField(max_length=200, help_text="Title of the content")
    slug = models.SlugField(
        max_length=100, unique=True, help_text="URL-friendly version of the title"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
