#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 3:11 下午
# @Author  : yangqiang
# @File    : crawler-ip-block-1.py
# @Software: PyCharm
from lxml import etree
from login.login import login_with_cookie, login_with_passwd
from easyPlog import Plog
from concurrent.futures import ThreadPoolExecutor


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36',
}

# session = login_with_cookie()
session = login_with_passwd()
log = Plog("now.txt", stream=True)
log2 = Plog("可用ip.txt", stream=True)

def crawler(paras):
    url, ip = paras
    proxies = {"http": ip}
    try:
        response = session.get(url, headers=headers, proxies=proxies, timeout=10)
        log2.log(ip, response.status_code)
    except:
        print(ip, "失败")
        return
    x_data = etree.HTML(response.text)
    nums = x_data.xpath("//div[@class='col-md-1']/text()")
    nums = [int(x.strip()) for x in nums]
    # if not nums:
    #     print(response.text)
    print(url, nums)
    if nums:
        log.log(f"{url.split('=')[-1]} {sum(nums)}")
    return sum(nums)


if __name__ == '__main__':
    paras_list = []
    ips = []
    for line in open("config/ip3.txt"):
        ips.append(line.strip())

    alerady = []
    for line in open("config/ip-block-1.txt"):
        alerady.append(int(line.split()[0]))
    not_yet = list(range(1, 1001))
    for i in alerady:
        not_yet.remove(i)
    print(f"已经爬取{len(alerady)}页，还剩{len(not_yet)}页未爬取")
    print(not_yet)

    # exit()
    for i, page in enumerate(not_yet):
        url = f"http://www.glidedsky.com/level/web/crawler-ip-block-1?page={page}"
        ip = ips[i+700]
        paras_list.append([url, ip])
    pool = ThreadPoolExecutor(max_workers=30)
    for result in pool.map(crawler, paras_list):
        # print(result)
        pass
