from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from author.forms import CreateAuthorForm, EditAuthorForm
from author.models import Author
from furryFunnies.mixins import get_author_obj
from furryFunniesExam.posts import Post


class CreateAuthorView(CreateView):
    model = Author
    form_class = CreateAuthorForm
    success_url = reverse_lazy('dashboard')
    template_name = 'author/../templates/author/create-author.html'


class EditAuthorView(UpdateView):
    model = Author
    form_class = EditAuthorForm
    template_name = 'author/../templates/author/edit-author.html'
    success_url = reverse_lazy('details-author')

    def get_object(self, queryset = ...):
        return get_author_obj()


class DetailsAuthorView(DetailView):
    model = Author
    template_name = 'author/../templates/author/details-author.html'

    def get_object(self, queryset = ...):
        return get_author_obj()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.object).order_by('-updated_at')
        return context


class DeleteAuthorView(DeleteView):
    model = Author
    template_name = 'author/../templates/author/delete-author.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset = ...):
        return get_author_obj()
