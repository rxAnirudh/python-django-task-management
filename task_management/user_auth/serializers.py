from dataclasses import fields
from rest_framework import serializers
from .models import *
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ["profile_pic","user_id","password"]
    def validate_password(self, value):
     password_validation.validate_password(value, self.instance)
     return value

    


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email']


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email','password']


class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email','password']


class DeleteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['mobile_number']

