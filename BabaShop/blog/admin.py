from django.contrib import admin

from blog.models import Category, Comment, Post, Tag
from django.utils.html import format_html

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    list_display = ('customer', 'post', 'title', 'created_at', 'show_image')

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
        'fields': (('title', 'post'), 'description', 'customer')
    }),

    ('more options', {
        'classes': ('collapse', ),
        'fields': ('like', ),
    }),
    )

admin.site.register(Comment, CommentAdmin)


class CagetoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)
    list_display_link = ('title',)
    # list_editable = ('title',)

admin.site.register(Category, CagetoryAdmin)


class TagAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)
    list_display_link = ('title',)

admin.site.register(Tag, TagAdmin)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'descrption')
    list_filter = ('status', 'tag', 'category', 'supplier')
    list_display = ('title', 'short_description', 'created_at', 'supplier', 'status', 'show_image')
    date_hierarchy = ('created_at')


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
            'fields': (('title', 'short_description'), 'descrption', ('supplier', 'image'), 'category')
        }),

        ('more options', {
            'classes': ('collapse',),
            'fields': ('tag', 'status'),
        }),
    )

    save_on_top =True
    inlines = [
        CommentInline,
    ]
    list_per_page = 10
    list_editable = ('status',)

admin.site.register(Post, PostAdmin)
