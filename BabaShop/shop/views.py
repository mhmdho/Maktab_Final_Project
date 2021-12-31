from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class OrdersList(TemplateView):
    template_name = 'shop/supplier_dashboard.html'

