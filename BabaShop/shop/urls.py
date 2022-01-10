from django.urls import path
from .views import CreateProduct, EditProduct, CreateShop, DeleteShop, ShopDetail, EditShop,\
                ShopListView


urlpatterns = [
    path('create_shop/', CreateShop.as_view(), name='create_shop_url'),
    path('shop_detail/<slug:slug>/', ShopDetail.as_view(), name='shop_detail_url'),
    path('edit_shop/<slug:slug>/', EditShop.as_view(), name='edit_shop_url'),
    path('delete_shop/<slug:slug>/', DeleteShop.as_view(), name='delete_shop_url'),
    path('create_product/<slug:slug>/', CreateProduct.as_view(), name='create_product_url'),
    path('edit_product/<slug:slug>/', EditProduct.as_view(), name='edit_product_url'),

    # API/DRF
    path('api/shop_list/', ShopListView.as_view(), name='shop_list_api'),
]