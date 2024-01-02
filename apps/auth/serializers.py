from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.serializers import UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
