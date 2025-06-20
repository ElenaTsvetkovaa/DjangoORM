from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from furryFunnies.mixins import AuthorObjectMixin, get_author_obj
from furryFunniesExam.posts import Post


class IndexView(AuthorObjectMixin, TemplateView):
    template_name = 'common/../templates/common/index.html'

class DashboardView(AuthorObjectMixin, ListView):
    template_name = 'common/../templates/common/dashboard.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        author = get_author_obj()
        return author.posts.all()


def dashboard(request):
    author = get_author_obj()
    posts = Post.objects.filter(author_id=author.pk)
    context = {
        'author': author,
        'posts': posts
    }
    return render(request, 'common/../templates/common/dashboard.html', context)
