from myapp.models import Stock
from myapp.models import User
from myapp.models import Theme
from jamo import h2j, j2hcj
# myapp::views.py에 필요한 함수에 대한 파일
class assist:
        
    def recommend(self, ustock:str, n:int, isTheme = False):
        """
        해당 종목이 없는 경우, 유사한 주식명 추천하기 위해 사용하는 함수
        parm : {ustock : 사용자의 잘못된 종목명/테마명 문자열, n: 출력 종목 수, isTheme : theme 추천 기능}
        return : 이와 가장 유사한 n개의 문자열
        (levenshtein 함수, jamo의 h2j 함수를 이용함)
        """
        print(f"<<assist::recommend>> : parm: {ustock}, {n}, {isTheme}")
        # 1. 한글 분해하여 1차원 배열로 저장
        ustock = ustock.strip()
        ustock_mod = self.decompKor(ustock)
        print(ustock_mod)
        # 2. 입력 문자열과 다른 종목명들의 레벤슈타인 거리 계산
        if isTheme:
            stocks = Theme.objects.all().values("code")    # 테마 정보를 받아옴
        else:    
            stocks = Stock.objects.all().values("sname")
        edit_distance_dict = {}
        for i in range(len(stocks)):
            if isTheme:
                dstock = stocks[i]['code']
            else:
                dstock = stocks[i]['sname'] #db에 있는 종목명 정보
            dstock_mod = self.decompKor(dstock) 
            # print(f"{stocks[i]['sname']}")
            edit_distance = self.levenshtein(ustock_mod, dstock_mod)
            # 3. 입력 문자열 길이 == 편집거리인 경우, 다 다르다는 의미이므로, 매우 큰수로 초기화
            if len(ustock_mod) <= edit_distance:
                edit_distance = 100000
            edit_distance_dict[i] = edit_distance   
            # 4. 해당 문자열이 포함된 종목의 경우, 편집 거리의 가산점을 줘보자! (optional)
            flag = 0
            before = 0
            for k in range(len(ustock)):
                char = ustock[k]
                x=dstock.find(char)
                if x >= 0 and before <=x:
                    before = x
                else:
                    flag = 1
                    break
            if (flag ==0) or (ustock in dstock):
                # edit_distance_dict[i] -= (len(ustock_mod)-len(ustock)) -> 이런 가산점 문제 있음. 걍 0 주자
                edit_distance_dict[i] = 0
        #5. 편집 거리 순으로 정렬 sort by value(item[1])
        edit_distance_dict = dict(sorted(edit_distance_dict.items(), key=lambda item: item[1]))
        return_list = []
        edit_distance_list = list(edit_distance_dict.keys())
        for i in range(n):
            if isTheme:
                return_list.append(stocks[edit_distance_list[i]]['code'])
            else:
                return_list.append(stocks[edit_distance_list[i]]['sname'])
        return return_list

    def decompKor(word:str):
        """
        한글 문자열 분해한 결과를 리턴
        '삼성전자' => 'ㅅㅏㅁ ㅅㅓㅇ ㅈㅓㄴ ㅈㅏ'
        """
        word = word.upper() # 영어인 경우, 일단 대문자로 바꿔줘야함
        mod_str = ""
        for i in range(len(word)):
            mod_str += f"{j2hcj(h2j(word[i]))} "
        mod_str = mod_str.strip()
        return mod_str

    def levenshtein(src: str, tar: str):
        """
        src와 tar 문자열의 편집거리를 계산한다.
        'cat' <-> 'call'은 2의 편집거리를 갖는다.
        한글의 경우, 삼성전자 ->'ㅅㅏㅁ ㅅㅓㅇ ㅈㅓㄴ ㅈㅏ'와 삼성전기 -> 'ㅅㅏㅁ ㅅㅓㅇ ㅈㅓㄴ ㄱㅣ'를 비교하면 편집거리는 2가 리턴될 것이다.
        """
        # print(f"<<assist::levenshtein>> : parm: {src}, {tar}")
        #1. 2차원 0으로 초기화된 배열 생성
        D = [[0 for _ in range(len(src) + 1)] for _ in range(len(tar) + 1)]
        #2. 0번 index 초기화
        for i in range(len(tar)+1):
            D[i][0] = i
        for i in range(len(src)+1):
            D[0][i] = i
        #3. for 문 돌리면서 edit distance update (replace, insert, delete 중 최소를 찾아서)
        # print(f"length of D : {len(D)}")
        # print(f"length of D[i] : {len(D[0])}")
        for i in range(1, len(D)):
            for j in range(1, len(D[i])):
                replace = D[i-1][j-1]
                insert = D[i-1][j]
                delete = D[i][j-1]
                min_before = min(replace, insert, delete)
                if src[j-1] == tar[i-1]:
                    D[i][j] = min_before
                else:
                    D[i][j] = min_before + 1
        # print(D)
        # print(f"<<assist::levenshtein>> : return: {D[len(tar)][len(src)]}")
        return D[len(tar)][len(src)]
        
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
            stock = stock.first()
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
            stock = stock.first()
            print(f"<<assist::codeToword>> : return: {stock.code}")
            return stock.code

    def parseTrade(self,msg):
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
            success = "/trade (buy/sell) &lt;stock&gt; &lt;count&gt; 의 형태로 입력되었는지 확인해주세요.\n"
            return [success, 0, 0]

        # <stock> 인자 확인
        # 주식 코드 받아오는 메소드 필요
        stock_code = Stock.objects.filter(sname=msg_split[2])
        if stock_code.count() == 1:
            stock_code = stock_code.first().code
        else:
            # 주식명이 잘못된 경우
            ustock_name = msg_split[2].strip()
            recommended_arr = self.recommend(self,ustock_name, 3)
            success = f"'{ustock_name}'에 해당하는 종목이 없습니다."
            success += " 주식 명을 확인해주세요.\n 유사종목: "
            for word in recommended_arr:
                success += f'{word} '
            success +='\n'
        count = 0
        # <count> 인자 확인
        try:
            count = int(msg_split[3])
            if count <= 0:
                success = "&lt;count&gt;에 자연수를 입력해주세요.\n"
        except:
            success = "&lt;count&gt;에 자연수를 입력해주세요.\n"

        return [success, stock_code, count]


    def parseCommunity(msg,room):
        msg_split = msg.split(" ")
        success = ""
        req_user = ""
        if len(msg_split) >= 2:
            if msg_split[1] == "rank":
                if len(msg_split) == 2:
                    success = "rank"
                else:
                    success = "/community rank 의 형태로 입력되었는지 확인해주세요.\n"
            else:
                msg_user = msg.split("/community ")
                # 해당 user가 존재하는지 확인하는 메소드 필요
                req_user = User.objects.filter(uname=msg_user[1],gid = room)
                if req_user.count() == 1:
                    success = "user"
                    req_user = req_user.first().uname
                else:
                    success = "사용자가 존재하지않습니다.\n"
                    req_user = ""
        else:
            success = "/community rank 혹은 /community &lt;user&gt; 형태로 입력되었는지 확인해주세요.\n"


        return [success, req_user]
    
    def parseStock(self, msg):
        msg_split = msg.split(" ")
        success = ""
        stock_code = ""
        theme = ""
        if len(msg_split) == 3:
            if msg_split[1] == "top":
                if msg_split[2] == "deal":
                    success = "deal"
                elif msg_split[2] == "sum":
                    success = "sum"
                elif msg_split[2] == "rise":
                    success = "rise"
                else:
                    success = "/stock top [deal/sum/rise] 로 입력되었는지 확인해주세요.\n"
            elif msg_split[1] == "theme":
                # 테마 정보 받아오는 메소드 필요함
                success = "theme"
                theme = msg_split[2]
            elif msg_split[1] == "state":
                success = "stock"
                stock_code = Stock.objects.filter(sname=msg_split[2])
                if stock_code.count() == 1:
                    stock_code = stock_code.first().code
                else:
                    ustock_name = msg_split[2].strip()
                    recommended_arr = self.recommend(self,ustock_name, 3)
                    success = f"'{ustock_name}'에 해당하는 종목이 없습니다."
                    success += " 주식 명을 확인해주세요.\n 유사종목: "
                    for word in recommended_arr:
                        success += f'{word} '
                    success +='\n'
            else:
                success = "/stock [top/theme/state] 로 시작하며 입력되었는지 확인해주세요.\n"
        else:
            success = "/stock top [deal/sum/rise] 혹은 /stock [theme/state] &lt;theme/stock&gt; 처럼 3개로 구성하여 명령어가 입력되었는지 확인해주세요.\n"
            

        return [success,stock_code, theme]
    
    def parseChart(msg):
        msg_split = msg.split(" ")
        success = ""
        stock_code = ""

        if len(msg_split) >= 2:
            stock_code = Stock.objects.filter(sname=msg_split[1])
            if stock_code.count() == 1:
                stock_code = stock_code.first().code
            else:
                success = "주식 명을 확인해주세요.\n"
                return [success,stock_code]
            if len(msg_split) == 2:
                success = "stock"
            elif len(msg_split) == 3:
                if msg_split[2] == "inform":
                    success = "inform"
                elif msg_split[2] == "institutional":
                    success = "institutional"
                elif msg_split[2] == "individual":
                    success = "individual"
                elif msg_split[2] == "foreign":
                    success = "foreign"
                else:
                    success = "/chart &lt;stock&gt; [inform/institutional/individual/foreign] 중 하나로 입력되었는지 확인해주세요.\n"
            else:
                success = "/chart &lt;stock&gt; [inform/institutional/individual/foreign] 의 형태로 입력되었는지 확인해주세요.\n"
        else:
            success = "/chart &lt;stock&gt; [inform/institutional/individual/foreign] 의 형태로 입력되었는지 확인해주세요.\n"


        return [success,stock_code]
        
    def parseRecord(msg,uroom):
        success = ""
        req_uname = ""

        msg_split = msg.split(" ")
        if len(msg_split) >= 3:
            if msg_split[0] == "/record":
                if msg_split[1] == "trade":
                    msg_user = msg.split("/record trade ")
                    req_user = User.objects.filter(uname=msg_user[1],gid = uroom)
                    if req_user.count() == 1:
                        success = "user"
                        req_uname = req_user.first().uname
                    else:
                        success = "사용자가 존재하지않습니다.\n"
                        req_uname = ""
                else:
                    success = "/record trade &lt;user&gt; 형태로 입력되었는지 확인해주세요.\n"
            else:
                success = "/record trade &lt;user&gt; 형태로 입력되었는지 확인해주세요.\n"
        else:
            success = "/record trade &lt;user&gt; 형태로 입력되었는지 확인해주세요.\n"
            
        return [success, req_uname]
