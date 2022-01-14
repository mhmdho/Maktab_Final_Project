from rest_framework import serializers
from order.models import OrderItem, Order


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'id', 'product', 'quantity']
        extra_kwargs = {
            'order': {
                'allow_null': True,
            },
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['is_payment']
