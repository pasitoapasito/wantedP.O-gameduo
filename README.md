## Intro

> **원티드X프리온보딩 게임듀오 팀 프로젝트를 학습 목적으로 처음부터 다시 구현한 레포지토리입니다.**

- 본 프로젝트에서 요구하는 서비스는 보스레이드(PVE GAME)입니다.
- 사용자는 본 서비스에 로그인하여, 보스레이드 게임을 플레이할 수 있습니다.
- 사용자는 본 서비스에 로그인하여, 본인의 랭킹조회 및 보스레이드 상태조회를 할 수 있습니다.
- 단, 로그인하지 않은 사용자는 보스레이드 서비스를 이용할 수 없습니다.

<br>

> **Index**
- [Team Project](#team-project)
- [Environments](#environments)
- [Personal Project](#personal-project)
- [Etc](#etc)

<br>
<hr>

## Team Project

> **팀 프로젝트 소개**
- #### 👉 [팀 프로젝트 레포지토리 주소](https://github.com/F5-Refresh/gameduo)
  ```
   > 과제 제출기업: 게임듀오(gameduo)
   > 팀명: F5-Refresh
   > 팀원: 5명
   > 프로젝트 기간: 22.07.11 ~ 22.07.15
  ```
<br>
<hr>

## Environments

<br>
<div align="center">
<img src="https://img.shields.io/badge/Python-blue?style=plastic&logo=Python&logoColor=white"/>
<img src="https://img.shields.io/badge/Django-092E20?style=plastic&logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/Django Rest Framework-EE350F?style=plastic&logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/MySQL-00979D?style=plastic&logo=MySQL&logoColor=white"/>
<img src="https://img.shields.io/badge/Redis-B32024?style=plastic&logo=Redis&logoColor=white"/>
</div>

<br>
<div align="center">
<img src="https://img.shields.io/badge/AWS EC2-FF9900?style=plastic&logo=Amazon AWS&logoColor=white"/>
<img src="https://img.shields.io/badge/AWS RDS-527FFF?style=plastic&logo=Amazon RDS&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-%230db7ed.svg?style=plastic&logo=Docker&logoColor=white"/>
<img src="https://img.shields.io/badge/nginx-%23009639.svg?style=plastic&logo=NGINX&logoColor=white"/>
<img src="https://img.shields.io/badge/gunicorn-EF2D5E?style=plastic&logo=Gunicorn&logoColor=white"/>
<img src="https://img.shields.io/badge/Swagger-%23Clojure?style=plastic&logo=swagger&logoColor=white"/>
</div>

<br>
<hr>


## Personal Project

> **Period**
- #### ⚡️ 22.08.01 ~ 22.08.09(1차 기능구현)

<br>

> **Analysis**
- #### 📌 필수 구현사항
  - 사용자 관리: 
    - 유저 회원가입
      ```
      * 사용자는 이메일과 비밀번호를 통해서 회원가입을 할 수 있습니다.
      * 사용자의 이메일이 유저 ID로 사용됩니다.
      ```
    - 유저 로그인 및 로그아웃
      ```
      * 사용자는 회원가입 이후, 로그인과 로그아웃을 할 수 있습니다.
      * 사용자는 로그인 이후에 보스레이드 관련 기능을 사용할 수 있습니다.
      * 로그인하지 않은 고객은 보스레이드에 접근할 수 없습니다.
      ```
    - 유저 정보조회
      ```
      * 사용자는 특정 유저의 보스레이드 기록을 조회할 수 있습니다.
      * 보스레이드의 기록은 총점수와 참여기록을 포함해야 합니다.
      ```
  - 보스레이드 관리:
    - 보스레이드 입장(시작)
      ```
      * 사용자는 보스레이드에 입장하여 시작할 수 있습니다.
      * 단, 동시에 한 명의 유저만 보스레이드를 진행할 수 있습니다.
      ```
    - 보스레이드 종료
      ```
      * 사용자는 본인의 보스레이드를 종료(클리어)할 수 있습니다.
      * 단, 이미 실패한 보스레이드는 종료할 수 없습니다.
      ```
    - 보스레이드 상태조회
      ```
      * 사용자는 보스레이드의 현재 입장가능 상태를 조회할 수 있습니다.
      * 현재 보스레이드를 진행중인 유저가 있다면, 사용자는 해당 유저의 정보를 제공 받습니다.
      * 현재 보스레이드를 진행중인 유저가 없다면, 사용자는 보스레이드의 시작가능 정보를 제공 받습니다.
      ```
    - 보스레이드 랭킹조회
      ```
      * 사용자는 보스레이드의 랭킹을 조회할 수 있습니다.
      * 사용자는 본인의 랭킹도 함께 조회할 수 있습니다.
      * 단, 사용자는 본인의 랭킹이 순위권일 경우에만 랭킹정보를 제공받습니다.
      ```
      
- #### 📌 선택 구현사항     
  - 레디스(Redis)를 사용하여 랭킹조회 기능 구현 시 가산점이 있습니다.
  - Static Data를 캐싱할 경우 가산점이 있습니다.
 
- #### 📌 평가요소
  - 요구한 기능들이 잘 잘동하는지를 평가합니다.
  - 동시성 문제를 고려하는지를 평가합니다.
  - 레이어 계층을 잘 분리하였는지를 평가합니다.
  - 발생할 수 있는 다양한 에러상황을 잘 처리하였는지를 평가합니다.
 
<br>

> **Development**
- #### 🔥 프로젝트 구현기능
  - 사용자 관리:
    - 유저 회원가입
      ```
      > 유저 회원가입 기능입니다.
      
      * 이메일, 닉네임, 패스워드는 필수값입니다.
      * 전화번호, 프로필 이미지는 선택값입니다.
      * 이메일, 닉네임은 중복되지 않습니다.
      * 패스워드는 반드시 8~20자리의 최소 1개의 소문자/대문자/숫자/(숫자키)특수문자로 구성됩니다.
      * 패스워드는 해싱 후 DB에 저장됩니다.
      ```
    - 유저 로그인
      ```
      > 유저 로그인 기능입니다.
      
      * DRF-SimpleJwt 라이브리러를 활용했습니다.
      * 이메일, 패스워드는 필수값입니다.
      * 입력받은 이메일과 패스워드가 유저 정보와 일치하는지 확인합니다.
      * 모든 유효성 검사에 통과하면 액세스토큰과 리프레시 토큰을 발급합니다.
      ```
    - 유저 로그아웃
      ```
      > 유저 로그아웃 기능입니다.
      
      * DRF-SimpleJwt 라이브리러를 활용했습니다.
      * 리프레시 토큰은 필수값입니다.
      * 유효한 토큰인지를 확인합니다.
      * 만료된 토큰인지를 확인합니다.
      * 모든 유효성 검사에 통과하면 요청받은 리프레시 토큰을 토큰 블랙리스트에 등록합니다.
      * 단, 기존에 발급된 리프레시 토큰은 모두 사용을 제한합니다.
      ```
    - 유저 토큰 재발급
      ```
      > 유저의 토큰을 재발급하는 기능입니다.
      
      * DRF-SimpleJwt의 TokenRefreshView 기능을 활용했습니다.
      * 리프레시 토큰은 필수값입니다.
      * 유효한 토큰인지를 확인합니다.
      * 만료된 토큰인지를 확인합니다.
      * 토큰의 타입을 확인합니다.(오직 리프레시 토큰만 사용가능)
      * 모든 유효성 검사에 통과하면 요청받은 리프레시 토큰을 기반으로 액세스토큰을 발급합니다.
      * 단, 리프레시 토큰은 추가로 발급하지 않습니다.
      ```
    - 유저 정보조회
      ```
      > 인증/인가에 통과한 사용자는 특정 유저의 보스레이드 관련 정보를 조회할 수 있습니다.
      
      * 유저 닉네임은 필수값입니다.(path parameter)
      * offset, limit값을 입력하여 원하는 크기의 데이터를 요청할 수 있습니다.(query string)
      * 해당 요청으로 입력받은 유저정보의 존재여부를 확인합니다.
      * 모든 유효성 검사에 통과하면 해당 유저의 닉네임, 총 점수, 보스레이드 히스토리 내역을 반환합니다.
      ```
  - 보스레이드 관리:
    - 보스레이드 생성
      ```
      > 인증/인가에 통과한 사용자는 보스레이드에 입장하여 시작할 수 있습니다.
      
      * 보스레이드 입장 요청이 들어오면 보스레이드의 캐싱정보를 초기화합니다.
      * 동시에 한 명의 유저만 보스레이드를 진행할 수 있기 때문에, 동시성 문제를 방지하고자 Redis Queue를 활용했습니다.
      * 즉, Redis Queue를 활용하여 유저 대기열을 만들고 가장 먼저 요청한 유저만 입장을 허용했습니다.(나머지 유저는 입장제한)
      * 보스레이드 입장이 성공적으로 이루어지면, 유저 대기열 및 보스레이드 정보를 모두 삭제합니다.
      * 이미 보스레이드가 진행중이라면 입장할 수 없습니다.(status code: 202)
      * 보스레이드가 시작되면 제한시간 내에 클리어해야 합니다.
      * 만약, 제한시간 내에 클리어하지 못할 경우 자동으로 실패처리 됩니다.(django background tasks 라이브러리 활용)
      * 보스레이드의 캐싱정보가 존재하지 않으면 에러를 반환합니다.
      ```
    - 보스레이드 종료
      ```
      > 인증/인가에 통과한 사용자는 본인의 보스레이드를 종료할 수 있습니다.
      
      * 보스레이드 종료 요청이 들어오면 보스레이드의 캐싱정보를 초기화합니다.
      * 존재하지 않는 보스레이드는 종료할 수 없습니다.
      * 본인의 보스레이드만 종료할 수 있습니다.
      * 현재 진행중인 보스레이드만 종료할 수 있습니다.
      * 즉, 이미 실패하거나 제한시간을 초과한 보스레이드는 종료할 수 없습니다.
      * 보스레이드를 성공적으로 종료하면, 보스레이드의 점수와 종료시간을 할당합니다.
      * 보스레이드를 성공적으로 종료하면, 보스레이드를 강제종료 시키는 background task도 함께 삭제합니다.
      ```
    - 보스레이드 상태조회
      ```
      > 인증/인가에 통과한 사용자는 보스레이드의 상태정보를 조회할 수 있습니다.
      
      * 이미 진행중인 보스레이드가 있으면, 보스레이드를 진행중인 유저정보와 입장불가 정보를 함께 반환합니다.
      * 현재 진행중인 보스레이드가 없다면, 입장가능 정보를 반환합니다.
      * 보스레이드의 캐싱정보가 존재하지 않으면 에러를 반환합니다.
      ```
    - 보스레이드 랭킹조회
      ```
      > 인증/인가에 통과한 사용자는 보스레이드의 랭킹정보를 조회할 수 있습니다.
      
      * 보스레이드의 상위권 TOP10 랭킹정보를 조회합니다.
      * 보스레이드 랭킹조회 요청 시, 사용자의 기록이 랭킹 순위권에 존재하는지 확인합니다.
      * 랭킹 순위권에 사용자의 기록이 존재할 경우, 사용자의 랭킹정보를 함께 반환합니다.
      * 랭킹 순위권에 사용자의 기록이 존재하지 않을 경우, 사용자의 기록이 순위권 밖이라는 메세지를 반환합니다.
      * 보스레이드의 캐싱정보가 존재하지 않으면 에러를 반환합니다.
      ```
       
<br>

> **Modeling**
- #### 🚀 ERD 구조
  <img width="1000px" alt="스크린샷 2022-08-11 09 23 13" src="https://user-images.githubusercontent.com/89829943/184044960-1e7cb945-e5b3-418f-931d-23b1d14cab7d.png">

<br> 

> **API Docs**
- #### 🌈 API 명세서
  |ID|Feature|Method|URL|
  |---|----------|----|----|
  |1|유저 회원가입|POST|api/users/signup|
  |2|유저 로그인|POST|api/users/signin|
  |3|유저 로그아웃|POST|api/users/signout|
  |4|유저 토큰 재발급|POST|api/users/token/refresh|
  |5|유저 정보조회|GET|api/users/search/<str:nickname>|
  |6|보스레이드 입장(시작)|POST|api/raids/enter|
  |7|보스레이드 종료|PATCH|api/raids/<int:raid_history_id>/end|
  |8|보스레이드 상태조회|GET|api/raids/status|
  |9|보스레이드 랭킹조회|GET|api/raids/ranking|
 
- #### ✨ Swagger UI
  #### ```✔️ 유저 회원가입``` 
  <img width="1000px" alt="스크린샷 2022-07-29 11 13 53" src="https://user-images.githubusercontent.com/89829943/181668672-d319ebc3-a0bf-4b0a-8163-ee0a21598b1b.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 14 16" src="https://user-images.githubusercontent.com/89829943/181668695-175afa5d-5223-4d98-a562-c09333658c4d.png">
  
  #### ```✔️ 유저 로그인```
  <img width="1000px" alt="스크린샷 2022-07-29 11 17 19" src="https://user-images.githubusercontent.com/89829943/181668976-e847610d-5dd0-4fab-a5fc-c5305b1d90ea.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 17 35" src="https://user-images.githubusercontent.com/89829943/181668993-bbab822b-1c93-49fa-a5d8-b6942beede35.png">
  
  #### ```✔️ 유저 로그아웃```
  <img width="1000px" alt="스크린샷 2022-07-29 11 21 01" src="https://user-images.githubusercontent.com/89829943/181669401-7540c353-7cdf-41ce-865a-2b3951a0a28b.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 19 44" src="https://user-images.githubusercontent.com/89829943/181669231-9b567817-0029-4f72-b16e-8578a9e2c381.png">

  #### ```✔️ 유저 토큰 재발급```
  <img width="1000px" alt="스크린샷 2022-07-29 11 22 49" src="https://user-images.githubusercontent.com/89829943/181669666-dc0f3a3c-e93c-4606-bd80-536e445f639a.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 23 06" src="https://user-images.githubusercontent.com/89829943/181669682-b09f3740-e2b1-439c-99bf-ebd5abd633bc.png">

  #### ```✔️ 유저 정보조회```
  <img width="1000px" alt="스크린샷 2022-08-11 11 11 13" src="https://user-images.githubusercontent.com/89829943/184053596-43b06a1d-170e-4d75-8616-6d9f16d2b75f.png">
  <img width="1000px" alt="스크린샷 2022-08-11 11 12 01" src="https://user-images.githubusercontent.com/89829943/184053622-28e64be0-247e-4b21-9049-4e454f60c906.png">

  #### ```✔️ 보스레이드 입장```
  <img width="1000px" alt="스크린샷 2022-08-11 11 13 55" src="https://user-images.githubusercontent.com/89829943/184053761-10fcd951-4946-406d-80fc-3aa7184d8ab0.png">
  <img width="1000px" alt="스크린샷 2022-08-11 11 14 15" src="https://user-images.githubusercontent.com/89829943/184053780-38ae62bc-94f1-4ab1-83ec-e08d76a6a6c1.png">

  #### ```✔️ 보스레이드 종료```
  <img width="1000px" alt="스크린샷 2022-08-11 11 15 35" src="https://user-images.githubusercontent.com/89829943/184053918-e5208ee7-47cb-4849-9000-ef1c2dfe54a2.png">
  <img width="1000px" alt="스크린샷 2022-08-11 11 16 04" src="https://user-images.githubusercontent.com/89829943/184053925-ba623c3d-3f37-46d9-8c8e-a5382da44e24.png">

  #### ```✔️ 보스레이드 상태조회```
  <img width="1000px" alt="스크린샷 2022-08-11 11 18 04" src="https://user-images.githubusercontent.com/89829943/184054111-d78f76b4-103c-457d-a44e-b31a62cb15ab.png">
  <img width="1000px" alt="스크린샷 2022-08-11 11 18 32" src="https://user-images.githubusercontent.com/89829943/184054129-9f2ea3e4-12a0-46aa-8860-dc0938be97c2.png">

  #### ```✔️ 보스레이드 랭킹조회```
  <img width="1000px" alt="스크린샷 2022-08-11 11 26 48" src="https://user-images.githubusercontent.com/89829943/184054957-224bef9d-3602-4478-8b56-cfb3ca908bb8.png">
  <img width="1000px" alt="스크린샷 2022-08-11 11 27 05" src="https://user-images.githubusercontent.com/89829943/184054967-3d342a31-1d08-475f-8893-1377fa38b220.png">

<br> 

> **Deploy**
- #### 🏖 프로젝트 배포
  #### Docker, Nginx, Gunicorn을 사용하여 AWS EC2 서버에 배포했으며, 비용 등의 이유로 현재는 배포를 중단했습니다.
  <img width="1000px" alt="스크린샷 2022-08-11 11 56 07" src="https://user-images.githubusercontent.com/89829943/184057633-fac6bfdd-ff66-4c47-b737-5ff65e3ebbe1.png">


<br> 

> **Test**
- #### 🚦 테스트코드 작성
  #### 현재 테스트코드 작성중
  
<br> 

> **Issue**
- #### ⏰ 프로젝트 일정관리
  #### 프로젝트 진행사항을 칸반보드와 이슈티켓으로 관리했습니다.
  <img width="1000px" alt="스크린샷 2022-08-04 09 10 46" src="https://user-images.githubusercontent.com/89829943/184055328-0252f2eb-676a-4211-9153-5165b8982f56.png">

<br>
<hr>

## Etc

> **Guides**
- #### ⚙️ 프로젝트 설치방법
  #### ```✔️ 로컬 개발 및 테스트용```
  
  1. 해당 프로젝트를 clone하고, 프로젝트 폴더로 이동합니다.
  <br>
  
   ```
   git clone https://github.com/pasitoapasito/wantedP.O-gameduo.git
   cd project directory
   ```
  
  2. 가상환경을 만들고, 프로젝트에 필요한 python package를 다운받습니다.
  <br>
  
  ```
  conda create --name project-name python=3.9
  conda activate project-name
  pip install -r requirements.txt
  ```
  
  3. manage.py 파일과 동일한 위치에서 환경설정 파일을 만듭니다.
  <br>
  
  ```
  ex) .env file 
  
  ## general ##
  DEBUG         = True
  ALLOWED_HOSTS = ALLOWED_HOSTS
  SECRET_KEY    = SECRET_KEY

  ## Docker DB ##
  MYSQL_TCP_PORT      = '3306'
  MYSQL_DATABASE      = MYSQL_DATABASE
  MYSQL_ROOT_PASSWORD = MYSQL_ROOT_PASSWORD
  MYSQL_USER          = MYSQL_USER
  MYSQL_PASSWORD      = MYSQL_PASSWORD

  ## AWS RDS ##
  RDS_HOSTNAME = RDS_HOSTNAME
  RDS_DB_NAME  = RDS_DB_NAME
  RDS_USERNAME = RDS_USERNAME
  RDS_PASSWORD = RDS_PASSWORD
  RDS_PORT     = '3306'
  
  ## Docker Redis ##
  REDIS_HOSTNAME = 'localhost'
  ```
  
  4. project-name/settings.py에서 DB설정을 적절하게 변경합니다.
  <br>
  
  ```
  Docker로 DB를 구축하는 경우 or AWS RDS로 DB를 구축하는 경우 등
  다양한 방법으로 DB를 구축하는 경우에 맞게 DB 설정을 변경합니다.
  
  
  ## Docker DB ##
  '''
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('MYSQL_DATABASE'),
          'USER'    : 'root',
          'PASSWORD': get_env_variable('MYSQL_ROOT_PASSWORD'),
          'HOST'    : 'localhost',
          'PORT'    : get_env_variable('MYSQL_TCP_PORT'),
      }
  }
  '''
  
  ## AWS RDS ##
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('RDS_DB_NAME'),
          'USER'    : get_env_variable('RDS_USERNAME'),
          'PASSWORD': get_env_variable('RDS_PASSWORD'),
          'HOST'    : get_env_variable('RDS_HOSTNAME'),
          'PORT'    : get_env_variable('RDS_PORT'),
          'OPTIONS' : {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
      }
  }
  ```
  
  5. DB의 Table 구조를 최신 modeling에 맞게 설정합니다.
  <br>
  
  ```
  python manage.py migrate
  ```
  
  6. 개발용 서버와 백그라운드 태스크를 실행합니다.
  <br>
  
  ```
  > 참고: 각각 다른 터미널에서 실행해야 합니다.
  
  python manage.py runserver 0:8000 (장고 개발서버)
  python manage.py process_tasks &  (장고 백그라운드 태스트)
  ```

  #### ```✔️ 배포용```
  1. 배포용 서버에서 해당 프로젝트를 clone하고, 프로젝트 폴더로 이동합니다.
  <br>
  
  ```
  git clone https://github.com/pasitoapasito/wantedP.O-gameduo.git
  cd project directory
  ```
  
  2. manage.py 파일과 동일한 위치에서 도커 환경설정 파일을 만듭니다.
  <br>
  
  ```
  ex) .env file 
  
  ## general ##
  DEBUG         = True
  ALLOWED_HOSTS = ALLOWED_HOSTS
  SECRET_KEY    = SECRET_KEY

  ## Docker DB ##
  MYSQL_TCP_PORT      = '3306'
  MYSQL_DATABASE      = MYSQL_DATABASE
  MYSQL_ROOT_PASSWORD = MYSQL_ROOT_PASSWORD
  MYSQL_USER          = MYSQL_USER
  MYSQL_PASSWORD      = MYSQL_PASSWORD

  ## AWS RDS ##
  RDS_HOSTNAME = RDS_HOSTNAME
  RDS_DB_NAME  = RDS_DB_NAME
  RDS_USERNAME = RDS_USERNAME
  RDS_PASSWORD = RDS_PASSWORD
  RDS_PORT     = '3306'
  
  ## Docker Redis ##
  REDIS_HOSTNAME = 'redis'
  ```
  
  3. project-name/settings.py에서 DB설정을 적절하게 변경합니다.
  <br>
  
  ```
  Docker로 DB를 구축하는 경우 or AWS RDS로 DB를 구축하는 경우 등
  다양한 방법으로 DB를 구축하는 경우에 맞게 DB 설정을 변경합니다.
  
  
  ## Docker DB ##
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('MYSQL_DATABASE'),
          'USER'    : 'root',
          'PASSWORD': get_env_variable('MYSQL_ROOT_PASSWORD'),
          'HOST'    : 'db',
          'PORT'    : get_env_variable('MYSQL_TCP_PORT'),
      }
  }
  
  '''
  ## AWS RDS ##
  DATABASES = {
      'default': {
          'ENGINE'  : 'django..backends.mysql',
          'NAME'    : get_env_variable('RDS_DB_NAME'),
          'USER'    : get_env_variable('RDS_USERNAME'),
          'PASSWORD': get_env_variable('RDS_PASSWORD'),
          'HOST'    : get_env_variable('RDS_HOSTNAME'),
          'PORT'    : get_env_variable('RDS_PORT'),
          'OPTIONS' : {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
      }
  }
  '''
  ```
  
  4. docker-compose 명령을 사용하여 Nginx, Redis, DB, Django 컨테이너를 실행시킵니다.
  <br>
  
  ```
  docker-compose -f ./docker-compose.yml up (-d)
  ```

<br>

> **Structure**
- #### 🛠 프로젝트 폴더구조
  ```
  📦cache
  ┗ 📜dump.rdb
  📦config
  ┗ 📂nginx
  ┃ ┗ 📜nginx.conf
  📦core
  ┣ 📂migrations
  ┃ ┗ 📜__init__.py
  ┣ 📂utils
  ┃ ┣ 📜check_obj_status.py
  ┃ ┣ 📜decorator.py
  ┃ ┣ 📜get_obj_n_check_err.py
  ┃ ┣ 📜redis_cache.py
  ┃ ┣ 📜redis_queue.py
  ┃ ┗ 📜redis_ranking.py
  ┣ 📜__init__.py
  ┣ 📜admin.py
  ┣ 📜apps.py
  ┣ 📜models.py
  ┣ 📜tests.py
  ┗ 📜views.py
  📦gameduo
  ┣ 📜__init__.py
  ┣ 📜asgi.py
  ┣ 📜settings.py
  ┣ 📜urls.py
  ┗ 📜wsgi.py
  📦raids
  ┣ 📂migrations
  ┃ ┣ 📜0001_initial.py
  ┃ ┣ 📜0002_alter_raidhistory_time_limit.py
  ┃ ┗ 📜__init__.py
  ┣ 📂views
  ┃ ┣ 📜raid_end.py
  ┃ ┣ 📜raid_enter.py
  ┃ ┣ 📜raid_ranking.py
  ┃ ┗ 📜raid_status.py
  ┣ 📜__init__.py
  ┣ 📜admin.py
  ┣ 📜apps.py
  ┣ 📜models.py
  ┣ 📜serializers.py
  ┣ 📜tests.py
  ┗ 📜urls.py
  📦users
  ┣ 📂migrations
  ┃ ┣ 📜0001_initial.py
  ┃ ┗ 📜__init__.py
  ┣ 📂views
  ┃ ┣ 📜user_search.py
  ┃ ┣ 📜user_signin.py
  ┃ ┣ 📜user_signout.py
  ┃ ┗ 📜user_signup.py
  ┣ 📜__init__.py
  ┣ 📜admin.py
  ┣ 📜apps.py
  ┣ 📜models.py
  ┣ 📜serializers.py
  ┣ 📜tests.py
  ┗ 📜urls.py
  ┣ 📜.env
  ┣ 📜.gitignore
  ┣ 📜docker-compose.yml
  ┣ 📜Dockerfile
  ┣ 📜manage.py
  ┣ 📜README.md
  ┗ 📜requirements.txt
  ```
  
