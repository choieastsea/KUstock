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
def index(request):
    return HttpResponse('''
    <html>
    <body>
        <h1>Django</h1>
        <ol>
            <li>routing</li>
            <li>view</li>
            <li>model</li>
        </ol>
        <h2>Welcome</h2>
    </body>
    </html>
    ''')
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
def read(request, id):
    return HttpResponse('Read..!'+id)