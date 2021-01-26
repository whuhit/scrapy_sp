#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/11 9:26 下午
# @Author  : yangqiang
# @File    : 8=crawler-captcha-1.py
import numpy as np
import time
import os
import cv2
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains


class Crawler:

    def __init__(self):
        self.driver = webdriver.Chrome(
            "/Users/yang/01_code/01_004_crawler/chromedriver")
        self.driver.maximize_window()
        self.driver.get('http://www.glidedsky.com/login')
        self.driver.find_element_by_id("email").send_keys(
            'zhifeix@foxmail.com')  # 输入用户名
        self.driver.find_element_by_id(
            "password").send_keys('19941025qy1111')  # 输入密码
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/main/div[1]/div/div/div/div[2]/form/div[4]/div/button').click()  # 点击登录按钮
        time.sleep(1)

    @staticmethod
    def get_track(distance):
        '''
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        '''
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move(self, distance):
        # move_distance = distance
        slid_ing = self.driver.find_element_by_xpath(
            '//div[@id="tcaptcha_drag_thumb"]')  # 滑块

        # 第一步按住鼠标
        ActionChains(
            self.driver).click_and_hold(
            on_element=slid_ing).perform()  # 点击鼠标左键，按住不放
        time.sleep(0.3)
        # print('第二步,拖动元素')
        # 模拟滑动
        track_list = self.get_track(distance)
        # print("distance", distance, track_list)
        for track in track_list:
            ActionChains(
                    self.driver).move_by_offset(
                    xoffset=track,
                    yoffset=0).perform()  # 鼠标移动到距离当前位置（x,y）
            time.sleep(0.001)
        time.sleep(0.5)
        # print('第三步,释放鼠标')
        ActionChains(self.driver).release(on_element=slid_ing).perform()
        time.sleep(1)

    def get_nums(self):
        window = self.driver.current_window_handle
        self.driver.switch_to.window(window)
        time.sleep(1)
        rows = BeautifulSoup(
            self.driver.page_source,
            'lxml').find_all(
            'div',
            class_="col-md-1")
        nums = [int(row.text) for row in rows]
        return nums

    def get_move_distance(self, url):
        self.driver.get(url)
        time.sleep(1)
        self.driver.switch_to.frame(self.driver.find_element_by_id(
            'tcaptcha_iframe'))  # switch 到 滑块frame

        slide_bg = self.driver.find_element_by_xpath(
            '//img[@id="slideBg"]')  # 大图
        # slide_bg_width = slide_bg.size['width']  # HTML px 像素宽度 341
        # slide_bg_x = slide_bg.location['x']  # 图像到左边界到距离 10

        slide_block = self.driver.find_element_by_xpath(
            '//img[@id="slideBlock"]')  # 小滑块
        # slide_block_x = slide_block.location['x']  # 滑块到左边界的距离 36

        slide_bg_url = slide_bg.get_attribute('src')  # 大图 url
        slide_block_url = slide_block.get_attribute('src')  # 小滑块 图片url

        slide_bg_image = np.asarray(
            bytearray(
                urlopen(slide_bg_url).read()),
            dtype="uint8")
        slide_bg_image = 255 - cv2.imdecode(slide_bg_image, 0)
        # slide_bg_image_width = slide_bg_image.shape[1]

        slide_block_image = np.asarray(
            bytearray(
                urlopen(slide_block_url).read()),
            dtype="uint8")
        slide_block_image = cv2.imdecode(slide_block_image, 0)

        result = cv2.matchTemplate(
            slide_bg_image,
            slide_block_image,
            cv2.TM_CCOEFF_NORMED)
        row, col = np.unravel_index(result.argmax(), result.shape)
        # print("row, col", row, col)

        # end_distance = x / slide_bg_image_width * slide_bg_width   # x/680*340.81
        # start_distance = slide_block_x - slide_bg_x  # 36-10
        # move_distance = end_distance - start_distance
        move_distance = col / 2 - 26
        return move_distance

        # cv2.imshow("slide_bg_image", slide_bg_image)
        # cv2.imshow("slide_block_image", slide_block_image)
        # cv2.waitKey()

    def main(self, urls, result_path):
        with open(result_path, 'r') as f:
            dt = json.load(f)
        for url in urls:
            for _ in range(10):
                try:
                    distance = self.get_move_distance(url)
                    time.sleep(0.5)
                    self.move(distance)
                    scores = self.get_nums()
                    # scores = self.crawler(url)
                except BaseException:
                    continue
                if scores:
                    print(
                        f"第{url.split('=')[-1]}页 合计:{sum(scores)} 明细:{scores}")
                    dt[url] = sum(scores)
                    with open(result_path, 'w') as f:
                        json.dump(dt, f)
                    break
                if _ > 5:
                    exit(9)

    # def __del__(self):
    #     self.driver.quit()
    #     shutil.rmtree(self.img_dir)


if __name__ == '__main__':

    result_path = f'crawler-captcha-1.json'
    if not os.path.exists(result_path):
        with open(result_path, 'w') as f:
            json.dump({}, f)

    with open(result_path, 'r') as f:
        dt = json.load(f)

    urls = [
        f'http://www.glidedsky.com/level/web/crawler-captcha-1?page={i}' for i in range(1, 1001)]

    for key, value in dt.items():
        if value > 0:
            urls.remove(key)

    if not urls:
        print(sum(dt.values()))
    else:
        print(f"剩余待采集页数:{len(urls)}")
        Crawler().main(urls, result_path)  # 2819405
