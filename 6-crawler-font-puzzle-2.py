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
from loguru import logger
import re
import base64
from tempfile import TemporaryFile
from fontTools.ttLib import TTFont


def get_real(chars, number_list, font_map):
    res = []
    for char in chars:
        sixteen_str = int(char.encode('unicode-escape').decode()[2:], 16)
        res.append(str(number_list.index(font_map[sixteen_str])))
    return int(''.join(res))


@logger.catch
def spider(url):
    response = session.get(url, headers=headers)
    font_face = re.findall(r'base64,(.*?)\)', response.text)
    with TemporaryFile() as f:
        f.write(base64.b64decode(font_face[0]))
        font = TTFont(f)
        number_list = font.getGlyphOrder()[1:11]
        font_map = font.getBestCmap()

    x_data = etree.HTML(response.text)
    nums = x_data.xpath("//div[@class='col-md-1']/text()")
    nums = [get_real(x.strip(), number_list, font_map) for x in nums]
    logger.debug("{} {} {}", url.split('=')[-1], sum(nums), nums)
    return sum(nums)


if __name__ == '__main__':
    path = "data/6-crawler-font-puzzle-2.txt"
    # 获取已经爬取过的
    already_page = set(int(line.split()[0]) for line in open(path) if '[' in line)
    # 没有爬完的
    not_ready_page = set(range(1, 1001)) - already_page
    if not not_ready_page:
        exit(0)

    urls = [
        f"http://glidedsky.com/level/web/crawler-font-puzzle-2?page={i}" for i in not_ready_page]
    print(f"剩余待采集页数:{len(urls)}")

    session = login_with_passwd()
    pool = ThreadPoolExecutor(max_workers=12)
    logger.add('data/6-crawler-font-puzzle-2.txt', format="{message}")
    for result in pool.map(spider, urls):
        pass
