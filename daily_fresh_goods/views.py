from django.shortcuts import render
from daily_fresh_goods import models
# Create your views here.
def index(request):
    # 注意商品id与输出个数的对应关系
    fruit_orderby_sale_num = models.Goods.objects.filter(goods_classification_id=10).order_by('-goods_sales_num')[0:4]
    fruit_orderby_id = models.Goods.objects.filter(goods_classification_id=10).order_by('id')[0:4]
    seafood_orderby_sale_num = models.Goods.objects.filter(goods_classification_id=5).order_by('id')[0:4]
    seafood_orderby_id = models.Goods.objects.filter(goods_classification_id=5).order_by('id')[0:4]
    context = {
        'fruit_orderby_sale_num':fruit_orderby_sale_num,
        'fruit_orderby_id':fruit_orderby_id,
        'seafood_orderby_sale_num':seafood_orderby_sale_num,
        'seafood_orderby_id':seafood_orderby_id,
    }
    return render(request,'daily_fresh_goods/index.html',context)

def list(request,type_num,sort):
    print(sort)
    # 新品推荐
    new_goods_recommend = models.Goods.objects.filter(goods_classification_id=int(type_num)).order_by('-id')[0:2]
    # 按最新排序
    if sort == 1 :
        goods_list = models.Goods.objects.filter(goods_classification_id=int(type_num)).order_by('-id')
    # 按销量排序
    elif sort == 2 :
        goods_list = models.Goods.objects.filter(goods_classification_id=int(type_num)).order_by('-goods_sales_num')
    # 按价格排序
    else:
        goods_list = models.Goods.objects.filter(goods_classification_id=int(type_num)).order_by('goods_price')

    context = {
        'type_num':type_num,
        'sort':sort,
        'goods_list': goods_list,
        'new_goods_recommend':new_goods_recommend,
    }
    print(goods_list)
    return render(request,'daily_fresh_goods/list.html',context)


def detail(request,gid):
    # print(request.COOKIES)
    # 记录当前的url到cookie中 登陆跳转用
    current_url = request.get_full_path()
    # 直接获取商品对象
    goods_detail = models.Goods.objects.get(id=gid)
    # 点击量+1
    goods_detail.goods_sales_num += 1
    # 保存点击量 到数据库
    goods_detail.save()
    type_id = goods_detail.goods_classification_id
    # 推荐同类商品
    new_goods_recommend = models.Goods.objects.filter(goods_classification_id=int(type_id)).order_by('-id')[0:2]
    print(goods_detail.goods_name,new_goods_recommend)
    context = {
        'goods_detail':goods_detail,
        'new_goods_recommend':new_goods_recommend
    }
    response = render(request,'daily_fresh_goods/detail.html',context)

    # 字符串才可以拼接 将id转化成str类型
    int_goods_id = str(goods_detail.id)
    # 获取cookie中的id
    lately_goods_id = request.COOKIES.get('lately_goods_id','')
    # cookie中不为空
    if lately_goods_id != '':
        lately_goods_id_list = lately_goods_id.split(',')
        # 判断该商品是否已经在列表中
        if int_goods_id in lately_goods_id_list:
            lately_goods_id_list.remove(int_goods_id)
        # 将刚刚浏览的产品加入到列表中(无论如何都会做)
        lately_goods_id_list.insert(0,int_goods_id)

        if len(lately_goods_id_list) > 5:
            lately_goods_id_list.pop()
        # 字符串拼接
        lately_goods_id = ','.join(lately_goods_id_list)
        print('join',lately_goods_id)
    # cookie中还没有元素
    else:
        lately_goods_id = int_goods_id

    context = {
        'goods_detail':goods_detail,
        'new_goods_recommend':new_goods_recommend,
    }
    response = render(request,'daily_fresh_goods/detail.html',context)

    response.set_cookie('lately_goods_id',lately_goods_id)
    response.set_cookie('url',current_url)
    print('finish',lately_goods_id)

    return response