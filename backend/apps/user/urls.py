from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    VerifyEmailView,
    WaitingListView,
    UserView,
)

router = DefaultRouter()
router.register(r"waitinglist", WaitingListView, basename="waitinglist")
router.register(r"user", UserView, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view({"post": "create"}), name="register"),
    path("verify/", VerifyEmailView.as_view({"post": "verify"}), name="verify"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
