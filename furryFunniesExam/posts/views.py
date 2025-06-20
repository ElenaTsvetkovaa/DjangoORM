from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from furryFunnies.mixins import get_author_obj, AuthorObjectMixin
from furryFunniesExam.posts.forms import CreatePostForm, EditPostForm, DeletePostForm
from furryFunniesExam.posts.models import Post


class CreatePostView(AuthorObjectMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    success_url = reverse_lazy('dashboard')
    template_name = 'posts/create-post.html'
    
    def form_valid(self, form):
        form.instance.author = get_author_obj()
        form.save()
        return super().form_valid(form)
    

class EditPostView(AuthorObjectMixin, UpdateView):
    model = Post
    form_class = EditPostForm
    pk_url_kwarg = 'id'
    template_name = 'posts/edit-post.html'
    success_url = reverse_lazy('dashboard')

class DetailsPostView(AuthorObjectMixin, DetailView):
    model = Post
    pk_url_kwarg = 'id'
    template_name = 'posts/details-post.html'


class DeletePostView(AuthorObjectMixin, DeleteView):
    model = Post
    form_class = DeletePostForm
    pk_url_kwarg = 'id'
    template_name = 'posts/delete-post.html'
    success_url = reverse_lazy('dashboard')

    def form_invalid(self, form):
        return self.form_valid(form)

    def get_initial(self):
        return self.object.__dict__


