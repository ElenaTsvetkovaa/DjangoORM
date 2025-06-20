from decimal import Decimal
from typing import Dict

from django.db import models
from django.db.models import QuerySet, Count, Avg


class RealEstateListingManager(models.Manager):

    def by_property_type(self, property_type: str) -> QuerySet['RealEstateListing']:
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal) -> QuerySet['RealEstateListing']:
        return self.filter(
            price__range=[min_price, max_price]
        )

    def with_bedrooms(self, bedrooms_count: int) -> QuerySet['RealEstateListing']:
        return self.filter(
            bedrooms=bedrooms_count)

    def popular_locations(self) -> QuerySet['RealEstateListing']:
        """
        SELECT
            location,
            COUNT(id) AS location_count
        FROM real_estate
        GROUP BY location_count
        ORDER BY location DESC
        LIMIT 2
        """
        return (self.values("location").annotate(location_count=Count('location'))
                .order_by('-location_count', 'location'))[:2]


class VideoGameManager(models.Manager):


    def games_by_genre(self, genre: str) -> QuerySet['VideoGame']:
        return self.filter(genre=genre)

    def recently_released_games(self, year: int) -> QuerySet['VideoGame']:
        return self.filter(release_year__gte=year)

    def highest_rated_game(self) -> 'VideoGame':
        return self.order_by('-rating').first()

    def lowest_rated_game(self) -> 'VideoGame':
        return self.order_by('rating').first()

    def average_rating(self) -> int:
        avg_rating = self.aggregate(avg_rating=Avg('rating'))["avg_rating"]
        return f"{avg_rating:.1f}"