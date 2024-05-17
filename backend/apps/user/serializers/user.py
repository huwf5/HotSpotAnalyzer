from apps.user.models import Role, User, WaitingList, check_email_suffix_format
from apps.user.utils.email import generate_verify_code, send_verify_email
from application.settings import EMAIL_VALIDATION_TIME_LIMIT
from rest_framework import serializers
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ["id"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["email", "role", "username"]
        exclude = ["password"]

    def create(self, validated_data):
        return super().create(validated_data)


class WaitingListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[validate_email, check_email_suffix_format]
    )

    class Meta:
        model = WaitingList
        fields = ["email", "username", "password", "verify_code"]
        extra_kwargs = {
            "password": {"write_only": True},
            "verify_code": {"write_only": True},
        }

    def update_verify_code(self, validated_data):
        """
        Update the verify code and send the email, will automatically set the expiration time
        But will not save the object to the database
        """

        verify_code = generate_verify_code()
        expired_at = timezone.now() + timedelta(minutes=EMAIL_VALIDATION_TIME_LIMIT)
        send_verify_email(
            validated_data["email"], validated_data["username"], verify_code
        )
        validated_data["verify_code"] = verify_code
        validated_data["expired_at"] = expired_at

    def create(self, validated_data):
        check_email_suffix_format(validated_data["email"])
        validated_data["password"] = make_password(validated_data["password"])
        self.update_verify_code(validated_data)
        return super().create(validated_data)
