from traveler.models import Traveler


def get_traveler_obj():
    return Traveler.objects.first()
