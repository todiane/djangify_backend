# Path: apps/portfolio/serializers.py

from rest_framework import serializers
from apps.core.serializers import TimeStampedModelSerializer, SEOModelSerializer
from apps.portfolio.models import Technology, Portfolio, PortfolioImage

class TechnologySerializer(TimeStampedModelSerializer):
    class Meta:
        model = Technology
        fields = ["id", "name", "slug", "icon", "created_at", "updated_at"]

class PortfolioImageSerializer(TimeStampedModelSerializer):
    display_image = serializers.CharField(read_only=True)
    
    class Meta:
        model = PortfolioImage
        fields = ["id", "image", "image_url", "caption", "order", "display_image", "created_at", "updated_at"]

class PortfolioSerializer(TimeStampedModelSerializer, SEOModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)
    images = PortfolioImageSerializer(many=True, read_only=True)
    display_image = serializers.CharField(read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            "id",
            "title",
            "slug", 
            "description",
            "short_description",
            "featured_image",
            "featured_image_url",
            "display_image",
            "technologies",
            "external_url_type",
            "external_url",
            "is_featured",
            "order",
            "images",
            "created_at",
            "updated_at",
            "meta_title",
            "meta_description", 
            "meta_keywords",
        ]
        