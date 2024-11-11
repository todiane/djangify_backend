from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, register, logout

urlpatterns = [
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
]
