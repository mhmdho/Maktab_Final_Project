from rest_framework import serializers
from shop.models import Product, Shop


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('name', 'type', 'address', 'supplier', 'is_confirmed', 'is_deleted' )


class ShopTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['type']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
