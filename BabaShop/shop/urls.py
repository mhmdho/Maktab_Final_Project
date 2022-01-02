from django.urls import path
from .views import CreateShop, ShopList


urlpatterns = [
    path('supplier_dashboard/', ShopList.as_view(), name='supplier_dashboard_url'),
    path('create_shop/', CreateShop.as_view(), name='create_shop_url'),

]