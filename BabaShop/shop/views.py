from typing_extensions import Required
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404


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
        # return redirect(f'/shop/shop_detail/{self.kwargs["slug"]}')
        return redirect("shop_detail_url", self.kwargs["slug"])



class DeleteShop(LoginRequiredMixin,UpdateView):
    model = Shop

    def get(self, request, *args, **kwargs):
        shop = (Shop.Undeleted.filter(slug=self.kwargs['slug']))
        shop.update(is_deleted=True, is_confirmed=True)
        return redirect(reverse('supplier_dashboard_url'))
