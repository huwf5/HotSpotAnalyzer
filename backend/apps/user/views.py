from apps.system.utils.api_response import APIResponse
from apps.user.models import User, WaitingList
from apps.user.serializers.user import (
    WaitingListSerializer,
    VerifyEmailSerializer,
    EmailListSerializer,
    LoginSerializer,
    UserSerializer,
)
from django.forms import ValidationError
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from rest_framework import status, viewsets, throttling, mixins
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import TokenError, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_USER, AdminList
from .permission import IsAdmin, IsSuperAdmin
from .utils.swagger_schemas import (
    emailList_schema,
    get_waitinglist_users_api_response_schema,
    user_get_profile_schema,
    get_userList_api_response_schema,
    user_update_profile_schema,
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Create your views here.
class RegisterView(viewsets.ViewSet):
    class RegisterThrottle(throttling.AnonRateThrottle):
        rate = "1/min"

    throttle_classes = [RegisterThrottle]

    @swagger_auto_schema(
        operation_summary="Create a new user",
        request_body=WaitingListSerializer,
        responses={
            201: "验证码已发送至您的邮箱,请查收",
            400: "请求参数错误,请检查后重试",
        },
    )
    def create(self, request: Request) -> APIResponse:
        serializer = WaitingListSerializer(data=request.data)
        # check validation of serializer(including email suffix format)
        if not serializer.is_valid():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serializer.errors,
            )
        try:
            # check if user already exists
            email = serializer.validated_data["email"]
            if User.objects.filter(email=email).exists():
                return APIResponse(
                    status=status.HTTP_400_BAD_REQUEST,
                    message="用户已存在,请直接登录",
                )

            # check if waiting user exists
            if WaitingList.objects.filter(email=email).exists():
                # update all the filed of the waiting user
                waiting_user = WaitingList.objects.get(email=email)
                if waiting_user.is_verified:
                    return APIResponse(
                        status=status.HTTP_400_BAD_REQUEST,
                        message="用户已注册，请联系管理员激活账户",
                    )

                waiting_user.username = serializer.validated_data["username"]
                waiting_user.password = serializer.validated_data["password"]
                waiting_user.update_verify_code()
                waiting_user.save()
            else:
                # create a new waiting user
                serializer.create(serializer.validated_data)

        except ValidationError as e:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message=e.message,
            )

        return APIResponse(
            status=status.HTTP_201_CREATED,
            message="验证码已发送至您的邮箱,请查收",
        )

    def throttle_failure(self, request, wait_time):
        return APIResponse(
            status=status.HTTP_429_TOO_MANY_REQUESTS,
            message=f"已超过速率限制。请在{wait_time}秒后重试。",
        )


class VerifyEmailView(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="Verify the email",
        request_body=VerifyEmailSerializer,
        responses={
            200: "邮箱验证成功,请联系管理员激活",
            400: "请求参数错误,请检查后重试",
        },
    )
    def verify(self, request: Request) -> APIResponse:
        serializer = VerifyEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serializer.errors,
            )

        # check existence of user
        if User.objects.filter(email=serializer.validated_data["email"]).exists():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="用户已存在,请直接登录",
            )
        # check existence of waiting user
        waiting_user = WaitingList.objects.filter(
            email=serializer.validated_data["email"]
        ).first()
        if not waiting_user:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="用户不存在,请先注册获取验证码",
            )

        if waiting_user.is_verified:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="用户已验证通过,请联系管理员激活",
            )

        if waiting_user.verify_code != serializer.validated_data["verify_code"]:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="验证码错误,请检查后重试",
            )
        if waiting_user.expired_at < timezone.now():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="验证码已过期,请重新获取新验证码",
            )

        waiting_user.is_verified = True
        waiting_user.plain_save(update_fields=["is_verified"])
        return APIResponse(
            status=status.HTTP_200_OK, message="邮箱验证成功,请联系管理员激活"
        )


class LoginView(TokenObtainPairView):
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
                    "token": openapi.Schema(type=openapi.TYPE_STRING),
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING),
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
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="登录失败,请检查邮箱和密码是否正确",
                data={"error": str(e)},
            )
        result = serializer.validated_data
        result["email"] = serializer.user.email
        result["username"] = serializer.user.username
        result["token"] = result.pop("access")

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
        except Exception:
            return APIResponse(status=status.HTTP_400_BAD_REQUEST, message="登出失败")


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
    @transaction.atomic
    def bulk_delete(self, request):
        serilizer = EmailListSerializer(data=request.data)
        if not serilizer.is_valid():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serilizer.errors,
            )

        emailList = serilizer.validated_data["emailList"]
        successful_delete = []
        failed_delete = []
        for email in emailList:
            try:
                waiting_user = WaitingList.objects.get(email=email)
                waiting_user.delete()
                successful_delete.append(email)
            except WaitingList.DoesNotExist:
                failed_delete.append(email)

        message = (
            "全部删除成功"
            if len(failed_delete) == 0
            else "有记录删除失败,请检查邮箱是否正确"
        )
        data = {"failed_delete": failed_delete} if failed_delete else {}
        return APIResponse(status=status.HTTP_200_OK, message=message, data=data)

    @swagger_auto_schema(
        operation_summary="Activate the waiting user",
        request_body=emailList_schema,
        responses={
            200: "激活成功",
            400: "请求参数错误,请检查后重试",
        },
    )
    @action(detail=False, methods=["post"], url_path="activate")
    @transaction.atomic
    def active(self, request):
        serializer = EmailListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    "message": "请求参数错误,请检查后重试",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        email_list = serializer.validated_data["emailList"]

        successful_activation = []
        failed_activation = []

        for email in email_list:
            try:
                waiting_user = WaitingList.objects.get(email=email)
                if not waiting_user.is_verified:
                    failed_activation.append(email)
                    continue
                User.objects.create_user_from_waiting_list(waiting_user)
                waiting_user.delete()
                successful_activation.append(email)
            except WaitingList.DoesNotExist:
                failed_activation.append(email)

        message = (
            "全部激活成功"
            if len(failed_activation) == 0
            else "有邮箱激活失败,请检查邮箱是否正确"
        )
        data = {"failed_activation": failed_activation} if failed_activation else {}
        return Response(
            data={"message": message, "data": data}, status=status.HTTP_200_OK
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
            )
        serializer.update_profile(
            instance=user, validated_data=serializer.validated_data
        )
        return APIResponse(status=status.HTTP_200_OK, message="更新成功")

    @swagger_auto_schema(
        operation_summary="Delete the user",
        request_body=emailList_schema,
        responses={
            200: "删除成功",
            400: "请求参数错误,请检查后重试",
        },
    )
    @action(
        detail=False, methods=["post"], url_path="delete", permission_classes=[IsAdmin]
    )
    def delete_user(self, request: Request) -> APIResponse:
        serializer = EmailListSerializer(data=request.data)
        if not serializer.is_valid() or not serializer.validated_data:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
            )
        emailList = serializer.validated_data["emailList"]
        deleted_email = []
        failed_email = []
        for email in emailList:
            try:
                user = User.objects.get(email=email)
                if request.user.role.role == ROLE_ADMIN:
                    if user.role.role in AdminList:
                        failed_email.append(email)
                        continue
                elif request.user.role.role == ROLE_SUPER_ADMIN:
                    if user.role.role == ROLE_SUPER_ADMIN:
                        failed_email.append(email)
                        continue
                else:
                    return APIResponse(
                        status=status.HTTP_403_FORBIDDEN, message="权限不足,无法访问"
                    )
                user.delete()
                deleted_email.append(email)
            except User.DoesNotExist:
                failed_email.append(email)
        message = (
            "删除成功" if len(deleted_email) != 0 else "删除失败,请检查邮箱是否正确"
        )
        data = {"failed_email": failed_email} if failed_email else {}
        return APIResponse(status=status.HTTP_200_OK, message=message, data=data)

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
            )
        emailList = serializer.validated_data["emailList"]
        upgrated_email = []
        failed_email = []

        for email in emailList:
            try:
                user = User.objects.get(email=email)
                if user.role.role == ROLE_USER:
                    user.upgrade_to_admin()
                    upgrated_email.append(email)
            except User.DoesNotExist:
                failed_email.append(email)
        return APIResponse(
            status=status.HTTP_200_OK,
            message=(
                "升级成功"
                if len(upgrated_email) != 0
                else "升级失败,请检查邮箱是否正确"
            ),
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
            )
        emailList = serializer.validated_data["emailList"]
        downgraded_email = []
        failed_email = []
        for email in emailList:
            try:
                user = User.objects.get(email=email)
                if user.role.role != ROLE_SUPER_ADMIN:
                    user.downgrade_to_user()
                    downgraded_email.append(email)
            except User.DoesNotExist:
                failed_email.append(email)
        return APIResponse(
            status=status.HTTP_200_OK,
            message=(
                "降级成功"
                if len(downgraded_email) != 0
                else "降级失败,请检查邮箱是否正确"
            ),
            data={"failed_email": failed_email} if failed_email else {},
        )
