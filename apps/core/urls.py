# Path: apps/core/urls.py

from django.urls import path
from apps.core.views import health_check

urlpatterns = [
    path("health/", health_check, name="health_check"),
]