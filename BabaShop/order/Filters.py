import django_filters

from order.models import Order

class OrderFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='order__created_at', lookup_expr='gt')
    end_date = django_filters.DateFilter(
        field_name='order__created_at', lookup_expr='lt')

    class Meta:
        model = Order
        fields = ['status', 'start_date', 'end_date']