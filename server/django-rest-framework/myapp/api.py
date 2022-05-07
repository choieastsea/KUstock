"""
주식 시세 조회를 위한 api 요청 등을 처리하고, views.py에서 원하는 결과에 맞게 응답하는 함수를 포함한다.
"""

from pathlib import Path
import os
import json
from django.core.exceptions import ImproperlyConfigured
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# https://jinmay.github.io/2019/10/12/django/django-secret-key-management/
secret_key = os.path.join(BASE_DIR, 'secret.json')
with open(secret_key) as f:
    secrets = json.loads(f.read())

def get_env_variable(key):
    try:
        return secrets[key]
    except KeyError:
        error_msg = f"Set the {key} environment variable"
        raise ImproperlyConfigured(error_msg)


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
