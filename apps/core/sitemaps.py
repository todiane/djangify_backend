# apps/core/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.blog.models import Post
from apps.portfolio.models import Portfolio


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated_at


class PortfolioSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Portfolio.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 1.0

    def items(self):
        return ["home", "portfolio", "blog", "contact"]

    def location(self, item):
        """
        Define the URL for each static page.
        Using forward slashes to maintain consistency with frontend routes.
        """
        if item == "home":
            return "/"
        return f"/{item}"
