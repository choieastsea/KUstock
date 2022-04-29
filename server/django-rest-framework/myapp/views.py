from django.http import HttpResponse
from django.shortcuts import render, HttpResponse

# Create your views here.
# model 객체 이용하여 view에 보여주도록 하자.
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
def create(request):
    return HttpResponse('Create!!')
def read(request, id):
    return HttpResponse('Read..!'+id)