from travelersHub.utils import get_traveler_obj


class GetUserInContextMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['traveler'] = get_traveler_obj()
        return context


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
