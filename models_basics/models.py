from datetime import date

from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)

class Department(models.Model):

    class CitiesChoices(models.TextChoices):
        SF = 'Sf', 'Sofia'
        PV = 'Pv', 'Plovdiv'
        BS = 'Bs', 'Burgas'
        VA = 'Va', 'Varna'

    code = models.CharField(
        primary_key=True,
        max_length=4,
        unique=True
    )

    name = models.CharField(max_length=50, unique=True)

    employees_count = models.PositiveIntegerField(
        verbose_name='Employees Count',
        default=1,
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=20,
        choices=CitiesChoices,
        blank=True,
        null=True
    )

    last_edited_on = models.DateTimeField(auto_now=True, editable=False)

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(
        null=True,
        blank=True,
    )
    budget = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2,

    )
    duration_in_days = models.PositiveIntegerField(
        verbose_name='Duration in Days',
        null=True,
        blank=True,
    )
    estimated_hours = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Estimated Hours'
    )
    start_date = models.DateField(
        verbose_name='Start Date',
        null=True,
        blank=True,
        default=date.today
    )
    created_on = models.DateTimeField(
        editable=False,
        auto_now_add=True
    )
    last_edited_on = models.DateTimeField(
        editable=False,
        auto_now=True
    )