from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from myuser.models import CustomUser
from shop.models import Shop
from myuser.forms import SupplierRegisterForm

# Create your views here.


class SupplierLogin(View):
    template_name = 'myuser/supplier_login.html'

    def get(self, request):
        if request.user.is_authenticated:
            shop = Shop.Undeleted.filter(supplier=self.request.user).first()
            if shop:
                return redirect('shop_detail_url', slug=shop.slug)
            return redirect('create_shop_url')


        return render(request, 'myuser/supplier_login.html')
    
    def post(self, request):
        user = authenticate(phone=request.POST.get('username'), password=request.POST.get('pass'))
        if user is not None:
            if user.is_supplier and user.is_active:
                login(request, user)
                shop = Shop.Undeleted.filter(supplier=self.request.user).first()
                if shop:
                    return redirect('shop_detail_url', slug=shop.slug)
                return redirect('create_shop_url')
            return HttpResponse("You are not a supplier.")

        return render(request, 'myuser/supplier_login.html')


class SupplierLogout(View):
    def get(self, request):
        logout(request)
        return render(request, 'myuser/supplier_login.html')


class SupplierRegister(CreateView):
    template_name = 'myuser/supplier_register.html'
    success_url = 'myuser/supplier_login.html'
    form_class = SupplierRegisterForm
    success_message = "You are registered successfully"

    def get(self, request):
        if request.user.is_authenticated:
            slug = Shop.Undeleted.filter(supplier=self.request.user).first().slug
            return redirect('shop_detail_url', slug=slug)
        form = SupplierRegisterForm()
        return render(request, 'forms/supplier_register.html',{'form': form})
    
    def post(self, request):
        form = SupplierRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful." )
            return redirect('supplier_login_url')

        return render(request, 'myuser/supplier_login.html')
