from dataclasses import field
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse
from urllib import parse
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
    if len(req_str) == 1:
        return JsonResponse({
            "data" : "명령어는 /로 시작하며 앞으로 나오는 "+
            "&lt;,&gt; 는 실제로 입력하지 않고 사용합니다.\n"+
            "help &lt;function/term&gt; : 'function'의 명령어를 출력합니다."+
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
                "data" : "trad buy &lt;stock&gt; &lt;count&gt; : \"stock\"에 해당하는 주식을 현재가로 \"count\"만큼 매수 요청\n"+
                "trade buy &lt;stock&gt; &lt;count&gt; : \"stock\"에 해당하는 주식을 현재가로 \"count\"만큼 매도 요청\n"
            })
        elif req_str[1] == "community":
            return JsonResponse({
                "data" : "community rank : 전체 사용자 수익률 랭킹 출력\n"+
                "community &lt;user&gt; : 특정 사용자 보유 종목 및  수익률 출력\n"
            })
        elif req_str[1] == "stock":
            return JsonResponse({
                "data" : "stock top deal : 거래수가 가장 많은 종목 5개를 출력\n" +
                "stock top sum : 거래대금이 가장 높은 종목 5개를 출력\n"+
                "stock top rise : 상승률이 가장 높은 종목 5개를 출력\n" +
                "stock theme &lt;theme&gt; : \"theme\"에 해당하는 테마 정보 출력\n"+
                "stock state &lt;stock&gt; : \"stock\"에 해당하는 기업의 재무제표 출력\n"
            })
        elif req_str[1] == "chart":
            return JsonResponse({
                "data" : "chart &lt;stock&gt; : 해당 주식의 차트를 출력\n" +
                "chart &lt;stock&gt; inform : 해당 주식의 가격, 거래량, 등락률 출력\n"+
                "chart &lt;stock&gt; institutional : 기관의 순매매량 출력\n"+
                "chart &lt;stock&gt; individual : 개인의 순매매량 출력\n"+
                "chart &lt;stock&gt; foreign : 외국인의 순매매량 출력\n"
            })
        elif req_str[1] == "alarm":
            return JsonResponse({
                "data" : "Alarm &lt;stock&gt; &lt;time&gt; : \"time\"으로 입력된 시각에 \"stock\"에 해당하는 주식정보 알림\n"+
                "Alarm on : 알람 on\n"+
                "Alarm off : 알람 off\n"
            })
        elif req_str[1] == "theme":
            return JsonResponse({
                "data" : "키움증권 API의 GetThemeGroupList 메소드에서 제공하는 테마그룹명을 뜻합니다."
            })
        elif req_str[1] == "stock":
            return JsonResponse({
                "data" : "주식 종목을 뜻합니다. KRX 정보데이터 시스템에서 한글종목 약명에 해당하는 값으로만 입력될수있습니다."
            })
        elif req_str[1] == "function":
            return JsonResponse({
                "data" : "사용자가 입력하는 명령어를 뜻합니다."
            })
        elif req_str[1] == "count":
            return JsonResponse({
                "data" : "몇 개인지를 뜻합니다. 자연수만 입력될수있습니다."
            })
        elif req_str[1] == "user":
            return JsonResponse({
                "data" : "사용자의 이름을 뜻합니다."
            })
        elif req_str[1] == "time":
            return JsonResponse({
                "data" : "시간을 뜻합니다. 입력할 때, xx:xx (x는 0~9의 자연수)의 형태로 입력하며, 24시간제 형태로 입력합니다."
            })