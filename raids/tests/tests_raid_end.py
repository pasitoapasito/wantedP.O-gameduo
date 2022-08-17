import json

from datetime import datetime, timedelta

from rest_framework.test import APITestCase, APIClient

from users.models import User
from raids.models import RaidHistory


class BossRaidEndTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(7개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) path param(필수 파라미터)
            - raid obj:
              * 존재하는 보스레이드인지 확인
              * 본인의 보스레이드인지 확인
        3) request body(level)
            - 필수 파라미터 확인
            - 유효한 파라미터인지 확인
              * 레벨정보가 일치하는지 확인
              * 캐싱정보 내에 존재하는 레벨정보인지 확인
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/보스레이드 정보)
    """
    
    def setUp(self):
        self.f_user = User.objects\
                          .create_user(
                              email    = 'userTest@example.com',
                              nickname = 'userTest',
                              password = 'Testpassw0rd!'
                          )

        self.s_user = User.objects\
                          .create_user(
                              email    = 'testUser@example.com',
                              nickname = 'testUser',
                              password = 'Testpassw3rd!'
                          )
                          
        self.f_client = APIClient()
        self.f_client.force_authenticate(user=self.f_user)
        
        RaidHistory.objects.create(
            id         = 1,
            users      = self.f_user,
            score      = 0,
            level      = 2,
            status     = 'in_progress',
            end_time   = None,
            time_limit = 180
        )
        
        RaidHistory.objects.create(
            id         = 2,
            users      = self.s_user,
            score      = 47,
            level      = 1,
            status     = 'success',
            end_time   = datetime.now()+timedelta(minutes=1),
            time_limit = 180
        )
        
        RaidHistory.objects.create(
            id         = 3,
            users      = self.f_user,
            score      = 0,
            level      = 0,
            status     = 'fail',
            end_time   = datetime.now()+timedelta(minutes=3),
            time_limit = 180
        )
    
    def tearDown(self):
        User.objects.all().delete()
        RaidHistory.objects.all().delete()
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_end_boss_raid(self):
        data = {
            'level': 2
        }
        
        response = self.f_client\
                       .patch('/api/raids/1/end', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'msg'   : '보스레이드를 성공적으로 클리어했습니다.',
                'result': {
                    'id'        : 1,
                    'nickname'  : 'userTest',
                    'level'     : 2,
                    'status'    : 'success',
                    'enter_time': (datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
                    'end_time'  : (datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
                    'score'     : 85,
                    'time_limit': 180
                }
            }
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_end_boss_raid_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        data = {
            'level': 2
        }
        
        response = self.client\
                       .patch('/api/raids/1/end', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    def test_fail_end_boss_raid_due_to_level_required(self):
        data = {}
        
        response = self.f_client\
                       .patch('/api/raids/1/end', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            [
                'detail: 보스레이드의 레벨은 필수 입력값입니다.'
            ]
        )
        
    def test_fail_end_boss_raid_due_to_invalid_level(self):
        data = {
            'level': 1
        }
        
        response = self.f_client\
                       .patch('/api/raids/1/end', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            [
                'detail: 보스레이드의 레벨을 잘못 입력했습니다.'
            ]
        )
        
    def test_fail_end_boss_raid_due_to_out_of_cache_level_range(self):
        data = {
            'level': 10
        }
        
        response = self.f_client\
                       .patch('/api/raids/1/end', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            [
                'detail: 보스레이드의 정보를 찾지 못했습니다.'
            ]
        )
    
    def test_fail_end_boss_raid_due_to_not_existed_raid(self):
        data = {
            'level': 2
        }
        
        response = self.f_client\
                       .patch('/api/raids/10/end', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '보스레이드 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_end_boss_raid_due_to_not_own_raid(self):
        data = {
            'level': 2
        }

        response = self.f_client\
                       .patch('/api/raids/2/end', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 보스레이드입니다.'
            }
        )
    
    def test_fail_end_boss_raid_due_to_already_failed_raid(self):
        data = {
            'level': 0
        }

        response = self.f_client\
                       .patch('/api/raids/3/end', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            [
                'detail: 보스레이드를 제한시간 내에 클리어하지 못했습니다.'
            ]
        )