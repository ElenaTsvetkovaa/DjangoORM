from django import forms
from furryFunniesExam.posts.models import Post


class BasePostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['author', 'updated_at']


class CreatePostForm(BasePostForm):

    class Meta(BasePostForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    labels = {
        'image_url': 'Post Image URL'
    }

    widgets = {
        'title': forms.TextInput(attrs={
            'placeholder': 'Put an attractive and unique title...'
        }),
        'content': forms.Textarea(attrs={
            'placeholder': 'Share some interesting facts about your adorable pets...'
        })
    }


class EditPostForm(BasePostForm):
    ...


class DeletePostForm(BasePostForm):

    class Meta(BasePostForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs['readonly'] = True
            self.fields[field_name].widget.attrs['disabled'] = True


