import requests
from config import global_config
from spider import SpiderSession
from lxml import etree
from cookie import load_cookie
from bs4 import BeautifulSoup


url = "http://www.glidedsky.com/level/web/crawler-basic-1"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}
data = {
    'email': 'zhifeix@foxmail.com',
    'password': '19941025qy1111',
    "_token": "XntZhdCtc2c2xdRDLTs4M1Q3OzSFHvSFb7QEnuW6"
}
# session = requests.Session()
# session.post(url, headers=headers, data=data)
# 登录后，我们需要获取另一个网页中的内容
# print(session.cookies)
cookie = load_cookie()
response = requests.get('http://www.glidedsky.com/level/web/crawler-basic-1', headers=headers,cookies=cookie)
print(response.status_code)
print(response.text)

rows = BeautifulSoup(response.text, 'lxml').find_all('div', class_="col-md-1")
score = sum(int(row.text) for row in rows)
print(score)