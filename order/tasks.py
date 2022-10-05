import string
from datetime import datetime

from celery import shared_task
from django.db import transaction
from django.utils.crypto import get_random_string

from .models import Order


@shared_task
def generate_orders():
    with transaction.atomic():
        name = f"order_{get_random_string(10, string.ascii_letters)}"
        order_id = Order.objects.get_next_order_id_for_day(datetime.today())
        Order.objects.create(name=name, order_id=order_id)
    return 'Orders created!'
