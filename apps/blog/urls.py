# Path: apps/blog/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.blog.views import PostViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]

