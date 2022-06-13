# KUstock
건국대학교 산학협력프로젝트1 (6팀 어쩔코딩)의 프로젝트 KU-STOCK을 위한 깃허브 저장소입니다.

# 주제

카카오톡 봇을 이용한 모의 주식 투자

# 프로젝트 파일 구조

- r : 모바일 상의 `메신저봇R`에서 실행할 `rhino.js`파일을 포함한다. 
- server : 서버에서 실행할 파일을 포함한다.
- db : DBMS에서 실행할 sql파일의 초기화문을 포함한다.

# 프로그램 실행 방법
실행 환경 : python, 안드로이드 핸드폰 (메신저봇 R + 카카오톡 설치 환경)


1. 가상 환경 구축(venv)
   `cd server/django-rest-framework`
   `python -m venv project_env`
   `source project_env/bin/activate` 로 가상 환경 활성화(Linux/Mac OS)
   `cd project_env/Scripts`로 접근하여 `activate`실행 (Windows)
   `pip install -r requirements.txt`로 의존성 패키지 설치

2. DB 구축
   
   `/db/ddl.sql` 파일 통하여 db 구축 (testinit.sql로 테스트 데이터 삽입 가능)
   
3. secret.json 파일 생성

   ```json
   {
       "DJANGO_SECRET_KEY" : "django scret key needed",
       "DB_HOST" : "localhost",
       "DB_PORT" : "db port",
       "DB_PASSWORD" : "db password",
       "DB_USER" : "root",
       "DB_NAME" : "kustock",
       "api_serviceKey" : "for api service key"
   }
   ```

   secret_key와 service_key는 깃허브에 공유 불가하므로, 개인 접근 요망

4. 장고 서버 실행
   `python3 manage.py runserver`로 실행 -> default로 8000번 포트에 서버 열리는 것 확인 가능

   localhost 통한 테스트는 `server/rest-django-framework/README.md` 파일 참고

5. 안드로이드 폰 내의 메신저봇 R 어플에서 r/KuStockR.js 를 실행

6. 카카오톡 알림 활성화

7. 정상 실행 확인

