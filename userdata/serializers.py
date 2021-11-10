from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate,login
from .models import *

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields= ('username', 'email','password')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, max_length=25)
    password = serializers.CharField(required=True, allow_blank=False, max_length=25)

    def validate(self,data):
        user = authenticate(username=data['username'],password=data['password'])
        if not user:
            raise serializers.ValidationError({'status':0, 'message':"Invalid username/password"})
        return data

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email')


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = UserDetail
        fields = ('username','designation','profile_picture','team')