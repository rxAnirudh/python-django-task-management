from dataclasses import fields
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ["profile_pic"]
    


