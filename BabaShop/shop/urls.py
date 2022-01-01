from django.urls import path
from .views import OrdersList, ShopList


urlpatterns = [
    path('supplier_dashboard/', ShopList.as_view(), name='supplier_dashboard_url'),

]