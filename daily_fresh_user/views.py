# coding:utf-8
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from daily_fresh_user.user_decorator import user_login_decorator

from daily_fresh_user.models import UserInfor
from daily_fresh_goods.models import Goods

import json
from hashlib import sha1
# Create your views here.
def register(request):
    return render(request,'../templates/daily_fresh_user/register.html',{'pagetitle':'天天生鲜，注册'})

def register_handel(request):
    # 接受用户输入值
    uname = request.POST.get('uname')
    pwd = request.POST.get('pwd')
    cpwd = request.POST.get('cpwd')
    email = request.POST.get('email')
    print(uname,pwd)
    # 判断两次密码是否一致
    if pwd != cpwd:
        return redirect('/user/register/')

    # 密码加密
    sha1_register = sha1()
    sha1_register.update(cpwd.encode('utf-8'))
    sha1_pwd = sha1_register.hexdigest()

    # 将新用户信息存入数据库
    UserInfor.objects.create(
        user_name=uname,
        user_password=sha1_pwd,
        user_email=email,
    )

    return redirect('/user/login/')

def register_exist(request):
    # 前端ajax请求以get形式提交
    uname_search = request.GET.get('uname')
    # 查询数据库中，该用户名出现频次
    count = UserInfor.objects.filter(user_name=uname_search).count()
    # 出现频次返回给前端
    return HttpResponse(json.dumps({'count':count}))

def login(request):
    if request.method == 'GET':
        uname = request.session.get('user_name','')
        context = {'error_name': 0, 'error_pwd': 0, 'user_name': uname}
        return render(request,'../templates/daily_fresh_user/login.html',context)
    elif request.method == 'POST':
        uname = request.POST.get('username')
        password = request.POST.get('pwd')
        # 是否记录 登录名 1 or None
        remember = request.POST.get('remember_username')
        search_user = UserInfor.objects.filter(user_name=uname)
        if len(search_user) == 1:
            s1_login = sha1()
            s1_login.update(password.encode('utf-8'))
            s1_pwd = s1_login.hexdigest()
            # 判断用户密码是否正确 并记录身份到cookie中
            if s1_pwd == search_user[0].user_password:
                # 回到用户登陆前所在的位置
                url = request.COOKIES.get('url','/goods/index')
                ret = redirect(url)
                if remember == 1:
                    # 保存用户名 设置cookie
                    ret.set_cookie('uname',uname)
                else:
                    # 设置cookie立即过期
                    ret.set_cookie('uname','',max_age=-1)
                # 只要用户登陆成功了 就写入session信息
                request.session['user_id'] = search_user[0].id
                request.session['user_name'] = search_user[0].user_name
                return ret
            else:
                context = {'error_name':0,'error_pwd':1,'user_name':uname}
        else:
            context = {'error_name': 1, 'error_pwd': 0, 'user_name': uname}
        # print(context)
        return render(request,'daily_fresh_user/login.html',context)

def logout(request):
    # 清空session 退出登陆
    request.session.flush()
    return redirect('/goods/index')

@user_login_decorator
def user_center_info(request):
    lately_goods_id = request.COOKIES.get('lately_goods_id','')
    # 如果存在最近浏览的商品则返回
    if lately_goods_id:
        # print(type(lately_goods_id),lately_goods_id)
        lately_goods_id = lately_goods_id.split(',')
        goods_list = []
        for items_id in lately_goods_id:
            query_goods = Goods.objects.get(id=int(items_id))
            goods_list.append(query_goods)
        print(goods_list)
        return render(request,'daily_fresh_user/user_center_info.html',{'good_list':goods_list})
    # 不存在最近浏览 直接返回
    return render(request,'daily_fresh_user/user_center_info.html')

@user_login_decorator
def user_center_site(request):
    if request.method == 'GET':
        user_id = request.session['user_id']
        user_name = request.session['user_name']
        print('user_id = %s and user_name = %s'%(user_id,user_name))
        object = UserInfor.objects.filter(id=user_id).first()
        context = {
            'object':object,
            'user_id':user_id,
            'user_name':user_name,
        }
        return render(request,'daily_fresh_user/user_center_site.html',context)
    # 编辑收货地址
    elif request.method =='POST':
        dict = {'status':True,'error':None,'data':None}
        user_id = request.session.get('user_id')
        receive_name = request.POST.get('receive_name')
        address = request.POST.get('address')
        zip_code = request.POST.get('zip_code')
        mobile_phone = request.POST.get('mobile_phone')
        # 异常处理
        try:
            UserInfor.objects.filter(id=user_id).update(
                user_receive_name=receive_name,
                user_address=address,
                user_mobile_phone_number = mobile_phone,
                user_zip_code = zip_code
            )
        except Exception:
            dict['status'] = False
            dict['error'] = '数据库录入错误'
        else:
            print(dict)
        return HttpResponse(json.dumps(dict))


