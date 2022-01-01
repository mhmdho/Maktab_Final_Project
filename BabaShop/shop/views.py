from django.shortcuts import render
from django.views.generic import ListView

from shop.models import Shop

# Create your views here.


class OrdersList(ListView):
    model = Shop
    template_name = 'shop/supplier_dashboard.html'

    def get_queryset(self):
        return Shop.Undeleted.filter(supplier=self.request.user
                            ).order_by('id')
