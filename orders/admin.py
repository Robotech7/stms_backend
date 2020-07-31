from django.contrib import admin
from .models import Orders, ProductsInOrder


class ProductsInOrderInline(admin.StackedInline):
    model = ProductsInOrder
    fields = ['product', 'amount']
    extra = 0



@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'client_email', 'total_price']
    readonly_fields = ['total_price', ]
    inlines = [ProductsInOrderInline]
    ordering = ('created', )
