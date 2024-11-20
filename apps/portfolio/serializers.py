# Path: apps/portfolio/serializers.py

from rest_framework import serializers
from apps.core.serializers import TimeStampedModelSerializer, SEOModelSerializer
from apps.portfolio.models import Technology, Portfolio, PortfolioImage


class TechnologySerializer(TimeStampedModelSerializer):
    class Meta:
        model = Technology
        fields = ["id", "name", "slug", "icon", "created_at", "updated_at"]


class PortfolioImageSerializer(TimeStampedModelSerializer):
    class Meta:
        model = PortfolioImage
        fields = ["id", "image", "caption", "order", "created_at", "updated_at"]


class PortfolioSerializer(TimeStampedModelSerializer, SEOModelSerializer):
    technologies = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

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

    def get_technologies(self, obj):
        return TechnologySerializer(obj.technologies.all(), many=True).data

    def get_images(self, obj):
        return PortfolioImageSerializer(obj.images.all(), many=True).data
    