from django.contrib import admin

from .models import Deliveries, ProductsInDeliveries


class ProductsInDeliveriesInline(admin.TabularInline):
    model = ProductsInDeliveries
    fields = ['product', 'amount']
    extra = 1


@admin.register(Deliveries)
class DeliveriesAdmin(admin.ModelAdmin):
    list_display = ['provider', 'status', 'total_price']
    inlines = [ProductsInDeliveriesInline]
    ordering = ('-created',)
    list_filter = ('status', 'created', 'updated')
    readonly_fields = ('total_amount',)
