from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None, avatar=None):
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')
        if not first_name:
            raise ValueError('First Name is required')
        if not last_name:
            raise ValueError('Last Name is required')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            avatar=avatar
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name=None, last_name=None, avatar=None):
        user = self.create_user(email, password, first_name, last_name, avatar)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, first_name=None, last_name=None, avatar=None):
        user = self.create_user(email, password, first_name, last_name, avatar)
        user.is_staff = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_notifications = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to="users/profile-pictures", blank=True, null=True, storage=S3Boto3Storage())

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email