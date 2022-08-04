from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer

from django.core.cache import cache
from raids.models      import RaidHistory


class BossRaidEnterSerializer(ModelSerializer):
    nickname = serializers.SerializerMethodField()
    
    def get_nickname(self, obj: RaidHistory) -> str:
        return obj.users.nickname
        
    def create(self, validated_data):
        time_limit = cache.get('limit_time')
        if not time_limit:
            raise serializers.ValidationError('detail: 보스레이드의 정보를 찾지 못했습니다.')
        
        raid = RaidHistory.objects\
                          .create(**validated_data, time_limit=time_limit)
        return raid
    
    def validate_level(self, value):
        if not cache.get(f'level-{value}'):
            raise serializers.ValidationError('detail: 보스레이드의 유효한 레벨이 아닙니다.')
        return value
    
    class Meta:
        model  = RaidHistory
        fields = [
            'id', 'nickname', 'level', 'status', 'enter_time', 'time_limit'
        ]
        extra_kwargs = {
            'id'        : {'read_only': True},
            'status'    : {'read_only': True},
            'time_limit': {'read_only': True},
            'enter_time': {'read_only': True},
        }