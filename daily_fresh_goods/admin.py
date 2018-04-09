from django.contrib import admin
from daily_fresh_goods.models import *
# Register your models here.
class GoodsTypeAdmin(admin.ModelAdmin):
    list_display = ['id','goods_type']
class GoodsAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id','goods_name','goods_pic','goods_price','goods_unit',
                    'goods_sales_num','goods_stock','goods_short_desc','goods_detail',
                    'goods_classification','is_delete']

admin.site.register(GoodsType)
admin.site.register(Goods)