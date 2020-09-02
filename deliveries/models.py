from enum import Enum

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from accounts.models import ProviderProfile
from products.models import Products


class StatusDeliveries(Enum):
    new = 'Новый'
    received = 'Получено'

    @classmethod
    def choices(cls):
        return tuple((attr.name, attr.value) for attr in cls)


class Deliveries(models.Model):
    """Модель поставок"""
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, verbose_name='Поставщик')
    status = models.CharField(choices=StatusDeliveries.choices(), max_length=255,
                              default=StatusDeliveries.new, verbose_name='Статус')
    total_amount = models.PositiveIntegerField(verbose_name='Количество позиций', null=True,
                                               blank=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Сумма', null=True,
                                      blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Создано')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return self.provider.provider_name

    def save(self, *args, **kwargs):
        if self.status == 'received':
            all_products = ProductsInDeliveries.objects.filter(delivery=self.id)
            for product in all_products:
                obj = get_object_or_404(Products, id=product.product_id)
                obj.in_storage = obj.in_storage + product.amount
                obj.save()
        return super(Deliveries, self).save(**kwargs)

    class Meta:
        verbose_name = "Поставка"
        verbose_name_plural = 'Поставки'


class ProductsInDeliveries(models.Model):
    """Модель позиций внутри поставки"""
    delivery = models.ForeignKey(Deliveries, on_delete=models.CASCADE, verbose_name='Поставка')
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, verbose_name='Товар', null=True)
    amount = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return 'Позиция: '

    class Meta:
        verbose_name = 'Товар в поставке'
        verbose_name_plural = 'Товары в поставке'


@receiver(post_save, sender=ProductsInDeliveries)
def init_total_amount(instance, **kwargs):
    delivery = instance.delivery
    all_products = ProductsInDeliveries.objects.filter(delivery=delivery)
    delivery.total_amount = len(all_products)
    delivery.save()
