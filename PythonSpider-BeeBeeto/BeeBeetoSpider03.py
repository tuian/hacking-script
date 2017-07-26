#!/usr/bin/env python
# coding=utf-8

"""
Function: Spider for BeeBeeto
Author: PyxYuYu
"""

import urllib2
from bs4 import BeautifulSoup
from threading import Thread
from threading import Lock
from Queue import Queue
import re
import os
import time

from argparse import ArgumentParser

# 创建解析对象
# description: 参数帮助信息之前的描述程序
# add_help： 默认是True，False就是禁用-h/-help
parser = ArgumentParser(usage="You can input the number of threads(default 10).", description="This is a spider for BeeBeeto.")
# 指定程序需要接受的命令参数
# 定位参数，执行程序时必选
# parser.add_argument('echo', help='echo the string')
# 可选参数，可选
parser.add_argument('--threads', default=10, type=int, help="input the number of threads")
# 忽略了错误参数的输入
args, remaining = parser.parse_known_args(args=None, namespace=None)
# 可以设置多个命令参数，利用if判断来达到希望达到的目的
print args.threads

url_base = 'http://www.beebeeto.com/pdb/public/?page='
# 创建一个队列保存poc_url
# queue效率比list高
url_queue = Queue()
# 创建一个队别保存poc_name
name_queue = Queue()
# 多个线程保存同一页的poc_name，需要锁定保存的位置，否则会保存同一个name
name_lock = Lock()
# 用来保证多个线程之间分别保存不同的页面
x = 1

# 获取POC和POCURL的一个线程类
class PocGet(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # 全局变量，在函数内声明来确定全局
        # 用来分隔每个线程处理不同的页面
        global x
        name_lock.acquire()
        get_poc(x)
        name_lock.release()
        x = x + 1


# 保存POC到txt文件
def poc_save(save_path, save_name, poc):
    # 创建保存路径
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + '/' + save_name
    with open(path, 'a+') as f:
        f.write(poc)
        f.write('\n')


# 利用POCURL队列获取具体POC内容一个线程类
# 这里一个线程只能获取一个POC，如果一个线程需要获取多个POC
# 就需要一个while循环
class SavePoc(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        poc_path = './BeeBeeto'
        # 方法一 ： 需要开启191条线程
        # url_poc = url_queue.get()
        # each_name = name_queue.get()
        # poc_detail = url_soup(url_poc).find_all('pre')
        # for each_detail in poc_detail:
        #     # 针对文件名中不能出现的几个符号正则替换成空
        #     r = re.compile('[/\?\\<>:\*]')
        #     poc_name = r.sub('', each_name.string) + '.txt'
        #     poc_save(poc_path, poc_name, each_detail.string.encode('utf-8'))
        # url_queue.task_done()
        # name_queue.task_done()
        # 方法二 : 使用while循环就可以自己设定线程数
        while True:
            # 开多少条线程，name_queue.qsize就从哪开始
            # 比如开100条，那么size直接从91开始，因为100条先内带了100个name
            if name_queue.qsize() > 0:
                poc_name = ''
                url_poc = url_queue.get()
                each_name = name_queue.get()
                poc_detail = url_soup(url_poc).find_all('pre')
                for each_detail in poc_detail:
                    # 针对文件名中不能出现的几个符号正则替换成空
                    r = re.compile('[/\?\\<>:\*]')
                    poc_name = r.sub('', each_name.string) + '.txt'
                    poc_save(poc_path, poc_name, each_detail.string.encode('utf-8'))
                print 'saving ' + poc_name
                url_queue.task_done()
                name_queue.task_done()
                print name_queue.qsize()
            else:
                break


def get_poc(page):
    url_first = url_base + str(page)
    full_poc = url_soup(url_first).find_all(href=re.compile(r'poc'))
    for each_public in full_poc:
        print each_public.string + ' is done.'
        url_vul = url_index + each_public.attrs['href']
        print url_vul
        name_queue.put(each_public)
        url_queue.put(url_vul)


def main():
    threads = []
    threads_poc = []
    # 一共有13页，所以开启13条线程获取
    for y in range(13):
        threads.append(PocGet())
        threads[y].setDaemon(True)
        threads[y].start()
    for i in range(13):
        threads[i].join()
    # 一共有191个POC
    # threads_num = int(raw_input('Please input the number of threads: '))
    for a in range(args.threads):
        threads_poc.append(SavePoc())
        threads_poc[a].setDaemon(True)
        threads_poc[a].start()
    for b in range(args.threads):
        threads_poc[b].join()


# 获取URL源码
def url_soup(url):
    # 网站禁止爬虫，需要伪装浏览器
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'
    request = urllib2.Request(url)
    request.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response.read(), 'html.parser')
    return soup

if __name__ == '__main__':
    st = time.time()
    url_index = 'http://www.beebeeto.com'
    print '----------begin----------'
    main()
    print '----------end------------'
    print (time.time() - st)
