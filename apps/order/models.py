from django.db import models
from db.base_model import BaseModel

# Create your models here.
class OrderInfo(models.Model):
    PAY_METHOD_CHOICES = (
        (0, "Pay on delivery"),
        (1, "WeChat Pay"),
        (2, "AliPay"),
        (3, "UniPay"),
    )
    ORDER_STATUS_CHOICES = (
        (0, 'To be paid'),
        (1, 'To be delivered'),
        (2, 'In transit'),
        (3, 'To be reviewed'),
        (4, 'Complete')
    )

    order_id = models.CharField(max_length=128, primary_key=True)
    user = models.ForeignKey('user.User', on_delete=False)
    addr = models.ForeignKey('user.Address', on_delete=False)
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=2)
    total_count = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    postage_fee = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    trade_no = models.CharField(max_length=128)


    class Meta:
        db_table = "fs_order"


class OrderGoods(BaseModel):
    order = models.ForeignKey('OrderInfo', on_delete=True)
    sku = models.ForeignKey('goods.GoodsSKU', on_delete=False)
    count = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.CharField(max_length=256)

    class Meta:
        db_table = 'fs_order_goods'
