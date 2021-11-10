from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import authenticate,login
from rest_framework import viewsets
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
# Create your views here.


class RegistrationView(APIView):
    def post(self,request):
        data = request.data
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user_obj = User.objects.create_user(username=data.get('username'),email=data.get('email'),password=data.get('password'))
            Token.objects.create(user=user_obj)
            return Response({
                "status":2,
                "message":"Success"
            })
        return Response({
            "status":0,
            "message":"Failed",
            "errors": serializer.errors
        }) 



class LoginView(APIView):
    def post(self,request):
        data = request.data
        serializer  = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=request.data['username'],password=request.data['password'])
            token = Token.objects.get(user = user)
            login(request, user)
            return Response({
                "status":2,
                "message":"Login Success",
                "token":token.key,
            })    
        return Response({
            "status":0,
            "message":"Invalid username/password",
        })


class UserListing(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = User.objects.all()
        serializer = UserListSerializer(user,many= True)
        return Response({"data":serializer.data}) 


class ProfileUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self,request,pk): 
        data = request.data
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = User.objects.get(id =pk)
            user_obj.username = data.get("username")
            profile_pic = request.FILES.get('profile_picture')
            if UserDetail.objects.filter(user_id = pk).exists():
                UserDetail.objects.filter(user_id = pk).update(designation = data.get("designation"),profile_picture = profile_pic)
                obj = UserDetail.objects.get(user_id = pk)
                obj.team.clear()
                for team_id in data.get("team") :
                    obj.team.add(team_id)
                    obj.save()
            else:
                obj = UserDetail.objects.create(user_id = pk,designation = data.get("designation"),profile_picture = profile_pic)
                for team_id in data.get('team') :
                    obj.team.add(team_id)
                    obj.save()
            user_obj.save() 
            return Response({
                "status":2,
                "message":"Updated"
            })
        return Response({
        "status":0,
        "message":"Update Failed"
        })      