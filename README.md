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
  - 작성중

