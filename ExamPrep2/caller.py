import os
import django
from django.db.models import Q, F, Case, When, Value
from django.db.models.aggregates import Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Product, Profile, Order
from populate_db import populate_model_with_data

# Import your models here

def populate_db():
    populate_model_with_data(Profile, 20)
    populate_model_with_data(Product, 20)
    populate_model_with_data(Order, 20)


def get_profiles(search_string=None):

    if search_string is not None:
        profiles = Profile.objects.prefetch_related('orders').filter(
            Q(full_name__icontains=search_string)
                    |
            Q(email__icontains=search_string)
                    |
            Q(phone_number__icontains=search_string)
        ).annotate(num_of_orders=Count('orders')).order_by('full_name')

        return '\n'.join(
            [f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.num_of_orders}"
             for p in profiles]
        )
    return ''


def get_loyal_profiles():

    return '\n'.join([
        f"Profile: {p.full_name}, orders: {p.orders_count}"
        for p in Profile.objects.get_regular_customers()
    ])


def get_last_sold_products():

    last_order = Order.objects.prefetch_related('products').order_by('-creation_date', 'products__name').first()

    if last_order is None or not last_order.products.exists():
        return ''

    return f"Last sold products: {', '.join([p.name for p in last_order.products.all()])}"


def get_top_products():

    products = (Product.objects
                .prefetch_related('orders')
                .annotate(orders_count=Count('orders'))
                .filter(orders_count__gt=0)
                .order_by('-orders_count','name')
                )

    if not products.exists():
        return ''

    return "Top products:\n" + '\n'.join([
        f"{p.name}, sold {p.orders_count} times" for p in products][:5])


def apply_discounts():

    discounted_products_count = (Order.objects
                                 .prefetch_related('products')
                                 .annotate(products_count=Count('products'))
                                 .filter(products_count__gt=2, is_completed=False)
                                 .update(total_price=F('total_price') * 0.90)
                                 )

    return f"Discount applied to {discounted_products_count} orders."

def complete_order():

    order = (Order.objects.prefetch_related('products')
             .order_by('creation_date')
             .filter(is_completed=False)
             .first()
             )

    if order is not None:
        order.is_completed = True
        order.save()
        order.products.update(
            in_stock=F('in_stock') - 1,
            is_available=Case(
                When(in_stock=1, then=Value(False)),
                default=F('is_available')
            )
        )
        return "Order has been completed!"
    return ''






