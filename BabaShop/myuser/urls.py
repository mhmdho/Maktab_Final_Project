from django.urls import path
from .views import SupplierLogin, SupplierLogout, SupplierRegister, CustomerRegister

# API / DRF
from myuser.views import MyObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('supplier_login/', SupplierLogin.as_view(), name='supplier_login_url'),
    path('supplier_logout/', SupplierLogout.as_view(), name='supplier_logout_url'),
    path('supplier_register/', SupplierRegister.as_view(), name='supplier_register_url'),
    
    # API/DRF
    path('api/customer_register/', CustomerRegister.as_view(), name='customer_register_api'),
    path('api/customer_login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/customer_login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
