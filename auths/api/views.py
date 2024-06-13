from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from auths.api.serializers import TokenPairSerializer, SignupSerializer


# Create your views here.

class RegistrationAPIView(APIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create_account(request.data)
            return Response({'success': "Account Created Successfully"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(TokenViewBase):
    serializer_class = TokenPairSerializer
