from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class GoodsType(models.Model):
    '''商品分类'''
    goods_type_name = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.goods_type_name

class Goods(models.Model):
    '''商品信息'''
    goods_name = models.CharField(max_length=20)
    goods_pic = models.CharField(null=True,max_length=200)
    # 总位 小数位
    goods_price = models.DecimalField(max_digits=5,decimal_places=2)
    goods_unit = models.CharField(max_length=20)
    # 销量或点击量 代表商品热度 字段存储 减少数据库聚合操作
    goods_sales_num = models.IntegerField()
    goods_stock = models.IntegerField()
    goods_short_desc = models.CharField(max_length=200)
    # 商品详细信息的维护 富文本编辑器
    goods_detail = HTMLField()
    # 设置外键
    goods_classification = models.ForeignKey('GoodsType',to_field='id',on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)

    good_advance = models.BooleanField(default=False)

    def __str__(self):
        return self.goods_name