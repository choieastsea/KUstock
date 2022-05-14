"""
주식 시세 조회를 위한 api 요청 등을 처리하고, views.py에서 원하는 결과에 맞게 응답하는 함수를 포함한다.
"""
from myproject.settings import get_env_variable
import requests


serviceKey = get_env_variable("api_serviceKey")
rootURL = "https://api.odcloud.kr/api/GetStockSecuritiesInfoService/v1/"

def getStockPrice(code):
    """
    parm : code(주식코드 6자리 문자열)
    return : price(주식 가격)/ -1(해당 종목 존재하지 않을 때)
    """
    # print("getStockPRice: "+code)
    url = rootURL + f"getStockPriceInfo?resultType=json&beginBasDt=20220502&likeSrtnCd={code}&serviceKey={serviceKey}"
    res = requests.get(url).json().get('response').get('body').get('items').get('item')
    if(len(res) == 0):
        price = -1
    else:
        price = int(res[0].get('clpr'))
    return price
