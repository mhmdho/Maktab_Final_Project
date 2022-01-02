from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from shop.models import Shop
from shop.forms import CreateShopForm

# Create your views here.


class ShopList(ListView):
    model = Shop
    template_name = 'shop/supplier_dashboard.html'

    def get_queryset(self):
        return Shop.Undeleted.filter(supplier=self.request.user).order_by('id')


class ShopDetail(DetailView):
    model = Shop
    template_name = 'shop/shop_detail.html'

    def get_queryset(self, *arg, **kwargs):
        return Shop.Undeleted.filter(slug=self.kwargs['slug'], supplier=self.request.user)


class CreateShop(LoginRequiredMixin,View):
    template_name = 'shop/create_shop.html'
    form_class = CreateShopForm

    def get(self, request):
        form = CreateShopForm()
        return render(request, 'shop/create_shop.html',{'form': form})

    def post(self, request):
        notconfirmed = Shop.Undeleted.filter(is_confirmed=False ,supplier=request.user).count()
        if notconfirmed != 0:
            return redirect('supplier_dashboard_url')
        form = CreateShopForm(request.POST)
        if form.is_valid():
            form.instance.supplier = request.user
            print(form)
            form.save()
            return redirect('supplier_dashboard_url')
    