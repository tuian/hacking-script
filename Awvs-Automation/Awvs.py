#!/usr/bin/env python
# coding=utf-8

import time
import subprocess
import os
from Queue import Queue
from threading import Thread
from parsexml import parse_xml
from cmdline import parse_args
from sendmail import send_main
from conf import wvs_console, save_folder, scan_command, mail_list
import sys

# 用于保存url的队列
url_queue = Queue()

def read_url(file):

    with open(file, 'r') as f:
        for each in f:
            # 每个读取出来的url都带了后面的\n，所以需要去除
            each_url = each.replace('\n', '')
            url_queue.put(each_url)


# 调用wvs_console进行扫描
def wvs_scan(url):

    save_name = time.strftime('%Y%m%d', time.localtime()) + r'\\' + url
    # 判断保存目录是否存在，不存在则创建
    save_path = save_folder + save_name
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    wvs_command = wvs_console + scan_command % (url, save_path)
    print wvs_command
    # 如果有漏洞，返回码大于0，小于0是异常
    exitcode = subprocess.call(wvs_command)
    if exitcode < 0:
        sys.exit()
    result = str(exitcode) + '|' + save_path
    return result


class ScanThread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            if url_queue.empty(): break
            scan_url = url_queue.get()
            scan_resutl = wvs_scan(scan_url)
            (code, save_load) = scan_resutl.split('|')
            if code > 0:
                xml_result = parse_xml(save_load + '\\export.xml')
                # str.join(sequence),序列之间用str间隔，这里用换行来间隔转换成字符串
                send_main(mail_list, 'WvsScanner Report--'+scan_url, '\n'.join(xml_result))
            url_queue.task_done()


def main(url_l, t_num):
    read_url(url_l)
    thread = []

    for x in range(t_num):
        thread.append(ScanThread())
        thread[x].start()

    for i in thread:
        if i.isAlive():
            i.join()


if __name__ == "__main__":

    arg = parse_args()
    url_list = arg.u
    cmd_num = arg.t
    main(url_list, cmd_num)
