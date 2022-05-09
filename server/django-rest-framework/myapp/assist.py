from myapp.models import Stock
from myapp.models import User
# myapp::views.py에 필요한 함수에 대한 파일
class assist:
    def codeToword(code):
        """
        문자열의 종목코드가 오면 종목명으로 반환한다
        만약 없다면, -1 문자열을 반환 
        """
        print(f"<<assist::codeToword>> : parm: {code}")
        stock = Stock.objects.filter(code=code)
        if stock.count() !=1:
            print("해당하는 종목명 없음")
            return -1
        else:
            print(f"<<assist::codeToword>> : return: {stock.sname}")
            return stock.sname

    def wordTocode(word):
        """
        문자열의 종목명이 오면 종목코드로 반환한다
        만약 없다면, -1 을 반환 
        """
        print(f"<<assist::wordTocode>> : parm: {word}")
        stock = Stock.objects.filter(sname=word)
        if stock.count() !=1:
            print("해당하는 stock code 없음")
            return -1
        else:
            print(f"<<assist::codeToword>> : return: {stock.code}")
            return stock.code

    def parseTrade(msg):
        """
        string type의 msg를 받아, [success: 메시지 문법 충족 여부, uname: 사용자 이름, stock_code: 매수 종목 코드, count: 매수량]를 리턴
        문법 오류 발생시, success에다가 문자열 실어주면 될듯
        """
        #msg를 파싱해주세요~
        msg_split = msg.split(" ")
        for msg in msg_split:
            msg = msg.strip()
        print("<<assist::parseTrade>>",end="")
        print(msg_split)
        success = ""
        # 명령어 입력 확인
        if len(msg_split) == 4:
            if msg_split[1] == "buy":
                success = "buy"
            elif msg_split[1] == "sell":
                success = "sell"
            else:
                success = "/trade buy 혹은 /trade sell 로 시작하였는지 확인해주세요.\n"
        else:
            success = "/trade (buy/sell) <stock> <count> 의 형태로 입력되었는지 확인해주세요.\n"
            return [success, 0, 0]

        # <stock> 인자 확인
        # 주식 코드 받아오는 메소드 필요
        stock_code = Stock.objects.filter(sname=msg_split[2])
        if stock_code.count() == 1:
            stock_code = stock_code.first().code
        else:
            success = "주식 명을 확인해주세요.\n"
        count = 0
        # <count> 인자 확인
        try:
            count = int(msg_split[3])
            if count <= 0:
                success = "<count>에 자연수를 입력해주세요.\n"
        except:
            success = "<count>에 자연수를 입력해주세요.\n"

        return [success, stock_code, count]


    def parseCommunity(msg):
        msg_split = msg.split(" ")
        success = ""
        req_user = ""
        if len(msg_split) == 2:
            if msg_split[1] == "rank":
                success = "rank"
            else:
                # 해당 user가 존재하는지 확인하는 메소드 필요
                req_user = User.objects.filter(uname=msg_split[1])
                if req_user.count() == 1:
                    success = "user"
                    req_user = req_user.first().uname
                else:
                    success = "사용자가 존재하지않습니다.\n"
        else:
            success = "/community rank 혹은 /community <user> 형태로 입력되었는지 확인해주세요.\n"


        return [success, req_user]