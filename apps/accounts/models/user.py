from django.contrib.auth.models import AbstractUser

from apps.core.models import BaseModel


class CustomUser(AbstractUser, BaseModel):
    """
    Custom user model.

    Additional fields will be added later:
    - avatar
    - preferred currency
    - theme
    - language
    """

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"