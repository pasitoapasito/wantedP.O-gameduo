from datetime import datetime, timedelta

from rest_framework.test import APITestCase, APIClient

from users.models import User
from raids.models import RaidHistory


class BossRaidRankingTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(2개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(1개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
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
        cls.f_user = User.objects\
                         .create_user(
                             email    = 'userTest@example.com',
                             nickname = 'userTest',
                             password = 'Testpassw0rd!'
                         )
                         
        cls.s_user = User.objects\
                         .create_user(
                             email    = 'userTest2@example.com',
                             nickname = 'userTest2',
                             password = 'Testpassw0rd!'
                         )
                         
        cls.t_user = User.objects\
                         .create_user(
                             email    = 'userTest3@example.com',
                             nickname = 'userTest3',
                             password = 'Testpassw0rd!'
                         )
                         
        cls.l_user = User.objects\
                         .create_user(
                             email    = 'userTest4@example.com',
                             nickname = 'userTest4',
                             password = 'Testpassw0rd!'
                         )
                       
        cls.f_client = APIClient()
        cls.f_client.force_authenticate(user=cls.f_user)
        
        cls.l_client = APIClient()
        cls.l_client.force_authenticate(user=cls.l_user)
        
        RaidHistory.objects.create(
            id         = 1,
            users      = cls.f_user,
            score      = 20,
            level      = 0,
            status     = 'success',
            end_time   = (datetime.now()+timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S'),
            time_limit = 180
        )
        
        RaidHistory.objects.create(
            id         = 2,
            users      = cls.f_user,
            score      = 47,
            level      = 1,
            status     = 'success',
            end_time   = (datetime.now()+timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'),
            time_limit = 180
        )
        
        RaidHistory.objects.create(
            id         = 3,
            users      = cls.f_user,
            score      = 85,
            level      = 2,
            status     = 'success',
            end_time   = (datetime.now()+timedelta(minutes=3)).strftime('%Y-%m-%d %H:%M:%S'),
            time_limit = 180
        )
        
        RaidHistory.objects.create(
            id         = 4,
            users      = cls.s_user,
            score      = 20,
            level      = 0,
            status     = 'success',
            end_time   = (datetime.now()+timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S'),
            time_limit = 180
        )
        
        RaidHistory.objects.create(
            id         = 5,
            users      = cls.s_user,
            score      = 47,
            level      = 1,
            status     = 'success',
            end_time   = (datetime.now()+timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'),
            time_limit = 180
        )

        RaidHistory.objects.create(
            id         = 6,
            users      = cls.t_user,
            score      = 20,
            level      = 0,
            status     = 'success',
            end_time   = (datetime.now()+timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S'),
            time_limit = 180
        )
        
        RaidHistory.objects.create(
            id         = 7,
            users      = cls.l_user,
            score      = 0,
            level      = 0,
            status     = 'fail',
            end_time   = (datetime.now()+timedelta(minutes=3)).strftime('%Y-%m-%d %H:%M:%S'),
            time_limit = 180
        )

    """
    성공 케이스 테스트코드
    """
    
    def test_success_list_raid_ranking_first_case(self):
        response = self.f_client\
                       .get('/api/raids/ranking', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'top_10_ranker': [
                    {
                        'users'      : User.objects.get(nickname='userTest').id,
                        'total_score': 152,
                        'nickname'   : 'userTest',
                        'ranking'    : 0
                    },
                    {
                        'users'      : User.objects.get(nickname='userTest2').id,
                        'total_score': 67,
                        'nickname'   : 'userTest2',
                        'ranking'    : 1
                    },
                    {
                        'users'      : User.objects.get(nickname='userTest3').id,
                        'total_score': 20,
                        'nickname'   : 'userTest3',
                        'ranking'    : 2
                    },
                    {
                        'users'      : User.objects.get(nickname='userTest4').id,
                        'total_score': 0,
                        'nickname'   : 'userTest4',
                        'ranking'    : None
                    }
                ],
                'my_ranking': {
                    'users'      : User.objects.get(nickname='userTest').id,
                    'total_score': 152,
                    'nickname'   : 'userTest',
                    'ranking'    : 0
                }
            }  
        )
    
    def test_success_list_raid_ranking_second_case(self):
        response = self.l_client\
                       .get('/api/raids/ranking', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'top_10_ranker': [
                    {
                        'users'      : User.objects.get(nickname='userTest').id,
                        'total_score': 152,
                        'nickname'   : 'userTest',
                        'ranking'    : 0
                    },
                    {
                        'users'      : User.objects.get(nickname='userTest2').id,
                        'total_score': 67,
                        'nickname'   : 'userTest2',
                        'ranking'    : 1
                    },
                    {
                        'users'      : User.objects.get(nickname='userTest3').id,
                        'total_score': 20,
                        'nickname'   : 'userTest3',
                        'ranking'    : 2
                    },
                    {
                        'users'      : User.objects.get(nickname='userTest4').id,
                        'total_score': 0,
                        'nickname'   : 'userTest4',
                        'ranking'    : None
                    }
                ],
                'my_ranking': {
                    'users'      : User.objects.get(nickname='userTest4').id,
                    'total_score': '랭킹 순위권에 존재하지 않는 점수입니다.',
                    'nickname'   : 'userTest4',
                    'ranking'    : 'userTest4님을 랭킹 TOP10 순위에서 찾을 수 없습니다.'
                }
            }  
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_list_raid_ranking_due_to_unauthorized_user(self):
        response = self.client\
                       .get('/api/raids/ranking', content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )