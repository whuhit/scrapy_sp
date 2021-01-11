#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/1/11 9:55 上午
# @Author  : yangqiang
# @File    : 7-crawler-css-puzzle-1.py
# @Software: PyCharm

# http://www.glidedsky.com/level/web/crawler-css-puzzle-1

import re
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from ip import headers
from login import login_with_passwd


def css_perse(divs, response_text):
    show_nums = ['' for _ in divs]
    for px, div in enumerate(divs):
        css_name = div.get('class')[0]
        value = div.text
        if re.findall(f'\.{css_name} \{{ opacity:0 \}}', response_text):
            # print(f"{css_name} {value} 透明")
            continue
        relative = re.findall(f'\.{css_name} \{{ position:relative \}}', response_text)
        left = re.findall(f'\.{css_name} \{{ left:(.*?)em \}}', response_text)
        before = re.findall(f'\.{css_name}:before \{{ content:"(\d+)" \}}', response_text)
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
    soup = BeautifulSoup(text, 'lxml')
    rows = soup.find_all('div', class_="col-md-1")
    scores = []
    for row in rows:
        score = css_perse(row.find_all('div'), text)
        scores.append(score)
    print(f"第{url.split('=')[-1]}页 合计:{sum(scores)} 明细:{scores}")
    return sum(scores)


if __name__ == "__main__":
    session = login_with_passwd()
    urls = []
    for i in range(1, 1001):
        url = f'http://www.glidedsky.com/level/web/crawler-css-puzzle-1?page={i}'
        urls.append(url)
    pool = ThreadPoolExecutor(max_workers=20)
    score = 0
    for result in pool.map(crawler, urls):
        score += result
    print(score)  # 3020613