from django.core.validators import MinLengthValidator
from django.db import models


class NameMixin(models.Model):
    MIN_LENGTH = 5
    MAX_LENGTH = 80

    name = models.CharField(
        max_length=MAX_LENGTH,
        validators=[
            MinLengthValidator(MIN_LENGTH)
        ],
        unique=True
    )

    class Meta:
        abstract = True

class WinsMixin(models.Model):
    DEFAULT_WINS = 0

    wins = models.PositiveSmallIntegerField(
        default=DEFAULT_WINS
    )

    class Meta:
        abstract = True

class TimeStampMixin(models.Model):

    modified_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True




