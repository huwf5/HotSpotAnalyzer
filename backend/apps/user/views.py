from application.settings import DEBUG, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME
from apps.system.utils.api_response import APIResponse
from apps.user.models import User, WaitingList
from apps.user.serializers.user import (
    WaitingListSerializer,
    EmailListSerializer,
    LoginSerializer,
    UserSerializer,
    ForgotPasswordSerializer,
    RegisterSerializer,
    RoleSerializer,
    UserMessageSettingSerializer,
    UserMessageSerializer,
)
from apps.user.serializers.email import EmailVerificationSerializer
from apps.user.models import (
    EMAIL_USAGE_FOR_REGISTER,
    EMAIL_USAGE_FOR_RESET_PASSWORD,
    MESSAGE_TYPE_INFO,
    MESSAGE_TYPE_WARNING,
)
from django.db import transaction
from django.db.utils import IntegrityError
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from rest_framework import status, viewsets, throttling, mixins
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import TokenError, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import (
    ROLE_SUPER_ADMIN,
    ROLE_ADMIN,
    ROLE_USER,
    Role,
    AdminList,
    EmailFormatTag,
    EmailVerification,
    EmailSuffixFormat,
    UserMessageSettings,
    Message,
    UserMessage,
)

from .permission import IsAdmin, IsSuperAdmin
from .utils.validator import validate_email_suffix_format
from .utils.swagger_schemas import (
    emailList_schema,
    get_waitinglist_users_api_response_schema,
    user_get_profile_schema,
    get_userList_api_response_schema,
    user_update_profile_schema,
    delete_emailTag_schema,
    get_emailTagList_api_response_schema,
    get_roleList_api_response_schema,
    email_format_schema,
    get_whiteList_api_response_schema,
    get_user_message_settings_api_response_schema,
    user_message_setting_update_schema,
    get_user_message_api_response_schema,
    user_message_update_schema,
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers.email import (
    EmailFormatTagSerializer,
    EmailSuffixFormatSerializer,
)


# Create your views here.
class RegisterView(viewsets.ViewSet):
    class RegisterThrottle(throttling.AnonRateThrottle):
        rate = "3/min"

    throttle_classes = [RegisterThrottle]

    @swagger_auto_schema(
        operation_summary="Create a new user",
        request_body=RegisterSerializer,
        responses={
            201: "验证码已发送至您的邮箱,请查收",
            400: "请求参数错误,请检查后重试",
        },
    )
    def create(self, request: Request) -> APIResponse:
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serializer.errors if DEBUG else None,
            )

        email = serializer.validated_data["email"]
        verify_code = serializer.validated_data.pop("verify_code")
        try:
            with transaction.atomic():
                validate_email_suffix_format(email)
                # check if user already exists
                if User.objects.select_for_update().filter(email=email).exists():
                    return APIResponse(
                        status=status.HTTP_400_BAD_REQUEST,
                        message="用户已存在,请直接登录",
                    )
                # check if waiting user already exists
                if WaitingList.objects.select_for_update().filter(email=email).exists():
                    return APIResponse(
                        status=status.HTTP_400_BAD_REQUEST,
                        message="用户已注册，请联系管理员激活账户",
                    )

                # Validate the email verification code
                email_verification_model = (
                    EmailVerification.objects.select_for_update()
                    .filter(email=email, usage=EMAIL_USAGE_FOR_REGISTER)
                    .first()
                )
                if not email_verification_model:
                    return APIResponse(
                        status=status.HTTP_400_BAD_REQUEST,
                        message="请先获取有效验证码",
                    )
                if (
                    email_verification_model.usage != EMAIL_USAGE_FOR_REGISTER
                    or not email_verification_model.is_valid(verify_code)
                ):
                    return APIResponse(
                        status=status.HTTP_400_BAD_REQUEST,
                        message="验证码错误或已过期,请检查后重试",
                    )
                # delete the email verification model
                email_verification_model.delete()
                # create the waiting user
                serializer.save()
        except ValidationError as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data={"error": e.message} if DEBUG else None,
            )
        except IntegrityError as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="数据库错误,请稍后重试",
                data={"error": str(e)} if DEBUG else None,
            )

        return APIResponse(
            status=status.HTTP_201_CREATED,
            message="用户已注册,请联系管理员激活账户",
        )


class SendCodeView(viewsets.ViewSet):
    class SendVerifyEmailThrottle(throttling.AnonRateThrottle):
        rate = "1/min"

    throttle_classes = [SendVerifyEmailThrottle]

    @swagger_auto_schema(
        operation_summary="Send the email verification code",
        request_body=EmailVerificationSerializer,
        responses={
            200: "邮箱验证成功,请联系管理员激活",
            400: "请求参数错误,请检查后重试",
        },
    )
    def send(self, request: Request) -> APIResponse:
        serializer = EmailVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serializer.errors if DEBUG else None,
            )

        email = serializer.validated_data["email"]
        usage = serializer.validated_data["usage"]

        try:
            with transaction.atomic():
                validate_email_suffix_format(email)
                if usage == EMAIL_USAGE_FOR_REGISTER:
                    return self._handle_register_verification(email, usage, serializer)
                elif usage == EMAIL_USAGE_FOR_RESET_PASSWORD:
                    return self._handle_reset_password_verification(
                        email, usage, serializer
                    )
        except ValidationError as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message=e.message,
            )
        except IntegrityError as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(e)} if DEBUG else None,
                message="数据库错误,请稍后重试",
            )
        return APIResponse(
            status=status.HTTP_200_OK,
            message="邮箱验证码已发送,请查收",
        )

    def _handle_register_verification(self, email, usage, serializer):
        if User.objects.select_for_update().filter(email=email).exists():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="用户已存在,请直接登录",
            )
        if WaitingList.objects.select_for_update().filter(email=email).exists():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="用户已注册，请联系管理员激活账户",
            )
        self._save_or_update_verification(email, usage, serializer)
        return APIResponse(
            status=status.HTTP_200_OK,
            message="邮箱验证码已发送,请查收",
        )

    def _handle_reset_password_verification(self, email, usage, serializer):
        if not User.objects.select_for_update().filter(email=email).exists():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="用户不存在,请先注册",
            )
        self._save_or_update_verification(email, usage, serializer)
        return APIResponse(
            status=status.HTTP_200_OK,
            message="邮箱验证码已发送,请查收",
        )

    def _save_or_update_verification(self, email, usage, serializer):
        email_verification_model = (
            EmailVerification.objects.select_for_update()
            .filter(email=email, usage=usage)
            .first()
        )
        if email_verification_model:
            email_verification_model.update_code()
            email_verification_model.save()
        else:
            serializer.save()


class LoginView(TokenObtainPairView):
    class LoginThrottle(throttling.AnonRateThrottle):
        rate = "3/min"

    throttle_classes = [LoginThrottle]
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_summary="Login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                    "username": openapi.Schema(type=openapi.TYPE_STRING),
                    "role": openapi.Schema(type=openapi.TYPE_STRING),
                    "token": openapi.Schema(type=openapi.TYPE_STRING),
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                    "token_lifetime": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "refresh_lifetime": openapi.Schema(type=openapi.TYPE_INTEGER),
                },
            ),
            400: "登录失败,请检查邮箱和密码是否正确",
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except Exception as e:
            if WaitingList.objects.filter(email=request.data["email"]).exists():
                return APIResponse(
                    status=status.HTTP_400_BAD_REQUEST,
                    message="用户尚未激活，请联系管理员激活账户",
                )
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="登录失败,请检查邮箱和密码是否正确",
                data={"error": str(e)} if DEBUG else None,
            )
        result = serializer.validated_data
        result["email"] = serializer.user.email
        result["username"] = serializer.user.username
        result["role"] = serializer.user.role.role
        result["token"] = result.pop("access")
        result["token_lifetime"] = ACCESS_TOKEN_LIFETIME
        result["refresh_lifetime"] = REFRESH_TOKEN_LIFETIME

        return APIResponse(status=status.HTTP_200_OK, message="登录成功", data=result)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Logout",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"refresh": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        responses={205: "登出成功", 400: "登出失败"},
    )
    def post(self, request: Request) -> APIResponse:
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return APIResponse(status=status.HTTP_205_RESET_CONTENT, message="登出成功")
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="登出失败",
                data={"error": str(e)} if DEBUG else None,
            )


class WaitingListView(mixins.ListModelMixin, viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return WaitingList.objects.all()

    def get_object(self):
        email = self.kwargs.get("email")
        return WaitingList.objects.get(email=email)

    @swagger_auto_schema(
        operation_summary="Get the waiting list",
        responses={200: get_waitinglist_users_api_response_schema},
    )
    def list(self, request):
        queryset = self.get_queryset()
        serializer = WaitingListSerializer(queryset, many=True)
        return APIResponse(
            status=status.HTTP_200_OK, data=serializer.data, message="获取成功"
        )

    @swagger_auto_schema(
        operation_summary="Delete the waiting user",
        request_body=emailList_schema,
        responses={
            200: "删除成功",
            400: "请求参数错误,请检查后重试",
        },
    )
    @action(detail=False, methods=["post"], url_path="bulk-delete")
    def bulk_delete(self, request):
        serilizer = EmailListSerializer(data=request.data)
        if not serilizer.is_valid():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serilizer.errors if DEBUG else None,
            )

        emailList = serilizer.validated_data["emailList"]
        successful_delete = []
        failed_delete = []
        try:
            with transaction.atomic():
                # delete the waiting user
                existing_user = WaitingList.objects.filter(email__in=emailList)
                successful_delete = list(existing_user.values_list("email", flat=True))
                existing_user.delete()
                failed_delete = [
                    email for email in emailList if email not in successful_delete
                ]
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="删除过程中出现错误,请稍后重试",
                data={"error": str(e)} if DEBUG else None,
            )
        return APIResponse(
            status=status.HTTP_200_OK,
            message="删除成功",
            data={"failed_delete": failed_delete} if failed_delete else None,
        )

    @swagger_auto_schema(
        operation_summary="Activate the waiting user",
        request_body=emailList_schema,
        responses={
            200: "激活成功",
            400: "请求参数错误,请检查后重试",
        },
    )
    @action(detail=False, methods=["post"], url_path="activate")
    def activate(self, request):
        serializer = EmailListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    "message": "请求参数错误,请检查后重试",
                    "errors": serializer.errors if DEBUG else None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        email_list = serializer.validated_data["emailList"]
        successful_activation = []
        failed_activation = []

        try:
            with transaction.atomic():
                # activate the waiting user
                waiting_users = WaitingList.objects.filter(email__in=email_list)
                email_2_waiting_user = {user.email: user for user in waiting_users}

                for email in email_list:
                    waiting_user = email_2_waiting_user.get(email)
                    if waiting_user:
                        User.objects.create_user_from_waiting_list(waiting_user)
                        waiting_user.delete()
                        successful_activation.append(email)
                    else:
                        failed_activation.append(email)
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="激活过程中出现错误,请稍后重试",
                data={"error": str(e)} if DEBUG else None,
            )
        return APIResponse(
            status=status.HTTP_200_OK,
            message="激活成功",
            data=(
                {"failed_activation": failed_activation} if failed_activation else None
            ),
        )


class UserView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get the user profile",
        responses={
            200: user_get_profile_schema,
        },
    )
    @action(detail=False, methods=["get"], url_path="profile")
    def get_profile(self, request: Request) -> APIResponse:
        user = request.user
        return APIResponse(
            status=status.HTTP_200_OK,
            message="获取成功",
            data={
                "email": user.email,
                "username": user.username,
                "role": user.role.role,
            },
        )

    @swagger_auto_schema(
        operation_summary="Delete account",
        responses={200: "删除成功", 403: "权限不足"},
    )
    @action(detail=False, methods=["delete"], url_path="delete")
    def delete(self, request: Request) -> APIResponse:
        user = request.user
        if user.role.role == ROLE_SUPER_ADMIN:
            return APIResponse(
                status=status.HTTP_403_FORBIDDEN, message="超级管理员无法注销账号"
            )
        user.delete()
        return APIResponse(status=status.HTTP_200_OK, message="注销成功")

    @swagger_auto_schema(
        operation_summary="Update the user profile",
        request_body=user_update_profile_schema,
        responses={
            200: "更新成功",
            400: "请求参数错误,请检查后重试",
        },
    )
    @action(detail=False, methods=["patch"], url_path="update-profile")
    def update_profile(self, request: Request) -> APIResponse:
        if not request.data:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数不能为空，请检查后重试",
            )
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid() or not serializer.validated_data:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serializer.errors if DEBUG else None,
            )
        try:
            with transaction.atomic():
                serializer.update_profile(
                    instance=user, validated_data=serializer.validated_data
                )
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="更新过程中出现错误,请稍后重试",
                data={"error": str(e)} if DEBUG else None,
            )
        return APIResponse(status=status.HTTP_200_OK, message="更新成功")

    @swagger_auto_schema(
        operation_summary="Delete multiple users",
        request_body=emailList_schema,
        responses={
            200: "删除成功",
            400: "请求参数错误,请检查后重试",
        },
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="delete-multiple",
        permission_classes=[IsAdmin],
    )
    def delete_user(self, request: Request) -> APIResponse:
        serializer = EmailListSerializer(data=request.data)
        if not serializer.is_valid() or not serializer.validated_data:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serializer.errors if DEBUG else None,
            )
        emailList = serializer.validated_data["emailList"]
        deleted_email = []
        failed_email = []
        try:
            with transaction.atomic():
                users = User.objects.filter(email__in=emailList)
                for user in users:
                    if (
                        request.user.role.role == ROLE_ADMIN
                        and user.role.role in AdminList
                    ):
                        failed_email.append(user.email)
                        continue
                    elif (
                        request.user.role.role == ROLE_SUPER_ADMIN
                        and user.role.role == ROLE_SUPER_ADMIN
                    ):
                        failed_email.append(user.email)
                        continue
                    user.delete()
                    deleted_email.append(user.email)
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="删除过程中出现错误,请稍后重试",
                data={"error": str(e)} if DEBUG else None,
            )
        return APIResponse(
            status=status.HTTP_200_OK,
            message="删除成功",
            data={"failed_email": failed_email} if failed_email else {},
        )

    @swagger_auto_schema(
        operation_summary="Get the user list",
        responses={
            200: get_userList_api_response_schema,
        },
    )
    @action(
        detail=False, methods=["get"], url_path="list", permission_classes=[IsAdmin]
    )
    def get_user_list(self, request: Request) -> APIResponse:
        if request.user.role.role == ROLE_ADMIN:
            queryset = User.objects.filter(role__role=ROLE_USER)
        elif request.user.role.role == ROLE_SUPER_ADMIN:
            queryset = User.objects.filter(~Q(role__role=ROLE_SUPER_ADMIN))
        else:
            return APIResponse(
                status=status.HTTP_403_FORBIDDEN, message="权限不足,无法访问"
            )
        serializer = UserSerializer(queryset, many=True)
        return APIResponse(
            status=status.HTTP_200_OK, data=serializer.data, message="请求成功"
        )

    @swagger_auto_schema(
        operation_summary="Upgrade the user role",
        request_body=emailList_schema,
        responses={
            200: "升级成功",
            400: "请求参数错误,请检查后重试",
        },
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="upgrade",
        permission_classes=[IsAdmin],
    )
    def upgrade_user_role(self, request: Request) -> APIResponse:
        serializer = EmailListSerializer(data=request.data)
        if not serializer.is_valid() or not serializer.validated_data:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serializer.errors if DEBUG else None,
            )
        emailList = serializer.validated_data["emailList"]
        upgraded_email = []
        failed_email = []
        try:
            with transaction.atomic():
                users = User.objects.filter(email__in=emailList)
                for user in users:
                    if user.role.role == ROLE_USER:
                        user.upgrade_to_admin()
                        upgraded_email.append(user.email)
                    else:
                        failed_email.append(user.email)
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="升级过程中出现错误,请稍后重试",
                data={"error": str(e)} if DEBUG else None,
            )
        return APIResponse(
            status=status.HTTP_200_OK,
            message="升级成功",
            data={"failed_email": failed_email} if failed_email else {},
        )

    @swagger_auto_schema(
        operation_summary="Downgrade the user role",
        request_body=emailList_schema,
        responses={
            200: "降级成功",
            400: "请求参数错误,请检查后重试",
        },
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="downgrade",
        permission_classes=[IsSuperAdmin],
    )
    def downgrade_user_role(self, request: Request) -> APIResponse:
        serializer = EmailListSerializer(data=request.data)
        if not serializer.is_valid() or not serializer.validated_data:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serializer.errors if DEBUG else None,
            )
        emailList = serializer.validated_data["emailList"]
        downgraded_email = []
        failed_email = []
        try:
            with transaction.atomic():
                users = User.objects.filter(email__in=emailList)
                for user in users:
                    if user.role.role != ROLE_SUPER_ADMIN:
                        user.downgrade_to_user()
                        downgraded_email.append(user.email)
                    else:
                        failed_email.append(user.email)
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="降级过程中出现错误,请稍后重试",
                data={"error": str(e)} if DEBUG else None,
            )
        return APIResponse(
            status=status.HTTP_200_OK,
            message="降级成功",
            data={"failed_email": failed_email} if failed_email else {},
        )

    class ForgetPasswordThrottle(throttling.AnonRateThrottle):
        rate = "3/min"

    @swagger_auto_schema(
        operation_summary="Forget the password",
        request_body=ForgotPasswordSerializer,
        responses={
            200: "重置密码成功,请重新登录",
            400: "请求参数错误,请检查后重试",
        },
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="forget",
        permission_classes=[AllowAny],
        throttle_classes=[ForgetPasswordThrottle],
    )
    def password_reset(self, request: Request) -> APIResponse:
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serializer.errors if DEBUG else None,
            )
        email = serializer.validated_data["email"]
        new_password = serializer.validated_data["password"]
        verify_code = serializer.validated_data["verify_code"]
        try:
            with transaction.atomic():
                user = User.objects.select_for_update().filter(email=email).first()
                email_verification_model = (
                    EmailVerification.objects.select_for_update()
                    .filter(email=email, usage=EMAIL_USAGE_FOR_RESET_PASSWORD)
                    .first()
                )
                if not email_verification_model:
                    return APIResponse(
                        status=status.HTTP_400_BAD_REQUEST,
                        message="请先获取有效验证码",
                    )
                if (
                    email_verification_model.usage != EMAIL_USAGE_FOR_RESET_PASSWORD
                    or not email_verification_model.is_valid(verify_code)
                ):
                    return APIResponse(
                        status=status.HTTP_400_BAD_REQUEST,
                        message="验证码错误或已过期,请检查后重试",
                    )
                email_verification_model.delete()
                user.set_password(new_password)
                user.save()
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="重置密码失败,请稍后重试",
                data={"error": str(e)} if DEBUG else None,
            )
        return APIResponse(
            status=status.HTTP_200_OK,
            message="重置密码成功,请重新登录",
        )


class WhiteListView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_summary="Create the email tag",
        responses={201: get_emailTagList_api_response_schema},
    )
    @action(detail=False, methods=["get"], url_path="get-tags")
    def get_tags(self, request: Request) -> APIResponse:
        serializer = EmailFormatTagSerializer(
            EmailFormatTagSerializer.Meta.model.objects.all(), many=True
        )
        return APIResponse(
            status=status.HTTP_200_OK,
            message="获取成功",
            data=serializer.data,
        )

    @swagger_auto_schema(
        operation_summary="Create the email tag",
        request_body=EmailFormatTagSerializer,
        responses={201: "添加成功", 400: "请求参数错误,请检查后重试"},
    )
    @action(detail=False, methods=["post"], url_path="add-tag")
    def add_tag(self, request: Request) -> APIResponse:
        serializer = EmailFormatTagSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serializer.errors if DEBUG else None,
            )
        serializer.save()
        return APIResponse(
            status=status.HTTP_201_CREATED,
            message="添加成功",
        )

    @swagger_auto_schema(
        operation_summary="Delete the email tag",
        request_body=delete_emailTag_schema,
        responses={200: "删除成功", 400: "请求参数错误,请检查后重试"},
    )
    @action(detail=False, methods=["delete"], url_path="delete-tag")
    def delete_tag(self, request: Request) -> APIResponse:
        email_format = request.data.get("email_format")
        email_tag = request.data.get("email_tag")
        if not email_format or not email_tag:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
            )
        try:
            EmailFormatTag.objects.get(
                email_format=email_format, email_tag=email_tag
            ).delete()
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="删除失败,请检查邮箱格式和原标签是否正确",
                data={"error": str(e)} if DEBUG else None,
            )
        return APIResponse(status=status.HTTP_200_OK, message="删除成功")

    @swagger_auto_schema(
        operation_summary="Get the white list format",
        responses={200: get_whiteList_api_response_schema},
    )
    @action(detail=False, methods=["get"], url_path="list")
    def get_white_list(self, request: Request) -> APIResponse:
        serializer = EmailSuffixFormatSerializer(
            EmailSuffixFormatSerializer.Meta.model.objects.all(), many=True
        )
        return APIResponse(
            status=status.HTTP_200_OK,
            message="获取成功",
            data=serializer.data,
        )

    @swagger_auto_schema(
        operation_summary="Add the white list format",
        request_body=email_format_schema,
        responses={201: "添加成功", 400: "请求参数错误,请检查后重试"},
    )
    @action(detail=False, methods=["post"], url_path="add")
    def add_white_list(self, request: Request) -> APIResponse:
        serializer = EmailSuffixFormatSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serializer.errors if DEBUG else None,
            )
        serializer.save()
        return APIResponse(
            status=status.HTTP_201_CREATED,
            message="添加成功",
        )

    @swagger_auto_schema(
        operation_summary="Activate the white list format",
        request_body=email_format_schema,
        responses={200: "激活成功", 400: "请求参数错误,请检查后重试"},
    )
    @action(detail=False, methods=["patch"], url_path="activate")
    def activate_white_list(self, request: Request) -> APIResponse:
        format = request.data.get("format")
        if not format:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
            )
        try:
            EmailSuffixFormat.objects.get(format=format).activate()
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="激活失败,请检查邮箱格式是否正确",
                data={"error": str(e)} if DEBUG else None,
            )
        return APIResponse(status=status.HTTP_200_OK, message="激活成功")

    @swagger_auto_schema(
        operation_summary="Deactivate the white list format",
        request_body=email_format_schema,
        responses={200: "停用成功", 400: "请求参数错误,请检查后重试"},
    )
    @action(detail=False, methods=["patch"], url_path="deactivate")
    def deactivate_white_list(self, request: Request) -> APIResponse:
        format = request.data.get("format")
        if not format:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
            )
        try:
            with transaction.atomic():
                # delete the waiting user with the email suffix, but when deactivate @* will not delete the waiting user
                EmailSuffixFormat.objects.select_for_update().get(
                    format=format
                ).deactivate()
                WaitingList.objects.select_for_update().filter(
                    email__endswith=format
                ).delete()
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="停用失败,请检查邮箱格式是否正确",
                data={"error": str(e)} if DEBUG else None,
            )
        return APIResponse(status=status.HTTP_200_OK, message="停用成功")

    @swagger_auto_schema(
        operation_summary="Delete the white list format",
        request_body=email_format_schema,
        responses={200: "删除成功", 400: "请求参数错误,请检查后重试"},
    )
    @action(detail=False, methods=["delete"], url_path="delete")
    def delete_white_list(self, request: Request) -> APIResponse:
        # 1. make sure user table has not such email suffix
        # 2. delete the waiting list with the email suffix
        # 3. delete the tag with the email suffix
        email_format = request.data.get("format")
        if not email_format:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
            )
        if not EmailSuffixFormat.objects.filter(format=email_format).exists():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="删除失败,请检查邮箱是否正确",
            )

        try:
            with transaction.atomic():
                if email_format != "@*":
                    if (
                        User.objects.select_for_update()
                        .filter(email__endswith=email_format)
                        .exists()
                    ):
                        return APIResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            message="删除失败,有现存用户使用该邮箱格式",
                        )
                WaitingList.clean_by_email_suffix(email_format.format())
                # clean by email suffix already locked the EmailSuffixFormat
                EmailSuffixFormat.objects.filter(format=email_format).delete()
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="删除失败,请检查邮箱格式是否正确",
                data={"error": str(e)} if DEBUG else None,
            )
        return APIResponse(status=status.HTTP_200_OK, message="删除成功")


class RoleView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get the role list",
        responses={200: get_roleList_api_response_schema},
    )
    def list(self, request):
        queryset = Role.objects.all()
        serializer = RoleSerializer(queryset, many=True)
        return APIResponse(
            status=status.HTTP_200_OK, data=serializer.data, message="获取成功"
        )


class MessageSettingView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get the message setting",
        responses={200: get_user_message_settings_api_response_schema},
    )
    def list(self, request: Request) -> APIResponse:
        try:
            user_message_setting = UserMessageSettings.objects.get(email=request.user)
            serializer = UserMessageSettingSerializer(user_message_setting)
            return APIResponse(
                status=status.HTTP_200_OK, data=serializer.data, message="获取成功"
            )
        except UserMessageSettings.DoesNotExist:
            return APIResponse(
                status=status.HTTP_404_NOT_FOUND,
                message="用户消息设置不存在",
            )

    @swagger_auto_schema(
        operation_summary="Update the message setting",
        request_body=user_message_setting_update_schema,
        responses={
            200: "更新成功",
            400: "请求参数错误,请检查后重试",
        },
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_setting(self, request: Request) -> APIResponse:
        if not request.data:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数不能为空，请检查后重试",
            )
        try:
            with transaction.atomic():
                user_message_setting = (
                    UserMessageSettings.objects.select_for_update().get(
                        email=request.user
                    )
                )
                serializer = UserMessageSettingSerializer(
                    user_message_setting, data=request.data, partial=True
                )
                if not serializer.is_valid():
                    return APIResponse(
                        status=status.HTTP_400_BAD_REQUEST,
                        message="请求参数错误,请检查后重试",
                        data=serializer.errors if DEBUG else None,
                    )
                serializer.save()
                self.create_or_update_user_messages(user_message_setting, False)
                return APIResponse(
                    status=status.HTTP_200_OK,
                    message="更新成功",
                )
        except UserMessageSettings.DoesNotExist:
            return APIResponse(
                status=status.HTTP_404_NOT_FOUND,
                message="用户消息设置不存在",
            )
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="更新过程中出现错误,请稍后重试",
                data={"error": str(e)} if DEBUG else None,
            )

    @swagger_auto_schema(
        operation_summary="Create the message setting",
        responses={
            201: get_user_message_settings_api_response_schema,
            400: "用户消息设置已存在",
        },
    )
    def create(self, request: Request) -> APIResponse:
        if UserMessageSettings.objects.filter(email=request.user).exists():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="用户消息设置已存在",
            )
        with transaction.atomic():
            user_message_setting = UserMessageSettings.objects.create(
                email=request.user
            )
            self.create_or_update_user_messages(user_message_setting, True)
        return APIResponse(
            status=status.HTTP_201_CREATED,
            message="创建成功",
            data=UserMessageSettingSerializer(user_message_setting).data,
        )

    def create_or_update_user_messages(self, user_setting, new_setting):
        now = timezone.now()
        one_month_ago = now - timedelta(days=30)
        messages = Message.objects.filter(created_at__gte=one_month_ago)
        user = user_setting.email

        for message in messages:
            if not message.is_news and not user_setting.allow_non_news:
                continue

            message_type = None
            if message.negative_sentiment_ratio >= user_setting.warning_threshold:
                message_type = MESSAGE_TYPE_WARNING
            elif message.negative_sentiment_ratio >= user_setting.info_threshold:
                message_type = MESSAGE_TYPE_INFO

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


class UserMessageView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get the user message",
        responses={200: get_user_message_api_response_schema},
    )
    def list(self, request: Request) -> APIResponse:
        queryset = UserMessage.objects.filter(user=request.user)
        serializer = UserMessageSerializer(queryset, many=True)
        return APIResponse(
            status=status.HTTP_200_OK, data=serializer.data, message="获取成功"
        )

    @swagger_auto_schema(
        operation_description="Update the user message",
        request_body=user_message_update_schema,
    )
    def update(self, request: Request, pk=None) -> APIResponse:
        if not request.data:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数不能为空，请检查后重试",
            )
        user = request.user
        try:
            user_message = UserMessage.objects.get(pk=pk, user=user)
            if not user_message:
                return APIResponse(
                    status=status.HTTP_404_NOT_FOUND,
                    message="用户消息不存在",
                )
            serializer = UserMessageSerializer(
                user_message, data=request.data, partial=True
            )
            if not serializer.is_valid() or not serializer.validated_data:
                return APIResponse(
                    status=status.HTTP_400_BAD_REQUEST,
                    message="请求参数错误,请检查后重试",
                    data=serializer.errors if DEBUG else None,
                )
            serializer.validated_data.pop("type", None)
            with transaction.atomic():
                serializer.update(
                    instance=user_message,
                    validated_data=serializer.validated_data,
                )
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="更新过程中出现错误,请稍后重试",
                data={"error": str(e)} if DEBUG else None,
            )
        return APIResponse(status=status.HTTP_200_OK, message="更新成功")

    @swagger_auto_schema(
        operation_summary="Delete the user message",
        operation_id="delete",
        responses={200: "删除成功", 400: "请求参数错误,请检查后重试"},
    )
    @action(detail=True, methods=["delete"], url_path="delete")
    def delete(self, request: Request, pk=None) -> APIResponse:
        user = request.user
        try:
            with transaction.atomic():
                user_message = UserMessage.objects.get(pk=pk, user=user)
                user_message.delete()
                return APIResponse(status=status.HTTP_200_OK, message="删除成功")
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="删除过程中出现错误,请稍后重试",
                data={"error": str(e)} if DEBUG else None,
            )

    @swagger_auto_schema(
        operation_summary="Refresh user messages based on new messages created within the last month",
        responses={
            200: get_user_message_api_response_schema,
            204: "无新消息",
            400: "请求参数错误，请检查后重试",
        },
    )
    @action(detail=False, methods=["get"], url_path="refresh")
    def refresh(self, request: Request) -> APIResponse:
        user = request.user
        now = timezone.now()
        one_month_ago = now - timedelta(days=30)
        try:
            with transaction.atomic():
                user_message_setting = (
                    UserMessageSettings.objects.select_for_update().get(email=user)
                )
                new_messages = Message.objects.filter(created_at__gte=one_month_ago)
                if not new_messages.exists():
                    return APIResponse(
                        status=status.HTTP_204_NO_CONTENT, message="无新消息"
                    )

                # create the new user message
                for message in new_messages:
                    if not message.is_news and not user_message_setting.allow_non_news:
                        continue

                    message_type = None
                    if (
                        message.negative_sentiment_ratio
                        >= user_message_setting.warning_threshold
                    ):
                        message_type = MESSAGE_TYPE_WARNING
                    elif (
                        message.negative_sentiment_ratio
                        >= user_message_setting.info_threshold
                    ):
                        message_type = MESSAGE_TYPE_INFO
                    if message_type:
                        UserMessage.objects.update_or_create(
                            user=user, message=message, defaults={"type": message_type}
                        )
                updated_user_messages = UserMessage.objects.filter(user=user)
                serializer = UserMessageSerializer(updated_user_messages, many=True)
                return APIResponse(
                    status=status.HTTP_200_OK, message="更新成功", data=serializer.data
                )
        except UserMessageSettings.DoesNotExist:
            return APIResponse(
                status=status.HTTP_404_NOT_FOUND, message="用户消息设置不存在"
            )
        except Exception as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="更新过程中出现错误,请稍后重试",
                data={"error": str(e)} if DEBUG else None,
            )
