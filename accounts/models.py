from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_user(self, email, name, last_name, password):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            last_name=last_name,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, last_name, password):
        user = self.create_user(email, name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Role(models.Model):
    name = models.CharField(max_length=40)
    status = models.CharField(max_length=40, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=40, null=True)
    token = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    rol = models.ForeignKey('Role', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name", "last_name"]

    def __str__(self):
        return "{}".format(self.name)

    def get_short_name(self):
        return "{}".format(self.name)

    def get_full_name(self):
        return "{} {}".format(self.name, self.last_name)