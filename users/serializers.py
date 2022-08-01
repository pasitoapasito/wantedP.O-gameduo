import re

from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer

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