from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_kwargs):
        if not email:
            raise ValueError('Thr email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_kwargs):
        extra_kwargs.setdefault('is_active', True)
        extra_kwargs.setdefault('is_scientist', True)
        extra_kwargs.setdefault('is_staff', True)
        extra_kwargs.setdefault('is_superuser', True)

        if not extra_kwargs.get('is_scientist'):
            raise ValueError('Is_scientist must have True')

        if not extra_kwargs.get('is_staff'):
            raise ValueError('Is_staff must have True')

        if not extra_kwargs.get('is_superuser'):
            raise ValueError('Is_superuser must have True')

        user = self.create_user(email, password, **extra_kwargs)
        return user
