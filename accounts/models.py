from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHERS = "O", "Others"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(
        "Username", max_length=30, unique=True, blank=True, null=True
    )

    display_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True)
    bio = models.TextField(blank=True)
    onboarding_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name or self.username or self.user.email
