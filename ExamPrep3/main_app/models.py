from datetime import date

from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from main_app.choices import DragonBreathChoices
from main_app.managers import HouseManager
from main_app.mixins import NameMixin, TimeStampMixin, WinsMixin


class House(NameMixin, WinsMixin, TimeStampMixin):

    CASTLE_MAX_LENGTH = 80

    motto = models.TextField(
        null=True,
        blank=True
    )
    is_ruling = models.BooleanField(
        default=False
    )
    castle = models.CharField(
        max_length=CASTLE_MAX_LENGTH,
        null=True,
        blank=True
    )
    objects = HouseManager()


class Dragon(NameMixin, WinsMixin, TimeStampMixin):

    MIN_POWER = 1.0
    MAX_POWER = 10.0
    MAX_BREATH_LENGTH = 9

    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(MIN_POWER),
            MaxValueValidator(MAX_POWER)
        ],
        default=MIN_POWER
    )
    breath = models.CharField(
        max_length=MAX_BREATH_LENGTH,
        choices=DragonBreathChoices,
        default=DragonBreathChoices.UNKNOWN
    )
    is_healthy = models.BooleanField(
        default=True
    )
    birth_date = models.DateField(
        default=date.today()
    )
    house = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
        related_name='dragons'
    )


class Quest(NameMixin, TimeStampMixin):

    MAX_CODE_CHARS = 4
    DEFAULT_REWARD = 100.0

    code = models.CharField(
        max_length=MAX_CODE_CHARS,
        validators=[
            RegexValidator(r"^[A-Za-z#]{4}$")
        ],
        unique=True
    )
    reward = models.FloatField(
        default=DEFAULT_REWARD
    )
    start_time = models.DateTimeField()
    dragons = models.ManyToManyField(
        to=Dragon,
        related_name='quests'
    )
    host = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
        related_name='quests'
    )



