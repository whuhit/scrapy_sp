from lxml import etree
from login import login_with_cookie
from ip import headers, proxies


def spider(url):
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        return
    x_data = etree.HTML(response.text)
    nums = x_data.xpath("//div[@class='col-md-1']/text()")
    nums = [int(x.strip()) for x in nums]
    return sum(nums)


if __name__ == '__main__':
    url = "http://www.glidedsky.com/level/web/crawler-basic-1"
    session = login_with_cookie()
    res = spider(url)
    print(res)  # 322217
