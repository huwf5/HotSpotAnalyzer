from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import LoginView, RegisterView, VerifyEmailView, ActiveView

urlpatterns = [
    path("register/", RegisterView.as_view({"post": "create"}), name="register"),
    path("verify/", VerifyEmailView.as_view({"post": "verify"}), name="verify"),
    path("active/", ActiveView.as_view({"post": "active"}), name="active"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
