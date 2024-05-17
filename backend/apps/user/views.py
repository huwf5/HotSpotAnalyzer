from apps.system.utils.api_response import APIResponse
from apps.user.models import check_email_suffix_format
from apps.user.utils.email import send_verify_email
from apps.user.models import User, WaitingList
from apps.user.serializers.user import WaitingListSerializer, VerifyEmailSerializer
from django.forms import ValidationError
from django.utils import timezone
from rest_framework import status, generics
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import ValidationError
from rest_framework import throttling


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

        try:
            waiting_user = WaitingList.objects.get(
                email=serializer.validated_data["email"]
            )
        except WaitingList.DoesNotExist:
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="用户不存在,请先注册",
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
    def post(self, request: Request, *args, **kwargs) -> APIResponse:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        result = serializer.validated_data
        result["email"] = serializer.user.email
        result["username"] = serializer.user.username
        result["token"] = result.pop("access")

        return APIResponse(result, status=status.HTTP_200_OK)
