from django.core.validators import RegexValidator, MinValueValidator
from django.db import models

from main_app.choices import MissionStatusChoices
from main_app.managers import AstronautManager
from main_app.mixins import NameMixin, UpdateAtMixin, LaunchDateMixin


class Astronaut(NameMixin, UpdateAtMixin):

    phone_number = models.CharField(
        unique=True,
        max_length=15,
        validators=[
            RegexValidator(r'^\d+$')
        ]
    )
    is_active = models.BooleanField(
        default=True
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    spacewalks = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(limit_value=0)
        ]
    )

    objects = AstronautManager()


class Spacecraft(NameMixin, UpdateAtMixin, LaunchDateMixin):

    manufacturer = models.CharField(
        max_length=120,
    )
    capacity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(limit_value=1)
        ]
    )
    weight = models.FloatField(
        validators=[
            MinValueValidator(limit_value=0.0)
        ]
    )


class Mission(NameMixin, UpdateAtMixin, LaunchDateMixin):

    description = models.TextField(
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=9,
        choices=MissionStatusChoices,
        default=MissionStatusChoices.PLANNED
    )
    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE
    )
    astronauts = models.ManyToManyField(
        to=Astronaut,
    )
    commander = models.ForeignKey(
        to=Astronaut,
        null=True,
        on_delete=models.SET_NULL,
        related_name='commanded_missions'
    )