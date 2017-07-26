#!/usr/bin/env python
# coding=utf-8

"""
Function: Ingored Vulnerabilities Spider for Wooyun
Author: PyxYuYu
Time: 2016年3月11日 23:05:44
"""

import urllib2
from bs4 import BeautifulSoup
import re
import time
from cmdline import parse_args
        

# 返回soup，获取url源码
def url_res(url):
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"
    req = urllib2.Request(url)
    req.add_header("User-Agent", user_agent)
    res = urllib2.urlopen(req).read()
    return res


# 分析源码，正则或者BeautifulSoup模块
def get_url(page):

    vul_public = "http://wooyun.org/bugs/new_public/page/" + str(page)
    # 测试用
    # print url_soup(vul_public).find_all('a')
    # 方法一：先找<a>这个tag，找到后在找href，然后匹配
    # for each in BeautifulSoup(url_res(vul_public),'html.parser', from_encoding='UTF-8').find_all('a'):
    #     # print each['href']
    #     # 判断一下是什么类型 unicode
    #     # print type(each['href'])
    #     # /bugs/wooyun-2016-0176846 正则匹配
    #     # 会有2个网址匹配出来，带个#就只能匹配出一个了
    #     url_re = re.compile(r'/bugs/.*\d{6}#')
    #     # 返回的是一个列表，没匹配到返回空列表
    #     each_url = url_re.findall(each['href'])
    #     if each_url != []:
    #         # 每个列表只有一个元素
    #         # vul_list.append(each_url[0])
    #         print each_url[0]
    #         # 寻找忽略漏洞
    #         if get_vul(each_url[0]) > 0:
    #             vul_detail(each_url[0])
    #         else:
    #             print "Didn't find."
    #     else:
    #         pass
    # 方法二：更加简单，直接匹配了找
    for each in BeautifulSoup(url_res(vul_public), 'html.parser', from_encoding='UTF-8').find_all(href=re.compile(
            r'/bugs/.*\d{6}'), title=None):
        # print each.string
        # 厂商忽略的漏洞
        if get_vul(each['href']) > 0:
            print each.string
            # vul_detail(each['href'])
            print "http://www.wooyun.org/" + each['href']
            print "The vulnerability is ignored."
        else:
            # print "The vulnerability is fixed."
            pass


def get_vul(url):

    url_ignored = "http://www.wooyun.org/" + url
    return url_res(url_ignored).find("忽略")


def vul_detail(url):

    url_vul = "http://www.wooyun.org/" + url
    soup = BeautifulSoup(url_res(url_vul), 'html.parser', from_encoding='UTF-8')
    # print soup.find_all('title')[0].string
    for each in soup.find_all('code'):
        # 因为each.string 无法获取其内包含多个子节点的内容，返回None
        # 所以用 get_text()
        print each.get_text()


def main(s_num, e_num):

    for i in range(s_num, e_num):
        get_url(i)

    print "-------------------It's done.--------------------"


if __name__ == "__main__":
    start_time = time.time()
    # 创建命令行参数 Namespace对象
    args = parse_args()
    main(args.s, args.e)
    cost_time = time.time() - start_time
    print "Current spider is finished in " + str(int(cost_time / 60)) + " mins %.2f seconds." % (cost_time % 60)
