import os
import json
from concurrent.futures import ThreadPoolExecutor
from login.login import login_with_passwd
from easyPlog import Plog
from lxml import etree
from ip import proxies, headers


# 重试装饰器
def retry(func):
    max_retry = 10

    def run(*args, **kwargs):
        for i in range(max_retry + 1):
            url, score = func(*args, **kwargs)
            if score > 0:
                return url, score
        return func(*args, **kwargs)

    return run


@retry
def crawler(url):
    try:
        response = session.get(url, headers=headers, proxies=proxies)
        x_data = etree.HTML(response.text)
        nums = x_data.xpath("//div[@class='col-md-1']/text()")
        nums = [int(x.strip()) for x in nums]
        score = sum(nums)
        if response.status_code == 200 and score > 0:
            log.log(url.split('=')[-1], score, nums)
    except BaseException:
        score = 0
    return url, score


if __name__ == "__main__":
    session = login_with_passwd()

    # 获取已经爬取过的
    path = "data/3-crawler-ip-block-1.txt"
    already_page = []
    for line in open(path):
        if "[" in line:
            already_page.append(int(line.split()[0]))

    # 没有爬完的
    not_ready_page = list(range(1, 1001))
    for page in already_page:
        not_ready_page.remove(page)

    if not not_ready_page:
        exit(0)
    urls = [
        f"http://www.glidedsky.com/level/web/crawler-ip-block-1?page={i}" for i in not_ready_page]

    log = Plog("data/3-crawler-ip-block-1.txt", stream=True)
    print(f"剩余待采集页数:{len(urls)}")
    pool = ThreadPoolExecutor(max_workers=5)
    pool.map(crawler, urls)
