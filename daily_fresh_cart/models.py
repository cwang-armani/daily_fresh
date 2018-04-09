from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class CartInfo(models.Model):
    '''购物车'''
    user = models.ForeignKey('daily_fresh_user.UserInfor',to_field='id',on_delete=models.CASCADE)
    goods = models.ForeignKey('daily_fresh_goods.Goods',to_field='id',on_delete=models.CASCADE)
    # 购买数量
    count = models.IntegerField()