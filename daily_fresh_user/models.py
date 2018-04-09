from django.db import models

# Create your models here.
class UserInfor(models.Model):
    '''用户信息'''
    user_name = models.CharField(max_length=20)
    user_password = models.CharField(max_length=40)
    user_email = models.CharField(max_length=30)
    user_receive_name = models.CharField(max_length=20,default="")
    user_address = models.CharField(max_length=20,default="")
    user_zip_code = models.CharField(max_length=10,default="")
    user_mobile_phone_number = models.CharField(max_length=11,default="")