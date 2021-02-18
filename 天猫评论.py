#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/18 16:48
# @Author  : yangqiang
# @File    : 天猫评论.py
import requests
import time
import json
from ip import proxies
from loguru import logger


headers = {
    # 'cookie': 'cna=sn8pGPljhTkCAWcrwF7ZpNhi; xlly_s=1; login=true; cookie2=19a021f7cd7a042b90dc13c49bd522d9; t=0f788266c03bfc19209fff381344a62c; _tb_token_=ee3eebb83babb; _m_h5_tk=395cbf8d1758482da0d5481fe86e3e92_1604659560022; _m_h5_tk_enc=83f1c7c092b6f082b5af4876835338f6; dnk=%5Cu7B1B%5Cu54E5wudi1205692955; uc1=existShop=false&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&pas=0&cookie14=Uoe0abRp%2BNkh7Q%3D%3D&cookie15=VT5L2FSpMGV7TQ%3D%3D&cookie21=WqG3DMC9Fb5mPLIQo9kR; uc3=id2=UUGq2QCLsBBMLg%3D%3D&vt3=F8dCufOGCvLrV96eAQI%3D&nk2=1p5O%2FF0swbAE8zhT4OaT04Gl&lg2=VT5L2FSpMGV7TQ%3D%3D; tracknick=%5Cu7B1B%5Cu54E5wudi1205692955; lid=%E7%AC%9B%E5%93%A5wudi1205692955; uc4=id4=0%40U2OdLQ3GfM3cc1vcJ42wnUb5La95&nk4=0%401C9mHOrX55%2FjNxwvJhLdBL2oXyNdp0jC1enYYA0%3D; _l_g_=Ug%3D%3D; unb=2988158160; lgc=%5Cu7B1B%5Cu54E5wudi1205692955; cookie1=B0E3JfOkAyZQf48jClVyq31E5B4zrJWjK2QFOKSgurc%3D; cookie17=UUGq2QCLsBBMLg%3D%3D; _nk_=%5Cu7B1B%5Cu54E5wudi1205692955; sgcookie=E100c0VbSCMjivQ%2FdVcOznJm3ne00CZ%2FibMjICX%2F6hlTkmRrSwIT6q1367tlHz10HAp9GDxf6DeMwwY4QuT6oHbvYA%3D%3D; sg=505; csg=594738b2; enc=jy%2F%2F%2BchU%2BotYBcMnUgCvc2sXETOGYd3wmCloqxARsiVgjgoHzfGi5TRlw4mpux4r%2Boc10jShp89tU0Ay%2BqsLfg%3D%3D',

              # 'cookie': "cna=hwX3F3F5LiACAbmndHNJRWQK; hng=TW|zh-TW|TWD|158; t=663c5331e259fd794ea4eecad15e4187; _tb_token_=4b966e34e153; cookie2=107f41b1acf56d26f89a8532ed29dfd5; xlly_s=1; _m_h5_tk=8f23f1689ed79dbb4d2cb5b0b6a2b8ee_1613647911527; _m_h5_tk_enc=f0f9c26a18d91f56e8a03ee0904311d1; dnk=\u77E5\u975Ess; uc1=cookie15=UIHiLt3xD8xYTw==&cookie21=VT5L2FSpczFp&cookie14=Uoe1gWFVVwDB6Q==&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA==&pas=0&existShop=false; uc3=id2=UoCIQBRNANRejA==&vt3=F8dCuASlpwsLMFZ+c34=&nk2=teFqpLe9&lg2=URm48syIIVrSKA==; tracknick=\u77E5\u975Ess; lid=知非ss; _l_g_=Ug==; uc4=id4=0@UOg0Mrq2gXi6ipynmTmswIIs1pcj&nk4=0@t1WzX9TAdJPrerJ38+ZVeMQ=; unb=1116179455; lgc=\u77E5\u975Ess; cookie1=BdM4/g4V6Wrl1Xct9a18J8L+LS+3a32Y24CVVm/2N7s=; login=true; cookie17=UoCIQBRNANRejA==; _nk_=\u77E5\u975Ess; sgcookie=E100Io2QxzHZk6uRLQ6mepGotiaHbJJ0elQwlzKRlq/MGQCf7DNdxbf3ZvjEs5GHUlTvweDIoAdS6KsIB2Rgt/iqOQ==; sg=s5e; csg=92962859; enc=OYcIHhV0JUEQ7L+qBIpxziJrU5Y7bAJXoELpg+yyH8H3kI46l/jENWwK0laioqG2EHQbdTLrpyFaS1D+rU46bw==; x5sec=7b22726174656d616e616765723b32223a22373939616536353534623337613733313935656631383165346461663737323843504c7675494547454a57383074794e6e4e656e61786f4d4d5445784e6a45334f5451314e5473784d4f32352f397a2b2f2f2f2f2f77453d227d; tfstk=cXMdBn1XNhIpHrqt0XdGPoOrpogdZzSL5MaPenjpJbODTuXRioHmHB6DOuQLBhC..; l=eBrzLQUcjS6UaqxvBOfwlurza77ORIRAguPzaNbMiOCPOWCNIDqhW6iEEnYeCnGVh64HR3uM7lA4BeYBchVgx6aNa6Fy_Ckmn; isg=BMbGpK_J2v81tI4bync9lMUYF7pIJwrhmqp29LDvkun4s2bNGLXo8cxNi-9_GwL5",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'referer': 'https://detail.tmall.com/item.htm?spm=a1z10.1-b-s.w15914280-23316158322.1.485e5f3bWA66GZ&id=634228151538&scene=taobao_shop&sku_properties=10004:7195672376',
}

logger.add("天猫—小米11.txt", format="{message}")

def crawler(start_page):
    for page in range(start_page, 1500):
        url = f"https://rate.tmall.com/list_detail_rate.htm?itemId=634228151538&spuId=1925594062&sellerId=1714128138&order=3&currentPage={page}&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvXQvWvRyvUpCkvvvvvjiWPLMOsjnHR2dOAjivPmPWzjYPP2zO6jrUPFFvzjrPRF9Cvvpvvvvv9vhv2nQwE0pnzYswMCsL7F9CvvpvvvvvvvhvC9v9vvCvp89Cvv9vvUmqY8MKaO9CvvOUvvVCJhmgvpvIvvvvFhCvvvvvvvP7phvvSQvv9QCvpCmCvvv2lyCvhC6vvvP7phvpNv9CvhQU6QZvC0Ergjc6%2Bul1bbmxfwkK5kx%2Fgj7QD46wjomxfw3lHdUf8cc60f06WeCp%2BExr18TJEcq9afmxdBQaUUkU%2BE7rVC69F7zZaB4A29hvCPMMvvmevpvhvvmv9IOCvvpvCvvvdvhvhovUMQc%2BqvphvmeS8kH2mOcE&needFold=0&_ksTS=1613638713024_534&callback=jsonp535"
        try:
            data = requests.get(url, headers=headers, proxies=proxies).text.replace('jsonp535(', '')[:-1]
            data = json.loads(data)
            print(data)
            for i, rate in enumerate(data['rateDetail']['rateList']):
                user_name = rate["displayUserNick"]
                product = rate['auctionSku']
                comment_time = rate['rateDate']
                comment = rate['rateContent']
                reply = rate['reply']
                logger.debug(f"page-{page}.{i+1} {user_name} {product} {comment_time} {comment} reply:{reply}")
                # time.sleep(2)
        except:
            return page
    return False


start_page = 125
while start_page:
    start_page = crawler(start_page)
    time.sleep(60)
