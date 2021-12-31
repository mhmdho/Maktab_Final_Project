from django.http.response import HttpResponse
from django.shortcuts import render

from django.views.generic import View
from django.contrib.auth import authenticate, login

# Create your views here.


class SupplierLogin(View):
    template_name = 'myuser/supplier_login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse('dash')

        return render(request, 'myuser/supplier_login.html')
    
    def post(self, request):
        print(request.POST.get('username'))
        print(request.POST.get('pass'))
        user = authenticate(phone=request.POST.get('username'), password=request.POST.get('pass'))
        if user is not None:
            login(request, user)
            return HttpResponse('log')

        return render(request, 'myuser/supplier_login.html')
