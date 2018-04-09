from django.shortcuts import render
from django.shortcuts import HttpResponse
import json
from django.http import JsonResponse
from daily_fresh_cart.models import CartInfo

from daily_fresh_user.user_decorator import user_login_decorator
# Create your views here.
@user_login_decorator
def cartinfo(request):
    user_id = request.session.get('user_id','')
    search_cart = CartInfo.objects.filter(user_id=user_id)
    context = {
        'search_cart':search_cart,
    }
    return render(request,'daily_fresh_cart/cart.html',context)

@user_login_decorator
def add_cart(request,gid,count):
    if request.method == 'POST':
        dict = {'status':True,'content':None,'error':None}
        user_id = request.session.get('user_id','')
        goods_id = int(gid)
        count_num = int(count)
        search_carts = CartInfo.objects.filter(user_id=user_id,goods_id=goods_id)
        # 如果已经添加了该商品，则增加数量
        if len(search_carts)>=1:
            search_carts[0].count += count_num
            search_carts[0].save()
        # 未添加该商品 数据库中新建对象
        else:
            new_carts = CartInfo()
            # cookie中拿到用户id
            new_carts.user_id = user_id
            # 商品id由post请求传入
            new_carts.goods_id = gid
            new_carts.count = count_num
            new_carts.save()

        goodstype_num_in_cart = CartInfo.objects.filter(user_id=user_id).count()
        dict['content'] = goodstype_num_in_cart
        request.session['goodstype_num_in_cart'] = goodstype_num_in_cart
        return HttpResponse(json.dumps(dict))

@user_login_decorator
def delete(request,cart_id):
    dict = {'status':True,'content':None,'error':None}
    if request.method == 'POST':
        CartInfo.objects.filter(id=int(cart_id)).delete()
        return HttpResponse(json.dumps(dict))


@user_login_decorator
def edit(request,cart_id,count):
    eidt_cart_id = cart_id
    edit_count = count
    search_cart = CartInfo.objects.get(id=int(eidt_cart_id))
    search_cart.count = int(edit_count)
    search_cart.save()
    dict = {'status':True,'error':None,'content':'商品修改成功'}
    return HttpResponse(json.dumps(dict))
