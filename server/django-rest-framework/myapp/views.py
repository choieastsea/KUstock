from dataclasses import field
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework import serializers, viewsets

#models import
from myapp import models
from myapp.models import User

# class UserSerializer(serializers.ModelSerializer):
#     """User Model Serializer"""
#     class Meta:
#         model = models.User # models.User와 연결
#         fields = '__all__' # 모든 필드 출력하기

# Create your views here.
# model 객체 이용하여 view에 보여주도록 하자.

def test(request):
    print(request.META)
    return JsonResponse({
        "status" : "200-OK",
        "room" : request.GET['room'],
        "id" : request.GET['id'],
        "msg" : request.GET['msg'],
        })
def createUser(request):
    if request.method == 'GET':
        gid = int(request.GET['gid'])
        uname = request.GET['uname']
        seed = int(request.GET['seed'])
        # 유효성 검사 해줄 필요 있음!
        User.objects.create(gid=gid,uname=uname, seed=seed)
        return JsonResponse({"status" : "200-OK"})
    elif request.method == 'POST':
        # jsoup에서 post 전송이 된다면 해야겠지만,
        # csrf 토큰 처리가 필요함!
        return HttpResponse('post Create!!')
def help(request):
    req_str = request.GET['msg'].split(' ')
    if req_str.size == 1:
        return JsonResponse({
            "data" : "명령어는 /로 시작하며 앞으로 나오는 "+
            "<,> 는 실제로 입력하지 않고 사용합니다.\n"+
            "help <function/term> : 'function'의 명령어를 출력합니다."+
            "'term'의 용어가 해당하는 의미/사용가능한 문자열을 출력합니다.\n"+
            "community : 사용자 랭킹 및 자산정보관련 명령어입니다.\n"+
            "trade : 주식으로 사고/팔때 사용하는 명령어입니다.\n"+
            "stock : 주식관련 정보를 요청하는 명령어입니다.\n"+
            "chart : 주식의 차트를 요청하는 명령어입니다.\n"+
            "alarm : 지정한 시각에 알림을 설정하는 명령어입니다.\n"
        })
    else:
        if req_str[1] == "trade":
            return JsonResponse({
                
            })
        elif req_str[1] == "community":
            return JsonResponse({

            })
        elif req_str[1] == "stock":
            return JsonResponse({

            })
        elif req_str[1] == "chart":
            return JsonResponse({

            })
        elif req_str[1] == "alarm":
            return JsonResponse({

            })