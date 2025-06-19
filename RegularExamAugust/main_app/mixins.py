from django.core.validators import MinLengthValidator
from django.db import models


class NameMixin(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(limit_value=2)
        ]
    )

class UpdateAtMixin(models.Model):

    class Meta:
        abstract = True

    updated_at = models.DateTimeField(
        auto_now=True
    )

class LaunchDateMixin(models.Model):

    class Meta:
        abstract = True

    launch_date = models.DateField()



