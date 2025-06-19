from msilib.schema import ListView

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from traveler.forms import CreateTravelerForm, EditTravelerForm
from traveler.models import Traveler
from travelersHub.mixins import GetUserInContextMixin
from travelersHub.utils import get_traveler_obj


class CreateTravelerView(CreateView):
    model = Traveler
    form_class = CreateTravelerForm
    template_name = 'traveler/../templates/traveler/create-traveler.html'
    success_url = reverse_lazy('all-trips')


class EditTravelerView(GetUserInContextMixin, UpdateView):
    model = Traveler
    form_class = EditTravelerForm
    template_name = 'traveler/../templates/traveler/edit-traveler.html'
    success_url = reverse_lazy('details-traveler')

    def get_object(self, queryset=...):
        return get_traveler_obj()

class DetailsTravelerView(DetailView):
    model = Traveler
    template_name = 'traveler/../templates/traveler/details-traveler.html'

    def get_object(self, queryset = ...):
        return get_traveler_obj()

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['trips'] = self.object.trips.order_by('-start_date')
        return context

class DeleteTravelerView(DeleteView):
    template_name = 'traveler/../templates/traveler/delete-traveler.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset = ...):
        return get_traveler_obj()