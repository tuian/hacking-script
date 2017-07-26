#!/usr/bin/python
# -*- coding: UTF-8 -*-

import Queue
import threading
import time
import socket
import urlparse
import sys
import threading
from optparse import OptionParser

'''
Redis 未授权批量扫描工具
'''

# 线程退出标志
exitFlag = 0
#默认线程数量
NUM = 50

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        #print "Starting " + self.name
        process_data(self.name, self.q)
        # print "Exiting " + self.name

# 调用线程 执行 
def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            ip = q.get()
            queueLock.release()
            print  u"\n\n【进度: %s/%s 】" % (zongshu - workQueue.qsize(), zongshu)
            ips = _verify(ip)
            czldlist.append(ips)
            czldlist.append(_verify(ip))
        else:
            queueLock.release()


def _verify(host):
    result = {}
    payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
    s = socket.socket()
    socket.setdefaulttimeout(1)
    try:
        # host = urlparse.urlparse(self.url).netloc
        print u'\n【测试】' + host
        port = 6379
        s.connect((host, port))
        s.send(payload)
        recvdata = s.recv(1024)
        # print recvdata
        if recvdata and 'redis_version' in recvdata:
            #print u'\n【警告】' + host + "【存在未授权访问】"
            return host
        else:
            print u'\n【不存在漏洞】 ' + host
    except:
        # return host
        pass
    s.close()
    # print result

    
def dec2bin(n, d=None):
    s = ""
    while n > 0:
        if n & 1:
            s = "1" + s
        else:
            s = "0" + s
        n >>= 1
    if d is not None:
        while len(s) < d:
            s = "0" + s
    if s == "": s = "0"
    return s
 
# ip转2进制    
def ip2bin(ip):
    b = ""
    inQuads = ip.split(".")
    outQuads = 4
    for q in inQuads:
        if q != "":
            b += dec2bin(int(q), 8)
            outQuads -= 1
    while outQuads > 0:
        b += "00000000"
        outQuads -= 1
    return b

    
# 2进制转IP
def bin2ip(b):
    ip = ""
    for i in range(0, len(b), 8):
        ip += str(int(b[i:i + 8], 2)) + "."
    return ip[:-1]    


# 根据掩码生成ip
def listCIDR(c):
    cidrlist = []
    parts = c.split("/")
    baseIP = ip2bin(parts[0])
    subnet = int(parts[1])
    if subnet == 32:
        print bin2ip(baseIP)
    else:
        ipPrefix = baseIP[:-(32 - subnet)]
        for i in range(2 ** (32 - subnet)):
            cidrlist.append(bin2ip(ipPrefix + dec2bin(i, (32 - subnet))))
        return cidrlist    
 

if __name__ == '__main__':
    usage = u"例如扫描：182.254.149.92段    redis.py 182.254.149.92/24     redis.py <hosts[/24|/CIDR]>  "
    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--thread", dest="NUM", help="The default 50 threads")
    #parser.add_option("-f", "--file", dest="ip list file ", help=" ip list file c:/ip.txt ")
    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        parser.print_help()
        sys.exit()
    
    
    queueLock = threading.Lock()
    workQueue = Queue.Queue()
    threads = []
    threadID = 1
    
    if options.NUM !=None and options.NUM!=0:
        NUM=int(options.NUM)
        print u'开启线程数为：',NUM,'...'
    
    #创建线程
    for tName in range(1,NUM):
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1        
    
    
    print u"\n正在初始化......"
    listIp = listCIDR(args[0])
    zongshu = len(listIp)
    # print u'count:' + len(listIp)
    i = 1
    czldlist = []
    
    # 填充队列
    queueLock.acquire()
    for ip in listIp:
        workQueue.put(ip)
  
    queueLock.release()
    
    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程退出
    exitFlag = 1

    # 等待所有线程完成
    for t in threads:
        t.join()
    
    print u"\n--- 扫描完成  --- \n正在整理结果漏洞信息"
    
    filePatch ="redis-" + time.strftime("%Y-%m-%d%H%M%S", time.localtime()) 
    f = open(filePatch +'.txt' , 'a')
    #结果输出
    czldlist = list(set(czldlist))
    for ip in czldlist:
        if ip:
            f.write(ip+"\n")
            print ip
    
    f.close()


