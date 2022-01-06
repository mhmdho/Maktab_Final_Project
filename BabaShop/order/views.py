from django.contrib import messages
from django.db.models.aggregates import Count
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from shop.models import Shop, Product
from order.models import Order

# Create your views here.


class OrderList(LoginRequiredMixin, DetailView):
    template_name = 'order/order_list.html'
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
        context['customer_count'] = Order.objects.filter(orderitem__product__shop__slug=self.kwargs['slug']).annotate(Count('customer_id')).count()
        orders_value  = 0
        for ord in context['order_list']:
            orders_value += ord.total_price
        context['orders_value'] = orders_value
        return context
