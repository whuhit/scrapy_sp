#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 3:11 下午
# @Author  : yangqiang
# @File    : crawler-ip-block-1.py
# @Software: PyCharm
from lxml import etree
from login.login import login_with_cookie, login_with_passwd
from easyPlog import Plog
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36',
}

# alerady_page = []
# for line in open("config/ip-block-1.txt"):
#     alerady_page.append(int(line.strip()[0]))
not_page = list(range(500, 1001))
# for i in alerady_page:
#     not_page.remove(i)


# session = login_with_cookie()
session = login_with_passwd()
sum_ = 0
log = Plog("now2.txt", stream=True)
for i in not_page:
    for line in open("config/ip2.txt"):
        proxies = {"http": line.strip()}
        try:
            response = session.get(f"http://www.glidedsky.com/level/web/crawler-ip-block-1?page={i}",
                                   headers=headers, proxies=proxies, timeout=10)
            if response.status_code == 200:
                break
        except:
            print(line.strip(), "失败")
        # if response.status_code != 200:
        #     print("status_code", response.status_code)
        #     continue
    x_data = etree.HTML(response.text)
    nums = x_data.xpath("//div[@class='col-md-1']/text()")
    nums = [int(x.strip()) for x in nums]
    print(nums)
    log.log(f"{i} {sum(nums)}")
    # sum_ += sum(nums)
# print(sum_)