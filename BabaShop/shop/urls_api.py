from django.urls import path
from .views_api import ShopListView, ShopProductsView, ShopTypesView


urlpatterns = [
    path('confirmed/', ShopListView.as_view(), name='shop_confirmed_api'),
    path('type/', ShopTypesView.as_view(), name='shop_types_api'),
    path('<slug:slug>/product/', ShopProductsView.as_view(), name='shop_products_api'),
]