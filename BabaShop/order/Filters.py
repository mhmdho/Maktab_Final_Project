

class OrderFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='order__order_date', lookup_expr='gt')
    end_date = django_filters.DateFilter(
        field_name='order__order_date', lookup_expr='lt')

    class Meta:
        model = OrderItem
        fields = ['status', 'start_date', 'end_date']