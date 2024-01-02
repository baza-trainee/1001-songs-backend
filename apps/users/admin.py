from django.contrib import admin

from .models import UserModel, ProfileModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'is_active', 'is_scientist', 'is_staff',  'is_superuser',
        'last_login', 'created_at', 'updated_at', 'profile'
    )


@admin.register(ProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname')
