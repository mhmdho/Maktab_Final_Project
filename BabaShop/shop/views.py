from django.contrib import messages
from django.db.models.aggregates import Count
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.edit import CreateView
from shop.models import Image, Shop, Product
from order.models import Order
from shop.forms import CreateShopForm, CreateProductForm


# Create your views here.


class ShopDetail(LoginRequiredMixin, DetailView):
    template_name = 'shop/shop_detail.html'
    login_url = '/myuser/supplier_login/'
    model = Shop

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
        context['order_list'] = Order.objects.filter(orderitem__product__shop__slug=self.kwargs['slug']).annotate(Count('id')).order_by('-created_at')
        context['order_count'] = context['order_list'].count()
        context['customer_count'] = Order.objects.filter(orderitem__product__shop__slug=self.kwargs['slug']).values('customer').annotate(Count('customer_id')).order_by().count()
        orders_value  = 0
        for ord in context['order_list']:
            orders_value += ord.total_price
            context['shop_order_total_price'] = ord.shop_order_total_price(self.kwargs['slug'])
            context['shop_order_total_quantity'] = ord.shop_order_total_quantity(self.kwargs['slug'])
        context['orders_value'] = orders_value

        return context


class CreateShop(LoginRequiredMixin, CreateView, ContextMixin):
    template_name = 'forms/create_shop.html'
    login_url = '/myuser/supplier_login/'
    form_class = CreateShopForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.Undeleted.filter(supplier=self.request.user).order_by('id')
        return context
    
    def post(self, request):
        not_confirmed = Shop.Undeleted.filter(is_confirmed=False ,supplier=request.user).first()
        if not_confirmed:
            messages.error(request, "You have unconfirmed shop." )
            return redirect('shop_detail_url', slug=not_confirmed.slug)
        form = CreateShopForm(request.POST)
        if form.is_valid():
            form.instance.supplier = request.user
            print(form)
            form.save()
            shop = Shop.Undeleted.filter(supplier=request.user).last()
            return redirect('shop_detail_url', shop.slug)
    

class EditShop(LoginRequiredMixin,UpdateView):
    template_name = 'shop/edit_shop.html'
    login_url = '/myuser/supplier_login/'
    model = Shop
    form_class = CreateShopForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.Undeleted.filter(supplier=self.request.user).order_by('id')
        return context

    def get_success_url(self):
        slug = self.kwargs["slug"]
        return reverse("shop_detail_url", kwargs={"slug": slug})

    def post(self, request, *args, **kwargs):
        shop = Shop.Undeleted.filter(slug=self.kwargs['slug'])
        shop.update(is_confirmed = False)
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class EditProduct(LoginRequiredMixin,UpdateView):
    template_name = 'shop/edit_product.html'
    login_url = '/myuser/supplier_login/'
    model = Shop
    form_class = CreateProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.Undeleted.filter(supplier=self.request.user).order_by('id')
        return context

    def get_success_url(self):
        slug = self.kwargs["slug"]
        return reverse("shop_detail_url", kwargs={"slug": slug})

    def post(self, request, *args, **kwargs):
        # shop = Shop.Undeleted.filter(slug=self.kwargs['slug'])
        # shop.update(is_confirmed = False)
        # self.object = self.get_object()
        # return super().post(request, *args, **kwargs)
        form = CreateProductForm(request.POST, request.FILES)
        form.instance.shop = Shop.Undeleted.get(slug=self.kwargs['slug'])
        if form.is_valid():
            form.save()
            for i in range(1,5):
                if form.cleaned_data[f'image{i}'] is not None:
                    Image.objects.create(image=form.cleaned_data[f'image{i}'], product=form.instance)
            
            messages.success(request, "New product created." )
            return redirect("shop_detail_url", self.kwargs["slug"])

        messages.info(request, "You must input all fields." )
        return redirect("create_product_url", self.kwargs["slug"])


class DeleteShop(LoginRequiredMixin,UpdateView):
    login_url = '/myuser/supplier_login/'
    model = Shop

    def get(self, request, *args, **kwargs):
        shop = Shop.Undeleted.filter(slug=self.kwargs['slug'])
        shop.update(is_deleted=True, is_confirmed=True)
        shop = Shop.Undeleted.filter(supplier=self.request.user).first()
        messages.info(request, "You deleted the shop." )
        if shop:
            return redirect('shop_detail_url', slug=shop.slug)
        return redirect('create_shop_url')


class CreateProduct(LoginRequiredMixin, CreateView, ContextMixin):
    template_name = 'forms/create_product.html'
    login_url = '/myuser/supplier_login/'
    form_class = CreateProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.Undeleted.filter(supplier=self.request.user).order_by('id')
        return context

    def post(self, request, *args, **kwargs):
        form = CreateProductForm(request.POST, request.FILES)
        form.instance.shop = Shop.Undeleted.get(slug=self.kwargs['slug'])
        if form.is_valid():
            form.save()
            for i in range(1,5):
                if form.cleaned_data[f'image{i}'] is not None:
                    Image.objects.create(image=form.cleaned_data[f'image{i}'], product=form.instance)
            
            messages.success(request, "New product created." )
            return redirect("shop_detail_url", self.kwargs["slug"])

        messages.info(request, "You must input all fields." )
        return redirect("create_product_url", self.kwargs["slug"])
