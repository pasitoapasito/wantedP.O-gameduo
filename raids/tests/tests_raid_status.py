import json

from rest_framework.test import APITestCase, APIClient

from unittest      import mock
from unittest.mock import patch

from core.utils.redis_queue import RedisQueue

from users.models     import User
from raids.models     import RaidHistory
from gameduo.settings import REDIS_HOSTNAME


class BossRaidStatusFirstSuccessTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        - success test case(1개)
          * 테스트 성공 시 성공 응답코드 확인
          * API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        - token(Authentication/Authorization)
          * 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/보스레이드 정보)
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
        
        RaidHistory.objects.create(
            id         = 1,
            users      = cls.user,
            score      = 0,
            level      = 2,
            status     = 'in_progress',
            end_time   = None,
            time_limit = 180
        )
        
    """
    성공 케이스 테스트코드
    """
    
    def test_success_check_raid_status_first_case(self):
        response = self.f_client\
                       .get('/api/raids/status', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'msg'            : '이미 진행중인 보스레이드가 있습니다.',
                'can_enter'      : False,
                'entered_user_id': User.objects.get(nickname='userTest').id
            }  
        )
        

class BossRaidStatusSecondSuccessTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        - success test case(1개)
          * 테스트 성공 시 성공 응답코드 확인
          * API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        - token(Authentication/Authorization)
          * 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
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
        
    def test_success_check_raid_status_second_case(self):
        response = self.f_client\
                       .get('/api/raids/status', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'msg'            : '현재 진행중인 보스레이드가 없습니다.',
                'can_enter'      : True,
                'entered_user_id': None
            }  
        )
        

class BossRaidStatusFailTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        - fail test case(2개)
          * 테스트 실패 발생 시 실패 응답코드 확인
          * API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        - token(Authentication/Authorization)
          * 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
    3. Data mocking
        - raid static data mocking
          * 보스레이드의 요청정보를 모킹(mocking)하여 캐싱정보가 존재하지 않는 케이스 설정
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
        
        queue = RedisQueue('queue', host=f'{REDIS_HOSTNAME}', port=6379, db=2)
        queue.clear()
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_check_raid_status_due_to_unauthorized_user(self):
        response = self.client\
                       .get('/api/raids/status', content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    @patch('core.utils.redis_cache.requests') 
    def test_fail_check_raid_status_due_to_not_existed_raid_cache_data(self, mocked_requests):
        
        class MockedResponse:
            data = {
                'bossRaids': [
                    {}
                ]
            }
            content = json.dumps(data)
        
        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        
        response = self.f_client\
                       .get('/api/raids/status', content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '보스레이드의 정보를 찾지 못했습니다.'
            }
        )