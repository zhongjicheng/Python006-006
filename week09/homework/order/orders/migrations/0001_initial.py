# Generated by Django 2.2.13 on 2021-02-28 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='factory_orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField(default=1, serialize=False, verbose_name='产品id')),
                ('product_name', models.CharField(default='', max_length=30, verbose_name='产品名')),
                ('product_size', models.BigIntegerField(default=1001, verbose_name='产品规格')),
                ('quantity', models.BigIntegerField(default=0, verbose_name='产品数量')),
                ('price', models.BigIntegerField(default=100, verbose_name='产品单价')),
                ('total_amount', models.BigIntegerField(default=100, verbose_name='总金额')),
                ('is_cancel', models.BooleanField(default=False, verbose_name='取消订单')),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('create_order_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
