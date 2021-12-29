from django.contrib import admin

from .models import Order, OrderItem, ProductComment, ProductLike

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductComment)
admin.site.register(ProductLike)