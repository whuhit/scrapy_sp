import requests
from lxml import etree
import json


url_login = "http://glidedsky.com/login"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111"
}
path = "cookie_login.json"


def load_cookie():
    with open(path, "r") as f:
        cookie = f.read()
    if cookie == '':
        cookie = {}
    else:
        cookie = json.loads(cookie)
    return cookie


def get_cookie():
    """重新模拟登录，获取cookie
    :return: None
    """
    data = {
            'email': 'zhifeix@foxmail.com',
            'password': '19941025qy1111',
    }
    with requests.Session() as s:
        # 先通过get获取一次token
        login_get = s.get(url_login, headers=headers)
        tree = etree.HTML(login_get.text)
        token = tree.xpath('//input[@type="hidden"]/@value')[0]
        data.update(_token=token)

        # 登陆除了邮箱和密码外还要有一个token参数
        login_post = s.post(url_login, headers=headers, data=data)
        cookie = login_post.cookies.get_dict()
        cookie = json.dumps(cookie, indent=4)
        with open(path, "w") as f:
            f.write(cookie)
