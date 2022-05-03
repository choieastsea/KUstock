# myapp::views.py에 필요한 함수에 대한 파일
class assist:
    def parseBuy(msg):
        """
        string type의 msg를 받아, [success: 메시지 문법 충족 여부, uname: 사용자 이름, stock_code: 매수 종목 코드, count: 매수량]를 리턴
        문법 오류 발생시, success에다가 문자열 실어주면 될듯
        """
        #msg를 파싱해주세요~
        return [True, '최동해','005930', 3]
