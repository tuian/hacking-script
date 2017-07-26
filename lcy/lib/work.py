#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lcy
# @Date:   2016-09-20 14:52:30
# @Last Modified by:   Lcy
# @Last Modified time: 2016-09-21 12:48:21
import threading
import sys
from util import saveResult
from Color import *
from consle_width import getTerminalSize
class Work():  
    def __init__(self,type,tnum,que=None,targets=None,filename=None):  
        sys.path.append('exploits/server')
        sys.path.append('exploits/website')
        self.type=type
        self.tnum = int(tnum)
        self.que = que 
        self.targets = targets
        self.filename = filename
        self.lock = threading.Lock()
        self.console_width = getTerminalSize()[0] - 2 
    def start(self): 
        ts = []
        for i in range(self.tnum):
                t = threading.Thread(target=self.works)
                t.setDaemon(True)
                ts.append(t)
                t.start()
        for t in ts:
            t.join()
    def works(self):
        while self.que.qsize() > 0:
            exp = self.que.get()
            m = __import__(exp[:-3])
            myplugin = getattr(m, "Exploit")
            for target in self.targets:
                msg = 'Scaning target:%s' % target
                sys.stdout.write(msg + ' ' * (self.console_width -len(msg)) + '\r')
                try:
                    p = myplugin(target,exp)
                    p.verify()
                    result = p.result
                    if result['status']:
                        self.lock.acquire()
                        color.cprint("[+] {target} | {file}".format(target=result['target'],file=exp),CYAN)
                        self.lock.release()
                        saveResult(self.filename,result)
                except Exception,e:
                    #print e
                    pass

