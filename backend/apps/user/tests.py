from django.test import TestCase
from rest_framework.test import APITestCase
from .fixtures.initialize import Initialize
from .serializers.user import RoleSerializer
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from .models import (
    User,
    EmailVerification,
    EmailSuffixFormat,
    Role,
    WaitingList,
    EmailFormatTag,
    Message,
    UserMessage,
    UserMessageSettings,
)
from .models import ROLE_ADMIN, ROLE_USER, MESSAGE_TYPE_INFO, MESSAGE_TYPE_WARNING
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from datetime import timedelta
from rest_framework.throttling import BaseThrottle
from unittest.mock import patch

# Create your tests here.


# Test if roles are initialized
class InitializeTestCase(TestCase):
    def test_init_role(self):
        Initialize(app="apps.user").run()
        # test if roles are initialized
        roles = RoleSerializer.Meta.model.objects.all()
        self.assertTrue(roles.exists(), "Roles should be initialized")


class NoThrottle(BaseThrottle):
    def allow_request(self, request, view):
        return True


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.role = Role.objects.create(role="User")

        self.user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "securepassword123",
            "verify_code": "123456",
            "role": self.role.id,
        }

        EmailSuffixFormat.objects.create(format="@example.com", is_active=True)

        EmailVerification.objects.create(
            email="test@example.com",
            verify_code="123456",
            usage="register",
            expired_at=timezone.now() + timedelta(minutes=30),
        )

    @patch("apps.user.views.RegisterView.throttle_classes", [NoThrottle])
    def test_register_with_listed_email_suffix(self):
        self.user_data["email"] = "test@example.com"
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=f"Expected HTTP 201 Created, got {response.status_code}. Response data: {response.data}",
        )
        self.assertIn("用户已注册,请联系管理员激活账户", response.data["message"])

    @patch("apps.user.views.RegisterView.throttle_classes", [NoThrottle])
    def test_register_with_unlisted_email_suffix(self):
        self.user_data["email"] = "user@unlisteddomain.com"
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("apps.user.views.RegisterView.throttle_classes", [NoThrottle])
    def test_register_existing_user(self):
        role = Role.objects.first()
        User.objects.create(email="test@example.com", username="testuser", role=role)
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("用户已存在,请直接登录", response.data["message"])

    @patch("apps.user.views.RegisterView.throttle_classes", [NoThrottle])
    def test_register_with_invalid_code(self):
        self.user_data["verify_code"] = "654321"
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("验证码错误或已过期", response.data["message"])

    @patch("apps.user.views.RegisterView.throttle_classes", [NoThrottle])
    def test_register_without_code(self):
        del self.user_data["verify_code"]
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("请求参数错误,请检查后重试", response.data["message"])

    @patch("apps.user.views.RegisterView.throttle_classes", [NoThrottle])
    def test_register_email_validation_error(self):
        self.user_data["email"] = "not-an-email"
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("请求参数错误,请检查后重试", response.data["message"])


class SendCodeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.send_code_url = reverse("send_verify_email")

        EmailSuffixFormat.objects.create(format="@example.com", is_active=True)
        self.user_data = {"email": "test@example.com", "usage": "register"}

    @patch("apps.user.views.SendCodeView.throttle_classes", [NoThrottle])
    def test_send_verification_code_success(self):
        response = self.client.post(self.send_code_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("邮箱验证码已发送,请查收", response.data["message"])

    @patch("apps.user.views.SendCodeView.throttle_classes", [NoThrottle])
    def test_send_verification_code_existing_user(self):
        Role.objects.create(role="User")
        User.objects.create(
            email="test@example.com", username="testuser", role=Role.objects.first()
        )
        response = self.client.post(self.send_code_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("用户已存在,请直接登录", response.data["message"])

    @patch("apps.user.views.SendCodeView.throttle_classes", [NoThrottle])
    def test_send_verification_code_without_parameters(self):
        response = self.client.post(self.send_code_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("请求参数错误,请检查后重试", response.data["message"])

    @patch("apps.user.views.SendCodeView.throttle_classes", [NoThrottle])
    def test_send_verification_code_invalid_email_format(self):
        self.user_data["email"] = "invalid-email"
        response = self.client.post(self.send_code_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("请求参数错误,请检查后重试", response.data["message"])


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")
        self.role_user = Role.objects.create(role="User")

        self.active_user = User.objects.create(
            email="active@example.com",
            username="activeuser",
            password=make_password("correctpassword"),
            role=self.role_user,
        )

        self.unactivated_user = WaitingList.objects.create(
            email="unactivated@example.com",
            username="unactivateduser",
            password=make_password("correctpassword"),
        )

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {"email": "active@example.com", "password": "correctpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data["data"])
        self.assertIn("username", response.data["data"])
        self.assertEqual(response.data["data"]["username"], "activeuser")

    def test_login_with_wrong_password(self):
        response = self.client.post(
            self.login_url,
            {"email": "active@example.com", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("登录失败,请检查邮箱和密码是否正确", response.data["message"])

    def test_login_with_nonexistent_email(self):
        response = self.client.post(
            self.login_url,
            {"email": "nonexistent@example.com", "password": "anypassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("登录失败,请检查邮箱和密码是否正确", response.data["message"])

    def test_login_unactivated_user(self):
        response = self.client.post(
            self.login_url,
            {"email": "unactivated@example.com", "password": "correctpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("用户尚未激活，请联系管理员激活账户", response.data["message"])

    def test_login_invalid_input(self):
        response = self.client.post(
            self.login_url,
            {"email": "not-an-email", "password": "password123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("登录失败,请检查邮箱和密码是否正确", response.data["message"])


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse("logout")
        role_user = Role.objects.create(role="User")
        self.user = User.objects.create(
            email="user@example.com",
            username="testuser",
            password=make_password("password123"),
            role=role_user,
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user)

    def test_logout_success(self):
        response = self.client.post(
            self.logout_url,
            {"refresh": str(self.refresh)},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertIn("登出成功", response.data["message"])

    def test_logout_with_invalid_token(self):
        invalid_refresh = "invalidtoken123"
        response = self.client.post(
            self.logout_url,
            {"refresh": invalid_refresh},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("登出失败", response.data["message"])

    def test_logout_without_token(self):
        response = self.client.post(
            self.logout_url,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("登出失败", response.data["message"])

    def tearDown(self):
        self.client.logout()


class WaitingListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_role = Role.objects.create(role="Admin")
        self.admin_user = User.objects.create(
            email="admin@example.com",
            username="adminuser",
            password=make_password("adminpassword"),
            role=self.admin_role,
        )

        self.client.force_authenticate(user=self.admin_user)

        self.waiting_user_1 = WaitingList.objects.create(
            email="wait1@example.com",
            username="waituser1",
            password=make_password("password123"),
        )
        self.waiting_user_2 = WaitingList.objects.create(
            email="wait2@example.com",
            username="waituser2",
            password=make_password("password123"),
        )

        self.waiting_list_url = reverse("waitinglist-list")
        self.bulk_delete_url = reverse("waitinglist-bulk-delete")
        self.activate_url = reverse("waitinglist-activate")

    def test_list_waiting_users(self):
        response = self.client.get(self.waiting_list_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Expected HTTP 200 OK, got response: {response}",
        )
        self.assertEqual(len(response.data), 2)

    def test_bulk_delete_waiting_users(self):
        response = self.client.post(
            self.bulk_delete_url,
            {"emailList": ["wait1@example.com", "wait2@example.com"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WaitingList.objects.count(), 0)

    def test_activate_waiting_users(self):
        Role.objects.create(role="User")
        response = self.client.post(
            self.activate_url, {"emailList": ["wait1@example.com"]}, format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Expected HTTP 200 OK, got response data: {response.data}",
        )
        self.assertTrue(User.objects.filter(email="wait1@example.com").exists())
        self.assertFalse(WaitingList.objects.filter(email="wait1@example.com").exists())

    def tearDown(self):
        User.objects.all().delete()
        Role.objects.all().delete()
        WaitingList.objects.all().delete()
        self.client.logout()


class UserViewTest(APITestCase):
    def setUp(self):
        # Create user, admin and super admin
        self.role_user = Role.objects.create(role="User")
        self.user = User.objects._create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            role=self.role_user,
        )
        self.admin_role = Role.objects.create(role="Admin")
        self.admin_user = User.objects._create_user(
            email="admin@example.com",
            username="adminuser",
            password="adminpassword",
            role=self.admin_role,
        )
        self.super_admin_role = Role.objects.create(role="Super Admin")
        self.super_admin_user = User.objects._create_user(
            email="superadmin@example.com",
            username="superadminuser",
            password="superadminpassword",
            role=self.super_admin_role,
        )

        refresh = RefreshToken.for_user(self.user)
        self.user_token = str(refresh.access_token)

        self.profile_url = reverse("user-get-profile")
        self.delete_url = reverse("user-delete")
        self.delete_user_url = reverse("user-delete-user")
        self.update_profile_url = reverse("user-update-profile")
        self.user_list_url = reverse("user-get-user-list")
        self.user_upgrade_url = reverse("user-upgrade-user-role")
        self.user_downgrade_url = reverse("user-downgrade-user-role")
        self.password_reset_url = reverse("user-password-reset")

    def test_get_profile_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user_token)
        response = self.client.get(self.profile_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Expected HTTP 200 OK, got response: {response.data}",
        )
        self.assertEqual(response.data["data"]["email"], self.user.email)

    def test_delete_account(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user_token)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user_token)
        data = {"username": "newusername"}
        response = self.client.patch(self.update_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newusername")

    def test_get_user_list(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "
            + str(RefreshToken.for_user(self.admin_user).access_token)
        )
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

    def test_upgrade_user_role(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "
            + str(RefreshToken.for_user(self.admin_user).access_token)
        )
        data = {"emailList": [self.user.email]}
        response = self.client.post(self.user_upgrade_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(
            self.user.role.role, ROLE_ADMIN, "User should have been upgraded to admin"
        )

    def test_downgrade_user_role(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "
            + str(RefreshToken.for_user(self.super_admin_user).access_token)
        )
        data = {"emailList": [self.admin_user.email]}
        response = self.client.post(self.user_downgrade_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admin_user.refresh_from_db()
        self.assertEqual(
            self.admin_user.role.role,
            ROLE_USER,
            "Admin should have been downgraded to user",
        )

    def test_password_reset(self):
        # Setup
        EmailVerification.objects.create(
            email=self.user.email,
            verify_code="123456",
            usage="reset_password",
            expired_at=timezone.now() + timedelta(minutes=10),
        )

        # Test password reset
        data = {
            "email": self.user.email,
            "password": "newpassword123",
            "verify_code": "123456",
        }
        response = self.client.post(self.password_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("重置密码成功,请重新登录", response.data["message"])

        # Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))


class WhiteListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.role_admin = Role.objects.create(role="Admin")
        self.admin_user = User.objects._create_user(
            email="admin@example.com",
            username="adminuser",
            password="adminpassword",
            role=self.role_admin,
        )
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)

        self.email_suffix_format = EmailSuffixFormat.objects.create(
            format="@example.com", is_active=True
        )
        self.email_format_tag = EmailFormatTag.objects.create(
            email_format=self.email_suffix_format, email_tag="VIP"
        )

        # Define URLs
        self.get_tags_url = reverse("whitelist-get-tags")
        self.add_tag_url = reverse("whitelist-add-tag")
        self.delete_tag_url = reverse("whitelist-delete-tag")
        self.list_white_url = reverse("whitelist-get-white-list")
        self.add_white_url = reverse("whitelist-add-white-list")
        self.activate_white_url = reverse("whitelist-activate-white-list")
        self.deactivate_white_url = reverse("whitelist-deactivate-white-list")
        self.delete_white_url = reverse("whitelist-delete-white-list")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")

    def test_get_tags(self):
        response = self.client.get(self.get_tags_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["email_tag"], "VIP")

    def test_add_tag(self):
        data = {
            "email_format": self.email_suffix_format.format,
            "email_tag": "Standard",
        }
        response = self.client.post(self.add_tag_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(EmailFormatTag.objects.filter(email_tag="Standard").exists())

    def test_delete_tag(self):
        data = {"email_format": self.email_suffix_format.format, "email_tag": "VIP"}
        response = self.client.delete(self.delete_tag_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(EmailFormatTag.objects.filter(email_tag="VIP").exists())

    def test_list(self):
        response = self.client.get(self.list_white_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["data"]) > 0)
        self.assertTrue(
            any(format["format"] == "@example.com" for format in response.data["data"])
        )

    def test_add(self):
        data = {"format": "@newexample.com"}
        response = self.client.post(self.add_white_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            EmailSuffixFormat.objects.filter(format="@newexample.com").exists()
        )

    def test_activate(self):
        data = {"format": self.email_suffix_format.format}
        response = self.client.patch(self.activate_white_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            EmailSuffixFormat.objects.get(
                format=self.email_suffix_format.format
            ).is_active
        )

    def test_deactivate(self):
        data = {"format": self.email_suffix_format.format}
        response = self.client.patch(self.deactivate_white_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            EmailSuffixFormat.objects.get(
                format=self.email_suffix_format.format
            ).is_active
        )

    def test_delete(self):
        EmailSuffixFormat.objects.create(format="@newexample.com", is_active=True)
        data = {"format": "@newexample.com"}
        response = self.client.delete(self.delete_white_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            EmailSuffixFormat.objects.filter(format="@newexample.com").exists()
        )

    def test_delete_nonexistent_format(self):
        data = {"format": "@nonexistent.com"}
        response = self.client.delete(self.delete_white_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_format_with_existing_users(self):
        role = Role.objects.create(role="User")
        User.objects.create(email="user@example.com", password="password", role=role)
        data = {"format": "@example.com"}
        response = self.client.delete(self.delete_white_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_without_format(self):
        response = self.client.delete(self.delete_white_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_with_invalid_format(self):
        data = {"format": "invalidformat"}
        response = self.client.delete(self.delete_white_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MessageSettingViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects._create_user(
            email="user@example.com",
            username="user",
            password="password",
            role=Role.objects.create(role="User"),
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)

        self.settings_url = reverse("messagesetting-list")
        self.update_settings_url = reverse("messagesetting-update-setting")
        self.create_settings_url = self.settings_url

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.message1 = Message.objects.create(
            title="重要新闻",
            summary="非常重要",
            negative_sentiment_ratio=0.9,
            is_news=True,
            created_at=timezone.now() - timedelta(days=10),
        )
        self.message2 = Message.objects.create(
            title="普通新闻",
            summary="不那么重要",
            negative_sentiment_ratio=0.4,
            is_news=True,
            created_at=timezone.now() - timedelta(days=15),
        )

    def test_create_message_setting(self):
        response = self.client.post(self.create_settings_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test default settings
        self.assertTrue(UserMessageSettings.objects.filter(email=self.user).exists())
        self.assertEqual(
            UserMessageSettings.objects.get(email=self.user).warning_threshold, 0.7
        )
        self.assertEqual(
            UserMessageSettings.objects.get(email=self.user).info_threshold, 0.5
        )
        self.assertEqual(UserMessage.objects.count(), 1)
        self.assertEqual(UserMessage.objects.get(user=self.user).message, self.message1)

    def test_update_message_setting_affects_user_messages(self):
        """Test updating message settings and checking the impact on UserMessages."""
        settings = UserMessageSettings.objects.create(
            email=self.user,
            allow_non_news=True,
            warning_threshold=0.9,
            info_threshold=0.3,
        )
        self.create_or_update_user_messages(settings, True)

        # Lower the warning threshold to include both messages as warnings
        response = self.client.patch(
            self.update_settings_url, {"warning_threshold": 0.3}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            UserMessage.objects.filter(user=self.user, message=self.message2)
            .first()
            .type,
            "warning",
        )

    def test_get_message_settings(self):
        """Test retrieving existing message settings."""
        UserMessageSettings.objects.create(
            email=self.user,
            allow_non_news=True,
            warning_threshold=0.7,
            info_threshold=0.3,
        )
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("allow_non_news", response.data["data"])
        self.assertTrue(response.data["data"]["allow_non_news"])

    def test_no_message_settings_found(self):
        """Test response when no user message settings are found."""
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def create_or_update_user_messages(self, user_setting, new_setting):
        """Helper function to create or update UserMessages based on message settings."""
        now = timezone.now()
        one_month_ago = now - timedelta(days=30)
        messages = Message.objects.filter(created_at__gte=one_month_ago)
        user = user_setting.email

        for message in messages:
            if not message.is_news and not user_setting.allow_non_news:
                continue

            message_type = (
                "info"
                if message.negative_sentiment_ratio >= user_setting.info_threshold
                else None
            )
            if message.negative_sentiment_ratio >= user_setting.warning_threshold:
                message_type = "warning"

            if message_type:
                defaults = {"type": message_type}
                if new_setting:
                    UserMessage.objects.create(
                        user=user, message=message, type=message_type
                    )
                else:
                    user_message, created = UserMessage.objects.update_or_create(
                        user=user, message=message, defaults=defaults
                    )
                    if not created and user_message.type != message_type:
                        user_message.type = message_type
                        user_message.save(update_fields=["type"])


class UserMessageViewTest(APITestCase):
    def setUp(self):
        self.role_user = Role.objects.create(role="User")
        self.user = User.objects._create_user(
            email="user@example.com",
            username="user",
            password="password",
            role=self.role_user,
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)

        self.message1 = Message.objects.create(
            title="重要新闻",
            summary="非常重要",
            negative_sentiment_ratio=0.9,
            is_news=True,
            created_at=timezone.now() - timedelta(days=10),
        )
        self.message2 = Message.objects.create(
            title="普通新闻",
            summary="不那么重要",
            negative_sentiment_ratio=0.4,
            is_news=True,
            created_at=timezone.now() - timedelta(days=15),
        )
        self.settings = UserMessageSettings.objects.create(
            email=self.user,
            allow_non_news=True,
            warning_threshold=0.8,
            info_threshold=0.5,
        )
        self.user_message = UserMessage.objects.create(
            user=self.user, message=self.message1, type="warning"
        )

        self.list_url = reverse("usermessage-list")
        self.refresh_url = reverse("usermessage-refresh")
        self.update_url = reverse("usermessage-detail", kwargs={"pk": self.user_message.pk})
        self.delete_url = reverse("usermessage-detail", kwargs={"pk": self.user_message.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_list_user_messages(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["id"], self.user_message.id)

    def test_update_user_message(self):
        data = {"is_read": True}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, 200)
        self.user_message.refresh_from_db()
        self.assertTrue(self.user_message.is_read)

    def test_delete_user_message(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(UserMessage.objects.filter(pk=self.user_message.pk).exists())

    def test_refresh_user_messages(self):
        new_message = Message.objects.create(
            title="最新新闻",
            summary="最新重要新闻",
            negative_sentiment_ratio=0.85,
            is_news=True,
            created_at=timezone.now() - timedelta(days=1),
        )
        response = self.client.get(self.refresh_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 2) 
        self.assertTrue(UserMessage.objects.filter(message=new_message).exists())

    def test_no_user_messages_found(self):
        UserMessage.objects.all().delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 0)
