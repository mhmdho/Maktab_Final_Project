import django_filters
from .models import Shop


class ShopListFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='type')

    class Meta:
        model = Shop
        fields = ['type']