import os, json, requests

from django.core.cache import cache
from django.core.wsgi  import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameduo.settings')

application = get_wsgi_application()


"""
CACHE SETTINGS
- 장고 서버가 시작할 때 보스레이드 정보를 cache에 저장합니다.

* 보스레이드 요청 데이터 반환 형태
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