import requests
from easyPlog import Plog
from lxml import etree


if __name__ == "__main__":
    # 进行多页爬取
    log = Plog('config/ip2.txt', stream=True)
    for i in range(100, 2000):
        url = f"http://www.66ip.cn/{i}.html"
        # 发送get请求
        response = requests.get(url=url)
        x_data = etree.HTML(response.content)
        info_list = x_data.xpath("//td/text()")
        index_ip = info_list.index('ip')
        ips = info_list[index_ip:-1:5]
        ports = info_list[index_ip+1:-1:5]
        assert len(ips) == len(ports)
        for ip, port in zip(ips[1:], ports[1:]):
            proxy = f"http://{ip}:{port}"
            log.log(proxy)
        # ips = x_data.xpath("//td[@data-title='IP']/text()")
        # ports = x_data.xpath("//td[@data-title='PORT']/text()")

        #

