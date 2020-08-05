from django.contrib import admin

from .models import Products, Categories, ProductsImage


class ProductsImageInline(admin.TabularInline):
    model = ProductsImage
    extra = 0
    fields = ('image_tag', 'image')
    readonly_fields = ('image_tag',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active')
    list_filter = ('category', )
    search_fields = ('bar_code', 'name')
    inlines = [ProductsImageInline]


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    exclude = ('id',)
    list_display = ('name', 'is_active')
