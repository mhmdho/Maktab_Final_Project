from django.urls import path
from .views import CustomerRegister
from myuser.views import MyObtainTokenPairView, CustomerProfileView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('customer_register/', CustomerRegister.as_view(), name='customer_register_api'),
    path('customer_login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('customer_login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('customer_profile/', CustomerProfileView.as_view(), name='customer_profile_api'),
]
