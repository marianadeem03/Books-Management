from django.urls import path
from auths.api.views import (
    LoginAPIView,
    RegistrationAPIView,
    ValidateTokenAPIView,
)

urlpatterns = [
    # Auth
    path("login/", LoginAPIView.as_view(), name="token_obtain_pair"),
    path("register/", RegistrationAPIView.as_view(), name="user_register"),
    path("token_validate/", ValidateTokenAPIView.as_view(), name="validate_token"),
]
