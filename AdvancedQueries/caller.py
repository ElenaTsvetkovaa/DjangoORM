import os
import django
from django.db import connection

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import OrderProduct
# # Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct
from django.db.models import Count, Max, Avg, Sum, Min, F, Q


def product_quantity_ordered():

    products = (OrderProduct.objects
                .filter(quantity__gte=1, product__is_available=True)
                .values(product_name=F('product__name'))
                .annotate(total_quantity=Sum('quantity'))
                .order_by('-total_quantity'))
    res = []

    for p in products:
        res.append(f"Quantity ordered of {p['product_name']}: {p['total_quantity']}")

    return '\n'.join(res)

def ordered_products_per_customer():
    res = []
    orders = Order.objects.prefetch_related("orderproduct_set").order_by("id")

    for order in orders:
        res.append(f"Order ID: {order.id}, Customer: {order.customer.username}")
        for ordered_products in order.orderproduct_set.all():
            res.append(f"- Product: {ordered_products.product.name}, Category: {ordered_products.product.category.name}")

    return '\n'.join(res)

def filter_products():
    filtered_products = Product.objects.filter(Q(is_available=True) & Q(price__gt=3.00)).order_by("-price", "name")
    res = []
    for p in filtered_products:
        res.append(f"{p.name}: {p.price}lv.")

    return '\n'.join(res)

def give_discount():
    (Product.objects
    .filter(Q(is_available=True) & Q(price__gt=3.00))
    .update(price=F("price") * 0.7))

    filtered_products = (Product.objects
                         .filter(is_available=True)
                         .order_by("-price", "name"))

    return '\n'.join([f"{p.name}: {p.price}lv." for p in filtered_products])

print(give_discount())