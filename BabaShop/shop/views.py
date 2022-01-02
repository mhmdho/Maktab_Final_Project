from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from order.models import Order

from shop.models import Shop

# Create your views here.


class ShopList(ListView):
    model = Shop
    template_name = 'shop/supplier_dashboard.html'

    def get_queryset(self):
        return Shop.Undeleted.filter(supplier=self.request.user).order_by('id')


class CreateShop(TemplateView):
    template_name = 'shop/create_shop.html'
    