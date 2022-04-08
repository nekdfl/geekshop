from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from authapp.validators import validate_username


class User(AbstractUser):
    # image = models.ImageField(upload_to="user_avatar", blank=True, validators=[validate_username])
    image = models.ImageField(upload_to="user_avatar", blank=True)
    age = models.PositiveIntegerField(default=18)
