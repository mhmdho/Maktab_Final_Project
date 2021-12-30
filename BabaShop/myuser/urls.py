from django.urls import path
from .views import SupplierLogin


urlpatterns = [
    path('supplier_login/', SupplierLogin.as_view(), name='supplier_login_url'),

]
