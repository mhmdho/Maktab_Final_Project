from django.urls import path
from .views import OrderList


urlpatterns = [
    path('order_list/<slug:slug>/', OrderList.as_view(), name='order_list_url'),
]