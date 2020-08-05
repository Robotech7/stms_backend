from django.contrib import admin

from .models import Orders, ProductsInOrder, QrCodesOrderVerify


class ProductsInOrderInline(admin.TabularInline):
    model = ProductsInOrder
    fields = ['product', 'amount', 'price_for_one']
    readonly_fields = ['price_for_one', ]
    extra = 0


class QrCodesOrderVerifyAdmin(admin.TabularInline):
    model = QrCodesOrderVerify
    fields = ('qr',)
    extra = 0


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'user', 'status', 'client_email', 'total_price']
    readonly_fields = ['total_price']
    inlines = [ProductsInOrderInline, QrCodesOrderVerifyAdmin]
    ordering = ('created',)
    list_filter = ('status', 'created', 'updated')
    search_fields = ('client_name', 'client_email')
