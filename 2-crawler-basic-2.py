#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 9:23 上午
# @Author  : yangqiang
# @File    : crawler-basic-2.py
from lxml import etree
from login import login_with_passwd
from ip import headers
from concurrent.futures import ThreadPoolExecutor
from loguru import logger


@logger.catch
def spider(url):
    response = session.get(url, headers=headers)
    x_data = etree.HTML(response.text)
    nums = x_data.xpath("//div[@class='col-md-1']/text()")
    nums = [int(x.strip()) for x in nums]
    logger.debug(f"{url.split('=')[-1]} {sum(nums)} {nums}")
    return sum(nums)


if __name__ == '__main__':
    urls = [
        f"http://www.glidedsky.com/level/web/crawler-basic-2?page={i}" for i in range(1, 1001)]
    session = login_with_passwd()
    logger.add('data/2-crawler-basic-2.txt', format="{message}")
    pool = ThreadPoolExecutor(max_workers=12)  # 我的cpu核心数是12
    res = 0
    for result in pool.map(spider, urls):
        res += result
    print(res)


