from django.contrib import admin

from accounts.models import ProviderProfile


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider_name', 'provider_phone')
    raw_id_fields = ('user',)


admin.site.site_header = 'STMS'
