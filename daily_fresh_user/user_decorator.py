from django.shortcuts import render
def user_login_decorator(inner_func):
    def login_func(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return inner_func(request,*args,**kwargs)
        else:
            # 回到 用户登陆前的位置 完整路径 写入到cookie中
            ret = render(request,'daily_fresh_user/login.html')
            ret.set_cookie('url',request.get_full_path())
            return ret
    return login_func