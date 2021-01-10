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


def get_real(chars, number_list, font_map):
    res = []
    for char in chars:
        sixteen_str = int(char.encode('unicode-escape').decode()[2:], 16)
        res.append(str(number_list.index(font_map[sixteen_str])))
    return int(''.join(res))
    # print(sixteen_str)
    # print(font_map[int(sixteen_str[0], 16)])



def spider(url):
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        print(response.status_code)
        return 0
    font_face = re.findall('base64,(.*?)\)', response.text)
    with TemporaryFile() as f:
        f.write(base64.b64decode(font_face[0]))
        f.seek(0)
        font = TTFont(f)
        number_list = font.getGlyphOrder()[1:11]
        font_map = font.getBestCmap()

    x_data = etree.HTML(response.text)
    nums = x_data.xpath("//div[@class='col-md-1']/text()")
    nums = [get_real(x.strip(), number_list, font_map) for x in nums]
    log.log(url.split('=')[-1], sum(nums), nums)
    return sum(nums)


if __name__ == '__main__':
    path = "data/6-crawler-font-puzzle-2.txt"
    already_page = []
    for line in open(path):
        if "[" in line:
            already_page.append(int(line.split()[0]))
    # print(sum(already_page))
    # exit()

    # 没有爬完的
    not_ready_page = list(range(1, 1001))
    for page in already_page:
        not_ready_page.remove(page)

    if not not_ready_page:
        exit(0)

    urls = [
        f"http://glidedsky.com/level/web/crawler-font-puzzle-2?page={i}" for i in not_ready_page]
    print(f"剩余待采集页数:{len(urls)}")

    session = login_with_passwd()
    # spider(urls[0])
    pool = ThreadPoolExecutor(max_workers=5)
    res = 0
    log = Plog('data/6-crawler-font-puzzle-2.txt', stream=True)
    for result in pool.map(spider, urls):
        # if result
        # res += result
        pass
    print(res)  # 2798506
