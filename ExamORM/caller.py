import os
import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from helpers import populate_model_with_data
from main_app.models import Publisher, Author, Book



def populate_db():

    populate_model_with_data(Publisher)
    populate_model_with_data(Author)
    populate_model_with_data(Book)


def get_publishers(search_string=None):

    if search_string is None:
        return "No search criteria."

    publishers = Publisher.objects.filter(
        Q(name__icontains=search_string) | Q(country__icontains=search_string)
    ).order_by('-rating', 'name')

    if not publishers.exists():
        return "No publishers found."

    return '\n'.join([
        f"Publisher: {p.name}, country: {p.country if p.country != 'TBC' else 'Unknown'}, rating: {p.rating:.1f}"
        for p in publishers
    ])


def get_top_publisher():

    top_publisher = Publisher.objects.get_publishers_by_books_count().first()

    if top_publisher is None:
        return "No publishers found."

    return f"Top Publisher: {top_publisher.name} with {top_publisher.books_count} books."



def get_top_main_author():

    author = (Author.objects.prefetch_related('main_books')
             .annotate(main_books_count=Count('main_books'),
                       books_avg_rating=Avg('main_books__rating'))
             .filter(main_books_count__gt=0)
             .order_by('-main_books_count', 'name').first())

    if author is None:
        return "No results."

    book_titles = ', '.join([b.title for b in author.main_books.order_by('title')])

    return (f"Top Author: {author.name}, "
            f"own book titles: {book_titles}, "
            f"books average rating: {author.books_avg_rating:.1f}")


def get_authors_by_books_count():

    authors = (Author.objects
               .annotate(main_books_count=Count('main_books'),
                         co_books_count=Count('co_books'),
                         total_books_count=F('main_books_count') + F('co_books_count'))
               .filter(total_books_count__gt=0)
               .order_by('-total_books_count', 'name'))[:3]

    if authors.exists():
        return '\n'.join([
            f"{a.name} authored {a.total_books_count} books."
            for a in authors
        ])

    return "No results."


def get_top_bestseller():

    book = (Book.objects.prefetch_related('co_authors')
            .filter(is_bestseller=True)
            .order_by('-rating', 'title')
            .first())

    if book is None:
        return "No results."

    co_authors = ', '.join([c.name for c in book.co_authors.order_by('name')]) if book.co_authors.exists() else 'N/A'
    return (f"Top bestseller: {book.title}, "
            f"rating: {book.rating:.1f}. Main author: {book.main_author.name}. "
            f"Co-authors: {co_authors}.")


def increase_price():

    num_of_updated_books = Book.objects.filter(
        publication_date__year=2025,
        rating__gte=4.0
    ).update(price=F('price') * 1.2)

    if num_of_updated_books > 0:
        return f"Prices increased for {num_of_updated_books} books."

    return "No changes in price."






