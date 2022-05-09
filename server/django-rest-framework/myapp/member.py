from myapp import models
from myapp.models import User
from myapp.assist import assist
from myapp.models import Trade
from myapp.api import getStockPrice

class Member:
    name=""
    rank=0
    proceed=0
    proceed_rate=0

    def __init__(self,name):
        print("테스트")
        self.name = name

    def ranking(self):
        trades = Trade.objects.all()
        total_buy_cnt = 0 #평균 매수 가격 구하기 위한 변수
        total_buy=0
        for trade in trades:
            if trade.uid.uname==self.name:
                if trade.buysell: #buy인 경우
                    total_buy_cnt+=trade.count
                    total_buy+=(trade.price*trade.count)
                elif not trade.buysell: #sell인 경우
                    avg_buy = total_buy/total_buy_cnt
                    self.proceed_rate = (self.proceed_rate+(avg_buy-trade.price)/trade.price)/2
                    self.proceed += (avg_buy-trade.price)*trade.count #수익금
                    # print(f"proceed_rate : {self.proceed_rate} proceed : {self.proceed}")
        return self.proceed