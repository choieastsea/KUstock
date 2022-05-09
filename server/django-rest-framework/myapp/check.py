import enum
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

    """def connect(self, id_, pwd, pwdcert , trycnt=300):
        if not self.connected()

    def connected(self):
        bConnected = self.objCpc
        """
    def getCode(self):
        self.objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        codeList = self.objCpCodeMgr.GetStockListByMarket(1)     #거래소
        codeList2 = self.objCpCodeMgr.GetStockListByMarket(2)     #코스닥
        
        codename_lst = []
        for i, code in enumerate(codeList):
            name = self.objCpCodeMgr.CodeToName(code)
            codename_lst.append([code, name])

        for i, code in enumerate(codeList2):
            name = self.objCpCodeMgr.CodeToName(code)
            codename_lst.append([code, name])
        #print(codename_lst) 
        return codename_lst
    

    def getCurPrice(self, code):
        self.objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
        self.objStockMst.SetInputValue(0, code)   
        self.objStockMst.BlockRequest()

        rqStatus = self.objStockMst.GetDibStatus()
        rqRet = self.objStockMst.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            exit()
        
        code = self.objStockMst.GetHeaderValue(0)
        name = self.objStockMst.GetHeaderValue(1)
        price = self.objStockMst.GetHeaderValue(13)
        #print("코드 : " + code)
        #print("이름 : "+ name)
        #print("시가 : " +str(price))
        if price==0:
            return -1
        else:
            return price
    
    