#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 9:23 上午
# @Author  : yangqiang
# @File    : 5-crawler-font-puzzle-1
# @Software: PyCharm
from lxml import etree
from login import login_with_passwd
from ip import headers
from concurrent.futures import ThreadPoolExecutor
from easyPlog import Plog
import re
import base64
from tempfile import TemporaryFile
from fontTools.ttLib import TTFont
number_map = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }


def get_real(font_map, num):
    res = []
    for n in num:
        res.append(font_map[n])
    return int(''.join(res))


def spider(url):
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        print(response.status_code)
        return
    font_face = re.findall('base64,(.*?)\)', response.text)
    with TemporaryFile() as f:
        f.write(base64.b64decode(font_face[0]))
        f.seek(0)
        font = TTFont(f)
        font_map = {str(number_map.get(value)): str(px) for px, value in enumerate(font.getGlyphOrder()[1:])}
        print("font_map", font_map)
    x_data = etree.HTML(response.text)
    nums = x_data.xpath("//div[@class='col-md-1']/text()")
    nums = [get_real(font_map, x.strip()) for x in nums]
    log.log(url.split('=')[-1], sum(nums), nums)
    return sum(nums)


if __name__ == '__main__':
    urls = [
        f"http://www.glidedsky.com/level/web/crawler-font-puzzle-1?page={i}" for i in range(1, 1001)]
    session = login_with_passwd()
    # spider(urls[0])
    pool = ThreadPoolExecutor(max_workers=30)
    res = 0
    log = Plog('data/5-crawler-font-puzzle-1.txt', stream=True)
    for result in pool.map(spider, urls):
        res += result
    print(res)  # 3424933
