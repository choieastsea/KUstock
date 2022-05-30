from dataclasses import field
from http.client import HTTPResponse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse
from urllib import parse
from .check import *
from rest_framework import serializers, viewsets
from pathlib import Path
from datetime import datetime
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from myapp.member import Member
from myapp import models
from myapp.models import User
from myapp.assist import assist
from myapp.models import Trade
from myapp.api import getStockPrice
from myapp.models import Stock

def stock_recommend(request):
    # stock_name = request.GET('name')
    stock_name = "hdc현대"
    return_str = assist.recommend(assist,stock_name, 5)
    print(return_str)
    return JsonResponse({
        "data" : return_str
    })
def check(request):
    creon = Creon()
    it = creon.getCurPrice("A005930")
    return JsonResponse({
               "status" : "200-OK",
               "data": it 
            })

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
        "data" : "/test 테스트 중 입니다.\n"
        })
def createUser(request):
    if request.method == 'GET':
        gid = request.GET['gid']
        uname = request.GET['uname']
        seed = int(request.GET['seed'])
        # 유효성 검사 해줄 필요 있음!
        User.objects.create(gid=gid,uname=uname, seed=seed)
        return JsonResponse({"status" : "200-OK"},{"data":"사용자 생성 완료"})
    elif request.method == 'POST':
        # jsoup에서 post 전송이 된다면 해야겠지만,
        # csrf 토큰 처리가 필요함!
        return HttpResponse('post Create!!')

def kustock(request):
    check = request.GET['msg'].split(" ")
    seed = 50000000
    if len(check) == 1:
        room = request.GET['room']
        sender = request.GET['id']
        user = User.objects.filter(uname=sender, gid = room)
        if user.count() != 1:
            User.objects.create(gid=room,uname=sender,seed=seed, profit = 0, status = 0)
            return_string = "채팅방 "+room+"에 "+sender+"님의 계정이 생성되었습니다.\n"
        else:
            return_string = "이미 "+sender+"유저가 존재합니다.\n"
    else:
        return_string = "명령어가 /kustock 으로 입력되었는지 확인해주세요.\n"

    return JsonResponse({"status" : "200-OK", "data" : return_string})   

def tutorial(request):
    uname = request.GET["id"]
    uroom = request.GET["room"]
    check = request.GET['msg'].split(" ")
    msg = request.GET['msg']
    user = User.objects.filter(uname=uname,gid=uroom)
    return_string = ""
    if user.count() != 1:
        return_string = f"{uname}에 해당하는 사용자가 없습니다.\n/kustock 명령어를 통해서 사용자 정보를 생성해주세요.\n"
    else:
        user = user.first()
        if user.status == 0:
            if len(check) == 1:
                user.status = 1
                user.save()
                return_string += "tutorial를 시작합니다. tutorial에서 나오는 주식 가격이나 사용자 정보는 모두 임의값입니다.\n"
                return_string += "먼저 \"/chart 삼성전자\" 를 입력해서 삼성전자 주식 가격을 확인해보세요."
            else:
                return_string += "명령어가 /tutorial 로 입력되었는지 확인해주세요.\n"
        if user.status == 1:
            if msg == "/chart 삼성전자":
                user.status = 2
                user.save()
                return_string += "삼성전자\n"
                return_string += "20xx.xx.27 66500원 (-0.91%)\n"
                return_string += "20xx.xx.26 65900원 (0.75%)\n"
                return_string += "20xx.xx.25 66400원 (0.16%)\n"
                return_string += "20xx.xx.24 66500원 (2.06%)\n"
                return_string += "20xx.xx.23 67900원 (0.15%)\n"
                return_string += "20xx.xx.20 68000원 (-0.74%)\n"
                return_string += "20xx.xx.19 67500원 (0.88%)\n"
                return_string += "이제 \"/trade buy 삼성전자 10\" 을 입력해서 삼성전자 주식을 10개 구매해보세요.\n"
            else:
                return_string += "/chart 삼성전자를 입력해주세요.\n"
                return_string += "(tutorial 탈출 명령어 /quit)\n"
        if user.status == 2:
            if msg == "/trade buy 삼성전자 10":
                user.status = 3
                user.save()
                return_string += uname+"님 삼성전자 주식 10주 매수 완료.\n"
                return_string += "잔고 : 49341000  추가748주 매수 가능\n"
                return_string += "삼성전자 10개를 구매를 완료했습니다.\n\"/community "+uname+"\" 을 입력해 구매한 주식을 확인해보세요.\n"
            else:
                return_string += "/trade buy 삼성전자 10 를 입력해주세요.\n"
                return_string += "(tutorial 탈출 명령어 /quit)\n"
        if user.status == 3:
            if msg == ("/community "+uname):
                user.status = 4
                user.save()
                return_string += uname+"님의 자산 정보 입니다.\n"
                return_string += "모의 자산 잔액 : 49341000 \n"
                return_string += "수익금 : 0\n"
                return_string += "(종목명/손익(수익률)/현재가/보유수량)\n"
                return_string += "============================\n"
                return_string += "(삼성전자/3000.0(4%)/69500원/10개)\n"
                return_string += "/community <user> 명령어를 통해서 자금, 수익금, 보유주식등의 정보를 확인할수있습니다.\n"
                return_string += "주식 정보를 확인하는동안 삼성전자 가격이 올랐습니다!\n"
                return_string += "\"/trade sell 삼성전자 10\" 를 통해서 구매했던 주식을 판매해보세요.\n"
            else:
                return_string += "/community "+uname+" 를 입력해주세요.\n"
                return_string += "(tutorial 탈출 명령어 /quit)\n"
        if user.status == 4:
            if msg == "/trade sell 삼성전자 10":
                user.status = 0
                user.save()
                return_string += uname+"님 삼성전자 주식 10주 매도 완료.\n"
                return_string += "잔고 : 50030000\n추가:751 매수 가능\n"
                return_string += "삼성전자 10개를 판매를 완료했습니다.\n"
            else:
                return_string += "/trade sell 삼성전자 10 를 입력해주세요.\n"
                return_string += "(tutorial 탈출 명령어 /quit)\n"



    return JsonResponse({"status" : "200-OK", "data" : return_string})

def quit(request):
    msg = request.GET["msg"].split(" ")
    uname = request.GET["id"]
    uroom = request.GET["room"]
    return_string = ""
    user = User.objects.filter(uname=uname,gid=uroom)
    if len(msg) != 1:
        return_string = "/quit 으로 입력해주세요.\n"
        return JsonResponse({"status" : "200-OK", "data" : return_string})
    if user.count() == 1:
        user = user.first()
        if user.status >= 1:
            user.status = 0
            user.save()
            return_string += "tutorial을 종료하였습니다.\n"
        else:
            return_string += "tutorial 상태가 아닙니다.\n"

    return JsonResponse({"status" : "200-OK", "data" : return_string})


def chart(request):
    # tutorial 기능을 위한 메세지 컷
    uname = request.GET["id"]
    uroom = request.GET["room"]
    user = User.objects.filter(uname=uname,gid=uroom)
    if user.count() == 1:
        user = user.first()
        if user.status >= 1:
            return_value = tutorial(request)
            return return_value

    # msg에서 명령어 파싱
    [success, stock_code] = assist.parseChart(request.GET['msg'])
    # 파싱 테스트
    print("success:"+ success+", stock_code : "+str(stock_code))
    
    return_string = "" 
    
    if success == "stock":
        # /chart <stock> 명령어
        result = [[],[]]
        url = "https://finance.naver.com/item/sise_day.nhn?code="+str(stock_code[1:])
        headers = {'User-agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        html = res.content
        soup = BeautifulSoup(html, 'html.parser')
        tr = soup.select('table>tr')

        for i in range(1, len(tr)-1):
           if tr[i].select('td')[0].text.strip():
                result[0].append(tr[i].select('td')[0].text.strip())
                result[1].append(int(tr[i].select('td')[1].text.strip().replace("," , "")))
        return_string += assist.codeToword(stock_code)+'\n'


        for i in range(7):
            dif = round((result[1][i+1] - result[1][i])/(result[1][i+1]) * 100, 2)
            return_string+= f"{result[0][i]}  {result[1][i]}원 ({dif}%)\n" 

    elif success == "inform":
        # /chart <stock> inform 명령어
        return_string+=f"현재 가격 : "
        url = "https://finance.naver.com/item/sise.naver?code=" +str(stock_code[1:])
        headers = {'User-agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        html = res.content
        soup = BeautifulSoup(html, 'html.parser')
        tr = soup.select('#middle>dl>dd')
        for i in range(1, len(tr)-1):
            print(tr[i].text)
            if tr[i].text.split()[0]=="현재가":
                lst = tr[i].text.split()[1:]
                sign = "+"
                if lst[2] == "하락":
                    sign = '-'
                return_string+= f"{lst[0]}({sign}{lst[3]}원, {lst[5]}%)\n"
            elif tr[i].text.split()[0] =="거래량":
                return_string +=f"거래량({tr[i].text.split()[1]}주)\n"
        print(return_string)

    elif success == "institutional":
        # /chart <stock> inform 명령어
        sell_lst = []
        buy_lst = []
        url = "https://finance.naver.com/item/frgn.naver?code=" +str(stock_code[1:])
        headers = {'User-agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        html = res.content
        soup = BeautifulSoup(html, 'html.parser')
        tr = soup.select('#content > div.section.inner_sub > table.type2>tr:nth-child(5)>td>span')
        for i in range(len(tr)-1):
            if i==5:
                return_string += f"기관 순 매매량 : {tr[i].text}\n\n"

        tr = soup.select('#content > div.section.inner_sub > div:nth-child(1) > table>tbody >tr >td>span')
        for i in range(0, len(tr)-5, 4):
            sell_lst.append([tr[i].text, tr[i+1].text])
            buy_lst.append([tr[i+2].text, tr[i+3].text])
        
        return_string +=f"매수 상위 기관 :\n"
        for i in range(5):
            return_string+=f"{buy_lst[i][0]}({buy_lst[i][1]}) "
        

        return_string +=f"\n\n매도 상위 기관 :\n"
        for i in range(5):
            return_string+=f"{sell_lst[i][0]}({sell_lst[i][1]}) "
        print(return_string)
    elif success == "individual":
        # /chart <stock> inform 명령어
        return_string = "개인 매매량은 지원해주지 않습니다.\n"
    elif success == "foreign":
        # /chart <stock> inform 명령어
        url = "https://finance.naver.com/item/frgn.naver?code=" +str(stock_code[1:])
        headers = {'User-agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        html = res.content
        soup = BeautifulSoup(html, 'html.parser')
        tr = soup.select('#content > div.section.inner_sub > table.type2>tr:nth-child(5)>td>span')
        for i in range(len(tr)-1):
            if i==6:
                return_string += f"외국인 순 매매량 : {tr[i].text}\n"
    else:
        return_string = success


    return JsonResponse({"status" : "200-OK", "data" : return_string})


def stock(request):
    # tutorial
    uname = request.GET["id"]
    uroom = request.GET["room"]
    user = User.objects.filter(uname=uname,gid=uroom)
    if user.count() == 1:
        user = user.first()
        if user.status >= 1:
            return_value = tutorial(request)
            return return_value

    # msg에서 명령어 파싱
    [success, stock_code, theme] = assist.parseStock(assist, request.GET['msg'])
    # 파싱 테스트
    print("success:"+ success+", stock_code : "+str(stock_code)+", theme:"+ str(theme))
    return_string = ""
    jusik_url = "https://finance.naver.com/sise/field_submit.naver?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.naver&fieldIds=quant&fieldIds=amount&fieldIds=market_sum&fieldIds=per&fieldIds=roe&fieldIds=listed_stock_cnt"
    # jusik_url = "https://finance.naver.com/sise/sise_market_sum.nhn?page=1"
    res=requests.get(jusik_url)
    soup=BeautifulSoup(res.text,'lxml')
    # print(soup)
    stock_head = soup.find("thead").find_all("tr")
    # print(stock_head)
    data_head=[head.get_text() for head in stock_head] 
    # data_head : [0'N', 1'종목명', 2'현재가', 3'전일비', 4'등락률', 5'액면가', 6'거래량', 7'거래대금', 8'상장주식수', ' 9'시가총액', 10'PER', 11'ROE', 12'토론실']
    # print(f"data_head : {data_head}")
    stock_list=soup.find("table",attrs={"class":"type_2"}).find("tbody").find_all("tr")
    stocks=[]
    # print(f"data_head : {data_head}")
    # print(f"len(data_head) : {len(data_head)}")
    # print(stock_list[0].get_text())
    # print(stock_list)
    for stock in stock_list:
        # print(f"stock:{stock}")
        if len(stock)>1:
            # print(stock.get_text().split())
            temp = stock.get_text().split()
            # print(f"temp : {temp} \n\n\n")
            # print(f"len(data_head) : {len(data_head)}")
            for i in range(12):
                if i==4:
                    temp[i]=temp[i].split("%")[0]
                    # print(f"{type(temp[i])} |||| {temp[i]}")
                if i!=1 and temp[i]!='N/A':
                    temp[i]=temp[i].replace(",","")
                    # print(f"temp는 {temp[i]}")
                    temp[i]=float(temp[i])
                    # print(f"temp[i] : {temp[i]}\n")
                    # print(f"{i}번 {temp[i]} {type(temp[i])}\n")
                # print(f"temp값은 {temp}")
            stocks.append(temp)
    # print(f"stocks = {stocks}")
    if success == "deal":
        # /stock top deal 명령어
        ans=""
        ans+=f"{datetime.today().date()} 거래량 상위 top5 종목\n"
        stocks = sorted(stocks,key=lambda x:x[6],reverse=True)
        i=0
        for stock in stocks:
            ans+=f"{i+1}. {stock[1]} | {int(stock[2])}원 | {int(stock[6])} 주\n"
            i+=1
            if i==5:
                break
        # ans+=str(stocks)
        print(ans)
        return_string = ans
    elif success == "sum":
        # /stock top sum 명령어
        ans=""
        ans+=f"{datetime.today().date()} 거래대금 상위 top5 종목\n"
        stocks = sorted(stocks,key=lambda x:x[7],reverse=True)
        i=0
        for stock in stocks:
            ans+=f"{i+1}. {stock[1]} | {int(stock[2])}원 | {int(stock[7])} 억 원\n"
            i+=1
            if i==5:
                break
        # ans+=str(stocks)
        print(ans)
        return_string = ans
    elif success == "rise":
        # /stock top rise 명령어
        ans=""
        ans+=f"{datetime.today().date()} 상승률 상위 top5 종목\n"
        stocks = sorted(stocks,key=lambda x:x[4],reverse=True)
        i=0
        for stock in stocks:
            ans+=f"{i+1}. {stock[1]} | {int(stock[2])}원 | +{stock[4]}% \n"
            i+=1
            if i==5:
                break
        # ans+=str(stocks)
        print(ans)
        return_string = ans
    elif success == "theme":
        # /stock theme <theme> 명령어 <theme>정보는 theme 변수에 저장됨
        ans=""
        ans+=f"{datetime.today().date()} {theme} 정보\n"
        find_thema = False
        for pagenum in range(1,8):
            theme_url = "https://finance.naver.com/sise/theme.nhn?field=name&ordering=asc&page={pagenum}".format(pagenum=pagenum)
            resp = requests.get(theme_url)
            soup = BeautifulSoup(resp.content, "html.parser")
            thema_num = 0
            # print(soup.select("#contentarea_left > table.type_1.theme > tr:nth-child("+str(thema_num)+") > td.col_type1"))
            while thema_num < 50:
                try:
                    thema_num += 1
                    board_date = soup.select("#contentarea_left > table.type_1.theme > tr:nth-child("+str(thema_num)+") > td.col_type1 > a")[0]
                    thema = board_date.text.strip()
                    if thema==theme:
                        find_thema=True
                        thema_rate = soup.select("#contentarea_left > table.type_1.theme > tr:nth-child("+str(thema_num)+") > td.col_type2 > span")[0].get_text()
                        # print(f"thema_rate : {thema_rate.get_text().strip()}")
                        thema_rate = thema_rate.lstrip()
                        ans+=(f"\n등락률 : {thema_rate}\n주요 종목 : ")
                        linkUrl = 'https://finance.naver.com' + board_date['href']
                        linkResp = requests.get(linkUrl)
                        linkSoup = BeautifulSoup(linkResp.content, "html.parser")   
                        for i in range(10):
                            link_board_date = linkSoup.select("#contentarea > div:nth-child(5) > table > tbody > tr:nth-child("+str(i+1)+") > td.name > div > a")[0].text.strip()
                            if i==9:
                                ans+=(f"{link_board_date} \n")
                            else:
                                ans+=(f"{link_board_date}, ")
                        print(ans)
                        return_string = ans
                except Exception as e:
                    continue
        if not find_thema:
            ans+="해당하는 테마를 찾지 못하였습니다.\n"
            return_string=ans
        # print(ans)
        # return_string = ans
    elif success == "stock":
        # /stock state <stock> 명령어 <stock>정보는 stock_code 변수에 저장됨
        ans=""
        stock_code=stock_code[1:]
        ans+=(f"{stock_code} 주요 재무제표\n")
        stock_url = f"https://finance.naver.com/item/main.nhn?code={stock_code}"
        r = requests.get(stock_url)
        df=pd.read_html(r.text)[3]
        df.set_index(df.columns[0],inplace=True)
        df.index.rename('<주요재무정보>',inplace=True)
        df.columns=df.columns.droplevel(2)
        # ans+=df
        annul_date = pd.DataFrame(df).xs('최근 연간 실적',axis=1)
        quater_date = pd.DataFrame(df).xs('최근 분기 실적',axis=1)
        ans+=(f"최근 연간 실적 \n {annul_date}\n\n")
        ans+=(f"최근 분기 실적 \n {quater_date}\n")
        # ans+=stock_code
        print(ans)
        return_string = ans
    else:
        return_string = success

    return JsonResponse({"status" : "200-OK", "data" : return_string})    
    
def trade(request):
    """
    test url : {root url}/api/trade?id=김태헌&room=1&msg=/trade buy 005980 2 (trade buy/sell stock_code count)
    ----[check list]----
    - 문자열 올바르지 않은 경우
    - 해당 이름 이용자 존재하지 않을 경우
    - 해당 room 존재하지 않을 경우
    - 해당 종목 코드가 존재하지 않는 경우
    - count가 음수인 경우
    - (buy) seed가 부족한 경우
    - (sell) 가지고 있는 주식이 count 보다 적은 경우
    - 정상 거래 진행
    """
    # room, id 인자 획득
    uname = request.GET["id"]
    uroom = request.GET["room"]
    # tutorial
    user = User.objects.filter(uname=uname,gid=uroom)
    if user.count() == 1:
        user = user.first()
        if user.status >= 1:
            return_value = tutorial(request)
            return return_value

    # msg에서 명령어 파싱
    [success, stock_code, count] = assist.parseTrade(assist, request.GET['msg'])
    # [success, stock_code, count] = ["buy","000020",2]
    # 파싱 테이스
    print("success:"+ success+", stock_code : "+str(stock_code)+", count:"+ str(count))

    return_string = "\n"
    # 사용자 조회 
    if success == "buy":
        user = User.objects.filter(uname=uname,gid=uroom)
        if user.count() != 1:
            return_string = f"{uname}에 해당하는 사용자가 없습니다.\n/kustock 명령어를 통해서 사용자 정보를 생성해주세요.\n"
        # elif:
        # 해당하는 room이 없는 경우
        # elif:
        # 동명이인인 경우
        # elif:
        # 해당하는 주식이 없는 경우
        else:
            # 사용자 잔고 조회
            user = user.first()
            # print(user.seed)
            #코드 조회
            price = getStockPrice(stock_code[1:])
            if price == -1:
                return_string = f"{assist.codeToword(stock_code)}에 해당하는 종목이 없습니다.\n"
            else:    
                user.seed -= int(price)*count
                if user.seed >= 0:
                    user.save()
                    Trade.objects.create(
                        uid=user,
                        buysell="TRUE",
                        date=datetime.today(),
                        price=price,
                        count=count,
                        code=stock_code)
                    # print(Trade.objects.filter(uid=User))
                    more_stock = user.seed//price
                    return_string = f"{user.uname}님 {assist.codeToword(stock_code)} 주식 {count} 주 매수 완료.\n 잔고 : {user.seed} 추가{more_stock}주 매수 가능.\n"
                else:
                    user.seed += int(price)*count
                    return_string = f"잔고가 부족하여 거래를 하지 못하였습니다 (현재 잔고: {user.seed})\n"
    elif success == "sell":
        user = User.objects.filter(uname=uname,gid=uroom)
        if user.count() != 1:
            return_string = f"{uname}에 해당하는 사용자가 없습니다.\n/kustock 명령어를 통해서 사용자 정보를 생성해주세요.\n"
        # elif:
        # 해당하는 room이 없는 경우
        # elif:
        # 동명이인인 경우
        # elif:
        # 해당하는 주식이 없는 경우
        else:
            user = user.first()
            price = getStockPrice(stock_code[1:])
            if price == -1:
                return_string = f"{assist.codeToword(stock_code)}에 해당하는 종목이 없습니다.\n"
            else:
                trades = Trade.objects.filter(uid = user.uid, code = stock_code)
                current_stock_count = 0
                for trade in trades:
                    if trade.buysell=="TRUE":
                        current_stock_count += trade.count
                    else:
                        current_stock_count -= trade.count
                    
                print(f"현재 남은 주식 개수 : {current_stock_count}\n")
                if current_stock_count<count:
                    # trade에 buy한 내역이 없는 경우 
                    return_string = f"{assist.codeToword(stock_code)} 종목을 {count}주 이상 소유하고 있지 않습니다.\n"
                else:
                    # 정상 매도 case
                    user.seed+=int(price)*count
                    total_buy=0
                    profit=0
                    for trade in trades:
                        if trade.buysell=="TRUE": #매수 기록
                            total_buy+=trade.price*trade.count
                        elif trade.buysell=="FALSE": #매도 기록
                            total_buy-=trade.price*trade.count
                    avg_buy = total_buy/current_stock_count
                    profit = (price-avg_buy)*count
                    user.profit +=profit
                    more_stock = user.seed//price
                    user.save()
                    Trade.objects.create(
                            uid=user,
                            buysell="False",
                            date=datetime.today(),
                            price=price,
                            count=count,
                            code=stock_code)
                    # User.objects.update()
                    print(user.profit)
                    return_string = f"{user.uname}님 {assist.codeToword(stock_code)} 주식 {count} 주 매도 완료. \n잔고 : {user.seed} 추가 : {more_stock} 매수 가능.\n"          
    else:
        return_string = success
    print(return_string)
    return JsonResponse({"status" : "200-OK", "data" : return_string})

def community(request):
    # room, id 인자 획득
    uname = request.GET["id"]
    uroom = request.GET["room"]
    # tutorial
    user = User.objects.filter(uname=uname,gid=uroom)
    if user.count() == 1:
        user = user.first()
        if user.status >= 1:
            return_value = tutorial(request)
            return return_value
    [success, req_uname] = assist.parseCommunity(request.GET['msg'],uroom)

    # 파싱 테스트
    print("success:"+ success+", req_uname:"+req_uname)
    trades = Trade.objects.all()

    #for trade in trades:
        # print(f" tid number : {trade.tid}\n uid number : {trade.uid.uname}\n date : {trade.date}\n price : {trade.price}\n count : {trade.count}\n buysell : {trade.buysell}\n code : {trade.code}\n")
        # print(f"{us.uid}\n {us.gid}\n {us.uname}\n {us.seed}")
    return_string = ""
    if success == "rank":
        temp="               "
        temp+="랭킹\n"
        temp+="======================\n"
        temp+="( 순위 / 이름 / 수익금 )\n"
        # 해당 uroom에 있는 모든 사람들의 정보.
        names = User.objects.filter(gid=uroom)
        tmembers=[]
        for name in names:
            tmembers.append([name.uname,name.profit])
        tmembers=sorted(tmembers,key=lambda x:-x[1])
        i=0
        for tmember in tmembers:
            temp+=f"{i+1}"
            temp+=f" / {tmember[0]} / {tmember[1]}  )\n"
            i+=1
        print(temp)
        return_string = temp
    elif success=="user":
        total_buy=0
        jusik_table = []
        jusiks=""
        req_user = User.objects.filter(uname=req_uname,gid=uroom).first()
        #req_user없는 경우 예외처리
        for trade in trades:
            # print(f">>>>>trade.uid : {type(trade.uid.uid)} // req_user: {type(req_user.uid)}")
            if trade.uid==req_user:
                print(f"<<trade code>> : {trade.code} jusik table : {jusik_table}")
                if trade.code not in jusik_table:
                    jusik_table.append(trade.code)
        print("jusik table : ",end="")
        print(jusik_table)
        return_string="          "
        return_string+=req_uname
        return_string+=" 님의 자산 정보입니다.\n"
        return_string+=f"모의 자산 잔액 : {req_user.seed}\n"
        return_string+=f"수익금 : {req_user.profit}\n"
        return_string+="( 종목명 / 손익(수익률) / 현재가 / 보유수량 )\n"
        return_string+="===================\n"
        # temp+="가지고 있는 종목 정보"
        for jusik in jusik_table:
            total_buy=0
            total_count=0
            temp = ""
            jusiks = Trade.objects.filter(uid=req_user.uid,code=jusik)
            temp+="( "
            temp+=assist.codeToword(jusik) # 코드명 이름변경 필요
            temp+=' / '
            # 평단가 구하는 코드    
            for trade in jusiks:
                if trade.buysell=="TRUE": #매수 기록
                    print(f"total_buy : {total_buy} trade.price : {trade.price} trade.count : {trade.count}")
                    total_buy+=(trade.price*trade.count)
                    total_count += trade.count
                elif trade.buysell=="FALSE": #매도 기록
                    print(f"total_buy : {total_buy} trade.price : {trade.price} trade.count : {trade.count}")
                    total_buy-=trade.price*trade.count
                    total_count -= trade.count
                print(f"total_buy : {total_buy} trade.price : {trade.price} trade.count : {trade.count}")
                print(f"avg_buy :  total_buy : {total_buy} total_count : {total_count}")
                #total_buy == 0 일때 오류메시지
            if total_count==0:
                return_string += temp
            else:
                avg_buy = total_buy/total_count
                print(f"avg_buy : {avg_buy} total_buy : {total_buy} total_count : {total_count}")
                print(f"jusik:{jusik[1:]}")
                current_price = getStockPrice(jusik[1:]) # 현재가 받아오는 메소드
                temp += str(current_price-avg_buy) +"("
                if avg_buy == 0:
                    temp += "0) / "
                else:
                    if (current_price-avg_buy)/avg_buy*100<0:
                        temp+="0) / "
                    else:
                        temp += str(int((current_price-avg_buy)/avg_buy*100)) + "%) / "
                temp+=str(current_price)+"원 / "
                temp+=str(total_count) + "개 ) \n"
                print(temp)
                return_string += temp
    else:
        return_string = success

    return JsonResponse({"status" : "200-ok", "data" : return_string})




def help(request):
    req_str = request.GET['msg'].split(' ')
    uname = request.GET["id"]
    if len(req_str) == 1:
        return JsonResponse({
            "data" : "명령어는 /로 시작하며 앞으로 나오는 "+
            "&lt;,&gt; 는 실제로 입력하지 않고 사용합니다.\n"+
            "kustock : trade와 community에 필요한 정보를 생성하는 명령어입니다. \n"+
            "trade : 주식으로 사고/팔때 사용하는 명령어입니다.\n"+
            "community : 사용자 랭킹 및 자산정보관련 명령어입니다.\n"+
            "stock : 주식관련 정보를 요청하는 명령어입니다.\n"+
            "chart : 주식의 차트를 요청하는 명령어입니다.\n"+
            "alarm : 지정한 시각에 알림을 설정하는 명령어입니다.\n"+
            "상세한 명령어의 정보가 필요하시면 아래와 같이 help 명령어를 입력해주세요.\n"+
            "help &lt;function/term&gt; : 'function'의 명령어의 상세 사용법을 출력합니다."+
            "'term'의 용어가 해당하는 의미/사용가능한 문자열을 출력합니다.\n"
        })
    else:
        if req_str[1] == "trade":
            return JsonResponse({
                "data" : "trade buy &lt;stock&gt; &lt;count&gt; : \"stock\"에 해당하는 주식을 현재가로 \"count\"만큼 매수 요청\n"+
                "trade buy &lt;stock&gt; &lt;count&gt; : \"stock\"에 해당하는 주식을 현재가로 \"count\"만큼 매도 요청\n"+
                "ex) /trade buy 삼성전자 10 => 삼성전자 주식 10개 구매\n /trade sell 삼성전자 10 => 삼성전자 주식 10개 판매\n"
            })
        elif req_str[1] == "community":
            return JsonResponse({
                "data" : "community rank : 전체 사용자 수익률 랭킹 출력\n"+
                "community &lt;user&gt; : 특정 사용자 보유 종목 및  수익률 출력\n"+
                "ex) /community rank => 전체 사용자 랭킹 출력\n /community "+uname+" => "+uname+"님의 보유 종목 및 수익률 출력\n"
            })
        elif req_str[1] == "stock":
            return JsonResponse({
                "data" : "stock top deal : 거래수가 가장 많은 종목 5개를 출력\n" +
                "stock top sum : 거래대금이 가장 높은 종목 5개를 출력\n"+
                "stock top rise : 상승률이 가장 높은 종목 5개를 출력\n" +
                "stock theme &lt;theme&gt; : \"theme\"에 해당하는 테마 정보 출력\n"+
                "stock state &lt;stock&gt; : \"stock\"에 해당하는 기업의 재무제표 출력\n"+
                "ex) /stock top deal \n /stock state 삼성전자 => 삼성전자의 재무제표 출력\n"+
                " /stock theme 2차전지 => 2차전지 관련 테마주의 정보 출력\n"
            })
        elif req_str[1] == "chart":
            return JsonResponse({
                "data" : "chart &lt;stock&gt; : 해당 주식의 차트를 출력\n" +
                "chart &lt;stock&gt; inform : 해당 주식의 가격, 거래량, 등락률 출력\n"+
                "chart &lt;stock&gt; institutional : 기관의 순매매량 출력\n"+
                "chart &lt;stock&gt; individual : 개인의 순매매량 출력\n"+
                "chart &lt;stock&gt; foreign : 외국인의 순매매량 출력\n"+
                "ex) /chart 삼성전자 => 삼성전자 주식의 차트 출력\n"+
                " /chart 삼성전자 inform => 삼성전자 주식의 가격,거래량,등락률 출력\n"
            })
        elif req_str[1] == "kustock":
            return JsonResponse({
                "data" : "/kustock : 서버에 사용자 정보를 생성해주는 명령어입니다.\n trade, community 등의 명령어를 사용하기 위해서 필요합니다.\n"
            })
        elif req_str[1] == "theme":
            return JsonResponse({
                "data" : "키움증권 API의 GetThemeGroupList 메소드에서 제공하는 테마그룹명을 뜻합니다.\n"
            })
        elif req_str[1] == "stock":
            return JsonResponse({
                "data" : "주식 종목을 뜻합니다. KRX 정보데이터 시스템에서 한글종목 약명에 해당하는 값으로만 입력될수있습니다.\n"
            })
        elif req_str[1] == "function":
            return JsonResponse({
                "data" : "사용자가 입력하는 명령어를 뜻합니다.\n"
            })
        elif req_str[1] == "count":
            return JsonResponse({
                "data" : "몇 개인지를 뜻합니다. 자연수만 입력될수있습니다.\n"
            })
        elif req_str[1] == "user":
            return JsonResponse({
                "data" : "사용자의 이름을 뜻합니다.\n"
            })
        elif req_str[1] == "time":
            return JsonResponse({
                "data" : "시간을 뜻합니다. 입력할 때, xx:xx (x는 0~9의 자연수)의 형태로 입력하며, 24시간제 형태로 입력합니다.\n"
            })

def dbInit(request):
    creon =Creon()
    lst = creon.getCode()
    Stock.objects.all().delete()
    for i,j in lst:
        Stock.objects.create(code=i,sname=j)
    return JsonResponse({"status" : "200-ok"})

def tradeRecord(request) :
    """
    localhost:8000/api/record?id=최동해&room=2&msg=/record trade 김경호
    """
    uname = request.GET["id"]
    uroom = request.GET["room"]
    # tutorial
    user = User.objects.filter(uname=uname,gid=uroom)
    if user.count() == 1:
        user = user.first()
        if user.status >= 1:
            return_value = tutorial(request)
            return return_value
    [success, req_uname] = assist.parseRecord(request.GET['msg'],uroom)

    # 파싱 테스트
    print("success:"+ success+", req_uname:"+req_uname)
    
    trades = Trade.objects.all()
    
    success = f"{uname} 님의 거래내역입니다. \n"
    for trade in trades:
        if(trade.uid.uname == uname) :
            stock = assist.codeToword(trade.code)
            buysell = ""
            if(trade.buysell == "TRUE"):
                buysell = "매수"
            else:
                buysell = "매도"
            success += f"{trade.date} {stock}\t {buysell} {trade.price}원 {trade.count}주 \n"

    return_string = success
    print(return_string)
    return JsonResponse({"status" : "200-ok", "data" : return_string})