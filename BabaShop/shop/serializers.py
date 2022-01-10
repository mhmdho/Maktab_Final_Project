from rest_framework import serializers
from shop.models import Shop


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('name', 'type', 'address', 'supplier', 'is_confirmed', 'is_deleted' )


class ShopTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['type']