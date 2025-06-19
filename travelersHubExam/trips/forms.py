from django import forms

from travelersHubExam.trips.models import Trip


class BaseTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        exclude = ['traveler', ]


class CreateTripForm(BaseTripForm):
    class Meta(BaseTripForm.Meta):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        labels = {
            'start_date': 'Started on',
            'image_url': 'Image URL'
        }

        widgets = {
            'destination': forms.TextInput(attrs={
                'placeholder': 'Enter a short destination note...',
            }),
            'summary': forms.Textarea(attrs={
                'placeholder': 'Share your exciting moments... ',
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'image_url': forms.URLInput(attrs={
                'placeholder': 'An optional image URL...'
            })
        }



class EditTripForm(BaseTripForm):
    ...

class DeleteTripForm(BaseTripForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs['readonly'] = True
            self.fields[field_name].widget.attrs['disabled'] = True
