from rest_framework import serializers
from apps.user.models import EmailSuffixFormat, EmailFormatTag
from django.core.validators import validate_email
from ..utils.email import generate_verify_code, send_verify_email
from ..models import EmailVerification
from application.settings import EMAIL_VALIDATION_TIME_LIMIT
from django.utils import timezone
from datetime import timedelta


class EmailVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailVerification
        fields = ["email", "usage"]

    def update_verify_code(self, validated_data):
        """
        Update the verify code and send the email, will automatically set the expiration time
        But will not save the object to the database
        """

        verify_code = generate_verify_code()
        expired_at = timezone.now() + timedelta(minutes=EMAIL_VALIDATION_TIME_LIMIT)
        send_verify_email(
            validated_data["email"], verify_code, usage=validated_data["usage"]
        )
        validated_data["verify_code"] = verify_code
        validated_data["expired_at"] = expired_at

    def create(self, validated_data):
        validate_email(validated_data["email"])
        self.update_verify_code(validated_data)
        return super().create(validated_data)


class EmailSuffixFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSuffixFormat
        fields = "__all__"
    
    def create(self, validated_data):
        validated_data["is_active"] = True
        return super().create(validated_data)


class EmailFormatTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailFormatTag
        fields = "__all__"
