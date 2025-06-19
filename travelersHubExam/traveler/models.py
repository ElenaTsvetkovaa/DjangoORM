from django.core.validators import MinLengthValidator
from django.db import models

from traveler.validators import NicknameValidator


class Traveler(models.Model):

    nickname = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(3),
            NicknameValidator()
        ],
        help_text= "*Nicknames can contain only letters and digits."
    )
    email = models.EmailField(
        max_length=30,
        unique=True,
        blank=False,
        null=False,
    )
    country = models.CharField(
        max_length=3,
        blank=False,
        null=False,
    )
    about_me = models.TextField(
        blank=True,
        null=True
    )
