import re

from django.contrib.auth.hashers import check_password

from rest_framework                       import serializers
from rest_framework.serializers           import ModelSerializer, Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens      import OutstandingToken, BlacklistedToken

from users.models import User


class UserSignUpSerializer(ModelSerializer):
    
    def create(self, validated_data):
        password = validated_data.get('password')
        
        password_regex = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,20}$'
        
        if not re.match(password_regex, password):
            raise serializers.ValidationError({'password': ['올바른 비밀번호를 입력하세요.']})
        
        user = User.objects.create_user(**validated_data)
        return user
        
    class Meta:
        model        = User
        fields       = ['email', 'nickname', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
        
class UserSignInSerializer(TokenObtainPairSerializer):
    
    email    = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, write_only=True, max_length=100)
    
    def validate(self, data):
        email    = data.get('email')
        password = data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('detail : 올바른 유저정보를 입력하세요.')
        
        if not check_password(password, user.password):
            raise serializers.ValidationError('detail : 올바른 유저정보를 입력하세요.')

        for token in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=token)
        
        token         = super().get_token(user)
        refresh_token = str(token)
        access_token  = str(token.access_token)
        
        data = {
            'refresh' : refresh_token,
            'access'  : access_token
        }
        return data
        
    class Meta:
        model  = User
        fields = ['email', 'password']


class UserSignInSchema(Serializer):
    
    refresh = serializers.CharField(max_length=255)
    access  = serializers.CharField(max_length=255)