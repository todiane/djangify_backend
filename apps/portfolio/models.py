# Path: apps/portfolio/models.py

from django.db import models
from django.core.validators import FileExtensionValidator
from apps.core.models import TimeStampedModel, SEOModel, SluggedModel, optimize_image
from django.conf import settings
import os
import re


def portfolio_image_path(instance, filename):
    """Generate upload path for portfolio's featured image"""
    ext = filename.split(".")[-1]
    filename = f"{instance.slug}.{ext}"
    return os.path.join("portfolio", filename)


def portfolio_gallery_image_path(instance, filename):
    """Generate upload path for portfolio gallery images"""
    ext = filename.split(".")[-1]
    return (
        f'portfolio/gallery/{instance.portfolio.slug}-{instance.order or "new"}.{ext}'
    )


def validate_github_url(value):
    """Simple validation for GitHub repository URL"""
    if not re.match(r"^https?://github\.com/", value):
        raise ValueError("Please enter a valid GitHub repository URL")


class Technology(TimeStampedModel):
    """Model representing a technology/skill used in portfolio projects"""

    name = models.CharField(
        max_length=100, help_text="Name of the technology (e.g., Python, React, Django)"
    )
    slug = models.SlugField(unique=True, help_text="URL-friendly version of the name")
    icon = models.CharField(
        max_length=50, help_text="Icon identifier or URL for the technology"
    )

    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Portfolio(TimeStampedModel, SEOModel):
    """Model representing a portfolio project"""

    title = models.CharField(max_length=200, help_text="Title of the portfolio project")
    slug = models.SlugField(unique=True, help_text="URL-friendly version of the title")
    description = models.TextField(help_text="Detailed description of the project")
    short_description = models.CharField(
        max_length=200, help_text="Brief summary of the project"
    )
    featured_image = models.ImageField(
        upload_to=portfolio_image_path,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
        ],
        help_text="Upload a JPG or PNG image",
        null=True,
        blank=True,
    )
    technologies = models.ManyToManyField(
        Technology,
        related_name="portfolios",
        help_text="Technologies used in this project",
    )
    project_url = models.URLField(
        blank=True, help_text="Live project URL (if available)"
    )
    github_url = models.URLField(
        blank=True, validators=[validate_github_url], help_text="GitHub repository URL"
    )
    is_featured = models.BooleanField(
        default=False, help_text="Display this project in featured sections"
    )
    order = models.IntegerField(
        default=0, help_text="Display order in the portfolio list"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Optimize image after save if it exists
        if self.featured_image:
            optimize_image(
                self.featured_image.path,
                max_size=getattr(settings, "PORTFOLIO_IMAGE_SIZE", (1200, 800)),
                quality=getattr(settings, "PORTFOLIO_IMAGE_QUALITY", 85),
            )

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name_plural = "Portfolios"

    def __str__(self):
        return self.title


class PortfolioImage(TimeStampedModel):
    """Model representing additional images for a portfolio project"""

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="Portfolio project this image belongs to",
    )
    image = models.ImageField(
        upload_to=portfolio_gallery_image_path,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
        ],
        help_text="Additional project image (JPG or PNG)",
    )
    caption = models.CharField(
        max_length=200, blank=True, help_text="Description of the image"
    )
    order = models.IntegerField(default=0, help_text="Display order in the gallery")

    def save(self, *args, **kwargs):
        if not self.order:
            max_order = PortfolioImage.objects.filter(
                portfolio=self.portfolio
            ).aggregate(models.Max("order"))["order__max"]
            self.order = (max_order or 0) + 1

        super().save(*args, **kwargs)

        # Optimize image after save
        if self.image:
            optimize_image(
                self.image.path,
                max_size=getattr(settings, "PORTFOLIO_GALLERY_IMAGE_SIZE", (1200, 800)),
                quality=getattr(settings, "PORTFOLIO_IMAGE_QUALITY", 85),
            )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image {self.order} for {self.portfolio.title}"
