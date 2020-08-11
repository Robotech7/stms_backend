from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from products.models import Categories


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/', verbose_name='Аватар', null=True, blank=True)


class ProviderProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    provider_phone = models.CharField(max_length=15, verbose_name='Номер телефона', null=True, blank=True)
    bank_details = models.CharField(max_length=30, verbose_name='Реквизиты', null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    provider_name = models.CharField(max_length=250, verbose_name='Наименование компании',
                                     null=True, blank=True)
    provider_email = models.EmailField(verbose_name='Email адресс компании', null=True, blank=True)
    provider_address = models.CharField(max_length=250, verbose_name='Адрес компании',
                                        null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль поставщика'
        verbose_name_plural = 'Поставщики'
