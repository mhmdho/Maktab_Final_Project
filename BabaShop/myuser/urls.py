from django.urls import path
from .views import SupplierLogin, SupplierLogout, SupplierPhoneVerify, SupplierRegister


urlpatterns = [
    path('supplier_login/', SupplierLogin.as_view(), name='supplier_login_url'),
    path('supplier_logout/', SupplierLogout.as_view(), name='supplier_logout_url'),
    path('supplier_register/', SupplierRegister.as_view(), name='supplier_register_url'),
    path('supplier/phone/verify/', SupplierPhoneVerify.as_view(), name='supplier_phone_verify_url'),
]
