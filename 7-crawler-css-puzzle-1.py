#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/11 9:55 上午
# @Author  : yangqiang
# @File    : 7-crawler-css-puzzle-1.py
# @Software: PyCharm
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from ip import headers
from login import login_with_passwd
from lxml import etree


def css_perse(divs, response_text):
    show_nums = ['' for _ in divs]
    print(show_nums)
    for px, div in enumerate(divs):
        css_name = div.get('class')[0]
        value = div.text
        print("css_name,value",css_name, value)
        if re.findall(rf'\.{css_name} \{{ opacity:0 \}}', response_text):
            continue
        relative = re.findall(
            rf'\.{css_name} \{{ position:relative \}}',
            response_text)
        left = re.findall(rf'\.{css_name} \{{ left:(.*?)em \}}', response_text)
        before = re.findall(
            rf'\.{css_name}:before \{{ content:"(\d+)" \}}',
            response_text)
        if left and relative:
            show_nums[px + int(left[0])] = value
            # print(f"{css_name} {value} left {int(left[0])}")
        elif before:
            show_nums[0] = before[0]
            # print(f"{css_name} {value} before {before[0]}")
        else:
            # print(f"{css_name} {value} 不变 ")
            show_nums[px] = value
    # print(show_nums, int(''.join(show_nums)))
    return int(''.join(show_nums))


def crawler(url):
    text = session.get(url, headers=headers).text

    # 获取12个数中每个数中的css
    x_data = etree.HTML(text)

    # div_elements = x_data.xpath("//div[@class='col-md-1']")
    # items = []  # len=12
    # for div_element in div_elements:
    #     css_name_value = []
    #     for div in div_element:
    #         css_name_value.append((div.attrib['class'], div.text))
    #     items.append(css_name_value)

    styles = x_data.xpath("//style//text()")[0].strip().split('\n')
    styles = [style.strip()[1:] for style in styles]
    for style in styles:
        print(style)
    # print(text)
    # scores = []
    # # print(text)
    # for row in rows:
    #     print("row", row.find_all('div'))
    #     score = css_perse(row.find_all('div'), text)
    #     exit()
    #     scores.append(score)
    # print(f"第{url.split('=')[-1]}页 合计:{sum(scores)} 明细:{scores}")
    return 0


if __name__ == "__main__":
    session = login_with_passwd()
    urls = []
    for i in range(1, 2):
        url = f'http://www.glidedsky.com/level/web/crawler-css-puzzle-1?page={i}'
        urls.append(url)
    pool = ThreadPoolExecutor(max_workers=12)
    score = 0
    for result in pool.map(crawler, urls):
        score += result
