"""
주식 시세 조회를 위한 api 요청 등을 처리하고, views.py에서 원하는 결과에 맞게 응답하는 함수를 포함한다.
"""
from myproject.settings import get_env_variable
from bs4 import BeautifulSoup
import requests

def getStockPrice(code):
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