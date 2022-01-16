from rest_framework import serializers
from shop.models import Product, Shop
from order.models import OrderItem, Order
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


from pprint import pprint

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'id', 'product', 'quantity']
        extra_kwargs = {
            'order': {
                'read_only': True,
            },
        }
    
    def create(self, validated_data):

        pprint(self.context['request'].user)
        shop = get_object_or_404(Shop, slug=self.context['request'].parser_context['kwargs']['slug'])
        product_id = self.data['product']
        print(product_id)
        if product_id:
            product = get_object_or_404(Product, id=product_id, shop__slug=self.context['request'].parser_context['kwargs']['slug'])
            if product.stock > 0:
                if product.is_active == True:
                    try:
                        order = Order.objects.get(shop=shop, customer=self.context['request'].user, is_payment=False)
                    except:
                        order = Order.objects.create(shop=shop, customer=self.context['request'].user)
                    validated_data['order'] = order
                    return super().create(validated_data)
            return Response({'Error': 'This product is out of order'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Error': 'Enter your product'}, status=status.HTTP_400_BAD_REQUEST)


    
    # def validate(self, attrs):
    #     print(attrs, '2------------------------------------------------')
    #     attrs["order"] = order
    #     return super().validate(attrs)




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
