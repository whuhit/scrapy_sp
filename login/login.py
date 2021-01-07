#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 2:09 下午
# @Author  : yangqiang
# @File    : login.py
# @Software: PyCharm
import requests
import json
from lxml import etree
from login.cookie import load_cookie

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111"
}


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
    login_post = s.post("http://glidedsky.com/login", headers=headers, data=data)
    return s


def login_with_cookie():
    session = requests.Session()
    cookie = load_cookie()
    session.cookies.update(cookie)
    return session
