from django.urls import path
from .views import SupplierLogin, SupplierLogout


urlpatterns = [
    path('supplier_login/', SupplierLogin.as_view(), name='supplier_login_url'),
    path('supplier_logout/', SupplierLogout.as_view(), name='supplier_logout_url'),

]
