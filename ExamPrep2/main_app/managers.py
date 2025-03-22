from django.db.models import manager
from django.db.models.aggregates import Count


class ProfileManger(manager.Manager):

    def get_regular_customers(self):

        return (self.prefetch_related('orders')
                .annotate(orders_count=Count('orders'))
                .filter(orders_count__gt=2)
                .order_by('-orders_count')
                )


