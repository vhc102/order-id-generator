from datetime import date, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.db.utils import IntegrityError


class OrderManager(models.Manager):
    @transaction.atomic()
    def get_next_order_id_for_day(self, date_time: datetime):
        try:
            with transaction.atomic():
                order_id = self._get_or_create_order_id_for_day(date_time)
                order_id = self._update_order_id(order_id)
                return order_id
        except IntegrityError:
            order_id = self._get_order_id_for_day(date_time)
            order_id = self._update_order_id(order_id)
            return order_id

    def _get_or_create_order_id_for_day(self, date_time: datetime):
        try:
            return self._get_order_id_for_day(date_time)
        except ObjectDoesNotExist:
            return f"{date.today().strftime('%Y%m%d')}-{0:05}"

    def _get_order_id_for_day(self, date_time: datetime):
        return self.get_queryset().select_for_update(of=("self",)).filter(date_time__date=date_time).latest(
            'date_time').order_id

    def _update_order_id(self, order_id):
        print(order_id)
        return f"{date.today().strftime('%Y%m%d')}-{(int(order_id.split('-')[1]) + 1):05}"


class Order(models.Model):
    name = models.CharField(max_length=100)
    order_id = models.CharField(max_length=200, unique=True)
    date_time = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id
