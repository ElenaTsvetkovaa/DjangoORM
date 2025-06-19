from django.core.validators import MinLengthValidator
from django.db import models

class Trip(models.Model):

    destination = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3)
        ],
        blank=False,
        null=False,
    )
    summary = models.TextField(
        blank=False,
        null=False,
    )
    start_date = models.DateField(
        blank=False,
        null=False,
    )
    duration = models.PositiveSmallIntegerField(
        default=1,
        help_text="*Duration in days is expected.",
        blank=False,
        null=False,
    )
    image_url = models.URLField(
        blank=True,
        null=True
    )
    traveler = models.ForeignKey(
        to='traveler.Traveler',
        on_delete=models.CASCADE,
        related_name='trips'
    )
