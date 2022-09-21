import requests
import json

data = {
"NAME_CONTRACT_TYPE":"Cash loans",
"CODE_GENDER":"M",
"FLAG_OWN_CAR":"Y",
"FLAG_OWN_REALTY": "Y",
"CNT_CHILDREN": 0,
"AMT_INCOME_TOTAL": 202500000000,
"AMT_CREDIT":406597.5,
"NAME_INCOME_TYPE": "Working",
"NAME_EDUCATION_TYPE": "Higher education",
"DAYS_BIRTH": 45,
"EXT_SOURCE_2": 0.5,
"FLAG_PHONE": 1
}

url = 'http://127.0.0.1:8000/predict'
headers = {"Content-Type": "application/json"}

response = requests.request(method='POST', headers=headers, url=url, json=data)

if response.status_code != 200:
    raise Exception(
        "Request failed with status {}, {}".format(response.status_code, response.text))

print(response.json())

#print(response.text)