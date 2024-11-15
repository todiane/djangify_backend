# Path: apps/core/urls.py

from django.urls import path
from apps.core.auth import CustomTokenObtainPairView
from apps.core.views import health_check, UserDetailView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("auth/user/", UserDetailView.as_view(), name="user_detail"),

]
