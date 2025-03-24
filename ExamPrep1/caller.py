import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from helpers import populate_model_with_data
from main_app.models import Actor, Movie, Director
from django.db.models import Q, Count, F


def populate_db():

    populate_model_with_data(Director)
    populate_model_with_data(Actor)
    populate_model_with_data(Movie)


def get_directors(search_name=None, search_nationality=None):

    directors = None
    if search_name is not None and search_nationality is not None:
        directors = Director.objects.filter(
            Q(full_name__icontains=search_name) | Q(nationality__icontains=search_nationality))
    elif search_name is not None:
        directors = Director.objects.filter(
                    full_name__icontains=search_name)
    elif search_nationality is not None:
        directors = Director.objects.filter(
                    nationality__icontains=search_nationality)

    if directors is None:
        return ''

    return '\n'.join([
        f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}"
        for d in directors.order_by('full_name')
    ])


def get_top_director():

    director = Director.objects.get_directors_by_movies_count().first()

    if not director:
        return ""

    return f"Top Director: {director.full_name}, movies: {director.movies_count}."


def get_top_actor():

    top_actor = (Actor.objects.prefetch_related('starring_movie')
                 .annotate(movies_count=Count('starring_movie'))
                 .filter(movies_count__gt=0)
                 .order_by('-movies_count', 'full_name').first()
                 )

    if top_actor is not None:

        avg_rating = sum([m.rating for m in top_actor.starring_movie.all()]) / top_actor.movies_count
        return (f"Top Actor: {top_actor.full_name}, "
                f"starring in movies: {', '.join([m.title for m in top_actor.starring_movie.all()])}, "
                f"movies average rating: {avg_rating:.1f}")
    return ''


def get_actors_by_movies_count():

    top_actors = (Actor.objects.prefetch_related('movies')
                        .annotate(movies_count=Count('movies'))
                        .filter(movies_count__gt=0)
                        .order_by('-movies_count', 'full_name')
                        )[:3]

    return '\n'.join([
        f"{a.full_name}, participated in {a.movies_count} movies"
        for a in top_actors
    ])

def get_top_rated_awarded_movie():

    movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if movie is None:
        return ''

    return (f"Top rated awarded movie: {movie.title}, "
            f"rating: {movie.rating:.1f}. Starring actor: {movie.starring_actor.full_name if movie.starring_actor else 'N/A'}. "
            f"Cast: {', '.join([a.full_name for a in movie.actors.order_by('full_name')])}.")


def increase_rating():

    updated_movies_count = (Movie.objects.filter(is_classic=True, rating__lt=10.0)
                            .update(rating=F('rating') + 0.1))

    if updated_movies_count == 0:
        return "No ratings increased."

    return f"Rating increased for {updated_movies_count} movies."


