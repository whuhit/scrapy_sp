import urllib.request
import json
import time
import xlwt
from loguru import logger
from ip import proxies
import requests
from retrying import retry  # 不用自己写了


logger.add("小米11.txt", format="{message}")


@retry(stop_max_attempt_number=10, retry_on_result=lambda x: x in [None, 0], wait_fixed=200)
def crawl(start_page):
    for i in range(start_page, 1000):
        print('第%s页开始爬取------'%(i+1))
        url = f'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100009956273&score=0&sortType=5&page={i}&pageSize=10&isShadowSku=0&fold=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Referer': 'https://item.jd.com/100004770259.html'
        }
        request = requests.get(url=url, headers=headers, proxies=proxies)
        content = request.text
        content = content.strip('fetchJSON_comment98();')
        try:
            obj = json.loads(content)
            comments = obj['comments']
            # print(content)
            # break
            # fp = open('小米11.txt','a',encoding='utf8')
            # print(comments)
            # if len(comments) == 0:
            #     count += 1
            # if count > 10:break
            for comment in comments:
                com = comment['content'].replace('\n', '\t')
                logger.debug(f"page-{i+1} {comment['productColor']} {comment['productSize']} {comment['score']} {comment['nickname']} {comment['creationTime']} {com}") #content
        except:
            return None
            # break
        # for comment in comments:
        #     print(comment.keys())
        # break
        # for comment in comments:
        #     #评论时间
        #     creationTime = comment['creationTime']
        #     #评论人
        #     nickname = comment['nickname']
        #     #评论内容
        #     contents = comment['content']
        #     item = {
        #         '评论时间': creationTime,
        #         '用户': nickname,
        #         '评论内容': contents,
        #     }
        #     string = str(item)
        #     fp.write(string + '\n')
        # print('第%s页完成----------'%(i+1))
        time.sleep(1)


crawl(87)
