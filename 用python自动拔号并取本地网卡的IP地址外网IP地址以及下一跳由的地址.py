# coding:utf-8


import socket
from json import load
from urllib2 import urlopen
import sys
import time
import os
from subprocess import Popen, PIPE

reload(sys)
sys.setdefaultencoding('utf-8')


def getAll():
    ip = socket.gethostbyname(socket.gethostname())
    ipAddr = u'本地显示:' + ip
    # print ipAddr
    try:
        my_ip = load(urlopen('https://api.ipify.org/?format=json'))['ip']
    except Exception, e:
        print e


    wanAddr = u'外网显示:' + my_ip
    # print wanAddr

    # import os
    # print os.system('tracert -d [url]www.baidu.com[/url]')




    ip2 = ip.split('.')[0:2]
    ip3 = '.'.join(ip2)  # IP地址的前两位
    host = '211.162.66.66'  # DNS
    p = Popen(['tracert', host], stdout=PIPE)
    while True:
        line = p.stdout.readline()
        if ip3 in line:
            routeAddr = u'路由地址:' + line.split()[7]
            break
            # Do stuff with line
    return ipAddr, wanAddr, routeAddr

def connectNet():
    cmd_str_dis="rasdial name  /disconnect"   #name是拔号名字
    cmd_str_con="rasdial name user passwd"
    os.system(cmd_str_dis)


    time.sleep(10)
    os.system(cmd_str_con)
    time.sleep(5)


if __name__ == '__main__':
    while 1:
        print '循环中.......'
        try:
            connectNet()
            ipAddr, wanAddr, routeAddr = getAll()
        except :
            pass

        print ipAddr, '\n', wanAddr, '\n', routeAddr
        output = open('data.txt', 'a')
        output.write("==============================\n")
        output.write(ipAddr + '\n')
        output.write(routeAddr + '\n')
        output.write(wanAddr + '\n')
        output.close()