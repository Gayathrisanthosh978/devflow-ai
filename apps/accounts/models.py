# Create your models here.

import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    PROJECT_MANAGER = "PROJECT_MANAGER", "Project Manager"
    DEVELOPER = "DEVELOPER", "Developer"
    QA = "QA", "QA Engineer"
    CLIENT = "CLIENT", "Client"


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for DevFlow AI."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name or self.email