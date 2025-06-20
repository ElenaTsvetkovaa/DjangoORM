from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.db import models

from main_app.choices import GenreChoices
from main_app.managers import PublisherManager
from main_app.mixins import NameAndCountryMixin, UpdatedAtMixin, RatingMixin


class Publisher(NameAndCountryMixin, RatingMixin):

    DEFAULT_ESTABLISHED_DATE = '1800-01-01'

    established_date = models.DateField(
        default=DEFAULT_ESTABLISHED_DATE
    )

    objects = PublisherManager()


class Author(NameAndCountryMixin, UpdatedAtMixin):

    birth_date = models.DateField(
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True
    )


class Book(UpdatedAtMixin, RatingMixin):

    TITLE_MAX_LENGTH = 200
    TITLE_MIN_LENGTH = 2
    GENRE_MAX_LENGTH = 11
    MIN_PRICE = 0.01
    MAX_PRICE = 9999.99

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        validators=[
            MinLengthValidator(TITLE_MIN_LENGTH)
        ]
    )
    publication_date = models.DateField()
    summary = models.TextField(
        blank=True,
        null=True
    )
    genre = models.CharField(
        max_length=GENRE_MAX_LENGTH,
        choices=GenreChoices,
        default=GenreChoices.OTHER
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(MIN_PRICE),
            MaxValueValidator(MAX_PRICE)
        ],
        default=MIN_PRICE
    )
    is_bestseller = models.BooleanField(
        default=False
    )
    publisher = models.ForeignKey(
        to=Publisher,
        on_delete=models.CASCADE,
        related_name='books'
    )
    main_author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='main_books'
    )
    co_authors = models.ManyToManyField(
        to=Author,
        related_name='co_books'
    )












