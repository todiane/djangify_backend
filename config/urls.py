from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def api_root(request):
    return Response(
        {
            "blog": request.build_absolute_uri("/api/v1/blog/"),
            "portfolio": request.build_absolute_uri("/api/v1/portfolio/"),
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "summernote/", include("django_summernote.urls")
    ),  # Make sure this is before other URLs
    path("api/", include("apps.core.urls")),
    path("api/v1", api_root, name="api-root"),
    path("api/v1/", api_root, name="api-root"),
    path("api/v1/blog/", include("apps.blog.urls")),
    path("api/v1/portfolio/", include("apps.portfolio.urls")),
]

# Add static and media URL patterns
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
