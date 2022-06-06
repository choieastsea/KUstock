"""
주식 시세 조회를 위한 api 요청 등을 처리하고, views.py에서 원하는 결과에 맞게 응답하는 함수를 포함한다.
"""
from myproject.settings import get_env_variable
from bs4 import BeautifulSoup
import requests
import random

def getStockPriceTest(code):
    url = "https://finance.naver.com/item/main.naver?code=" +str(code)
    print(url)
    headers = {'User-agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    html = res.content
    soup = BeautifulSoup(html, 'html.parser')
    tr = soup.select('div > p.no_today > em> span.blind')
    print(tr)
    in_str = int(tr[0].text.replace(",", ""))
    return in_str

def getStockPrice(code):
    """
    this function is for test
    """
    rootURL = "https://api.odcloud.kr/api/GetStockSecuritiesInfoService/v1/"
    url = rootURL + f"getStockPriceInfo?resultType=json&likeSrtnCd={code}&basDt=20220602&serviceKey=9OdEbSYuSWsY3x8Jk%2Bm%2FbFKeOKKPfY6olRpGAUQ8QVVC3xgfbEq8NdZvwscyJTv0KpH2TJIX3E3YylLo%2BUntsA%3D%3D"
    res = requests.get(url).json()
    # print(res)
    high_price = int(res['response']['body']['items']['item'][0]['hipr'])
    low_price = int(res['response']['body']['items']['item'][0]['lopr'])
    # print(high_price, low_price)
    # 100000원 이상은 500원 ,50000원 이상은 100원, 10000원 이상은 50원, 1000원 이상은 10원, 100원 이상은 5원
    unit = 0
    if high_price > 100000:
        unit = 500
    elif high_price >50000:
        unit = 100
    elif high_price > 10000:
        unit = 50
    elif high_price > 5000:
        unit = 10
    else:
        unit = 5
    print(high_price, low_price, unit)
    return random.randint(0,int((high_price-low_price)/unit))*unit + low_price