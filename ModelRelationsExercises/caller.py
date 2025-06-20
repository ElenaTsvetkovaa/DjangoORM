
import os
from datetime import timedelta, datetime

import django
from django.db.models.aggregates import Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Book, Author, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Car, \
    Registration


def show_all_authors_with_their_books():

    authors_with_books = []

    for a in Author.objects.exclude(book__isnull=True).order_by("id"):
        authors_with_books.append(f"{a.name} has written - {', '.join(b.title for b in a.book_set.all())}!")

    return '\n'.join(authors_with_books)

def delete_all_authors_without_books():

    Author.objects.filter(book__isnull=True).delete()


# MUSIC APP

def add_song_to_artist(artist_name: str, song_title: str):

    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)

def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)

    return artist.songs.order_by("-id")

def remove_song_from_artist(artist_name: str, song_title: str):

    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)

# SHOP

def calculate_average_rating_for_product_by_name(product_name: str):

    product = Product.objects.get(name=product_name)
    avg_rating = product.reviews.aggregate(avg_rating=Avg("rating")).get("avg_rating")
    return avg_rating

def get_reviews_with_high_ratings(threshold: int):

    return Review.objects.filter(rating__gte=threshold)

def get_products_with_no_reviews():

    return Product.objects.filter(reviews__isnull=True).order_by("-name")

def delete_products_without_reviews():
    Product.objects.exclude(reviews__isnull=False).delete()

# LICENSE

def calculate_licenses_expiration_dates():
    result = []

    for l in DrivingLicense.objects.all().order_by("-license_number"):
        result.append(f"License with number: {l.license_number} expires on {l.issue_date + timedelta(days=365)}!")

    return '\n'.join(result)

def get_drivers_with_expired_licenses(due_date: datetime.date):
    """
    SELECT
        *
    FROM
        driver AS d
    JOIN
        license AS l
    ON d.id = l.driver_id
    WHERE
        l.issue_date + INTERVAL '365 days' > due_date;
    """
    last_possible_issue_date = due_date - timedelta(days=365)

    drivers_with_expired_licences = Driver.objects.filter(license__issue_date__gt=last_possible_issue_date)
    return drivers_with_expired_licences

def register_car_by_owner(owner: Owner):

    car = Car.objects.filter(registration__isnull=True).first()
    registration = Registration.objects.filter(car__isnull=True).first()

    car.owner = owner
    car.save()

    registration.registration_date = datetime.today()
    registration.car = car
    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."




