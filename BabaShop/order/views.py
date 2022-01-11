from django.contrib import messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from rest_framework.response import Response
from order.Filters import OrderFilter
from order.models import OrderItem
from django.shortcuts import get_object_or_404, redirect
from shop.models import Shop, Product
from order.models import Order

# API/DRF
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderItemSerializer, OrderSerializer
from rest_framework import generics, status, viewsets


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
        context['orderitem_list'] = Order.objects.filter(orderitem__product__shop__slug=self.kwargs['slug']).annotate(Count('customer_id'))
        
        # for order in context['order_list']:
        #     items = order.orderitem_set.all()
        #     for item in items:
        #         shop_total_price = 0
        #         shop_total_quantity = 0
        #         shop_total_price += item.total_item_price
        #         shop_total_quantity += item.quantity
        # context['shop_total_price'] = shop_total_price
        # context['shop_total_quantity'] = shop_total_quantity
        # for order in context['order_list']:
        #     context['shop_order_total_quantity'] = order.shop_order_total_quantity(self.kwargs['slug'])
        #     context['shop_order_total_price'] = order.shop_order_total_price(self.kwargs['slug'])
        
        orders_value  = 0
        for ord in context['order_list']:
            orders_value += ord.total_price
            context['shop_order_total_price'] = ord.shop_order_total_price(self.kwargs['slug'])
            context['shop_order_total_quantity'] = ord.shop_order_total_quantity(self.kwargs['slug'])
        context['orders_value'] = orders_value
          
        filter_order = OrderFilter(self.request.GET, queryset=Order.objects.filter(
            orderitem__product__shop__slug=self.kwargs['slug']).annotate(Count('id')).order_by('-created_at'))
        # for ord in filter_order.queryset:
            # print(ord)
            # context['total_price'] = ord.shop_order_total_price(self.kwargs['slug'])
            # print(ord['shop_order_total_price'])
            # context['shop_order_total_quantity'] = ord.shop_order_total_quantity(self.kwargs['slug'])
        context['filter'] = filter_order
        for ord in context['filter'].queryset:
            print(ord)
            context['shop_order_total_price'] = ord.shop_order_total_price(self.kwargs['slug'])
            print(context['shop_order_total_price'])
            context['shop_order_total_quantity'] = ord.shop_order_total_quantity(self.kwargs['slug'])
        return context


class ProductList(LoginRequiredMixin, DetailView):
    template_name = 'order/product_list.html'
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
        context['orderitem_list'] = Order.objects.filter(orderitem__product__shop__slug=self.kwargs['slug']).annotate(Count('customer_id'))
        orders_value  = 0
        for ord in context['order_list']:
            orders_value += ord.total_price
        context['orders_value'] = orders_value
        filter_order = OrderFilter(self.request.GET, queryset=Order.objects.filter(
            orderitem__product__shop__slug=self.kwargs['slug']).annotate(Count('id')).order_by('-created_at'))
        print(filter_order)
        context['filter'] = filter_order
        return context


class OrderDetail(LoginRequiredMixin, DetailView):
    template_name = 'order/order_detail.html'
    login_url = '/myuser/supplier_login/'
    model = Order

    def get_queryset(self, *arg, **kwargs):
        return Shop.Undeleted.filter(slug=self.kwargs['slug'], supplier=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.Undeleted.filter(supplier=self.request.user).order_by('id')
        context['order_list'] = Order.objects.filter(id=self.kwargs['id'], orderitem__product__shop__slug=self.kwargs['slug']).annotate(Count('id')).order_by('-created_at')
        context['orderitem_list'] = OrderItem.objects.filter(order_id=self.kwargs['id'], product__shop__slug=self.kwargs['slug'])
        shop_total_price = 0
        shop_total_quantity = 0
        for item in context['orderitem_list']:
            shop_total_price += item.total_item_price
            shop_total_quantity += item.quantity
        context['shop_total_price'] = shop_total_price
        context['shop_total_quantity'] = shop_total_quantity
        return context


class OrderEditstatus(LoginRequiredMixin, View):
    login_url = '/myuser/supplier_login/'
    model = Order

    def get(self, request, *args, **kwargs):
        obj = self.model.objects.filter(pk=self.kwargs['pk'])
        obj = Order.objects.filter(pk=self.kwargs['pk']).first()
        if obj.status == 'CONFIRMED':
            self.model.objects.filter(pk=self.kwargs['pk']).update(status= 'CANCELED')
        elif obj.status == 'CANCELED':
            self.model.objects.filter(pk=self.kwargs['pk']).update(status= 'CHECKING')
        else:
            self.model.objects.filter(pk=self.kwargs['pk']).update(status= 'CONFIRMED')
            messages.error(request, f"The order NO. {obj.id} is Canceled." )
        return redirect('order_list_url', self.kwargs['slug'])


# ----------------- API / DRF -------------------------

class CreateOrderView(generics.ListCreateAPIView, generics.DestroyAPIView):
    model = OrderItem
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderItemSerializer

    def get_queryset(self, *arg, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        order = Order.objects.get(shop=shop, customer=self.request.user, is_payment=False)
        return OrderItem.objects.filter(order=order)

    def create(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        try:
            order = Order.objects.get(shop=shop, customer=self.request.user, is_payment=False)
        except:
            order = Order.objects.create(shop=shop, customer=self.request.user)
        
        request.data['order'] = order.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DeleteOrderView(generics.DestroyAPIView):
    model = OrderItem
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderItemSerializer

    def get_queryset(self, *arg, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        order = Order.objects.get(shop=shop, customer=self.request.user, is_payment=False)
        return OrderItem.objects.filter(order=order)


class PayOrderView(generics.UpdateAPIView):
    model = Order
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self, *arg, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        order = Order.objects.get(shop=shop, customer=self.request.user, is_payment=False)
        return order
    
    def put(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        order = Order.objects.filter(shop=shop, customer=self.request.user, is_payment=False)
        if order.first()['id'] == self.kwargs['pk']:
            order.update(is_payment=True)
            return Response({'success': 'payment done'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error:incorrect order id'}, status=status.HTTP_400_BAD_REQUEST)