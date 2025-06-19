from datetime import datetime, date

from django.core.exceptions import ValidationError
from django.db import models

from main_app.choices import SpecialtyChoices
from main_app.fields import BooleanChoiceField


class Animal(models.Model):

    name = models.CharField(
        max_length=100
    )
    species = models.CharField(
        max_length=100
    )
    birth_date = models.DateField()
    sound = models.CharField(
        max_length=100
    )

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
                 (today.month, today.day) <
                 (self.birth_date.month, self.birth_date.day))


class Mammal(Animal):

    fur_color = models.CharField(
        max_length=50
    )

class Bird(Animal):

    wing_span = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

class Reptile(Animal):

    scale_type = models.CharField(
        max_length=50
    )

class Employee(models.Model):

    first_name = models.CharField(
        max_length=50
    )
    last_name = models.CharField(
        max_length=50
    )
    phone_number = models.CharField(
        max_length=10
    )

    class Meta:
        abstract = True


class ZooKeeper(Employee):

    specialty = models.CharField(
        max_length=10,
        choices=SpecialtyChoices
    )
    managed_animals = models.ManyToManyField(
        Animal
    )

    def clean(self):

        if self.specialty not in SpecialtyChoices:
            raise ValidationError("Specialty must be a valid choice.")


class Veterinarian(Employee):

    license_number = models.CharField(
        max_length=10
    )

    availability = BooleanChoiceField()


class ZooDisplayAnimal(Animal):

    def display_info(self):
        return f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. It makes a noise like '{self.sound}'."

    def is_endangered(self):
        ENDANGERED_SPECIES = ["Cross River Gorilla", "Orangutan", "Green Turtle"]

        if self.species in ENDANGERED_SPECIES:
            return f"{self.species} is at risk!"
        return f"{self.species} is not at risk."


    class Meta:
        proxy = True



