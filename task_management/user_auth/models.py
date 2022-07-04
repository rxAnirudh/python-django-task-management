from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime    
# Create your models here.

class UserModel(models.Model):
    first_name = models.CharField(max_length=50,blank=False)
    user_id = models.CharField(max_length=50,default="")
    last_name = models.CharField(max_length=50)
    status = models.CharField(max_length=50,default="Active")
    profile_pic = models.FileField()
    email = models.EmailField()
    mobile_number = PhoneNumberField()
    password = models.CharField(max_length=40)
    role = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)



    