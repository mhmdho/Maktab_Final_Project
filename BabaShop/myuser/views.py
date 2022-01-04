from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from django.views.generic import View
from django.contrib.auth import authenticate, login

# Create your views here.


class SupplierLogin(View):
    template_name = 'myuser/supplier_login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('supplier_dashboard_url')

        return render(request, 'myuser/supplier_login.html')
    
    def post(self, request):
        user = authenticate(phone=request.POST.get('username'), password=request.POST.get('pass'))
        if user is not None:
            login(request, user)
            return redirect('supplier_dashboard_url')

        return render(request, 'myuser/supplier_login.html')
