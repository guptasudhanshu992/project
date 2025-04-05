import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class NewUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    source = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = NewUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserDetails(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    country_id = models.CharField(max_length=100, blank=True, null=True)


class Roles(models.Model):
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)


class CountryList(models.Model):
    country_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)


class Permissions(models.Model):
    permission_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)


class UserRoles(models.Model):
    user_id = models.UUIDField()
    role_id = models.UUIDField()


class RolePermissions(models.Model):
    role_id = models.UUIDField()
    permission_id = models.UUIDField()


class Tokens(models.Model):
    token_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
