# Path: apps/core/serializers.py

from rest_framework import serializers
from apps.core.models import TimeStampedModel, SEOModel


class TimeStampedModelSerializer(serializers.ModelSerializer):
    """Base serializer for models with timestamps"""

    class Meta:
        model = TimeStampedModel
        fields = ["created_at", "updated_at"]


class SEOModelSerializer(serializers.ModelSerializer):
    """Base serializer for models with SEO fields"""

    class Meta:
        model = SEOModel
        fields = ["meta_title", "meta_description", "meta_keywords"]
