from author.models import Author


def get_author_obj():
    return Author.objects.first()



class AuthorObjectMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = get_author_obj()
        return context

