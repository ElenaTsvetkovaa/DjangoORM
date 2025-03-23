from django.db import models


class GenreChoices(models.TextChoices):
    """
    'Action', 'Comedy', 'Drama', and 'Other'.
    """
    ACTION = 'Action', 'Action'
    COMEDY = 'Comedy', 'Comedy'
    DRAMA = 'Drama', 'Drama'
    OTHER = 'Other', 'Other'


