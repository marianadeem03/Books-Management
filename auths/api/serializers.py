import re

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from auths.models import User
from auths.helper import CreateUser


class TokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user_data = {
            "userid": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "access": data["access"],
            "refresh": data["refresh"]
        }
        return user_data


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def validate(self, attrs):
        password = attrs.get('password')
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError(
                "The password must contain at least one uppercase letter."
            )
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError(
                "The password must contain at least one lowercase letter."
            )
        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError(
                "The password must contain at least one digit."
            )
        if not re.search(r'[^A-Za-z0-9]', password):
            raise serializers.ValidationError(
                "The password must contain at least one special character."
            )
        return attrs

    @staticmethod
    def create_account(validated_data):
        user_data = CreateUser(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role'],
        )
        return user_data
