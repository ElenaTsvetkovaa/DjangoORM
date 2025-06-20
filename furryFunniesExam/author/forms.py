from django import forms

from author.models import Author


class BaseAuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = '__all__'

class CreateAuthorForm(BaseAuthorForm):

    class Meta(BaseAuthorForm.Meta):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        fields = ['first_name', 'last_name', 'passcode', 'pets_number']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter your first name...',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter your last name...',
            }),
            'passcode': forms.PasswordInput(attrs={
                'placeholder': 'Enter 6 digits...',
            }),
            'pets_number': forms.NumberInput(attrs={
                'placeholder': 'Enter the number of your pets...',
            }),
        }

class EditAuthorForm(BaseAuthorForm):
    pass
