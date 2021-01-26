#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 9:23 上午
# @Author  : yangqiang
# @File    : 5-crawler-font-puzzle-1
from lxml import etree
from login import login_with_passwd
from ip import headers
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
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
    return int(''.join([font_map[n] for n in num]))


@logger.catch
def spider(url):
    response = session.get(url, headers=headers)
    font_face = re.findall(r'base64,(.*?)\)', response.text)
    with TemporaryFile() as f:
        f.write(base64.b64decode(font_face[0]))
        font = TTFont(f)
        font_map = {str(number_map.get(value)): str(px)
                    for px, value in enumerate(font.getGlyphOrder()[1:])}
    x_data = etree.HTML(response.text)
    nums = x_data.xpath("//div[@class='col-md-1']/text()")
    nums = [get_real(font_map, x.strip()) for x in nums]
    logger.debug("{} {} {}", url.split('=')[-1], sum(nums), nums)
    return sum(nums)


if __name__ == '__main__':
    urls = [
        f"http://www.glidedsky.com/level/web/crawler-font-puzzle-1?page={i}" for i in range(1, 10)]
    session = login_with_passwd()
    pool = ThreadPoolExecutor(max_workers=12)
    res = 0
    logger.add('data/5-crawler-font-puzzle-1.txt', format="{message}")
    for result in pool.map(spider, urls):
        res += result
    print(res)
