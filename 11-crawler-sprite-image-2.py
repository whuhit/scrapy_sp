#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 10:14 上午
# @Author  : yangqiang
# @File    : 11-crawler-sprite-image-2.py
import json
import base64
import re
from PIL import Image
from io import BytesIO

import os
import requests
import numpy as np
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from tensorflow import keras
from collections import Counter

from ip import headers

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

model = keras.models.load_model(
    '/Users/yang/01_code/01_004_crawler/captcha_glidedsky/model.h5')


def pic2num(img, box):
    img = img.crop(box).resize((20, 20)).convert('L')
    img_arr = 1 - np.reshape(img, (20, 20, 1)) / 255.0
    x = np.array([img_arr])
    y = model.predict(x)
    return str(np.argmax(y[0]))


def get_img(text):
    """
    :param text: 获取图片模板
    :return:
    """
    img_str = re.findall('base64,(.*?)"', text)[0]
    img_fp = BytesIO(base64.b64decode(img_str.encode('utf-8')))
    img = Image.open(img_fp)
    return img


def crawler(url):
    text = session.get(url, headers=headers).text
    img = get_img(text)
    rows = BeautifulSoup(text, 'lxml').find_all('div', class_="col-md-1")
    scores = []
    for row in rows:
        nums = []
        for div in row.find_all('div'):
            css_name = div.get('class')[0].split(' ')[0]
            tag_x = re.findall(
                rf'\.{css_name} \{{ background-position-x:(.*?)px \}}', text)
            tag_y = re.findall(
                rf'\.{css_name} \{{ background-position-y:(.*?)px \}}', text)
            width = re.findall(rf'\.{css_name} \{{ width:(.*?)px \}}', text)
            height = re.findall(rf'\.{css_name} \{{ height:(.*?)px \}}', text)
            tag_x = abs(int(tag_x[0]))
            tag_y = abs(int(tag_y[0]))
            width = int(width[0])
            height = int(height[0])
            box = (tag_x, tag_y, tag_x + width, tag_y + height)
            num = pic2num(img, box)
            nums.append(num)
        scores.append(int(''.join(nums)))
    # print(f"第{url.split('=')[-1]}页 合计:{sum(scores)} 明细:{scores}")
    log.log(url.split('=')[-1], sum(scores), scores)
    return url, scores


def main(result_path):
    if not os.path.exists(result_path):
        with open(result_path, 'w') as f:
            json.dump({}, f)

    with open(result_path, 'r') as f:
        dt = json.load(f)

    urls = []
    for i in range(1, 1001):
        url = f'http://www.glidedsky.com/level/web/crawler-sprite-image-2?page={i}'
        urls.append(url)

    pool = ThreadPoolExecutor(max_workers=20)
    for result in pool.map(crawler, urls):
        url, scores = result
        if url in dt:
            dt[url].append(scores)
        else:
            dt[url] = [scores]

    with open(result_path, 'w') as f:
        json.dump(dt, f)

    total = 0
    for scores in dt.values():
        total += sum(map(lambda x: Counter(x).most_common(1)
                         [0][0], zip(*scores)))
    print(total)


if __name__ == "__main__":
    from login import login_with_passwd
    from easyPlog import Plog

    log = Plog("data/11-crawler-sprite-image-2.txt", stream=True)
    session = login_with_passwd()

    result_path = 'crawler-sprite-image-2.json'
    for _ in range(5):
        main(result_path)  # 2857209 2857209
