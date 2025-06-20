from django.core.validators import MinLengthValidator
from django.db import models

class Post(models.Model):

    title = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            MinLengthValidator(5)
        ],
        error_messages={
            "unique": "Oops! That title is already taken. How about something fresh and fun?"
        },
        blank=False,
        null=False
    )
    image_url = models.URLField(
        help_text="Share your funniest furry photo URL!",
        blank=False,
        null=False
    )
    content = models.TextField(
        blank=False,
        null=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=False
    )
    author = models.ForeignKey(
        to='author.Author',
        on_delete=models.CASCADE,
        related_name='posts'
    )