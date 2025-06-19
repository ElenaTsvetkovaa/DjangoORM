from django.db import models

class HotelRoomChoices(models.TextChoices):

    STANDARD = "Standard", "Standard"
    DELUXE = "Deluxe", "Deluxe"
    SUITE = "Suite", "Suite"


class CharacterChoices(models.TextChoices):

    MAGE = "Mage", "Mage"
    WARRIOR = "Warrior", "Warrior"
    ASSASSIN = "Assassin", "Assassin"
    SCOUT = "Scout", "Scout"
    FUSION = "Fusion", "Fusion"


