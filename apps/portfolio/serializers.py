# Path: apps/portfolio/serializers.py

from rest_framework import serializers
from apps.portfolio.models import Technology, Portfolio, PortfolioImage
from apps.core.serializers import TimeStampedModelSerializer, SEOModelSerializer


class TechnologySerializer(TimeStampedModelSerializer):
    class Meta:
        model = Technology
        fields = ["id", "name", "slug", "icon", "created_at", "updated_at"]


class PortfolioImageSerializer(TimeStampedModelSerializer):
    class Meta:
        model = PortfolioImage
        fields = ["id", "image", "caption", "order", "created_at", "updated_at"]


class PortfolioSerializer(TimeStampedModelSerializer, SEOModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)
    images = PortfolioImageSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "short_description",
            "featured_image",
            "technologies",
            "project_url",
            "github_url",
            "is_featured",
            "order",
            "images",
            "created_at",
            "updated_at",
            "meta_title",
            "meta_description",
            "meta_keywords",
        ]
