from django.urls import path
from .views import SupplierLogin, SupplierLogout, SupplierPhoneOtp,\
    SupplierPhoneVerify, SupplierRegister, SupplierLoginOtp


urlpatterns = [
    path('supplier_login/', SupplierLogin.as_view(), name='supplier_login_url'),
    path('supplier_logout/', SupplierLogout.as_view(), name='supplier_logout_url'),
    path('supplier_register/', SupplierRegister.as_view(), name='supplier_register_url'),
    path('supplier/phone/verify/', SupplierPhoneVerify.as_view(), name='supplier_phone_verify_url'),
    path('supplier/phone/otp/', SupplierPhoneOtp.as_view(), name='supplier_phone_otp_url'),
    path('supplier/login/otp/', SupplierLoginOtp.as_view(), name='supplier_login_otp_url'),
]
