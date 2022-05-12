"""myapp URL Configuration
   myapp에서 처리할 url을 받아서, 처리함
"""
from django.urls import path
from myapp import views

urlpatterns = [
    path('test',views.test), # msg 그대로 전송
    path('help',views.help), # /help 명령어 수행
    path('create',views.createUser),
    path('kustock',views.kustock),    # /kustock 명령어 수행
    path('trade', views.trade), # /trade 명령어 수행
    path('community', views.community), # /community 명령어 수행
    path('stock',views.stock),   # /stock 명령어 수행
    path('chart',views.chart),   # /chart 명령어 수행
    path('check', views.check),  #김혁진 추가 나중에 빼야됨.
    path('dbInit', views.dbInit)  #김혁진 추가 나중에 빼야됨.
]

