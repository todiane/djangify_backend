# Path: apps/core/models.py

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image
import os
import logging
import time

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


def optimize_image(image_path, max_size=(800, 800), quality=85):
    """
    Enhanced utility function to optimize images with performance logging.
    """
    performance_logger = logging.getLogger("performance")
    start_time = time.time()

    try:
        # Get original file size
        original_size = os.path.getsize(image_path)

        img = Image.open(image_path)
        original_dimensions = img.size

        # Convert to RGB if needed
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Resize if larger than max size
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save optimized image
        img.save(image_path, quality=quality, optimize=True)

        # Get optimized file size
        optimized_size = os.path.getsize(image_path)

        # Calculate processing time
        duration = time.time() - start_time

        # Log optimization results
        performance_logger.info(
            f"Image optimization | "
            f"Path: {image_path} | "
            f"Original size: {original_size/1024:.1f}KB | "
            f"Optimized size: {optimized_size/1024:.1f}KB | "
            f"Reduction: {((original_size - optimized_size)/original_size)*100:.1f}% | "
            f"Original dimensions: {original_dimensions} | "
            f"New dimensions: {img.size} | "
            f"Duration: {duration:.2f}s"
        )

    except Exception as e:
        logger.error(f"Error optimizing image {image_path}: {str(e)}")
        performance_logger.error(
            f"Image optimization failed | "
            f"Path: {image_path} | "
            f"Error: {str(e)} | "
            f"Duration: {time.time() - start_time:.2f}s"
        )
        raise
