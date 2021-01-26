#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 10:05 上午
# @Author  : yangqiang
# @File    : 9-crawler-javascript-obfuscation-1.py
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor
from ip import headers
from login import login_with_passwd
from loguru import logger


@logger.catch
def crawler(url):
    t = int(time.time())
    sign = hashlib.sha1(
        f'Xr0Z-javascript-obfuscation-1{t}'.encode()).hexdigest()
    real_url = f'{url}&t={t}&sign={sign}'
    response = session.get(real_url, headers=headers).json()
    items = response.get('items')
    logger.debug("{page} {page_sum} {items}", page=url.split(
        '=')[-1], page_sum=sum(items), items=items)
    return sum(items)


if __name__ == "__main__":
    logger.add(
        "data/9-crawler-javascript-obfuscation-1.txt",
        format='{message}')
    session = login_with_passwd()  # 保持登陆状态
    urls = [
        f'http://www.glidedsky.com/api/level/web/crawler-javascript-obfuscation-1/items?page={i}' for i in range(1, 1001)]
    pool = ThreadPoolExecutor(max_workers=12)
    res = 0
    for page_sum in pool.map(crawler, urls):
        res += page_sum
    print(res)
