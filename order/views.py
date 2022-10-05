from datetime import datetime

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from order.tasks import generate_orders
from .forms import OrderForm, GenerateOrdersForm
from .models import Order


class IndexView(FormView):
    form_class = OrderForm
    template_name = "order/index.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.order_id = Order.objects.get_next_order_id_for_day(datetime.today())
        form.save()
        return super(IndexView, self).form_valid(form)


class GenerateOrdersView(FormView):
    template_name = 'order/generate_orders.html'
    form_class = GenerateOrdersForm
    success_url = reverse_lazy("order_generate")

    def form_valid(self, form):
        for _ in range(form.cleaned_data.get("total")):
            generate_orders.delay()
        messages.success(self.request, 'We are generating your orders! Wait a moment and refresh this page.')
        return super(GenerateOrdersView, self).form_valid(form)

