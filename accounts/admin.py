from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts.models import ProviderProfile


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider_name', 'provider_phone')
    raw_id_fields = ('user',)


admin.site.site_header = 'STMS'


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('avatar',)}),)
