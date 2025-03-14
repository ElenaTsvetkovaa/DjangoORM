from datetime import date

from django.core.validators import  MinValueValidator, MaxValueValidator, \
    RegexValidator
from django.db import models

from main_app.choices import DragonBreath
from main_app.mixins import NameMixin, WinsMixin, ModifiedAtMixin


class House(NameMixin, WinsMixin, ModifiedAtMixin):

    motto = models.TextField(
        blank=True,
        null=True
    )
    is_ruling = models.BooleanField(
        default=False
    )
    castle = models.CharField(
        max_length=80,
        blank=True,
        null=True,
    )


class Dragon(NameMixin, WinsMixin, ModifiedAtMixin):

    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(limit_value=1.0),
            MaxValueValidator(limit_value=10.0)
        ],
        default=1.0
    )
    breath = models.CharField(
        max_length=9,
        choices=DragonBreath,
        default='Unknown'
    )
    is_healthy = models.BooleanField(
        default=True
    )
    birth_date = models.DateField(
        default=date.today
    )
    house = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
    )


class Quest(NameMixin, ModifiedAtMixin):

    code = models.CharField(
        max_length=4,
        validators=[
            RegexValidator(regex=r'^[A-Za-z#]{4}$')
        ],
        unique=True
    )
    reward = models.FloatField(
        default=100.0
    )
    start_time = models.DateTimeField()
    dragons = models.ManyToManyField(
        to=Dragon
    )
    host = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
    )









