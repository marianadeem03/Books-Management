from rest_framework import serializers
from django.contrib.auth import password_validation
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from auths.models import User


class TokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, value):
        value['email'] = value.get(self.username_field).lower()
        data = super().validate(value)
        user_data = {
            "id": self.user.id,
            "role": self.user.role,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "is_active": self.user.is_active,
            "last_active": self.user.last_login,
            "creation_time": self.user.date_joined,
            "token": data["access"],
        }
        return user_data


class TokenValidationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate(self, data):
        token = data.get('token')

        try:
            AccessToken(token)
        except Exception as e:
            raise serializers.ValidationError({'error': e})
        return data


class SignupSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'is_active',
            'last_login',
            'date_joined',
            'token',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'is_active': {'read_only': True},
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
            'token': {'read_only': True},
        }

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    @staticmethod
    def validate_email(value):
        value = value.lower()
        # Ensure email uniqueness with case insensitivity
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        user.token = AccessToken.for_user(user)
        return user
