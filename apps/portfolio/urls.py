# Path: apps/portfolio/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.portfolio.views import (
    PortfolioViewSet,
    TechnologyViewSet,
    PortfolioImageViewSet,
)

router = DefaultRouter()
router.register(
    r"projects", PortfolioViewSet, basename="project"
)  # Keep projects URL for consistency
router.register(r"technologies", TechnologyViewSet, basename="technology")
router.register(r"project-images", PortfolioImageViewSet, basename="project-image")

urlpatterns = [
    path("", include(router.urls)),
]
