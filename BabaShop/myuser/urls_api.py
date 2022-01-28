from django.urls import path
from .views_api import CustomerLoginOtp, CustomerPhoneVerify, CustomerRegister,\
                    MyObtainTokenPairView, CustomerProfileView, TokenRefreshView2


urlpatterns = [
    path('customer/register/', CustomerRegister.as_view(), name='customer_register_api'),
    path('customer/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('customer/login/refresh/', TokenRefreshView2.as_view(), name='token_refresh'),
    path('customer/profile/', CustomerProfileView.as_view(), name='customer_profile_api'),
    path('customer/phone/verify/', CustomerPhoneVerify.as_view(), name='customer_phone_verify_api'),
    path('customer/login/otp/', CustomerLoginOtp.as_view(), name='supplier_login_otp_api'),
]
