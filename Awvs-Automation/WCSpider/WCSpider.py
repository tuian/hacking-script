#!/usr/bin/env python
# coding=utf-8

"""
Function: Wooyun Company Spider
Author:   Pyx
Time:     2016年3月16日 15:05:19
"""

import urllib2
from bs4 import BeautifulSoup
import random
import time
import argparse


def url_res(url):
    # 设置一个随机的用户代理，模拟浏览器
    user_agent = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
                  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
                  "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                  "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
                  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"]
    req = urllib2.Request(url)
    req.add_header('User-Agent', random.choice(user_agent))

    while True:
        try:
            res = urllib2.urlopen(req)
        except Exception, e:
            continue
        else:
            return res


def url_soup(url):
    soup = BeautifulSoup(url_res(url).read(), 'html.parser', from_encoding='UTF-8')
    soup = soup.find_all('a', rel="nofollow")
    for each in soup:
        print each.string
        save_result(each.string.encode('utf-8'))


def save_result(company):
    # 保存文件名附带时间
    report_name = 'WooyunCompany' + time.strftime('%Y%m%d', time.localtime()) + '.txt'
    with open(report_name, 'a+') as f:
        f.write(company)
        f.write('\n')


def main(p_num):
    # 从第一页开始，最后一页加1
    for x in range(1, p_num+1):
        url = "http://www.wooyun.org/corps/page/" + str(x)
        url_soup(url)

if __name__ == '__main__':
    # 设置一个命令行参数p，默认45页，以后厂商多了，可以自行设定
    parser = argparse.ArgumentParser(prog='WCSpider', usage='WCSpider.py [option]',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="* Wooyun Company Spider *")
    parser.add_argument('-p', metavar='Page', default=45, type=int, help='The end page for crawling')
    arg = parser.parse_args()
    page = arg.p
    main(page)
    print "-----------------It's done-------------------"
