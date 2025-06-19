from django import forms

from traveler.models import Traveler


class BaseTravelerForm(forms.ModelForm):

    class Meta:
        model = Traveler
        fields = '__all__'

class CreateTravelerForm(BaseTravelerForm):

    class Meta(BaseTravelerForm.Meta):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        exclude = ['about_me',]

        widgets = {
            'nickname': forms.TextInput(attrs={
                'placeholder': 'Enter a unique nickname...',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter a valid email address...',
            }),
            'country': forms.TextInput(attrs={
                'placeholder': 'Enter a country code like <BGR>...',
            }),

        }

class EditTravelerForm(BaseTravelerForm):

    class Meta(BaseTravelerForm.Meta):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        fields = '__all__'