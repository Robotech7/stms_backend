from django.contrib import admin

from .models import Deliveries, ProductsInDeliveries


class ProductsInDeliveriesInline(admin.TabularInline):
    model = ProductsInDeliveries
    fields = ['product', 'amount']
    extra = 1


@admin.register(Deliveries)
class DeliveriesAdmin(admin.ModelAdmin):
    list_display = ['provider', 'get_provider_name', 'status', 'total_price']
    inlines = [ProductsInDeliveriesInline]
    ordering = ('-created',)
    list_filter = ('status', 'created', 'updated')
    readonly_fields = ('total_amount',)
    search_fields = ('provider__provider_name__icontains', 'status', 'id')
    list_select_related = True

    def get_provider_name(self, obj):
        return obj.provider.provider_name

    get_provider_name.short_description = 'Наименование компании'
