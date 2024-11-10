# Path: apps/blog/admin.py

from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Category, Tag


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = ("title", "category", "status", "created_at", "is_featured")
    list_filter = ("status", "category", "tags", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    list_editable = ("status", "is_featured")

    fieldsets = (
        (
            "Content",
            {"fields": ("title", "slug", "content", "excerpt", "featured_image")},
        ),
        ("Categories and Tags", {"fields": ("category", "tags")}),
        ("Publishing", {"fields": ("status", "published_date", "is_featured")}),
        (
            "SEO",
            {
                "fields": ("meta_title", "meta_description", "meta_keywords"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "post_count")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)

    def post_count(self, obj):
        return obj.posts.count()

    post_count.short_description = "Number of Posts"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "post_count")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)

    def post_count(self, obj):
        return obj.posts.count()

    post_count.short_description = "Number of Posts"
