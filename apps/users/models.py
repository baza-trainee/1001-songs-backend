from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'users'
        verbose_name = 'user'

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_scientist = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()


class ProfileModel(models.Model):
    class Meta:
        db_table = 'profile'
        verbose_name = 'profile'

    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
