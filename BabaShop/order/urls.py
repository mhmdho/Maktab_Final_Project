from django.urls import path
from .views import OrderList, OrderDetail


urlpatterns = [
    path('order_list/<slug:slug>/', OrderList.as_view(), name='order_list_url'),
    path('order_detail/<slug:slug>/<int:id>/', OrderDetail.as_view(), name='order_detail_url'),
]