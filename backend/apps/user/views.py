from apps.system.utils.api_response import APIResponse
from apps.user.models import User, WaitingList
from apps.user.serializers.user import (
    WaitingListSerializer,
    VerifyEmailSerializer,
    ActiveSerializer,
    LoginSerializer,
)
from django.forms import ValidationError
from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework import viewsets
from rest_framework import throttling
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .permission import IsAdmin


# Create your views here.
class RegisterView(viewsets.ViewSet):
    class RegisterThrottle(throttling.AnonRateThrottle):
        rate = "1/min"

    throttle_classes = [RegisterThrottle]

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


class ActiveView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    @transaction.atomic
    def active(self, request: Request) -> APIResponse:

        serializer = ActiveSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请求参数错误,请检查后重试",
                data=serializer.errors,
            )
        emailList = serializer.validated_data["emailList"]

        successful_activation = []
        failed_activation = []

        for email in emailList:
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

        if len(successful_activation) == 0:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="激活失败,请检查邮箱是否正确",
                data={"failed_activation": failed_activation},
            )

        message = ""
        data = {}
        if len(failed_activation) == 0:
            message = "全部激活成功"
        else:
            message = "有部分邮箱激活失败,请检查邮箱是否正确"
            data = {"failed_activation": failed_activation}
        return APIResponse(status=status.HTTP_200_OK, message=message, data=data)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request: Request, *args, **kwargs) -> Response:

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        result = serializer.validated_data
        result["email"] = serializer.user.email
        result["username"] = serializer.user.username
        result["token"] = result.pop("access")

        return APIResponse(status=status.HTTP_200_OK, message="登录成功", data=result)

    # def post(self, request: Request) -> APIResponse:
    #     serializer = LoginSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return APIResponse(
    #             status=status.HTTP_400_BAD_REQUEST,
    #             message="请求参数错误,请检查后重试",
    #             data=serializer.errors,
    #         )
    #     user = authenticate(
    #         request,
    #         email=serializer.validated_data["email"],
    #         password=serializer.validated_data["password"],
    #     )
    #     if user is not None:
    #         login(request, user)
    #         return APIResponse(
    #             status=status.HTTP_200_OK,
    #             message="登录成功",
    #             data={"email": user.email, "username": user.username},
    #         )
    #     else:
    #         return APIResponse(
    #             status=status.HTTP_400_BAD_REQUEST,
    #             message="邮箱或密码错误,请检查后重试",
    #         )
