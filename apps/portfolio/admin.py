# Path: apps/portfolio/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin
from .models import Technology, Portfolio, PortfolioImage


class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1
    fields = ("image", "caption", "order", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>', obj.image.url
            )
        return "No image"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields["order"].required = False
        return formset


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Portfolio)
class PortfolioAdmin(SummernoteModelAdmin):
    summernote_fields = ("description",)

    list_display = (
        "title",
        "featured_image_preview",
        "is_featured",
        "order",
        "created_at",
    )
    list_filter = ("is_featured", "technologies", "created_at")
    search_fields = ("title", "description", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    inlines = [PortfolioImageInline]
    list_editable = ("order", "is_featured")

    fieldsets = (
        ("Basic Information", {"fields": ("title", "slug", "short_description")}),
        ("Content", {"fields": ("description", "featured_image", "technologies")}),
        (
            "Project Details",
            {"fields": ("project_url", "github_url", "is_featured", "order")},
        ),
        (
            "SEO",
            {
                "fields": ("meta_title", "meta_description", "meta_keywords"),
                "classes": ("collapse",),
            },
        ),
    )

    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>', obj.featured_image.url
            )
        return "No image"

    featured_image_preview.short_description = "Preview"

    class Media:
        js = (
            "admin/js/vendor/jquery/jquery.min.js",
            "admin/js/jquery.init.js",
            "js/admin_customizations.js",
        )
