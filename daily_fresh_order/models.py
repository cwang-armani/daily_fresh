from django.db import models

# Create your models here.
class Order(models.Model):
    order_id = models.CharField(max_length=30,primary_key=True)
    user = models.ForeignKey('daily_fresh_user.UserInfor',to_field='id',on_delete=models.CASCADE)
    order_date = models.TimeField(auto_now=True)
    order_ispay = models.BooleanField(default=False)
    order_total_num = models.DecimalField(max_digits=6,decimal_places=2)
    user_address = models.CharField(max_length=120, default="")
    pay_tyepe = models.IntegerField(default=0)

class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('daily_fresh_goods.Goods',to_field='id',on_delete=models.CASCADE)
    order = models.ForeignKey('daily_fresh_order.Order',to_field='order_id',on_delete=models.CASCADE)
    single_price = models.DecimalField(max_digits=5,decimal_places=2)
    count = models.IntegerField()