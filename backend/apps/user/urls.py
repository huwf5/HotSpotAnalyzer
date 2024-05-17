from django.urls import path
from .views import LoginView, RegisterView, VerifyEmailView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view({"post": "create"}), name="register"),
    path("verify/", VerifyEmailView.as_view({"post": "verify"}), name="verify"),
]
