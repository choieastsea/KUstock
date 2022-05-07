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


# 서버 api 연동 확인

1. anaconda에 가상환경 32bit interpreter 설치(참고: https://baessi.tistory.com/125)

2. 가상환경이 생성된 후 anaconda prompt를 관리자 권한으로 실행, `activate '가상환경 이름'`으로 가상환경 실행.
prompt의 맨앞이 해당 가상환경의 이름으로 바뀌면 실행완료. ex) (base) --> (creaon32)
가상환경이 실행되고 32bit임을 확인. `python`, `import platform` 후 `platform.architecture()`했을시 32BIT라고 나오면 됨. 

3. 가상환경의 경로를 Django서버 실행 코드가 있는 위치로 바꿔주고, python manage.py runserver로 실행.

4. 웹 브라우저에 127.0.0.1:포트/api/check실행 했을때, prompt에 연결성공이라고 나오면 성공~

# 테스트 url 문구

기본 테스트
```
http://localhost:8000/api/test?room=테스트&id=테스터&msg=/test
```
/help 테스트
```
http://localhost:8000/api/help?room=테스트&id=테스터&msg=/help
http://localhost:8000/api/help?room=테스트&id=테스터&msg=/help user
```
/trade 테스트
```
http://localhost:8000/api/trade?room=테스트&id=테스터&msg=/trade buy 삼성 10
http://localhost:8000/api/trade?room=테스트&id=테스터&msg=/trade sell 삼성 10
http://localhost:8000/api/trade?room=테스트&id=테스터&msg=/trade sell 삼성 십
```
/community 테스트
```
http://localhost:8000/api/community?room=테스트&id=테스터&msg=/community rank
http://localhost:8000/api/community?room=테스트&id=테스터&msg=/community 테스터
```

# ⭐️메소드 작성 요령⭐️

url 요청이 들어왔을 때, `myserver`의 `urls.py` 에서, `path('api/',include('myapp.urls'))`에 의하여 `myapp`의 `urls.py`로 매핑되어 전달될 것이다. localhost:8000/api/로 시작하는 모든 url요청은 밑의 파일로 넘어가게 된다.

```python
#myapp/urls.py
urlpatterns = [
    path('test',views.test), # msg 그대로 전송
    path('help',views.help), # /help 명령어 수행
    path('trade', views.trade), # /trade 명령어 수행
    path('community', views.community), # /trade 명령어 수행
    path('check', views.check)  #김혁진 추가 나중에 빼야됨.
]

```

sub url에 맞게 `myapp/views.py`의 메소드와 각각 연결이 된다. 그러니까, 메소드는 views.py만 신경쓰면 된다.

## views.py 작성 요령

`localhost:8000/api/test/?room=1&sender=heeyon&msg=안녕하세요` url요청은 views.py의 test 메소드에서 처리하게 될 것이다.

```python
def test(request):
    print(request.META)
    print("room : " + parse.unquote(request.GET['room']))
    print("sender : " + parse.unquote(request.GET['id']))
    print("msg : " + parse.unquote(request.GET['msg']))
    return JsonResponse({
        "status" : "200-OK",
        "room" : request.GET['room'],
        "id" : request.GET['id'],
        "msg" : request.GET['msg'],
        "data" : "/test 테스트 중 입니다."
        })
```

url의 요청 정보는 request로 넘어오게 되어, `request.GET['room']`과 같이 url query 정보를 얻을 수 있다. 메신저봇에서 room, id, msg를 실은 url을 보낼 것이므로, 저것들을 이용하여 체크하고 로직을 만들면 된다.

return은 JSON type으로 하며, 전송할 메시지는 "data"에 실어서 보내면 된다.

## assist.py 와 api.py

msg는 채팅창에서 보낸 문자열 그대로가 올 것이므로, 이를 원하는 데이터에 따라 파싱하고 적절하게 처리를 하는 것이 필요하다. 이는 `assist.py`에서 각 함수에 필요한 파싱함수를 만들면 된다. 이는 파싱 담당의 일이므로, 테스트할 때 간단하게 특정 값을 return하도록 하여 해보도록 하자.

또한, 증권사 api를 통하여 요청을 보내고 받는 부분은 api.py에 넣어놓았다. 증권사 api의 환경이 복잡하여 현재는 [이곳](https://www.data.go.kr/iim/api/selectAPIAcountView.do#/%EA%B8%88%EC%9C%B5%EC%9C%84%EC%9B%90%ED%9A%8C_%EC%A3%BC%EC%8B%9D%EC%8B%9C%EC%84%B8%EC%A0%95%EB%B3%B4/getStockPriceInfo)의 api를 사용하도록 하였지만, 실제에서는 증권사 api를 사용할 예정이다. 

## DB 접근

현재, modles.py에 db에 저장된 테이블을 객체화하여 가져올 수 있는 상태이며, 장고 orm , 혹은 django orm 등으로 검색하여 db에 접근하고 변경할 수 있는 메소드를 찾아볼 수 있다.

간단하게, `from myapp.models import User` 와 같이 models.py에서 테이블 정보를 가져온다. 

- tuple 생성 :  User.objects.create(gid=gid,uname=uname, seed=seed)
- select (특정 조건 만족하는 튜플 리스트 가져오기): User.objects.filter(uname=uname)
- update(튜플 값 바꾼 후, db에 반영하기): user.save()

하고 나서, local db에 값이 반영이 되었나 확인하면 테스트 끝!

+사용자가 없는 경우, 문자열이 올바르지 않은 경우 등의 Error는 일관적으로(string을 보관하고 코드로 제공하는 방법도 있음), 예외없이 제공되어야 하므로 주의 부탁드립니다!
