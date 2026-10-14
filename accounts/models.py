from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHERS = "O", "Others"

    email = models.EmailField("email address", unique=True)

    gender = models.CharField(max_length=1, choices=Gender.choices)
    bio = models.TextField()

    def __str__(self):
        return self.email
