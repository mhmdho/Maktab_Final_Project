from django.urls import path
from .views_api import CustomerPhoneVerify, CustomerRegister, MyObtainTokenPairView,\
                    CustomerProfileView, TokenRefreshView2


urlpatterns = [
    path('customer_register/', CustomerRegister.as_view(), name='customer_register_api'),
    path('customer_login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('customer_login/refresh/', TokenRefreshView2.as_view(), name='token_refresh'),
    path('customer_profile/', CustomerProfileView.as_view(), name='customer_profile_api'),
    path('customer/phone/verify/', CustomerPhoneVerify.as_view(), name='customer_phone_verify_api'),
]
