import sys
import win32com.client
import threading
import pythoncom

class Creon:
    def __init__(self):
        pythoncom.CoInitialize()
        self.objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        bConnect = self.objCpCybos.IsConnect
        print(bConnect)
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            exit()
        else:
            print("ok")
        
        self.objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
        self.objStockMst.SetInputValue(0, 'A005930')   #종목 코드 - 삼성전자
        self.objStockMst.BlockRequest()
        
        # 현재가 통신 및 통신 에러 처리 
        rqStatus = self.objStockMst.GetDibStatus()
        rqRet = self.objStockMst.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            exit()
        
        # 현재가 정보 조회
        code = self.objStockMst.GetHeaderValue(0)  #종목코드
        name= self.objStockMst.GetHeaderValue(1)  # 종목명
        time= self.objStockMst.GetHeaderValue(4)  # 시간
        cprice= self.objStockMst.GetHeaderValue(11) # 종가
        diff= self.objStockMst.GetHeaderValue(12)  # 대비
        open= self.objStockMst.GetHeaderValue(13)  # 시가
        high= self.objStockMst.GetHeaderValue(14)  # 고가
        low= self.objStockMst.GetHeaderValue(15)   # 저가
        offer = self.objStockMst.GetHeaderValue(16)  #매도호가
        bid = self.objStockMst.GetHeaderValue(17)   #매수호가
        vol= self.objStockMst.GetHeaderValue(18)   #거래량
        vol_value= self.objStockMst.GetHeaderValue(19)  #거래대금
        
        # 예상 체결관련 정보
        exFlag = self.objStockMst.GetHeaderValue(58) #예상체결가 구분 플래그
        exPrice = self.objStockMst.GetHeaderValue(55) #예상체결가
        exDiff = self.objStockMst.GetHeaderValue(56) #예상체결가 전일대비
        exVol = self.objStockMst.GetHeaderValue(57) #예상체결수량
        
        
        print("코드", code)
        print("이름", name)
        print("시간", time)
        print("종가", cprice)
        print("대비", diff)
        print("시가", open)
        print("고가", high)
        print("저가", low)
        print("매도호가", offer)
        print("매수호가", bid)
        print("거래량", vol)
        print("거래대금", vol_value)
        
        
        if (exFlag == ord('0')):
            print("장 구분값: 동시호가와 장중 이외의 시간")
        elif (exFlag == ord('1')) :
            print("장 구분값: 동시호가 시간")
        elif (exFlag == ord('2')):
            print("장 구분값: 장중 또는 장종료")
        
        print("예상체결가 대비 수량")
        print("예상체결가", exPrice)
        print("예상체결가 대비", exDiff)
        print("예상체결수량", exVol)