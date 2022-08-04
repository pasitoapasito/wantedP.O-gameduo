from datetime import datetime

from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer

from django.db         import transaction
from django.core.cache import cache

from raids.models           import RaidHistory
from background_task.models import Task


class BossRaidEnterSerializer(ModelSerializer):
    nickname = serializers.SerializerMethodField()
    enter_time = serializers.SerializerMethodField()
    
    def get_nickname(self, obj: RaidHistory) -> str:
        return obj.users.nickname
        
    def get_enter_time(self, obj: RaidHistory) -> str:
        return (obj.enter_time).strftime('%Y-%m-%d %H:%M:%S')
        
    def create(self, validated_data) -> object:
        time_limit = cache.get('limit_time')
        if not time_limit:
            raise serializers.ValidationError('detail: 보스레이드의 정보를 찾지 못했습니다.')
        
        raid = RaidHistory.objects\
                          .create(**validated_data, time_limit=time_limit)
        return raid
    
    def validate_level(self, value) -> int:
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
        

class BossRaidEndSerializer(ModelSerializer):
    nickname   = serializers.SerializerMethodField()
    enter_time = serializers.SerializerMethodField()
    end_time   = serializers.SerializerMethodField()
    
    def get_nickname(self, obj: RaidHistory) -> str:
        return obj.users.nickname
    
    def get_enter_time(self, obj: RaidHistory) -> str:
        return (obj.enter_time).strftime('%Y-%m-%d %H:%M:%S')
    
    def get_end_time(self, obj: RaidHistory) -> str:
        return (obj.end_time).strftime('%Y-%m-%d %H:%M:%S')
    
    @transaction.atomic()
    def update(self, instance: RaidHistory, validated_data) -> object:
        level = validated_data.pop('level', None)
        if level is None:
            raise serializers.ValidationError('detail: 보스레이드의 레벨은 필수 입력값입니다.')
        
        score = cache.get(f'level-{level}')
        if score is None:
            raise serializers.ValidationError('detail: 보스레이드의 정보를 찾지 못했습니다.')
        
        if not instance.level == level:
            raise serializers.ValidationError('detail: 보스레이드의 레벨을 잘못 입력했습니다.')
        
        if instance.status == 'fail':
            raise serializers.ValidationError('detail: 보스레이드를 제한시간 내에 클리어하지 못했습니다.')
        
        instance.score    = score
        instance.status   = 'success'
        instance.end_time = datetime.now()
        
        tasks = Task.objects\
                    .filter(task_name='core.utils.check_obj_status.check_raid_time')
            
        for task in tasks:
            task.delete()
        
        instance.save()
        return instance        
    
    class Meta:
        model  = RaidHistory
        fields = [
            'id', 'nickname', 'level', 'status', 'enter_time', 'end_time',\
            'score', 'time_limit'
        ]
        extra_kwargs = {
            'id'        : {'read_only': True},
            'score'     : {'read_only': True},
            'status'    : {'read_only': True},
            'enter_time': {'read_only': True},
            'time_limit': {'read_only': True},
        }