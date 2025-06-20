from django.core.validators import MinLengthValidator
from django.db import models
from author.validators import NameValidator, PasswordValidator


class Author(models.Model):

    first_name = models.CharField(
        max_length=40,
        validators=[
            MinLengthValidator(4),
            NameValidator()
        ],
        blank=False,
        null=False
    )
    last_name = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(2),
            NameValidator()
        ],
        blank=False,
        null=False
    )
    passcode = models.CharField(
        max_length=6,
        validators=[
            PasswordValidator()
        ],
        help_text="Your passcode must be a combination of 6 digits",
        blank=False,
        null=False
    )
    pets_number = models.PositiveSmallIntegerField(
        blank=False,
        null=False
    )
    info = models.TextField(
        blank=True,
        null=True
    )
    image_url = models.URLField(
        blank=True,
        null=True
    )

