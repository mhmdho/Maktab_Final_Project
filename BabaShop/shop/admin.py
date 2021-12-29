from django.contrib import admin

from .models import Product, ProductCategory, ProductTag, Shop

# Register your models here.

admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductTag)
