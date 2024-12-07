from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _

class Contact(models.Model):
    CONTACT_REASONS = (
        ('other', 'Other'),
        ('buy_project', 'Buy a project that is for sale'),
        ('ecommerce', 'Bespoke eCommerce store'),
        ('lms', 'Bespoke Learning Management System'),
        ('speaking', 'Speaking/Training Opportunity'),
    )

    STATUS_CHOICES = (
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    )

    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        help_text="Name of the person making contact"
    )
    email = models.EmailField(
        help_text="Email address for correspondence"
    )
    contact_reason = models.CharField(
        max_length=20,
        choices=CONTACT_REASONS,
        default='other',
        help_text="Reason for making contact"
    )
    message = models.TextField(
        validators=[
            MinLengthValidator(10, "Message must be at least 10 characters long"),
            MaxLengthValidator(1000, "Message cannot exceed 1000 characters")
        ],
        help_text="The message content (1000 characters max)"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address of the sender"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the message was sent"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        help_text="Current status of the contact message"
    )
    user_agent = models.TextField(
        blank=True,
        null=True,
        help_text="Browser/client information"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ip_address', 'created_at']),
            models.Index(fields=['status']),
        ]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def mark_as_read(self):
        if self.status == 'new':
            self.status = 'read'
            self.save()

    def mark_as_replied(self):
        self.status = 'replied'
        self.save()
