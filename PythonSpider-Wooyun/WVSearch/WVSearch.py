#!/usr/bin/env python
# coding=utf-8

"""
Function: Wooyun Vulnerabilities Search
Author:   PyxYuYu
Time:     2016年3月14日 20:10:37
"""

import urllib2
from bs4 import BeautifulSoup
from Queue import Queue
from threading import Thread
from string import Template
from cmdline import parse_args
from report import TEMPLATE_html, TEMPLATE_result
import random
import re
import time
import os, sys
import webbrowser


# url页面解析
def url_res(url):
    req = urllib2.Request(url)
    # 随机User-Agent
    ua_list = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
               "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
               "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
               "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
               "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"]
    user_agent = random.choice(ua_list)
    req.add_header('User-Agent', user_agent)
    while 1:
        try:
            res = urllib2.urlopen(req)
        except Exception, e:
            # pass
            continue
        else:
            return res


# 创建一个队列，用于存放所有的url页面
def page_queue(s_page, e_page):
    url = "http://wooyun.org/bugs/page/"
    # 循环放入到队列中，不包括e_page
    for i in xrange(s_page, e_page):
        url_num = url + str(i)
        url_queue.put(url_num)
    # 最后一个页面也放入队列中
    e_url = url + str(e_page)
    url_queue.put(e_url)


# url页面分析，寻找关键字
def search_key(url, key):

    # IDE输入中文是utf-8
    # key = unicode(key, 'utf-8')
    # cmd输入中文是gb18030
    key = unicode(key, 'gb18030')
    key_list = key.split('|')
    html = url_res(url).read()
    soup = BeautifulSoup(html, 'html.parser', from_encoding='UTF-8')
    url_tag = soup.find_all(href=re.compile(r'/bugs/.*\d{6}'), title=None)
    global _str
    # 检测是否有重名的漏洞被写入到_str中

    for each in url_tag:
        # print each.string
        for i in xrange(len(key_list)):
            if key_list[i] in each.string:
                # name = each.string.encode('gb18030')
                _name = each.string
                # 检测是否有重名的漏洞
                if _name not in test_name:
                    test_name.append(_name)
                    _url =  "http://www.wooyun.org/" + each['href']
                    _str += t_result.substitute({'name': _name, 'url': _url})


# 多线程采集url分析关键字漏洞
class SearchThread(Thread):

    def __init__(self, key):
        Thread.__init__(self)
        # super(Thread, self).__init__()
        self.key = key
        # self.lock = Lock()

    def run(self):
        # global start_time
        while True:
            if url_queue.empty(): break
            url_now = url_queue.get()
            # print url_now # 测试用
            search_key(url_now, self.key)
            url_queue.task_done()

            # 最下面显示实时信息，清除缓冲
            # self.lock.acquire() 因为光标会重新回到开头，队列又是安全的，所以不用锁
            msg = '%s remaining in %.2f seconds' % (
            url_queue.qsize(), time.time() - start_time)
            # 用 \r 来保证每个线程输出都在同一行，光标从新回到开头
            sys.stdout.write('\r' + ' ' * 40)
            sys.stdout.flush()
            sys.stdout.write('\r' + msg)
            # 清除缓冲一般都用于实时监测
            sys.stdout.flush()
            # self.lock.release()


def main(num_t, key):

    threads = []
    for x in xrange(num_t):
        threads.append(SearchThread(key))
        threads[x].start()

    for y in threads:
        y.join()


if __name__ == "__main__":

    url_queue = Queue()
    test_name = []
    start_time = time.time()
    args = parse_args()
    s_page = args.s
    e_page = args.e
    n_thread = args.t
    keywords = args.k
    page_queue(s_page, e_page)

    # 用于保存所有的漏洞名和漏洞链接
    _str = ''
    _content = ''
    t_html = Template(TEMPLATE_html)
    t_result = Template(TEMPLATE_result)

    main(n_thread, keywords)
    print "\n--------------------It's done.---------------------"
    cost_time = time.time() - start_time
    _content += _str
    cost_min = int(cost_time / 60)
    cost_seconds = '%.2f' % (cost_time % 60)
    total_name = len(test_name)
    # 模板替换
    html_doc = t_html.substitute({'cost_min': cost_min, 'cost_seconds': cost_seconds, 'total_name': total_name,
                                  'content': _content})
    key_name = re.sub(r'\|', '_', keywords)
    report_name = key_name + '_' + str(s_page) + '_' + str(e_page) + '_' + \
                  time.strftime('%Y%m%d_%H%M%S', time.localtime()) + '.html'
    with open('report/%s' % report_name, 'w') as outFile:
        # 输出保存到html，Unicode要编码成gb18030，否则乱码
        outFile.write(html_doc.encode('gb18030'))
    print "Current search is finished in %d mins %.2f seconds." % (cost_time / 60, cost_time % 60)

    if args.browser:
        try:
            webbrowser.open_new_tab(os.path.abspath('report/%s' % report_name))
        except:
            print '[ERROR] Fail to open file with web browser: report/%s' % report_name
