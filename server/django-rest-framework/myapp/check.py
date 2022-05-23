import enum
import sys
import win32com.client
import threading
import pythoncom
import win32event

global creon
StopEvent = win32event.CreateEvent(None, 0, 0, None)

class CpEvent:
    def set_params(self, client, name, caller):
        self.client = client  # CP 실시간 통신 object
        self.name = name  # 서비스가 다른 이벤트를 구분하기 위한 이름
        self.caller = caller  # callback 을 위해 보관
 
    def OnReceived(self):
        # 실시간 처리 - 현재가 주문 체결
        if self.name == 'stockmst':
            print('recieved')
            win32event.SetEvent(StopEvent)
            return

class CpCurReply:
    def __init__(self, objEvent):
        self.name = "stockmst"
        self.obj = objEvent
 
    def Subscribe(self):
        handler = win32com.client.WithEvents(self.obj, CpEvent)
        handler.set_params(self.obj, self.name, None)

def MessagePump(timeout):
    waitables = [StopEvent]
    while 1:
        rc = win32event.MsgWaitForMultipleObjects(
            waitables,
            0,  # Wait for all = false, so it waits for anyone
            timeout, #(or win32event.INFINITE)
            win32event.QS_ALLEVENTS)  # Accepts all input
 
        if rc == win32event.WAIT_OBJECT_0:
            # Our first event listed, the StopEvent, was triggered, so we must exit
            print('stop event')
            break
 
        elif rc == win32event.WAIT_OBJECT_0 + len(waitables):
            # A windows message is waiting - take care of it. (Don't ask me
            # why a WAIT_OBJECT_MSG isn't defined < WAIT_OBJECT_0...!).
            # This message-serving MUST be done for COM, DDE, and other
            # Windowsy things to work properly!
            print('pump')
            if pythoncom.PumpWaitingMessages():
                break  # we received a wm_quit message
        elif rc == win32event.WAIT_TIMEOUT:
            print('timeout')
            return
            pass
        else:
            print('exception')
            raise RuntimeError("unexpected win32wait return value")

class Creon:
    check = "check"
    def __init__(self):
        pythoncom.CoInitialize()
        self.objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        self.objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
        self.objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        bConnect = self.objCpCybos.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            exit()
        else:
            print("ok")


    def getCode(self):
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
        objReply = CpCurReply(self.objStockMst)
        objReply.Subscribe()

        self.objStockMst.SetInputValue(0, code) 
        
        self.objStockMst.Request()
        print(self.objStockMst.GetDibStatus())
        MessagePump(10000)

        rqStatus = self.objStockMst.GetDibStatus()
        rqRet = self.objStockMst.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        print(rqStatus)
        if not (rqStatus ==0 or rqStatus ==1):
            return -2
        

        code = self.objStockMst.GetHeaderValue(0)
        name = self.objStockMst.GetHeaderValue(1)
        price = self.objStockMst.GetHeaderValue(11)
        print("코드 : " + code)
        print("이름 : "+ name)
        print("시가 : " +str(price))
        
        if price==0:
            return -1
        else:
            return price
       
       