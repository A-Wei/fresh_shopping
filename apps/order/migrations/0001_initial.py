# Generated by Django 2.2.4 on 2019-08-13 13:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('order_id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('pay_method', models.SmallIntegerField(choices=[(0, 'Pay on delivery'), (1, 'WeChat Pay'), (2, 'AliPay'), (3, 'UniPay')], default=2)),
                ('total_count', models.IntegerField(default=1)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('postage_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_status', models.SmallIntegerField(choices=[(0, 'To be paid'), (1, 'To be delivered'), (2, 'In transit'), (3, 'To be reviewed'), (4, 'Complete')], default=1)),
                ('trade_no', models.CharField(max_length=128)),
                ('addr', models.ForeignKey(on_delete=False, to='user.Address')),
                ('user', models.ForeignKey(on_delete=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fs_order',
            },
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('count', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('comment', models.CharField(max_length=256)),
                ('order', models.ForeignKey(on_delete=True, to='order.OrderInfo')),
                ('sku', models.ForeignKey(on_delete=False, to='goods.GoodsSKU')),
            ],
            options={
                'db_table': 'fs_order_goods',
            },
        ),
    ]