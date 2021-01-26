from concurrent.futures import ThreadPoolExecutor
from login.login import login_with_passwd
from loguru import logger
from lxml import etree
from ip import proxies, headers


# 重试装饰器
def retry(func):
    def wrapper(url):
        for i in range(10):
            score = func(url)
            if score > 0:
                return score
        return 0
    return wrapper


@retry
def crawler(url):
    try:
        response = session.get(url, headers=headers, proxies=proxies)
        x_data = etree.HTML(response.text)
        nums = x_data.xpath("//div[@class='col-md-1']/text()")
        nums = [int(x.strip()) for x in nums]
        page_sum = sum(nums)
        if response.status_code == 200 and page_sum > 0:
            logger.debug("{page} {page_sum} {nums}", page=url.split('=')[-1], page_sum=page_sum, nums=nums)
    except:
        logger.error(url)
        page_sum = 0
    return page_sum


if __name__ == "__main__":
    session = login_with_passwd()

    logger.add("data/4-crawler-ip-block-2.txt", format='{message}')

    # 获取已经爬取过的
    already_page = set(int(line.split()[0]) for line in open("data/4-crawler-ip-block-2.txt") if '[' in line)
    # 没有爬完的
    not_ready_page = set(range(1, 1001)) - already_page

    if not not_ready_page:
        exit(0)
    urls = [
        f"http://glidedsky.com/level/web/crawler-ip-block-2?page={i}" for i in not_ready_page]

    print(f"剩余待采集页数:{len(urls)}")
    pool = ThreadPoolExecutor(max_workers=5)  # 除了cpu核数外，还需要考虑代理每秒能提供的ip数
    for res in pool.map(crawler, urls):
        pass


