from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomTokenObtainPairView


from apps.auth.views import AuthRegisterView

urlpatterns = [
    path('', CustomTokenObtainPairView.as_view(), name='auth_login'),
    path('/refresh', TokenRefreshView.as_view(), name='auth_refresh'),
    path('/register', AuthRegisterView.as_view(), name='auth_register'),
]
