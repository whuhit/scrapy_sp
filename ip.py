import requests
from easyPlog import Plog
from lxml import etree


if __name__ == "__main__":
    # 进行多页爬取
    log = Plog('config/ip4.txt', stream=True)
    for i in range(1, 2):
        url = f"http://www.xsdaili.cn/dayProxy/ip/2641.html"
        # 发送get请求
        response = requests.get(url=url)
        x_data = etree.HTML(response.content)
        info_list = x_data.xpath("//div/text()")
        # print(info_list)
        # break
        # index_ip = info_list.index('ip')
        # proxy = info_list[::8]
        for ip in info_list:
            if ':' in ip:
                log.log(ip)
        # print(proxy)
        # ips = info_list[index_ip:-1:5]
        # ports = info_list[index_ip+1:-1:5]
        # assert len(ips) == len(ports)
        # break
        # for ip, port in zip(ips[1:], ports[1:]):
        #     proxy = f"http://{ip}:{port}"
        #     log.log(proxy)
        # ips = x_data.xpath("//td[@data-title='IP']/text()")
        # ports = x_data.xpath("//td[@data-title='PORT']/text()")

        #

