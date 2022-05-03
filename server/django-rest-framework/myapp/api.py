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
    # print("getStockPRice: "+code)
    url = rootURL + f"getStockPriceInfo?resultType=json&beginBasDt=20220502&likeSrtnCd={code}&serviceKey={serviceKey}"
    res = requests.get(url).json()
    price = res['response']['body']['items']['item'][0]['clpr']
    return price
