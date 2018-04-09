from django.shortcuts import render
from django.shortcuts import HttpResponse

from daily_fresh_user.models import UserInfor
from daily_fresh_goods.models import Goods
from daily_fresh_cart.models import CartInfo
from daily_fresh_order.models import Order
from daily_fresh_order.models import OrderDetailInfo

from daily_fresh_user.user_decorator import user_login_decorator
from django.db import transaction
import json
from datetime import datetime
# Create your views here.
@user_login_decorator
def orderinfo(request):
    if request.method == 'GET':
        # 获取用户信息
        uid = request.session.get('user_id')
        user = UserInfor.objects.get(id=uid)
        # 获取前端订单id组成的字符串
        data_list = request.GET.get('data_list')
        # 对前端获取的字符串进行拆分 切片
        search_list = data_list.split(',')
        order_list = []
        # 查询相关订单
        for i in search_list[:-1]:
            order_list.append(CartInfo.objects.get(id=int(i)))
        # 移动电话 打码处理
        phone_number = user.user_mobile_phone_number
        privacy_phone_number = phone_number[0:3] + '****' + phone_number[-4:]
        context = {
            'user':user,
            'order_list':order_list,
            'count':len(order_list),
            'privacy_phone_number':privacy_phone_number,
        }
        return render(request, 'daily_fresh_order/place_order.html',context)

# 事务 装饰器 一旦操作失败 回滚
@transaction.atomic()
@user_login_decorator
def order_submit(request):
    dict = {'order_status': True, 'error_msg': None}
    tran_id = transaction.savepoint()
    try:
        uid = request.session.get('user_id')
        ajax_cart_id = request.POST.get('cart_id')
        ajax_practical_pay = request.POST.get('practical_pay')
        ajax_pay_type = request.POST.get('pay_type')
        # 构造时间对象
        time = datetime.now()
        # 时间对象格式化
        timeformat_and_uid = "%s%d" %(time.strftime('%Y%m%d%H%M%S'),uid)
        user_addr = request.POST.get('user_addr')
        # 创建订单
        Order.objects.create(
            order_id=timeformat_and_uid,
            user_id=uid,
            order_date=time,
            order_total_num=ajax_practical_pay,
            pay_tyepe=ajax_pay_type,
            user_address=user_addr,
            order_ispay=False,
        )
        # 创建订单详情
        cart_id_list = ajax_cart_id.split(',')
        print(cart_id_list)
        num = request.session.get('goodstype_num_in_cart','')
        for cart_id in cart_id_list[:-1]:
            # 购物车所有对象
            cart_info = CartInfo.objects.get(id=cart_id)
            # 获取对象的商品id 数量
            goods_info = Goods.objects.get(id=cart_info.goods_id)
            count = cart_info.count
            # 库存大于购买量
            if goods_info.goods_stock >= count:
                goods_info.goods_stock -= count
                goods_info.save()

                OrderDetailInfo.objects.create(
                    order_id=timeformat_and_uid,
                    goods_id=goods_info.id,
                    single_price=goods_info.goods_price,
                    count=count
                )

                # 删除购物车对象
                cart_info.delete()
                num -= 1
            else:
                # 库存不足发出事务回滚
                transaction.savepoint_rollback(tran_id)
                dict['order_status'] = False
                dict['error_msg'] = '库存不足'

        #购物车中的商品数量重置
        request.session['goodstype_num_in_cart'] = num

    except Exception as e:
        dict['order_status'] = False
        dict['error_msg'] = e
        print('==============%s=============='%e)
        # 出现异常 回滚操作
        transaction.savepoint_rollback(tran_id)

    return HttpResponse(json.dumps(dict))

@user_login_decorator
def pay_info(request):
    return render(request,'daily_fresh_order/pay.html')