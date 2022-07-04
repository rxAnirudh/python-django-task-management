import profile
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .threads import send_forgot_email_customer
from .serializers import *
from .models import UserModel
import uuid
from django.core.files.storage import FileSystemStorage
import os
import base64
# Create your views here.

@api_view(["POST"])
def signup(request):
    try:
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            email_id = serializer.data["email"]
            password = serializer.data["password"]
            user_id = serializer.data["user_id"]
            role = serializer.data["role"]
            mobile_number = serializer.data["mobile_number"]
            if UserModel.objects.filter(mobile_number=mobile_number).first():
                return Response({"successs" : True,"Data" : serializer.data,"message":"Profile already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_user = UserModel.objects.create(first_name=first_name,
            last_name=last_name,email=email_id,mobile_number=mobile_number,password=password,role=role,user_id=user_id)
            new_user.save()
            return Response({"successs" : True,"Data" : serializer.data,"message":"User created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


