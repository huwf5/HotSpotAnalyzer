from rest_framework import serializers
from apps.user.models import Role, User, WaitingList, check_email_suffix_format

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ['id',]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['email','role','username']
        exclude = ['password']

    def create(self, validated_data):
        return super().create(validated_data)
    

class WaitingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitingList
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_email(self, value):
        value = super().validate_email(value)
        check_email_suffix_format(value)
        return value
            

    def create(self, validated_data):
        return WaitingList.objects.create(**validated_data)