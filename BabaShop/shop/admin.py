from django.contrib import admin

from .models import Image, Product, ProductCategory, ProductTag, Shop
from django.utils.html import format_html

# Register your models here.

admin.site.register(ProductCategory)
admin.site.register(ProductTag)
admin.site.register(Image)


class ShopAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('type', 'is_confirmed', 'is_deleted')
    list_display = ('name', 'type', 'address', 'supplier', 'is_confirmed')
    
    @admin.action(description='Select shops to confirmed')
    def publish_shop(modeladmin, request, queryset):
        queryset.update(is_confirmed=True)

    actions = [publish_shop]
    list_editable = ('is_confirmed',)


admin.site.register(Shop, ShopAdmin)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name', 'descrption')
    list_filter = ('category', 'tag', 'shop', 'is_confirmed')
    list_display = ('name', 'price', 'stock', 'shop', 'is_confirmed', 'show_image')
    date_hierarchy = ('created_at')

    @admin.display(empty_value='-',description="show image")
    def show_image(self, obj):
        if (obj.get_image()):
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.get_image(),   
            )
        return '-'
    
    fieldsets = (
        (None, {
            'fields': (('name', 'price'), 'description', ('shop', 'category'), 'tag', ('stock', 'weight'))
        }),

        ('more options', {
            'classes': ('collapse',),
            'fields':  ('is_active', 'is_confirmed'),
        }),
    )

    save_on_top =True
    inlines = [
        ImageInline,
    ]
    list_per_page = 10
    list_editable = ('is_confirmed',)

admin.site.register(Product, ProductAdmin)
