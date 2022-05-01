"""myapp URL Configuration
   myapp에서 처리할 url을 받아서, 처리함
"""
from django.urls import path
from myapp import views

urlpatterns = [
    path('read/<id>/',views.read),   #id는 바뀌는 값으로 들어가게 됨
    path('test',views.test) # msg 그대로 전송
    path('help',views.help) # /help 명령어 수행
]

