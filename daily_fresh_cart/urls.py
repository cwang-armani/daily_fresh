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
from daily_fresh_cart import views

urlpatterns = [
    # 首页
    url('^cartinfo/$',views.cartinfo),
    # 增加商品
    url('^add_cart-(?P<gid>\d+)-(?P<count>\d+)/$',views.add_cart),
    # 删除商品
    url('^delete-(?P<cart_id>\d+)/$',views.delete),
    # 编辑商品
    url('^edit-(?P<cart_id>\d+)-(?P<count>\d+)/$',views.edit),

]
