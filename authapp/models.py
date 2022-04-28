from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.utils.timezone import now


class User(AbstractUser):
    # image = models.ImageField(upload_to="user_avatar", blank=True, validators=[validate_username])
    image = models.ImageField(upload_to="user_avatar", blank=True)
    age = models.PositiveIntegerField(default=18)
    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expire = models.DateTimeField(null=True, blank=True, default=now() + timedelta(
        hours=settings.ACTIVATION_KEY_EXPIRED_HOURS if 'settings.ACTIVATION_KEY_EXPIRED_HOURS' in globals() else 72))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expire:
            return False
        return True
