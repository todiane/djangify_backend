from django.db import models
from cloudinary.models import CloudinaryField

class Technology(models.Model):
    TECH_CATEGORIES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('mobile', 'Mobile'),
        ('other', 'Other')
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50)
    category = models.CharField(
        max_length=20,
        choices=TECH_CATEGORIES,
        default='other',
        help_text="Category of the technology"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['name', '-created_at']

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    EXTERNAL_URL_TYPES = (
        ('github', 'GitHub Repository'),
        ('marketplace', 'Marketplace Listing'),
    )

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200)
    featured_image = CloudinaryField('image', blank=True, null=True, folder='portfolio/featured')
    featured_image_url = models.URLField(blank=True, null=True)
    technologies = models.ManyToManyField(Technology, related_name="portfolios")
    external_url_type = models.CharField(
        max_length=20,
        choices=EXTERNAL_URL_TYPES,
        blank=True,
        null=True
    )
    external_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Current status of the portfolio item"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name_plural = "Portfolios"

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        return self.featured_image_url or self.featured_image.url if self.featured_image else None

class PortfolioImage(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', blank=True, null=True, folder='portfolio/gallery')
    image_url = models.URLField(blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    @property
    def display_image(self):
        return self.image_url or self.image.url if self.image else None

    def __str__(self):
        return f"{self.portfolio.title} - Image {self.order}"
