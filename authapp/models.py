import base64
import os
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


def get_b64_avatr_filename(filename, user_pk):
    file_ext = str(filename).split(".")[-1]
    new_filename = base64.urlsafe_b64encode(f'user-{user_pk}'.encode('ascii')).decode('ascii')
    return f'{new_filename}.{file_ext}'


def delete_old_photo(filename, user_pk):
    upload_dir = "user_avatar"
    file_ext = str(filename).split(".")[-1]
    new_filename = base64.urlsafe_b64encode(f'user-{user_pk}'.encode('ascii')).decode('ascii')
    filepath = os.path.join(upload_dir, f'{new_filename}.{file_ext}')
    os.remove(filepath)


def upload_avatar(instance, filename):
    upload_dir = "user_avatar"
    if os.path.exists(os.path.join(upload_dir, str(instance.image))):
        delete_old_photo(instance.image, instance.pk)
    file_ext = str(filename).split(".")[len(str(filename).split(".")) - 1]
    new_filename = base64.urlsafe_b64encode(f'user-{instance.pk}'.encode('ascii')).decode('ascii')
    return os.path.join(upload_dir, f'{new_filename}.{file_ext}')


class User(AbstractUser):
    # image = models.ImageField(upload_to="user_avatar", blank=True, validators=[validate_username])
    image = models.ImageField(upload_to=upload_avatar, blank=True)
    age = models.PositiveIntegerField(default=18)
    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expire = models.DateTimeField(null=True, blank=True, auto_now=True)

    def is_activation_key_expired(self):
        vtimedelta = timedelta(
            hours=settings.ACTIVATION_KEY_EXPIRED_HOURS if 'settings.ACTIVATION_KEY_EXPIRED_HOURS' in globals() else 72)
        if now() <= self.activation_key_expire + vtimedelta:
            return False
        return True

    def get_avatar(self):
        if self.image:
            return self.image.url
        elif self.userprofile.photo:
            return self.userprofile.photo
        else:
            return None


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М',),
        (FEMALE, 'Ж',),
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    about = models.TextField(verbose_name='о себе', blank=True, null=True)
    gender = models.CharField(verbose_name='пол', blank=True, choices=GENDER_CHOICES, max_length=2)
    photo = models.CharField(verbose_name='Фото', blank=True, null=True, max_length=2084)
    language = models.CharField(verbose_name='Язык', blank=True, max_length=25, default='ru')


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    pass
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(instance, created, **kwargs):
    if not created:
        instance.userprofile.save()
