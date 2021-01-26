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

reg1 = "var mihomeData=(.*);"
res1=json.loads(re.findall(reg1, r)[0])
reg2 = "var joinMihomeData=(.*)</script>"
res2=json.loads(re.findall(reg2, r)[0])

mijia={}
for key in res1:
    for key2 in res1[key]:
        for i in range(0,len(res1[key][key2])):
            mijia['province_name']=res1[key][key2][i]['province_name']
            mijia['city_name'] = res1[key][key2][i]['city_name']
            mijia['name'] = res1[key][key2][i]['name']
            mijia['address'] = res1[key][key2][i]['address']
            mijia['tel'] = res1[key][key2][i]['tel']
            with open("mijia.json", "a+") as f:
                json.dump(mijia, f, ensure_ascii=True)
                f.write("\n")
for key in res2:
    for key2 in res2[key]:
        for i in range(0,len(res2[key][key2])):
            mijia['province_name']=res2[key][key2][i]['province_name']
            mijia['city_name'] = res2[key][key2][i]['city_name']
            mijia['name'] = res2[key][key2][i]['name']
            mijia['address'] = res2[key][key2][i]['address']
            mijia['tel'] = res2[key][key2][i]['tel']
            with open("mijia.json", "a+") as f:
                json.dump(mijia, f, ensure_ascii=True)
                f.write("\n")
df = pd.read_json("mijia.json", lines=True, encoding="UTF-8")
df.to_excel("mijia.xlsx")