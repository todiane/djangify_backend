# Path: apps/blog/serializers.py

from rest_framework import serializers
from apps.blog.models import Category, Tag, Post
from apps.core.serializers import TimeStampedModelSerializer, SEOModelSerializer


class CategorySerializer(TimeStampedModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "post_count",
            "created_at",
            "updated_at",
        ]

    def get_post_count(self, obj):
        return obj.posts.count()


class TagSerializer(TimeStampedModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ["id", "title", "slug", "post_count", "created_at", "updated_at"]

    def get_post_count(self, obj):
        return obj.posts.count()


class PostSerializer(TimeStampedModelSerializer, SEOModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "excerpt",
            "featured_image",
            "category",
            "tags",
            "status",
            "published_date",
            "is_featured",
            "created_at",
            "updated_at",
            "meta_title",
            "meta_description",
            "meta_keywords",
            "reading_time",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_reading_time(self, obj):
        word_count = len(obj.content.split())
        minutes = word_count / 200  # Assuming average reading speed of 200 words/minute
        return max(1, round(minutes))  # Minimum 1 minute reading time
