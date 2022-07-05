from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from .models import UserModel
import uuid
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
            password = data["password"]
            role = serializer.data["role"]
            mobile_number = serializer.data["mobile_number"]
            user = UserModel.objects.filter(mobile_number=mobile_number).first()
            if user:
                userdata=list(UserModel.objects.values().filter(email=email_id))
                userdata[0].pop("password")
                return Response({"successs" : False,"data" : userdata[0],"message":"Profile already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_user = UserModel.objects.create(first_name=first_name,
            last_name=last_name,email=email_id,mobile_number=mobile_number,password=password,role=role)
            new_user.save()
            return Response({"successs" : True,"data" : serializer.data,"message":"User created successfully"}, status=status.HTTP_201_CREATED)
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


@api_view(["POST"])
def signin(request):
    try:
        data = request.data
        serializer = SignInSerializer(data=data)
        if serializer.is_valid():
            password = serializer.data["password"]
            email = serializer.data["email"]
            user = UserModel.objects.filter(email=email,password=password).first()
            if not user:
                return Response({"successs" : False,"message":"Account does not exists, please register first"}, status=status.HTTP_201_CREATED)
            userdata=list(UserModel.objects.values().filter(email=email))
            userdata[0].pop("password")
            return JsonResponse({"successs" : True,"data" : userdata[0],"message":"User logged in successfully"}, safe=False)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def deleteprofile(request):
    try:
        data = request.data
        serializer = DeleteProfileSerializer(data=data)
        if serializer.is_valid():
            mobile_number = serializer.data["mobile_number"]
            if not UserModel.objects.filter(mobile_number=mobile_number).first():
                return Response({"successs" : False,"message":"Account does not exists"}, status=status.HTTP_201_CREATED)
            UserModel.objects.filter(mobile_number=mobile_number).delete()
            return Response({"success" : True,"message":"Profile deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def updateprofile(request):
    try:
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            userdata = UserModel.objects.filter(user_id=serializer.data["user_id"]).first()
            if not userdata:
                return Response({"successs" : False,"message":"Profile does not exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            userdata.first_name = serializer.data["first_name"]
            userdata.last_name = serializer.data["last_name"]
            userdata.email_id = serializer.data["email"]
            userdata.password = serializer.data["password"]
            userdata.role = serializer.data["role"]
            userdata.mobile_number = serializer.data["mobile_number"]
            userdata.save()
            return Response({"successs" : True,"data" : serializer.data,"message":"User profile updated successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)