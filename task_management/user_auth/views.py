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
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage  

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


@api_view(["POST"])
def forgotpassword(request):
    try:
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            # user = UserModel.objects.get(email=email)
            # if not user:
            #     return Response({"message":"Account does not exists"}, status=status.HTTP_404_NOT_FOUND)
            otp = uuid.uuid4()
            # user.token = otp
            # user.save()
            mail_subject = 'Activation link has been sent to your email id'  
            email = EmailMessage(  
                        mail_subject, str(otp), to=[email]  
            )  
            emailSentID = email.send()
            print(f"SendIT : {emailSentID}")
            return Response({"message":"reset mail sent"}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
def resetpassword(request):
    try:
        data = request.data
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid():
         userdata = UserModel.objects.filter(user_id=serializer.data["user_id"]).first()
         if not userdata:
            return Response({"success" : False,"message":"Account does not exists"}, status=status.HTTP_404_NOT_FOUND)
         userdata.password = serializer.data["password"]
         userdata.save()
         return Response({"success" : True,"message":"Password changed successfully"}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

