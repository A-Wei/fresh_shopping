from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField
# Create your models here.


class GoodsType(BaseModel):
    name = models.CharField(max_length=20)
    logo = models.CharField(max_length=20)
    image = models.ImageField(upload_to='type')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'fs_goods_type'


class GoodsSKU(BaseModel):
    STATUS_CHOICES = (
        (0, 'Unavailable'),
        (1, 'Available'),
    )
    type = models.ForeignKey('GoodsType', on_delete=False)
    goods = models.ForeignKey('Goods', on_delete=True)
    name = models.CharField(max_length=20)
    desc = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)
    image = models.ImageField(upload_to='goods')
    stock = models.IntegerField(default=1)
    sales_volume = models.IntegerField(default=0)
    status = models.SmallIntegerField(default=1, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'fs_goods_sku'


class Goods(BaseModel):
    name = models.CharField(max_length=20)
    detail = HTMLField(blank=True)

    class Meta:
        db_table = 'fs_goods'


class GoodsImage(BaseModel):
    sku = models.ForeignKey('GoodsSKU', on_delete=True)
    image = models.ImageField(upload_to='goods')

    class Meta:
        db_table = 'fs_goods_image'


class IndexGoodsBanner(BaseModel):
    sku = models.ForeignKey('GoodsSKU', on_delete=True)
    image = models.ImageField(upload_to='banner')
    index = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'fs_index_banner'


class IndexTypeGoodsBanner(BaseModel):
    DISPLAY_TYPE_CHOICES = (
        (0, "title"),
        (1, "image")
    )

    type = models.ForeignKey('GoodsType', on_delete=True)
    sku = models.ForeignKey('GoodsSKU', on_delete=True)
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES)
    index = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'fs_index_type_goods'


class IndexPromotionBanner(BaseModel):
    name = models.CharField(max_length=20)
    url = models.URLField()
    image = models.ImageField(upload_to='banner')
    index = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'fs_index_promotion'
