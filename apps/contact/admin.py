from django.contrib import admin
from .models import Contact
from django.utils.html import format_html

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact_reason', 'status', 'created_at', 'ip_address')
    list_filter = ('status', 'contact_reason', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at', 'ip_address', 'user_agent')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'contact_reason')
        }),
        ('Message', {
            'fields': ('message', 'status')
        }),
        ('Meta Information', {
            'fields': ('created_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return False  # Prevent adding messages through admin

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('name', 'email', 'message', 'contact_reason')
        return self.readonly_fields
