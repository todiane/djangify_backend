from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import PortfolioSitemap, StaticSitemap
from django.views.generic import TemplateView

sitemaps = {
    "portfolio": PortfolioSitemap,
    "static": StaticSitemap,
}

@api_view(["GET"])
def api_root(request):
    return Response(
        {
            "portfolio": request.build_absolute_uri("/api/v1/portfolio/"),
        }
    )

urlpatterns = [
    path("admin/", admin.site.urls),
    path("summernote/", include("django_summernote.urls")),
    path("api/", include("apps.core.urls")),
    path("api/v1/", api_root, name="api-root"),
    path("api/v1/portfolio/", include("apps.portfolio.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
]

handler404 = "apps.core.views.custom_404"
handler500 = "apps.core.views.custom_500"

# Add static and media URL patterns
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
