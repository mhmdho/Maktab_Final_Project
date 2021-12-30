from django.shortcuts import render

from django.views.generic import TemplateView
# Create your views here.


class SupplierLogin(TemplateView):
    template_name = 'myuser\supplier_login.html'
    