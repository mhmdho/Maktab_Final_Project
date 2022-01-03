from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404

from shop.models import Shop, Product
from shop.forms import CreateShopForm, CreateProductForm

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.Undeleted.filter(supplier=self.request.user).order_by('id')
        context['product_list'] = Product.objects.filter(shop=context['shop'])
        context['product_count'] = Product.objects.filter(shop=context['shop']).count()
        context['active_product_count'] = context['product_list'].filter(is_active=True).count()
        total_product_stock = 0
        for pro in context['product_list'].filter(is_active=True):
            total_product_stock += pro.stock
        context['total_product_stock'] = total_product_stock
        return context


class CreateShop(LoginRequiredMixin,View):
    template_name = 'forms/create_shop.html'
    form_class = CreateShopForm

    def get(self, request):
        form = CreateShopForm()
        return render(request, 'forms/create_shop.html',{'form': form})

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
    

class EditShop(LoginRequiredMixin,UpdateView):
    template_name = 'shop/edit_shop.html'
    model = Shop
    form_class = CreateShopForm

    def get_success_url(self):
        slug = self.kwargs["slug"]
        return reverse("shop_detail_url", kwargs={"slug": slug})

    def post(self, request, *args, **kwargs):
        shop = (Shop.Undeleted.filter(slug=self.kwargs['slug']))
        shop.update(is_confirmed = False)
        return redirect("shop_detail_url", self.kwargs["slug"])


class DeleteShop(LoginRequiredMixin,UpdateView):
    model = Shop

    def get(self, request, *args, **kwargs):
        shop = (Shop.Undeleted.filter(slug=self.kwargs['slug']))
        shop.update(is_deleted=True, is_confirmed=True)
        return redirect(reverse('supplier_dashboard_url'))


class CreateProduct(LoginRequiredMixin, View):
    template_name = 'forms/create_product.html'
    form_class = CreateProductForm

    def get(self, request):
        form = CreateProductForm()
        return render(request, 'forms/create_Product.html',{'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateShopForm(request.POST)
        if form.is_valid():
            form.instance.shop = self.kwargs
            form.save()
            return redirect("shop_detail_url", self.kwargs["slug"])
