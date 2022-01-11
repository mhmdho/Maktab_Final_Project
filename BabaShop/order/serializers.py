from rest_framework import serializers
from order.models import OrderItem, Order


class OrderItemSeriailizer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderitem = OrderItemSeriailizer(source='order_set', many=True)
    class Meta:
        model = Order
        fields = '__all__'
