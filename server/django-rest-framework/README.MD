# 실행 방법
1. 가상 환경 구축(venv) : django-restframework 디렉토리에서 아래의 것들을 해주자.
`python -m venv project_env`
`source project_env/bin/activate` 로 가상 환경 활성화 -> `deactivate`로 비활성화 할 수 있음
윈도우에서는 `cd project_env/Scripts`로 접근하여 `activate`실행해야함!
`pip install -r requirements.txt`로 의존성 패키지 설치

2. 장고 서버 실행 
  `python3 manage.py runserver`로 실행 -> default로 8000번 포트에 서버 열릴 것

3. secret.json 파일 생성

  실행했는데, 뭔가 오류가 나온다면 secret.json 파일이 안만들어졌을 수 있다. 자신의 dbms 설정을 넣어주도록 하자. mysql 기반의 dbms에서 db를 생성하고 다음과 같이 넣어주면 된다. 

  - `/db/ddl.sql` 파일 복붙해서 db 초기화 하면 됩니다. 

  (개인마다 db 정보 조금씩 다르니, 이는 각자 만들어도 git에 저장안되게 해놓았음)

  ```json
  {
      "DJANGO_SECRET_KEY" : "django-insecure-ibyt6$*8%#)^46-^607l3z#!tm03xn=_2&==mg5ix0hd!u1_e6",
      "DB_HOST" : "localhost",
      "DB_PORT" : "3306",
      "DB_PASSWORD" : "db 비밀번호",
      "DB_USER" : "root",
      "DB_NAME" : "kustock"
  }
  ```

4. 간단한 테스트

   웹 브라우저에 `http://localhost:8000/api/user/?gid=1&uname=김경호&seed=5000000`를 입력해보자. "status": "200-OK"가 나오면 성공이다~

# Django 프로젝트 구조

project(myproject)가 있고, app(myapp)이 있다. `project`는 전체 서비스에 대한 것이고, `app`은 기능에 대한 것이다. url을 통하여 오는 요청에 대하여 처리하여 결과를 보내는 서버 프로그램에서, 사용자의 모든 경로는 urls.py를 통하여 이에 적당한 app에 위임이 될 것이다. app 내에서 urls.py에서 view와 매칭을 하여 응답을 하는 형식이라고 보면 될 것 같다. view는 model에 따라 보이는 것이 달라질 수 있다. (model은 db에서 가져온 값을 직렬화하여 객체로써 갖고 있는다)

