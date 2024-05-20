from rest_framework import serializers
from apps.user.models import EmailSuffixFormat, EmailTag, EmailFormatTag

class EmailSuffixFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSuffixFormat
        fields = '__all__'

class EmailTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTag
        fields = '__all__'

class EmailFormatTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailFormatTag
        fields = '__all__'
        