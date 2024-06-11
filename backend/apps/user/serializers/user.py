from typing import Dict, Any
from apps.user.models import (
    Role,
    User,
    WaitingList,
    UserMessageSettings,
    Message,
    UserMessage,
)
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ["id"]


class UserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = User
        fields = ["email", "role", "username", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def update_profile(self, instance, validated_data):
        validated_data.pop("email", None)
        validated_data.pop("role", None)
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class WaitingListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = WaitingList
        fields = ["email", "username"]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    verify_code = serializers.CharField(required=True)

    class Meta:
        model = WaitingList
        fields = ["email", "username", "password", "verify_code"]
        extra_kwargs = {
            "password": {"write_only": True},
            "verify_code": {"write_only": True},
        }

    def create(self, validated_data):
        instance = WaitingList(**validated_data)
        instance.encrypt_password_and_save()
        return instance


class LoginSerializer(TokenObtainPairSerializer):
    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_email"] = user.email
        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data.update({"email": self.user.email})
        return data


class EmailListSerializer(serializers.Serializer):
    emailList = serializers.ListField(child=serializers.EmailField())


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    verify_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email", "verify_code", "password"]


class UserMessageSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessageSettings
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class UserMessageSerializer(serializers.ModelSerializer):
    message = MessageSerializer(read_only=True)

    class Meta:
        model = UserMessage
        fields = ["id", "type", "message", "is_read", "is_starred"]
        write_only_fields = ["user"]
