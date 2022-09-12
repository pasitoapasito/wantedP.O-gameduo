import json

from datetime import datetime

from rest_framework.test import APITestCase, APIClient

from unittest      import mock
from unittest.mock import patch

from core.utils.redis_queue import RedisQueue

from users.models      import User
from raids.models      import RaidHistory
from gameduo.settings  import REDIS_HOSTNAME


class BossRaidEnterSuccessTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        - success test case(1개)
          * 테스트 성공 시 성공 응답코드 확인
          * API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) request body(level)
            - 필수 파라미터 확인
            - 유효한 파라미터인지 확인
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저 정보)
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects\
                       .create_user(
                           email    = 'userTest@example.com',
                           nickname = 'userTest',
                           password = 'Testpassw0rd!'
                       )
                       
        cls.f_client = APIClient()
        cls.f_client.force_authenticate(user=cls.user)
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_enter_n_start_boss_raid(self):
        data = {
            'level': 0
        }
        
        response = self.f_client\
                       .post('/api/raids/enter', data=json.dumps(data), content_type='application/json')
    
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'msg'       : '보스레이드에 입장했습니다.',
                'is_entered': True,
                'result': {
                    'id'        : RaidHistory.objects.get(users=self.user).id,
                    'nickname'  : 'userTest',
                    'level'     : 0,
                    'status'    : 'in_progress',
                    'enter_time': (datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
                    'time_limit': 180
                }
            }
        )
        

class BossRaidEnterErrorTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        - error test case(2개)
          * 테스트 에러 발생 시 에러 응답코드 확인
          * API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) request body(level)
            - 필수 파라미터 확인
            - 유효한 파라미터인지 확인
    3. Data mocking
        - raid static data mocking
          * 보스레이드의 요청정보를 모킹(mocking)하여 캐싱정보가 존재하지 않는 케이스 설정
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/보스레이드 정보)
    """
    
    def setUp(self):
        self.user = User.objects\
                        .create_user(
                            email    = 'userTest@example.com',
                            nickname = 'userTest',
                            password = 'Testpassw0rd!'
                        )
                       
        self.f_client = APIClient()
        self.f_client.force_authenticate(user=self.user)
        
        RaidHistory.objects.create(
            id         = 1,
            users      = self.user,
            score      = 0,
            level      = 2,
            status     = 'in_progress',
            end_time   = None,
            time_limit = 180
        )
        
        queue = RedisQueue('queue', host=f'{REDIS_HOSTNAME}', port=6379, db=2)
        queue.clear()
        
    def tearDown(self):
        User.objects.all().delete()
        RaidHistory.objects.all().delete()
    
    """
    에러 케이스 테스트코드
    """
        
    @patch('core.utils.redis_cache.requests')    
    def test_error_enter_n_start_boss_raid_due_to_not_existed_raid_cache_data(self, mocked_requests):
        
        class MockedResponse:
            data = {
                'bossRaids': [
                    {}
                ]
            }
            content = json.dumps(data)
        
        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        data = {
            'level': 0
        }
        
        response = self.f_client\
                       .post('/api/raids/enter', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '보스레이드의 정보를 찾지 못했습니다.'
            }
        )
        
    def test_error_enter_n_start_boss_raid_due_to_already_in_progress_raid(self):
        data = {
            'level': 0
        }
        
        response = self.f_client\
                       .post('/api/raids/enter', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 202)
        self.assertEqual(
            response.json(),
            {
                'msg': '이미 진행중인 보스레이드가 있습니다.', 'is_entered': False,\
                'raid_history_id': 1
            }
        )
          
        
class BossRaidEnterFailTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        - fail test case(3개)
          * 테스트 실패 시 실패 응답코드 확인
          * API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) request body(level)
            - 필수 파라미터 확인
            - 유효한 파라미터인지 확인
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저 정보)
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects\
                       .create_user(
                           email    = 'userTest@example.com',
                           nickname = 'userTest',
                           password = 'Testpassw0rd!'
                       )
                       
        cls.f_client = APIClient()
        cls.f_client.force_authenticate(user=cls.user)
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_enter_n_start_boss_raid_due_to_unauthorized_user(self):
        data = {
            'level': 0
        }
        
        response = self.client\
                       .post('/api/raids/enter', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
        
    def test_fail_enter_n_start_boss_raid_due_to_level_required(self):
        data = {}
        
        response = self.f_client\
                       .post('/api/raids/enter', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'level': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
        
    def test_fail_enter_n_start_boss_raid_due_to_invalid_level(self):
        data = {
            'level': 10
        }
        
        response = self.f_client\
                       .post('/api/raids/enter', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'level': [
                    'detail: 보스레이드의 유효한 레벨이 아닙니다.'
                ]
            }
        )