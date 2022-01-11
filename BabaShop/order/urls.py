from django.urls import path
from .views import CreateOrderView, DeleteOrderView, OrderEditstatus, OrderList, PayOrderView, ProductList, OrderDetail


urlpatterns = [
    path('order_list/<slug:slug>/', OrderList.as_view(), name='order_list_url'),
    path('product_list/<slug:slug>/', ProductList.as_view(), name='product_list_url'),
    path('order_detail/<slug:slug>/<int:id>/', OrderDetail.as_view(), name='order_detail_url'),
    path('order_eidt_status/<slug:slug>/<int:pk>/', OrderEditstatus.as_view(), name='order_status_url'),

    # API/DRF
    path('api/shop/<slug:slug>/order/', CreateOrderView.as_view(), name='create_order_api'),
    path('api/shop/<slug:slug>/order/<int:pk>/', DeleteOrderView.as_view(), name='delete_order_api'),
    path('api/shop/<slug:slug>/order/<int:pk>/pay/', PayOrderView.as_view(), name='pay_order_api'),

]