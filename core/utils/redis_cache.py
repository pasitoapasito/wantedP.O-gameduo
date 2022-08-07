import json, requests

from django.core.cache import cache


class RedisCache:
    """
    Assignee: 김동규
    
    detail:
      > Cache Settings
        * 보스레이드 정보를 요청하여 레디스에 캐싱(저장)함
        * 캐싱정보를 받아오지 못하거나 캐싱정보가 부족할 경우 에러 메세지를 출력함

      > 보스레이드 요청 데이터 반환 형태(json)
        {
          'bossRaids': [
            {
              'bossRaidLimitSeconds': 180,
              'levels': [
                {
                  'level': 0,
                  'score': 20
                },
                {
                  'level': 1,
                  'score': 47
                },
                {
                  'level': 2,
                  'score': 85
                }
              ]
            }
          ]
        }
    """    
    def set_raid_data_in_cache():
        URL          = 'https://dmpilf5svl7rv.cloudfront.net'
        ASSIGNMENT   = 'assignment'
        BACKEND      = 'backend'
        BOSSRAIDDATA = 'bossRaidData' 
        TYPE         = 'json'
        
        try:
            url = URL + '/{}/{}/{}.{}'.format(
                            ASSIGNMENT,
                            BACKEND,
                            BOSSRAIDDATA,
                            TYPE,
                        )

            res  = requests.get(url)
            data = json.loads(res.content)
            
            limit_time = data['bossRaids'][0]['bossRaidLimitSeconds']
            levels     = data['bossRaids'][0]['levels']
            
            cache.set('limit_time', limit_time, timeout=None)
            
            for raid in levels:
                level = raid['level']
                score = raid['score']
                
                cache.set(f'level-{level}', score, timeout=None)

        except KeyError:
            print({'detail': '보스레이드 정보가 존재하지 않습니다.', 'status': 500})