from django.forms import ValidationError
from django.db import transaction
from rest_framework import status, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import AnonRateThrottle
from apps.system.utils.api_response import APIResponse
from apps.user.models import check_email_suffix_format
from apps.user.utils.email import (
    send_verify_email
)
from apps.user.models import User, WaitingList
from apps.user.serializers.user import WaitingListSerializer


# Create your views here.
class LoginView(TokenObtainPairView):
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

        return Response(result, status=status.HTTP_200_OK)


class RegisterView(ModelViewSet):
    class RegisterThrottle(AnonRateThrottle):
        rate = "1/min"

    queryset = WaitingList.objects.all()
    serializer_class = WaitingListSerializer
    throttle_classes = [RegisterThrottle]

    def create(self,request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(status=status.HTTP_400_BAD_REQUEST, message="请求参数错误,请检查后重试", data=serializer.errors)
        email = serializer.validated_data["email"]
        check_email_suffix_format(email)
        if (
            WaitingList.objects.filter(email=email).exists()
            or User.objects.filter(email=email).exists()
        ):
            raise ValidationError("user with this email already exists")

        with transaction.atomic():
            waitling_user = serializer.save()
            waitling_user.update_verify_code()
            send_verify_email(waitling_user.email,waitling_user.username, waitling_user.verify_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def throttle_failure(self, request, wait_time):
        return APIResponse(status=status.HTTP_429_TOO_MANY_REQUESTS, message=f"已超过速率限制。请在{wait_time}秒后重试。")

    # def create(self, request: Request, *args, **kwargs) -> Response:
    # def perform_create(self, serializer):
    #     email = serializer.validated_data["email"]

    #     if not check_email_format(email):
    #         raise ValidationError(
    #             "Please provide a valid email, check the valid email format"
    #         )

    #     if (
    #         WaitingList.objects.filter(email=email).exists()
    #         or User.objects.filter(email=email).exists()
    #     ):
    #         raise ValidationError("user with this email already exists")

    #     with transaction.atomic():
    #         waitling_user = serializer.save()
    #         waitling_user.update_verify_code()
