import os

import django
from django.db.models import Count, Avg, Sum



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Article, Review


def get_authors(search_name=None, search_email=None):
    authors = None
    if search_name is None and search_email is None:
        return ''

    if search_name and search_email:
        authors = Author.objects.filter(
            full_name__icontains=search_name,
            email__icontains=search_email
        )
    elif search_name:
        authors = Author.objects.filter(full_name__icontains=search_name)
    elif search_email:
        authors = Author.objects.filter(email__icontains=search_email)

    return '\n'.join([
        f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}"
        for a in authors.order_by('-full_name')
    ])

def get_top_publisher():

    top_publisher = Author.objects.get_authors_by_article_count().first()

    if top_publisher and top_publisher.articles_count > 0:
        return f"Top Author: {top_publisher.full_name} with {top_publisher.articles_count} published articles."
    return ''

def get_top_reviewer():

    top_reviewer = (Author.objects
                    .prefetch_related('reviews')
                    .annotate(reviews_count=Count('reviews'))
                    .order_by('-reviews_count', 'email').first()
                    )
    if top_reviewer and top_reviewer.reviews_count > 0:
        return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.reviews_count} published reviews."
    return ''


def get_latest_article():

    article = (Article.objects
               .prefetch_related('reviews', 'authors')
               .annotate(num_reviews=Count('reviews'), avg_reviews_rating=Avg('reviews__rating'))
               .order_by('-published_on').first()
               )

    if article is None:
        return ''
    avg_rating = sum([r.rating for r in article.reviews.all()]) / article.num_reviews if article.num_reviews else 0.0
    return (f"The latest article is: {article.title}. "
            f"Authors: {', '.join([a.full_name for a in article.authors.order_by('full_name')])}. "
            f"Reviewed: {article.num_reviews} times. "
            f"Average Rating: {avg_rating:.2f}.")



def get_top_rated_article():

    article = (Article.objects
               .annotate(avg_rating=Avg('reviews__rating'),
                         num_reviews=Count('reviews'))
               .order_by('-avg_rating', 'title')
               .first()
               )
    if article is None or article.num_reviews == 0:
        return ''

    avg_rating = article.avg_rating or 0.0

    return f"The top-rated article is: {article.title}, with an average rating of {avg_rating:.2f}, " \
           f"reviewed {article.num_reviews} times."

def ban_author(email=None):

    if email is None:
        return "No authors banned."

    author_to_ban = (Author.objects
                     .prefetch_related('reviews')
                     .filter(email=email).first())

    if author_to_ban is not None:
        author_to_ban.is_banned = True
        author_to_ban.save()
        deleted_reviews_count, _ = Review.objects.filter(author=author_to_ban).delete()
        return f"Author: {author_to_ban.full_name} is banned! {deleted_reviews_count} reviews deleted."
    return "No authors banned."


