from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from travelersHub.mixins import GetUserInContextMixin
from travelersHub.utils import get_traveler_obj
from travelersHubExam.trips.forms import CreateTripForm, EditTripForm, DeleteTripForm
from travelersHubExam.trips.models import Trip


class CreateTripView(GetUserInContextMixin, CreateView):
    model = Trip
    form_class = CreateTripForm
    template_name = 'trips/create-trip.html'
    success_url = reverse_lazy('all-trips')
    
    def form_valid(self, form):
        form.instance.traveler = get_traveler_obj()
        form.save()
        return super().form_valid(form)


class EditTripView(GetUserInContextMixin, UpdateView):
    model = Trip
    form_class = EditTripForm
    template_name = 'trips/edit-trip.html'
    success_url = reverse_lazy('all-trips')

class DetailsTripView(GetUserInContextMixin, DetailView):
    model = Trip
    template_name = 'trips/details-trip.html'


class DeleteTripView(GetUserInContextMixin, DeleteView):
    model = Trip
    form_class = DeleteTripForm
    template_name = 'trips/delete-trip.html'
    success_url = reverse_lazy('all-trips')

    def form_invalid(self, form):
        return self.form_valid(form)

    def get_initial(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        trip  =self.model.objects.get(pk=pk)
        return trip.__dict__