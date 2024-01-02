from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.auth.serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializers
from apps.users.serializers import UserSerializer


class AuthRegisterView(CreateAPIView):
    """
        Register User
    """
    serializer_class = UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
        Login User
    """
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
        Refresh
    """
    serializer_class = CustomTokenRefreshSerializers
