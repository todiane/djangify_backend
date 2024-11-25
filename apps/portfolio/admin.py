# apps/portfolio/admin.py

import logging
from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Technology, Portfolio, PortfolioImage

# Add this new form class
class PortfolioAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditor5Widget())
    
    class Meta:
        model = Portfolio
        fields = '__all__'

class PortfolioImageInline(admin.TabularInline):
    # Your existing PortfolioImageInline code remains the same
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
    # Your existing TechnologyAdmin code remains the same
    list_display = ("name", "slug", "icon", "category")
    list_filter = ("category",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name", "-created_at"]

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    form = PortfolioAdminForm  # Add this line to use the custom form
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
        ("Basic Information", {
            "fields": ("title", "slug", "short_description", "status"),
            "classes": ("wide", "extrapretty"),  # Add these classes
        }),
        ("Content", {
            "fields": ("description", "featured_image", "featured_image_url", "technologies"),
            "classes": ("wide", "extrapretty"),
        }),
        ("Project Details", {
            "fields": (
                "external_url_type",
                "external_url",
                "live_site_url",
                "is_featured",
                "order"
            ),
            "classes": ("wide", "extrapretty"),
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description", "meta_keywords"),
            "classes": ("collapse", "wide", "extrapretty"),
        }),
    )

    def image_preview(self, obj):
        if obj.display_image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.display_image)
        return "No image"

    image_preview.short_description = "Preview"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            logger = logging.getLogger('apps.portfolio')
            logger.error(f"Error saving portfolio {obj.title}: {str(e)}")
            raise