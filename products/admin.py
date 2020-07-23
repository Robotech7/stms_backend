from django.contrib import admin
from .models import Products, Categories, ProductsImage


class ProductsImageInline(admin.TabularInline):
    model = ProductsImage
    extra = 0


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active')
    inlines = [ProductsImageInline]


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    exclude = ('id',)
