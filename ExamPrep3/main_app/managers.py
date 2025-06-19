from django.db.models import manager, Count


class HouseManager(manager.Manager):

    def get_houses_by_dragons_count(self):

        return (self.prefetch_related('dragons')
                .annotate(dragons_count=Count('dragons'))
                .filter('-dragons_count', 'name'))






