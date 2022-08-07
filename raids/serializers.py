from datetime import datetime

from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer

from django.db         import transaction
from django.core.cache import cache

from raids.models           import RaidHistory
from background_task.models import Task


class BossRaidEnterSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail: 보스레이드 입장 시리얼라이저[POST 기능 유효성 검사]
    model: RaidHistory
    """
    
    nickname   = serializers.SerializerMethodField()
    enter_time = serializers.SerializerMethodField()
    
    def get_nickname(self, obj: RaidHistory) -> str:
        return obj.users.nickname
        
    def get_enter_time(self, obj: RaidHistory) -> str:
        return (obj.enter_time).strftime('%Y-%m-%d %H:%M:%S')
       
    def create(self, validated_data) -> object:
        """
        보스레이드 히스토리 생성
        - 보스레이드의 캐싱정보 활용(제한시간)
        """ 
        time_limit = cache.get('limit_time')
        if not time_limit:
            raise serializers.ValidationError('detail: 보스레이드의 정보를 찾지 못했습니다.')
        
        raid = RaidHistory.objects\
                          .create(**validated_data, time_limit=time_limit)
        return raid
     
    def validate_level(self, value) -> int:
        """
        보스레이드 히스토리 유효성 검사(컬럼 레벨)
        - 보스레이드 캐싱정보에 존재하는 레벨이 아니면 에러 반환
        """
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
    """
    Assignee: 김동규
    
    detail: 보스레이드 종료 시리얼라이저[PATCH 기능 유효성 검사]
    model: RaidHistory
    """
    
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
        """
        보스레이드 종료(데이터 수정)
          - 유효성 검사
            * 보스레이드 종료 필수 입력값 확인(레벨정보)
            * 보스레이드 캐싱정보 확인 및 활용(제한시간) 
            * 보스레이드 레벨 유효성 확인
            * 보스레이드 진행여부 확인(이미 종료된 보스레이드는 종료할 수 없음)
        """
        
        """
        필수 입력값(레벨정보) 유효성 검사 
        """
        level = validated_data.pop('level', None)
        if level is None:
            raise serializers.ValidationError('detail: 보스레이드의 레벨은 필수 입력값입니다.')
        
        """
        보스레이드 캐싱정보(점수) 존재여부 유효성 검사
        """
        score = cache.get(f'level-{level}')
        if score is None:
            raise serializers.ValidationError('detail: 보스레이드의 정보를 찾지 못했습니다.')
        
        """
        보스레이드 레벨 유효성 검사
        """
        if not instance.level == level:
            raise serializers.ValidationError('detail: 보스레이드의 레벨을 잘못 입력했습니다.')
        
        """
        보스레이드 상태(진행여부) 유효성 검사
        """
        if instance.status == 'fail':
            raise serializers.ValidationError('detail: 보스레이드를 제한시간 내에 클리어하지 못했습니다.')
        
        instance.score    = score
        instance.status   = 'success'
        instance.end_time = datetime.now()
        
        """
        보스레이드 강제종료 백그라운드 태스크(TASK) 삭제
        """
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
        
        
class BossRaidStatusSerializer(ModelSerializer):
    """
    Assignee: 김동규
    
    detail: 보스레이드 상태조회 시리얼라이저[GET 기능 유효성 검사]
    model: RaidHistory
    """
    
    user_id = serializers.SerializerMethodField()
    
    def get_user_id(self, obj: RaidHistory) -> int:
        return obj.users.id
    
    class Meta:
        model  = RaidHistory
        fields = [
            'id', 'user_id', 'status', 'level', 'score', 'enter_time',\
            'time_limit'
        ]
        extra_kwargs = {
            'id': {'read_only': True}
        }
        

class BossRaidStatusSchema(serializers.Serializer):
    """
    Assignee: 김동규
    
    detail: 보스레이드 상태조회 스키마 시리얼라이저[only used for swagger]
    """
    
    msg             = serializers.CharField(max_length=200)
    can_enter       = serializers.BooleanField()
    entered_user_id = serializers.IntegerField(allow_null=True)