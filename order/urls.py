from django.urls import path
from .views import IndexView, GenerateOrdersView


urlpatterns = [
    path('', IndexView.as_view(), name="home"),
    path('order-generate', GenerateOrdersView.as_view(), name="order_generate"),
]
