from django.contrib import admin

from .models import Order, OrderItem, ProductComment, ProductLike
from django.utils.html import format_html

# Register your models here.


class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ('product',)
    list_filter = ('product', 'order')
    list_display = ('product', 'unit_price', 'quantity', 'total_item_price', 'discount', 'show_image', 'order')

    @admin.display(empty_value='-',description="show image")
    def show_image(self, obj):
        if (obj.product.get_image()):
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.product.get_image(),   
            )
        return '-'

    fieldsets = (
        (None, {
            'fields': ('product', ('unit_price', 'quantity'), 'discount', 'order')
        }),

        ('more options', {
            'classes': ('collapse',),
            'fields':  ('total_item_price',),
        }),
    )

    list_per_page = 10
    list_editable = ()

admin.site.register(OrderItem, OrderItemAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    search_fields = ('product',)
    list_filter = ('status', 'is_payment')
    list_display = ('customer', 'total_price', 'total_quantity', 'discount', 'created_at', 'status', 'show_image')

    @admin.display(empty_value='-',description="show image")
    def show_image(self, obj):
        if (obj.customer.image):
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.customer.image.url,   
            )
        return '-'

    fieldsets = (
        (None, {
            'fields': ('customer', ('status', 'is_payment'), 'discount')
        }),

        ('more options', {
            'classes': ('collapse',),
            'fields':  ('total_price', 'total_quantity'),
        }),
    )

    inlines = [
        OrderItemInline,
    ]
    list_per_page = 10
    list_editable = ('status',)

admin.site.register(Order, OrderAdmin)


class ProductCommentAdmin(admin.ModelAdmin):
    search_fields = ('subject', 'description')
    list_filter = ('created_at',)
    list_display = ('customer', 'product', 'subject', 'created_at', 'show_image')

    @admin.display(empty_value='-',description="show image")
    def show_image(self, obj):
        if (obj.customer.image):
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.customer.image.url,   
            )
        return '-'

    fieldsets = (
    (None, {
        'fields': (('subject', 'product'), 'description', 'customer')
    }),
    )

admin.site.register(ProductComment, ProductCommentAdmin)


class ProductLikeAdmin(admin.ModelAdmin):
    search_fields = ('product', )
    list_filter = ('default',)
    list_display = ('customer', 'product', 'default')

admin.site.register(ProductLike, ProductLikeAdmin)