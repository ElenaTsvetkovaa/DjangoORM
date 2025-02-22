from django.db import models

class StatusChoices(models.TextChoices):

    PENDING = 'P', 'Pending'
    COMPLETED = 'COM', 'Completed'
    CANCELED = 'CAN', 'Canceled'