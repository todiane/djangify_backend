# apps/core/sitemaps.py
from django.contrib.sitemaps import Sitemap
from apps.portfolio.models import Portfolio


class PortfolioSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Portfolio.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return ["home", "portfolio", "contact"]

    def location(self, item):
        """
        Define the URL for each static page.
        Using forward slashes to maintain consistency with frontend routes.
        """
        if item == "home":
            return "/"
        return f"/{item}"
