import os
from decimal import Decimal

import django
from django.db.models import F

from main_app.choices import HotelRoomChoices, CharacterChoices

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def create_pet(name: str, species: str):

    Pet.objects.create(name=name, species=species)

    return f"{name} is a very cute {species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):

    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {name} is {age} years old!"

def rename_artifact(artifact: Artifact, new_name: str):


    if artifact.age > 250 and artifact.is_magical == True:
        artifact.name = new_name
        artifact.save()

def delete_all_artifacts():
    Artifact.objects.all().delete()

# Locations

def show_all_locations():

    return "\n".join(
        f"{l.name} has a population of {l.population}!"
        for l in Location.objects.all().order_by("-id")
    )

def new_capital():

    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()

def get_capitals():
    return Location.objects.filter(is_capital=True).values("name")

def delete_first_location():
    Location.objects.first().delete()


# Car
def apply_discount():
    discount_factor = Decimal("0.01")
    cars = Car.objects.all()

    for c in cars:
        digit_sum = sum(map(int, str(c.year))) * discount_factor
        c.price_with_discount = c.price - (c.price * digit_sum)

    Car.objects.bulk_update(cars, ["price_with_discount"])


def get_recent_cars():

    return Car.objects.filter(year__gt=2020).values("model", "price", "price_with_discount")

def delete_last_car():

    return Car.objects.last().delete()


# Task Encoder

def show_unfinished_tasks():

    return '\n'.join(
        f"Task - {t.title} needs to be done until {t.due_date}!"
        for t in Task.objects.filter(is_finished=False)
    )

def complete_odd_tasks():
    tasks = Task.objects.all()
    for t in tasks:
        if t.id % 2 == 1:
            t.is_finished = True

    Task.objects.bulk_update(tasks, ["is_finished"])

def encode_and_replace(text: str, task_title: str):
    encoded_mes = ''

    for el in text:
        encoded_mes += chr(ord(el) - 3)

    Task.objects.filter(title=task_title).update(description=encoded_mes)


def get_deluxe_rooms():
    rooms = []

    for r in HotelRoom.objects.filter(room_type="Deluxe"):
        if r.id % 2 == 0:
            rooms.append(f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!")

    return '\n'.join(rooms)

def increase_room_capacity():
    rooms = HotelRoom.objects.order_by("id")
    previous_room = None

    for r in rooms:

        if not r.is_reserved:
            continue
        elif previous_room:
            r.capacity += previous_room.capacity
        else:
            r.capacity += r.id

        previous_room = r

    HotelRoom.objects.bulk_update(rooms, ["capacity"])

def reserve_first_room():
    first_room = HotelRoom.objects.first()

    if first_room:
        first_room.is_reserved = True
        first_room.save()

def delete_last_room():
    last_room = HotelRoom.objects.last()

    if last_room and not last_room.is_reserved:
        last_room.delete()


def update_characters():

    Character.objects.filter(class_name=CharacterChoices.MAGE).update(
        level=F("level") + 3,
        intelligence= F("intelligence") - 7
    )
    Character.objects.filter(class_name=CharacterChoices.WARRIOR).update(
        hit_points=F("hit_points") / 2,
        dexterity=F("dexterity") + 4
    )
    Character.objects.filter(class_name__in=[CharacterChoices.SCOUT, CharacterChoices.ASSASSIN]).update(
        inventory="The inventory is empty"
    )

def fuse_characters(first_character: Character, second_character: Character):
    fusion_inventory = ''

    if first_character.class_name in (CharacterChoices.MAGE, CharacterChoices.SCOUT):
        fusion_inventory="Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in (CharacterChoices.ASSASSIN, CharacterChoices.WARRIOR):
        fusion_inventory="Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=f"{first_character.name} {second_character.name}",
        class_name=CharacterChoices.FUSION,
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=fusion_inventory
    )
    first_character.delete()
    second_character.delete()

def grand_dexterity():

    Character.objects.update(dexterity=30)

def grand_intelligence():

    Character.objects.update(intelligence=40)

def grand_strength():

    Character.objects.update(strength=50)

def delete_characters():

    Character.objects.filter(inventory="The inventory is empty").delete()




