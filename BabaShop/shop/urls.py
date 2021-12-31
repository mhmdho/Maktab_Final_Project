from django.urls import path
from .views import OrdersList


urlpatterns = [
    path('supplier_dashboard/', OrdersList.as_view(), name='supplier_dashboard_url'),

]