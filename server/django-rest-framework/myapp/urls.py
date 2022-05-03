"""myapp URL Configuration
   myapp에서 처리할 url을 받아서, 처리함
"""
from django.urls import path
from myapp import views

urlpatterns = [
    path('test',views.test), # msg 그대로 전송
    path('help',views.help), # /help 명령어 수행
    path('buy', views.buy)
]

