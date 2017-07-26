#!/usr/bin/env python
# coding=utf-8

"""
Function: Spider for BeeBeeto
Author: PyxYuYu
"""

import urllib2
from bs4 import BeautifulSoup
import re
import os
import sys
import argparse

# 保存POC到txt文件
def Poc_Save(save_path, save_name, poc):
    # 创建保存路径
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + '/' + save_name
    with open(path, 'a+') as f:
        f.write(poc)
        f.write('\n')

# 获取URL源码
def Url_Soup(url):
    # 网站禁止爬虫，需要伪装浏览器
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'
    request = urllib2.Request(url)
    request.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response.read(), 'html.parser')
    return soup

# 获取POC数据
def Poc_Get():

    global poc_list
    global sign
    x = 1
    url_base = 'http://www.beebeeto.com/pdb/public/?page='
    url_first = url_base + str(x)
    poc_path = './BeeBeeto'
    full_poc = Url_Soup(url_first).find_all(href=re.compile(r'poc'))
    for each_public in full_poc:
        poc_list.append(each_public.string)
        print each_public.string + ' is done.'
        url_vul = url_index + each_public.attrs['href']
        poc_detail = Url_Soup(url_vul).find_all('pre')
        for each_detail in poc_detail:
            poc_name = each_public.string.replace('/', '') + '.txt'
            Poc_Save(poc_path, poc_name, each_detail.string.encode('utf-8'))
    print 'This page is done.The next page is starting.'
    x = 2
    url = url_base + str(x)
    while x <= 100:
        if (sign!=0):
            Poc_Get1(url)
            x = x + 1
            url = url_base + str(x)
        else:
            break

def Poc_Get1(url):

    global poc_list
    global sign
    poc_path = './BeeBeeto'
    full_poc = Url_Soup(url).find_all(href=re.compile(r'poc'))
    for each_public in full_poc:
        if each_public.string in poc_list:
            print "It's over."
            sign = 0
            return 0
        else:
            poc_list.append(each_public.string)
            print each_public.string + ' is done.'
            url_vul = url_index + each_public.attrs['href']
            poc_detail = Url_Soup(url_vul).find_all('pre')
            for each_detail in poc_detail:
                # 针对文件名中不能出现的几个符号正则替换成空
                a = re.compile('[/\?\\<>:\*]')
                poc_name = a.sub('', each_public.string) + '.txt'
                Poc_Save(poc_path, poc_name, each_detail.string.encode('utf-8'))
    print 'This page is done.The next page is starting.'


if __name__ == '__main__':
    sign = 1
    poc_list = []
    print '----start----'
    url_index = 'http://www.beebeeto.com'
    Poc_Get()
    print '----end------'
    
