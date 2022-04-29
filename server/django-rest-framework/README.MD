참고 : https://windybay.net/post/13/
venv : https://hleecaster.com/python-venv/

# 실행 방법
1. 가상 환경 구축(venv)
`python -m venv project_env`
`source project_env/bin/activate` 로 가상 환경 활성화 -> `deactivate`로 비활성화 할 수 있음
`pip install -r requirements.txt`로 의존성 패키지 설치

2. 장고 서버 실행 
`python3 manage.py runserver`로 실행 -> default로 8000번 포트에 서버 열릴 것


requirements.txt를 통하여 python packages를 설치해줄 수 있고, 이후, `python3 manage.py runserver`로 서버 실행할 수 있다.

project(myproject)가 있고, app(myapp)이 있다.
사용자의 모든 경로는 urls.py를 통하여 이에 적당한 app에 위임이 될 것이다. app 내에서 urls.py에서 view와 매칭을 하여 응답을 하는 형식이라고 보면 될 것 같다. view는 model에 따라 보이는 것이 달라질 수 있다.

