from datetime import timedelta
from enum import StrEnum

from django.core.exceptions import ValidationError
from django.db import models


class StudentIDField(models.PositiveIntegerField):

    @staticmethod
    def validate_field(value):
        try:
            return int(value)
        except ValueError:
            raise ValueError("Invalid input for student ID")

    def to_python(self, value):

        return self.validate_field(value)


    def get_prep_value(self, value):

        validated_value = self.validate_field(value)

        if validated_value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")
        return validated_value


class MaskedCreditCardField(models.CharField):
    
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 20
        super().__init__(*args, **kwargs)


    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")

        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")

        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        return f"****-****-****-{value[-4:]}"

