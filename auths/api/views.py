from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from auths.api.serializers import (TokenPairSerializer,
                                   SignupSerializer,
                                   TokenValidationSerializer)


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = SignupSerializer


class LoginAPIView(TokenViewBase):
    serializer_class = TokenPairSerializer


class ValidateTokenAPIView(APIView):
    serializer_class = TokenValidationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validate(serializer.validated_data)
        return Response({'message': 'Token is valid'}, status=status.HTTP_200_OK)
