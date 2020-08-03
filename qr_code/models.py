from django.db import models
import qrcode
import random

from orders.models import Orders


class QrVerify(models.Model):
    """Модель подтверждения получения заказа с помощью QR"""
    order = models.OneToOneField(Orders, on_delete=models.CASCADE, verbose_name='Заказ')
    qr = models.ImageField(upload_to='qrcode/', verbose_name='QR код')
    verify_key = models.IntegerField(verbose_name='Код подтверждения')

    class Meta:
        verbose_name = 'QR код на получение заказа'
        verbose_name_plural = 'QR коды на получение заказа'
