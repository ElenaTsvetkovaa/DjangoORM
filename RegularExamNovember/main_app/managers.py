from django.db.models import manager, Count


class AuthorManager(manager.Manager):

    def get_authors_by_article_count(self):
        return self.annotate(
            articles_count=Count('articles')
        ).order_by('-articles_count', 'email')





