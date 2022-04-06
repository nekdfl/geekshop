from django.utils.translation import gettext_lazy as _


def validate_username(value):
    if not value.isalpha():
        raise ValueError(_(f"Invalid username {value}. Username can't contain digits"))
