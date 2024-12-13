from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase

from auths.api.serializers import (
    UserSerializer,
    SignupSerializer,
    TokenPairSerializer,
)


class RegistrationAPIView(APIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = str(AccessToken.for_user(user))
        response_data = {**serializer.data, "token": token}
        return Response(response_data, status.HTTP_201_CREATED)


class LoginAPIView(TokenViewBase):
    serializer_class = TokenPairSerializer


class ValidateTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        serializer = UserSerializer(request.user).data
        return Response(serializer, status=status.HTTP_200_OK)
