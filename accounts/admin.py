from django.contrib import admin

from accounts.models import ProviderProfile


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider_name', 'provider_phone')

admin.site.site_header = 'STMS'