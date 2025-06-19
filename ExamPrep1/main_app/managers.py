from django.db.models import manager, Count


class DirectorManager(manager.Manager):

    def get_directors_by_movies_count(self):

        return (self.annotate(movies_count=Count('movies'))
                .order_by('-movies_count', 'full_name')
                )

