from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
# from django.contrib.auth.mixins import LoginRequiredMixin
from myuser.auth import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import CreateView
from shop.models import Shop
from myuser.forms import SupplierRegisterForm,\
                    SupplierLoginForm, SupplierPhoneVerifyForm
from .utils import OTP
from myuser.tasks import kavenegar_otp, smsir_otp


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


class SupplierPhoneVerify(LoginRequiredMixin, View):
    """
    Takes otp and verify supplier phone if
    the inputed otp be correct.
    """
    template_name = 'forms/supplier_phone_verify.html'
    login_url = '/myuser/supplier_login/'
    form_class = SupplierPhoneVerifyForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_phone_verified:
            messages.info(request, "You have verified your phone before." )
            return redirect('supplier_login_url')
        return render(request, self.template_name, {'form': self.form_class})
    
    def post(self, request, *args, **kwargs):
        otp = OTP(self.request.user.phone)
        if otp.verify_token(self.request.POST['otp']):
            self.request.user.is_phone_verified = True
            self.request.user.save()
            messages.success(request, "Phone verified successfully." )
            return redirect('supplier_login_url')
        messages.error(request, "Expired or wrong code." )
        return redirect('supplier_phone_verify_url')


class SupplierPhoneOtp(View):
    """
    Generate otp to verify supplier phone.
    """
    def get(self, request, *args, **kwargs):
        phone = self.request.user.phone
        otp = OTP(phone)
        smsir_otp(settings.PHONE, otp.generate_token())
        # kavenegar_otp(phone, otp)
        show_phone = phone[0:5] + '****' + phone[9:]
        messages.success(request, f"SMS sent to {show_phone}" )
        messages.success(request, f" - [{otp.generate_token()}]" )
        return redirect('supplier_phone_verify_url')
