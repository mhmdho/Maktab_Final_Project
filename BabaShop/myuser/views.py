from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from myuser.models import CustomUser
from myuser.forms import SupplierPhoneVerifyForm
from shop.models import Shop
from myuser.forms import SupplierRegisterForm, SupplierLoginForm
from django.contrib.auth.views import LoginView, LogoutView
from .utils import OTP
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.


class SupplierLogin(LoginView):
    """
    Takes a set of supplier credentials and prove
    the authentication of those credentials and login.
    """
    template_name = 'forms/supplier_login.html'
    form_class = SupplierLoginForm

    def get(self, request):
        if request.user.is_authenticated:
            messages.success(request, "Your are logged in before." )
            shop = Shop.Undeleted.filter(supplier=self.request.user).first()
            if shop:
                return redirect('shop_detail_url', slug=shop.slug)
            return redirect('create_shop_url')
        form = SupplierLoginForm()
        return render(request, 'forms/supplier_login.html', {'form': form})
    
    def post(self, request):
        form = SupplierLoginForm(request.POST)
        print(form)
        if form.is_valid():
            user = authenticate(phone=form.cleaned_data['phone'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_supplier and user.is_active:
                        login(request, user)
                        shop = Shop.Undeleted.filter(supplier=self.request.user).first()
                        messages.success(request, "Login successfully." )
                        if shop:
                            return redirect('shop_detail_url', slug=shop.slug)
                        return redirect('create_shop_url')
                messages.info(request, "You are not a supplier or your acount suspended." )
                return redirect('supplier_login_url')

        messages.error(request, "Unsuccessful login. Invalid user" )
        return redirect('supplier_login_url')


class SupplierLogout(LogoutView):
    """
    Loguot the authenticated supplier.
    """
    # next_page = 'supplier_login_url'
    def get(self, request):
        logout(request)
        messages.info(request, "logout successfully." )
        return redirect('supplier_login_url')


class SupplierRegister(CreateView):
    """
    Takes a set of supplier credentials and register.
    """
    template_name = 'myuser/supplier_register.html'
    success_url = 'myuser/supplier_login.html'
    form_class = SupplierRegisterForm
    success_message = "You are registered successfully"

    def get(self, request):
        if request.user.is_authenticated:
            slug = Shop.Undeleted.filter(supplier=self.request.user).first().slug
            messages.success(request, "Your are loged in before." )
            return redirect('shop_detail_url', slug=slug)
        form = SupplierRegisterForm()
        return render(request, 'forms/supplier_register.html',{'form': form})
    
    def post(self, request):
        form = SupplierRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration was successful." )
            return redirect('supplier_login_url')
        messages.error(request, "Invalid Input!." )
        return redirect('supplier_register_url')


class SupplierPhoneVerify(LoginRequiredMixin, UpdateView):
    template_name = 'forms/supplier_phone_verify.html'
    login_url = '/myuser/supplier_login/'
    form_class = SupplierPhoneVerifyForm

    def get(self, request):
        supplier = CustomUser.objects.filter(pk=self.request.user.id).first()
        if supplier.is_phone_verified:
            messages.info(request, "You have verified your phone before." )
            return redirect('supplier_login_url')
        return render(request, self.template_name, {'form': self.form_class})
    
    def post(self, request, *args, **kwargs):
        supplier = CustomUser.objects.filter(pk=self.request.user.id).first()
        otp = OTP(supplier.phone)
        if otp.verify_token(self.request.POST['otp']):
            supplier.is_phone_verified = True
            supplier.save()
            messages.success(request, "Phone verified successfully." )
            return redirect('supplier_login_url')
        messages.error(request, "Expired or wrong code." )
        return redirect('supplier_phone_verify_url')


class SupplierPhoneOtp(View):
    model = CustomUser
    
    def get(self, request, *args, **kwargs):
        obj = self.model.objects.filter(pk=self.request.user.id).first()
        otp = OTP(obj.phone)
        messages.success(request, f"OTP: {otp.generate_token()}" )
        return redirect('supplier_phone_verify_url')
