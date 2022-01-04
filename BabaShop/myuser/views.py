from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from django.views.generic import View
from django.contrib.auth import authenticate, login, logout

from shop.models import Shop

# Create your views here.


class SupplierLogin(View):
    template_name = 'myuser/supplier_login.html'

    def get(self, request):
        if request.user.is_authenticated:
            slug = Shop.Undeleted.filter(supplier=self.request.user).first().slug
            return redirect('shop_detail_url', slug=slug)

        return render(request, 'myuser/supplier_login.html')
    
    def post(self, request):
        user = authenticate(phone=request.POST.get('username'), password=request.POST.get('pass'))
        if user is not None:
            if user.is_supplier:
                login(request, user)
                slug = Shop.Undeleted.filter(supplier=self.request.user).first().slug
                return redirect('shop_detail_url', slug=slug)
            return HttpResponse("You are not a supplier.")

        return render(request, 'myuser/supplier_login.html')


class SupplierLogout(View):
    def get(self, request):
        logout(request)
        return render(request, 'myuser/supplier_login.html')
