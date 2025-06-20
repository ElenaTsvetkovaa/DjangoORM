from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class NicknameValidator:

    def __init__(self, message=None):
        self.message = message


    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = "Your nickname is invalid!"
        else:
            self.__message = value

    def __call__(self, value: str):
        if not value.isalnum():
            raise ValidationError(self.message)
