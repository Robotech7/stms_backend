from django.contrib import admin

from accounts.models import ProviderProfile


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    pass
