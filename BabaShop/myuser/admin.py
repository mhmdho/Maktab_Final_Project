from django.contrib import admin

from .models import Address, CustomUser
from django.utils.html import format_html

# Register your models here.


class AddressInline(admin.TabularInline):
    model = Address
    exclude = ('slug',)
    extra = 1

class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('phone', 'username')
    list_filter = ('is_customer', 'is_supplier')
    list_display = ('phone', 'email', 'username', 'is_supplier', 'is_customer', 'show_image', 'date_joined')
    date_hierarchy = ('date_joined')

    @admin.display(empty_value='-',description="show image")
    def show_image(self, obj):
        if (obj.image):
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.image.url,   
            )
        return '-'
    
    fieldsets = (
        (None, {
            'fields': (('phone', 'password'), ('username', 'email'), ('is_customer', 'is_supplier'))
        }),

        ('more options', {
            'classes': ('collapse',),
            'fields':  ('first_name', 'last_name', 'image'),
        }),
    )

    save_on_top =True
    inlines = [
        AddressInline,
    ]
    list_editable = ('is_customer', 'is_supplier')

admin.site.register(CustomUser, CustomUserAdmin)


class AddressAdmin(admin.ModelAdmin):
    search_fields = ('city',)
    list_filter = ('city', 'country')
    list_display = ('label', 'customer', 'country', 'city', 'zipcode', 'show_image')

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
            'fields': ('customer', 'label', ('country', 'city'), 'address', 'zipcode')
        }),

        ('more options', {
            'classes': ('collapse',),
            'fields':  ('slug',),
        }),
    )

    list_per_page = 5
    list_editable = ()

admin.site.register(Address, AddressAdmin)
