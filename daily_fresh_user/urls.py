"""daily_fresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import url
from daily_fresh_user import views

urlpatterns = [

    # 注册页面
    url('^register/$',views.register),
    # 用户注册信息提交
    url('^register_handel/$',views.register_handel),
    # ajax判断注册时用户名是否存在
    url('^register_exist/$',views.register_exist),

    # 登陆页面
    url('^login/$',views.login),
    # 退出登陆
    url('^logout/$',views.logout),

    # 用户中心
    url('^user_center_info/$',views.user_center_info),
    # 地址表单提交
    url('^user_center_site/$',views.user_center_site),
]
