from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework.serializers import ModelSerializer

from apps.users.models import ProfileModel

UserModel = get_user_model()


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('id', 'name', 'surname')


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = (
            'id', 'email', 'password', 'is_active', 'is_scientist', 'is_staff',  'is_superuser',
            'last_login', 'created_at', 'updated_at', 'profile'
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    @atomic
    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_user(**validated_data)
        ProfileModel.objects.create(**profile, user=user)
        return user
