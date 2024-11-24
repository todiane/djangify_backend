import logging
from django.contrib import admin
from django.utils.html import format_html
from .models import Technology, Portfolio, PortfolioImage

class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1
    fields = ('image', 'image_url', 'caption', 'order', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.display_image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.display_image)
        return "No image"

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "category")
    list_filter = ("category",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name", "-created_at"]

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "image_preview",
        "status",
        "external_url_type",
        "is_featured",
        "order",
        "created_at",
    )
    list_filter = ("status", "is_featured", "external_url_type", "technologies", "created_at")
    search_fields = ("title", "description", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    inlines = [PortfolioImageInline]
    list_editable = ("order", "is_featured", "status")
    ordering = ["order", "-created_at"]

    fieldsets = (
        ("Basic Information", {"fields": ("title", "slug", "short_description", "status")}),
        ("Content", {"fields": ("description", "featured_image", "featured_image_url", "technologies")}),
        (
            "Project Details",
            {
                "fields": (
                    "external_url_type",
                    "external_url",
                    "live_site_url",
                    "is_featured",
                    "order"
                )
            },
        ),
        (
            "SEO",
            {
                "fields": ("meta_title", "meta_description", "meta_keywords"),
                "classes": ("collapse",),
            },
        ),
    )

    def image_preview(self, obj):
        if obj.display_image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.display_image)
        return "No image"

    image_preview.short_description = "Preview"

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            logger = logging.getLogger('apps.portfolio')
            logger.error(f"Error saving portfolio {obj.title}: {str(e)}")
            raise
        