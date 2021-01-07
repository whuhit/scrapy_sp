import requests
from lxml import etree
from login.cookie import load_cookie

url = "http://www.glidedsky.com/level/web/crawler-basic-1"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}
data = {
    'email': 'zhifeix@foxmail.com',
    'password': '19941025qy1111',
    "_token": "XntZhdCtc2c2xdRDLTs4M1Q3OzSFHvSFb7QEnuW6"
}
cookie = load_cookie()
response = requests.get('http://www.glidedsky.com/level/web/crawler-basic-1', headers=headers, cookies=cookie)

x_data = etree.HTML(response.text)
nums = x_data.xpath("//div[@class='col-md-1']/text()")
nums = [int(x.strip()) for x in nums]
print(nums)
print(sum(nums))