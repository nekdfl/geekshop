from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username(value):
    if not value.isalpha():
        raise ValidationError(_(f"Invalid username {value}. \
Username must contain only a-z A-Z chars"))
