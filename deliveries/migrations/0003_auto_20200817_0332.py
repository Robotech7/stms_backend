# Generated by Django 3.0.8 on 2020-08-17 03:32

from django.db import migrations, models

import deliveries.models


class Migration(migrations.Migration):
    dependencies = [
        ('deliveries', '0002_auto_20200810_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveries',
            name='status',
            field=models.CharField(choices=[('new', 'Новый'), ('received', 'Получено')],
                                   default=deliveries.models.StatusDeliveries['new'], max_length=255,
                                   verbose_name='Статус'),
        ),
    ]
