from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models


class NameAndCountryMixin(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3)
        ]
    )

    country = models.CharField(
        max_length=40,
        default='TBC'
    )

class RatingMixin(models.Model):

    MIN_RATING = 0.0
    MAX_RATING = 5.0

    class Meta:
        abstract = True

    rating = models.FloatField(
        validators=[
            MinValueValidator(MIN_RATING),
            MaxValueValidator(MAX_RATING)
        ],
        default=MIN_RATING
    )

class UpdatedAtMixin(models.Model):

    class Meta:
        abstract = True

    updated_at = models.DateTimeField(
        auto_now=True
    )

