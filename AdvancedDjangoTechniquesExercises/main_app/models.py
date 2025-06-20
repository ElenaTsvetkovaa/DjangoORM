from decimal import Decimal
from tkinter.messagebox import RETRY

from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models

from main_app.validators import NameValidator, PhoneValidator


class Customer(models.Model):

    name = models.CharField(
        max_length=100,
        validators=[
            NameValidator(message="Name can only contain letters and spaces")]
    )
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(18, message="Age must be greater than or equal to 18")
        ]
    )
    email = models.EmailField(
        error_messages={"invalid": "Enter a valid email address"},
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[
            PhoneValidator(message="Phone number must start with '+359' followed by 9 digits")
        ]
    )
    website_url = models.URLField(
        error_messages={"invalid": "Enter a valid URL"},
    )

class BaseMedia(models.Model):

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']

    title = models.CharField(
        max_length=100
    )
    description = models.TextField()
    genre = models.CharField(
        max_length=50
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

class Book(BaseMedia):

    author = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(5, message="Author must be at least 5 characters long")
        ]
    )
    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(6, message="ISBN must be at least 6 characters long")
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"


class Movie(BaseMedia):

    director = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(8, message="Director must be at least 8 characters long")
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"

class Music(BaseMedia):

    artist = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(9, message="Artist must be at least 9 characters long")
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"

class Product(models.Model):
    TAX_PERCENT = 0.08
    SHIPPING_COST = 2.00

    name = models.CharField(
        max_length=100
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def calculate_tax(self):
        return self.price * Decimal(str(self.TAX_PERCENT))

    def calculate_shipping_cost(self, weight: Decimal) -> Decimal:
        return weight * Decimal(str(self.SHIPPING_COST))

    def format_product_name(self):
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    TAX_PERCENT = 0.05
    SHIPPING_COST = 1.5
    PRICE_INCREASE_PERCENT = 0.2

    class Meta:
        proxy = True

    def calculate_price_without_discount(self) -> Decimal:
        return self.price * Decimal(str(1 + self.PRICE_INCREASE_PERCENT))

    def format_product_name(self):
        return f"Discounted Product: {self.name}"


class RechargeEnergyMixin(models.Model):

    class Meta:
        abstract = True

    def recharge_energy(self, amount: int):
        new_energy = min(self.energy + amount, 100)
        if new_energy != self.energy:
            self.energy = new_energy
            self.save()


class Hero(RechargeEnergyMixin):
    ENERGY_DECREASE = 0

    name = models.CharField(
        max_length=100
    )
    hero_title = models.CharField(
        max_length=100
    )
    energy = models.PositiveIntegerField()

    def has_enough_energy(self):
        return self.energy >= self.ENERGY_DECREASE

    def clean(self):
        if self.energy == 0:
            self.energy = 1

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class SpiderHero(Hero):
    ENERGY_DECREASE = 80

    def swing_from_buildings(self):
        if not self.has_enough_energy():
            return f"{self.name} as Spider Hero is out of web shooter fluid"

        self.energy -= self.ENERGY_DECREASE
        self.save()

        return f"{self.name} as Spider Hero swings from buildings using web shooters"

    class Meta:
        proxy = True


class FlashHero(Hero):
    ENERGY_DECREASE = 65

    def run_at_super_speed(self):

        if not self.has_enough_energy():
            return f"{self.name} as Flash Hero needs to recharge the speed force"

        self.energy -= self.ENERGY_DECREASE
        self.save()

        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    class Meta:
        proxy = True


