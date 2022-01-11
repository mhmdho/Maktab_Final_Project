from django.urls import path
from .views import CreateOrderView, OrderEditstatus, OrderList, ProductList, OrderDetail


urlpatterns = [
    path('order_list/<slug:slug>/', OrderList.as_view(), name='order_list_url'),
    path('product_list/<slug:slug>/', ProductList.as_view(), name='product_list_url'),
    path('order_detail/<slug:slug>/<int:id>/', OrderDetail.as_view(), name='order_detail_url'),
    path('order_eidt_status/<slug:slug>/<int:pk>/', OrderEditstatus.as_view(), name='order_status_url'),

    # API/DRF
    path('api/create_order/', CreateOrderView.as_view(), name='create_order_api'),
]