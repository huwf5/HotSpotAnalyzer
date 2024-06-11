from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    SendCodeView,
    WaitingListView,
    UserView,
    WhiteListView,
    RoleView,
    MessageSettingView,
    UserMessageView
)

router = DefaultRouter()
router.register(r"waitinglist", WaitingListView, basename="waitinglist")
router.register(r"user", UserView, basename="user")
router.register(r"whitelist", WhiteListView, basename="whitelist")
router.register(r"role", RoleView, basename="role")
router.register(r"messagesetting", MessageSettingView, basename="messagesetting")
router.register(r"usermessage", UserMessageView, basename="usermessage")


urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view({"post": "create"}), name="register"),
    path(
        "send-code/", SendCodeView.as_view({"post": "send"}), name="send_verify_email"
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
