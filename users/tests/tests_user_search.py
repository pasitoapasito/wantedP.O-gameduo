from datetime import datetime, timedelta

from rest_framework.test import APITestCase, APIClient

from users.models import User
from raids.models import RaidHistory


class UserSearchTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(3개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(2개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    2. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) path param(필수 파라미터)
            - user nickname
        3) query string(선택 파라미터)
            - offset/limit
              * in data range: 데이터 범위내(해당 개수의 데이터 반환)
              * out of data range: 데이터 범위밖(0개의 데이터 반환)
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
            score      = 85,
            level      = 2,
            status     = 'success',
            end_time   = (datetime.now()+timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'),
            time_limit = 180
        )
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_user_search_without_any_condition(self):
        nickname = 'userTest'
        response = self.f_client\
                       .get(f'/api/users/search/{nickname}', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'   : 'userTest',
                'total_score': 85,
                'histories': [
                    {
                    'id'        : 1,
                    'score'     : 85,
                    'level'     : 2,
                    'enter_time': (datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
                    'end_time'  : (datetime.now()+timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'),
                    'time_limit': 180,
                    'status'    : 'success'
                    }
                ]
            }  
        )
        
    def test_success_user_search_with_offset_limit_in_data_range(self):
        offset   = 0
        limit    = 1
        nickname = 'userTest'
        response = self.f_client\
                       .get(f'/api/users/search/{nickname}?offset={offset}&limit={limit}', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'   : 'userTest',
                'total_score': 85,
                'histories': [
                    {
                    'id'        : 1,
                    'score'     : 85,
                    'level'     : 2,
                    'enter_time': (datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
                    'end_time'  : (datetime.now()+timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'),
                    'time_limit': 180,
                    'status'    : 'success'
                    }
                ]
            }  
        )
    
    def test_success_user_search_with_offset_limit_out_of_data_range(self):
        offset   = 2
        limit    = 1
        nickname = 'userTest'
        response = self.f_client\
                       .get(f'/api/users/search/{nickname}?offset={offset}&limit={limit}', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'   : 'userTest',
                'total_score': 0,
                'histories': []
            }  
        )
    
    """
    실패 케이스 테스트코드
    """
    
    def test_fail_user_search_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        nickname = 'userTest'
        response = self.client\
                       .get(f'/api/users/search/{nickname}', content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
        
    def test_fail_user_search_due_to_not_existed_user(self):
        nickname = 'userTest2'
        response = self.f_client\
                       .get(f'/api/users/search/{nickname}', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '유저 userTest2는 존재하지 않습니다.'
            }
        )