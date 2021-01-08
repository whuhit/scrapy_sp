#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 9:23 上午
# @Author  : yangqiang
# @File    : crawler-basic-2.py
# @Software: PyCharm
from lxml import etree
from login import login_with_passwd
from ip import headers, proxies
from concurrent.futures import ThreadPoolExecutor
from easyPlog import Plog


def spider(url):
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        print(response.status_code)
        return
    x_data = etree.HTML(response.text)
    nums = x_data.xpath("//div[@class='col-md-1']/text()")
    nums = [int(x.strip()) for x in nums]
    log.log(url.split('=')[-1], sum(nums), nums)
    return sum(nums)


if __name__ == '__main__':
    urls = [
        f"http://www.glidedsky.com/level/web/crawler-basic-2?page={i}" for i in range(1, 1001)]
    session = login_with_passwd()
    pool = ThreadPoolExecutor(max_workers=5)
    res = 0
    log = Plog('data/2-crawler-basic-2.txt', stream=True)
    for result in pool.map(spider, urls):
        res += result
    print(res)  # 2692501
