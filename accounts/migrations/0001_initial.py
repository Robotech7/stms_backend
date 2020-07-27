# Generated by Django 3.0.8 on 2020-07-27 03:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Номер телефона')),
                ('bank_details', models.CharField(blank=True, max_length=30, null=True, verbose_name='Реквизиты')),
                ('provider_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Наименование компании')),
                ('provider_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email адресс компании')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Categories')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
