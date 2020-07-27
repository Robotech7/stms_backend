from django.contrib.auth import get_user_model
from django.db import models


class Categories(models.Model):
    """Модель категорий"""
    name = models.CharField(max_length=128, verbose_name='Название')
    is_active = models.BooleanField(default=True, verbose_name='Активная категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'


class Products(models.Model):
    """Модель товаров"""
    name = models.CharField(max_length=128, verbose_name='Наименование товара')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE,
                                 verbose_name='Категория')
    is_active = models.BooleanField(default=True, verbose_name='Активный товар')
    description = models.TextField(verbose_name='Описание товара')
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Добавлено')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлено')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена, руб')
    in_storage = models.PositiveIntegerField(verbose_name='В наличии')
    bar_code = models.IntegerField(verbose_name='Артикул')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


def directory_path(instance, filename):
    return f'media/products/{instance.product.name}/{filename}'


class ProductsImage(models.Model):
    """Изображения к товару"""
    product = models.ForeignKey(Products, on_delete=models.SET_NULL,
                                verbose_name='Продукт',
                                null=True)
    image = models.ImageField(upload_to=directory_path, verbose_name='Фото')
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Добавлено')

    def __str__(self):
        return f'{self.product.name}-{self.id}'

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
