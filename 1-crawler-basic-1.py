from lxml import etree
from login import login_with_passwd
from ip import headers


def spider(url):
    response = session.get(url, headers=headers)
    x_data = etree.HTML(response.text)
    nums = x_data.xpath("//div[@class='col-md-1']/text()")
    nums = [int(x.strip()) for x in nums]
    return sum(nums)


if __name__ == '__main__':
    url = "http://www.glidedsky.com/level/web/crawler-basic-1"
    session = login_with_passwd()
    res = spider(url)
    print(res)
