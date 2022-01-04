from django.urls import path
from .views import CreateProduct, CreateShop, DeleteShop, ShopDetail, ShopList, EditShop


urlpatterns = [
    path('supplier_dashboard/', ShopList.as_view(), name='supplier_dashboard_url'),
    path('create_shop/', CreateShop.as_view(), name='create_shop_url'),
    path('shop_detail/<slug:slug>/', ShopDetail.as_view(), name='shop_detail_url'),
    path('edit_shop/<slug:slug>/', EditShop.as_view(), name='edit_shop_url'),
    path('delete_shop/<slug:slug>/', DeleteShop.as_view(), name='delete_shop_url'),

    path('create_product/<slug:slug>/', CreateProduct.as_view(), name='create_product_url'),

]