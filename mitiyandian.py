#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/1/26 12:49 PM
# @Author  : yangqiang
# @File    : mitiyandian.py
# @Software: PyCharm
import requests
import re
import pandas as pd
import time
import random
import json

def write_brows_info_to_file():
    my_user_agent=requests.get("https://fake-useragent.herokuapp.com/browsers/0.1.11")
    with open("browser_info.json","w") as f:
        json.dump(my_user_agent.text, f)

write_brows_info_to_file()

def get_random_browser():
    with open("browser_info.json","r") as f:
        browsers_json=json.loads(json.load(f))

    browsers = browsers_json["browsers"]
    i=random.randint(0, len(browsers)-1)
    if i==0:
        browsers_name = "chrome"
    elif i==1:
        browsers_name = "opera"
    elif i == 2:
        browsers_name = "firefox"
    elif i == 3:
        browsers_name = "internetexplorer"
    elif i == 4:
        browsers_name = "safari"
    j= random.randint(0,len(browsers[browsers_name])-1)
    return browsers[browsers_name][j]


user_agent = get_random_browser()
headers = {
    "user-agent": user_agent,
    'Referer':"https://www.mi.com/static/familyLocation"
}
proxies = {
    "url": "http://80.241.251.54:8080"
}

# https://api2.service.order.mi.com/aftersale/sitelist?province_id=3&t=1610179994
# url = f"https://api2.service.order.mi.com/aftersale/sitelist?province_id=&t={int(time.time())}"
# r = requests.get(url,headers=headers)
# if r.status_code == 200:
#     with open(f"data/0.json", 'w') as f:
#         f.write(r.text)
# exit(1)
for i in range(1, 40):
    url = f"https://api2.service.order.mi.com/aftersale/sitelist?province_id={i}&t={int(time.time())}"
    r = requests.get(url,headers=headers, proxies=proxies)
    if r.status_code == 200:
        with open(f"data/{i}.json", 'w') as f:
            f.write(r.text)
print(r)
# exit()
