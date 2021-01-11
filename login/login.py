#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 2:09 下午
# @Author  : yangqiang
# @File    : login.py
# @Software: PyCharm
import requests
import json
from lxml import etree
from ip import headers


def login_with_passwd():
    data = {
        'email': 'zhifeix@foxmail.com',
        'password': '19941025qy1111',
    }
    s = requests.Session()
    # 先通过get获取一次token
    login_get = s.get("http://glidedsky.com/login", headers=headers)
    tree = etree.HTML(login_get.text)
    token = tree.xpath('//input[@type="hidden"]/@value')[0]
    data.update(_token=token)

    # 登陆除了邮箱和密码外还要有一个token参数
    s.post("http://glidedsky.com/login",
           headers=headers,
           data=data)
    return s


def get_cookie():
    data = {
        'email': 'zhifeix@foxmail.com',
        'password': '19941025qy1111',
    }
    with requests.Session() as s:
        # 先通过get获取一次token
        login_get = s.get("http://glidedsky.com/login", headers=headers)
        tree = etree.HTML(login_get.text)
        token = tree.xpath('//input[@type="hidden"]/@value')[0]
        data.update(_token=token)

        # 登陆除了邮箱和密码外还要有一个token参数
        login_post = s.post(
            "http://glidedsky.com/login",
            headers=headers,
            data=data)
        cookie = login_post.cookies.get_dict()
        cookie = json.dumps(cookie, indent=4)
        with open("cookie_login.json", "w") as f:
            f.write(cookie)


# 如果cookie没有或者失效，可以用上面的函数生成cookie
def login_with_cookie():
    session = requests.Session()
    cookie = json.loads(open("login/cookie_login.json"))  # cookie有效期过后会失效
    # print(cookie)
    session.cookies.update(cookie)
    return session


if __name__ == '__main__':
    get_cookie()