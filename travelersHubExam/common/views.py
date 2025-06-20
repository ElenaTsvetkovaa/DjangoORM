
from django.views.generic import TemplateView, ListView

from travelersHub.mixins import GetUserInContextMixin
from travelersHubExam.trips.models import Trip


class IndexView(GetUserInContextMixin, TemplateView):
    template_name = 'common/../templates/common/index.html'



class AllTripsView(GetUserInContextMixin, ListView):
    template_name = 'common/../templates/common/all-trips.html'
    model = Trip
    context_object_name = 'trips'

    def get_ordering(self):
        self.ordering = '-start_date'
        return self.ordering
