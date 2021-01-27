#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/1/26 12:50 PM
# @Author  : yangqiang
# @File    : mishouquanfuwuzhongxin.py
# @Software: PyCharm
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


# def write_brows_info_to_file():
#     my_user_agent=requests.get("https://fake-useragent.herokuapp.com/browsers/0.1.11")
#     with open("browser_info.json","w") as f:
#         json.dump(my_user_agent.text, f)

# write_brows_info_to_file()

# def get_random_browser():
#     with open("browser_info.json","r") as f:
#         browsers_json=json.loads(json.load(f))
#
#     browsers = browsers_json["browsers"]
#     i=random.randint(0, len(browsers)-1)
#     if i==0:
#         browsers_name = "chrome"
#     elif i==1:
#         browsers_name = "opera"
#     elif i == 2:
#         browsers_name = "firefox"
#     elif i == 3:
#         browsers_name = "internetexplorer"
#     elif i == 4:
#         browsers_name = "safari"
#     j= random.randint(0,len(browsers[browsers_name])-1)
#     return browsers[browsers_name][j]


# user_agent = get_random_browser()
# headers = {
#     "user-agent": user_agent,
#     'Referer':"https://www.mi.com/static/familyLocation"
# }
# proxies = {
#     "url": "http://80.241.251.54:8080"
# }

# https://api2.service.order.mi.com/aftersale/salestore_list?city_id=36&t=1611675629
# url = f"https://api2.service.order.mi.com/aftersale/salestore_list?city_id=36&t={int(time.time())}"
# r = requests.get(url,headers=headers)
# if r.status_code == 200:
#     with open(f"data2/0.json", 'w') as f:
#         f.write(r.text)
# exit(1)
# for i in range(0, 500):
#     url = f"https://api2.service.order.mi.com/aftersale/salestore_list?city_id={i}&t={int(time.time())}"
#     r = requests.get(url,headers=headers, proxies=proxies)
#     if r.status_code == 200:
#         with open(f"data2/{i}.json", 'w') as f:
#             f.write(r.text)
# print(r)
# exit()
import glob
#
res = []
for file in glob.glob("data2/*.json"):
    df = json.load(open(file))
    for store in df['data']['storeList']:
        res.append([df['data']['addr']['province_name'], df['data']['addr']['city_name'], store['store_name'], store['store_addr'],store['group_name'], store['store_tel']])
df = pd.DataFrame(res)
df.to_excel("授权体验店.xlsx")