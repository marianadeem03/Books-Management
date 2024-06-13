from django.urls import path
from auths.api.views import LoginAPIView, RegistrationAPIView

urlpatterns = [
    # Auth
    path("", LoginAPIView.as_view(), name="token_obtain_pair"),
    path("register/", RegistrationAPIView.as_view(), name="user_register"),


]
