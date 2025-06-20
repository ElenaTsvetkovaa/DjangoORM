from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models


class NameMixin(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[
            MinLengthValidator(limit_value=5),
            MaxLengthValidator(limit_value=80),
        ]
    )
    class Meta:
        abstract = True

class WinsMixin(models.Model):

    wins = models.PositiveSmallIntegerField(
        default=0,
    )
    class Meta:
        abstract = True

class ModifiedAtMixin(models.Model):
    modified_at = models.DateTimeField(
        auto_now=True
    )
    class Meta:
        abstract = True



