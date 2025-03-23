from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.choices import GenreChoices
from main_app.managers import DirectorManager
from main_app.mixins import BaseInformation, LastUpdateMixin


# Create your models here.

class Director(BaseInformation):

    years_of_experience = models.SmallIntegerField(
        validators=[
            MinValueValidator(0),
        ],
        default=0
    )

    objects = DirectorManager()


class Actor(BaseInformation, LastUpdateMixin):

    is_awarded = models.BooleanField(
        default=False
    )


class Movie(LastUpdateMixin):

    title = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(5)
        ]
    )
    release_date = models.DateField()
    storyline = models.TextField(
        blank=True,
        null=True
    )
    genre = models.CharField(
        max_length=6,
        choices=GenreChoices,
        default=GenreChoices.OTHER
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ],
        default=0.0
    )
    is_classic = models.BooleanField(
        default=False
    )
    is_awarded = models.BooleanField(
        default=False
    )
    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='movies'
    )
    starring_actor = models.ForeignKey(
        to=Actor,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='starring_movie'
    )
    actors = models.ManyToManyField(
        to=Actor,
        related_name='movies'
    )




