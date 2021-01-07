#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 9:23 上午
# @Author  : yangqiang
# @File    : crawler-basic-2.py
# @Software: PyCharm
from lxml import etree
from login.login import login_with_cookie, login_with_passwd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36',
}


# session = login_with_cookie()
session = login_with_passwd()
sum_ = 0
for i in range(1, 1001):
    response = session.get(f"http://www.glidedsky.com/level/web/crawler-basic-2?page={i}", headers=headers)
    x_data = etree.HTML(response.text)
    nums = x_data.xpath("//div[@class='col-md-1']/text()")
    nums = [int(x.strip()) for x in nums]
    # print(nums)
    sum_ += sum(nums)
print(sum_)
