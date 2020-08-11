import qrcode
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from products.models import Products

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Номер телефона имеет формат: +777777777, от 9 до 15 символов"
)

STATUS = (
    ('new', 'Новый'),
    ('form', 'Формируется'),
    ('ready', 'Готов к выдаче'),
    ('received', 'Получено'),
    ('error', 'Ошибка, обратитесь в службу поддержки')
)


class Orders(models.Model):
    """Модель заказов"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    client_phone = models.CharField(max_length=18, validators=[phone_regex], verbose_name='Номер телефона')
    client_name = models.CharField(max_length=128, verbose_name='Имя клиента')
    client_surname = models.CharField(max_length=128, verbose_name='Фамилия клиента')
    client_email = models.EmailField(max_length=128, verbose_name='E-mail клиента')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Сумма', null=True)
    status = models.CharField(choices=STATUS, max_length=255, default='new', verbose_name='Статус заказа')
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Создано')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлено')

    def save(self, *args, **kwargs):
        if self.status == 'ready' and not QrCodesOrderVerify.objects.filter(order=self.id).exists():
            # Кажется накостылял жестко, надо разбираться с более лучшим вариантом
            obj = QrCodesOrderVerify()
            obj.order = self
            obj.qr = self.qr_generate()
            obj.save()
        return super().save()

    def qr_generate(self):
        img = qrcode.make(''.join([settings.URL, 'api/orders/verify/', str(self.id)]))
        filename = f'qr-{self.id}.png'
        img.save(settings.MEDIA_ROOT + '/qr_codes/' + filename)
        img_path = '/qr_codes/' + filename
        return img_path

    def __str__(self):
        return f'{self.user.username}/{self.client_name}-{self.client_surname}'

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


class ProductsInOrder(models.Model):
    """Модель позиций к заказу"""
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, verbose_name='Заказ')
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, verbose_name='Продукт')
    price_for_one = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Цена за единицу')
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.product.name}'

    def save(self, *args, **kwargs):
        price_for_one = self.product.price
        self.price_for_one = price_for_one
        return super(ProductsInOrder, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'


class QrCodesOrderVerify(models.Model):
    """Модель хранящая QR коды, для подтверждения получения заказа"""
    order = models.OneToOneField(Orders, on_delete=models.CASCADE, verbose_name='Заказ')
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Создано')
    qr = models.ImageField(upload_to='qr_codes/', verbose_name='QR код')

    def qr_tag(self):
        return mark_safe('<img src="%s" width="100" height="100" />' % self.qr.url)

    qr_tag.short_description = 'QR код'

    def __str__(self):
        return f'{self.order}'

    class Meta:
        verbose_name_plural = 'QR коды подтверждения'
        verbose_name = 'QR код подтверждения'


# Сигнал для подсчета суммы стоимости в заказе, после сохранения позиций
@receiver(post_save, sender=ProductsInOrder)
def init_price(instance, **kwargs):
    order = instance.order
    all_products = ProductsInOrder.objects.filter(order=order)
    total_price = 0
    for item in all_products:
        total_price += item.price_for_one * item.amount
    order.total_price = total_price
    order.save()
