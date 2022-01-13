from django.urls import path
from .views import ShopListView, ShopProductsView, ShopTypesView


urlpatterns = [
    path('shop/', ShopListView.as_view(), name='shop_list_api'),
    path('shop_types/', ShopTypesView.as_view(), name='shop_types_api'),
    path('shop/<slug:slug>/product/', ShopProductsView.as_view(), name='shop_products_api'),
]