from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


@api_view(["GET"])
def api_root(request):
    return Response(
        {
            "blog": request.build_absolute_uri("/api/v1/blog/"),
            "portfolio": request.build_absolute_uri("/api/v1/portfolio/"),
            "schema": request.build_absolute_uri("/api/schema/"),
            "docs": request.build_absolute_uri("/api/docs/"),
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("summernote/", include("django_summernote.urls")),
    path("api/", include("apps.core.urls")),
    path("api/v1", api_root, name="api-root"),
    path("api/v1/", api_root, name="api-root"),
    path("api/v1/blog/", include("apps.blog.urls")),
    path("api/v1/portfolio/", include("apps.portfolio.urls")),
    # API Documentation URLs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

# Add static and media URL patterns
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
