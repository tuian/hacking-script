#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lcy
# @Date:   2016-09-20 10:19:39
# @Last Modified by:   Lcy
# @Last Modified time: 2016-09-21 13:20:10
from datetime import datetime
from Color import *
from util import *
from work import *
import time
import Queue
import random
import os
class framework:
    def __init__(self):
        self.ip = ''
        self.ips = ''
        self.url = ''
        self.urls = ''
        self.exploit = 'ALL'
        self.thread = '10'

    def lbanner(self):
        banner = '''
 _                                   
| |    ___ _   _ ___  ___ __ _ _ __  
| |   / __| | | / __|/ __/ _` | '_ \ 
| |__| (__| |_| \__ \ (_| (_| | | | |
|_____\___|\__, |___/\___\__,_|_| |_|
           |___/                     
                 
blog:https://phpinfo.me
'''
        color.cprint(banner,GREEN)

    def formatCmd(self,cmd):
        cmds = cmd.split(" ")
        fil = lambda str:(True, False)[str == '']
        cmds = filter(fil, cmds)
        return cmds
    def lexit(self):
        color.cprint("[*] Bye Bye",RED)
        exit(0)
    def lshow(self,cmds):
        if len(cmds) ==0 or cmds[0] not in ['options','exploits']:
            color.cprint("[-] Usage:show (options|exploits)",RED)
        elif cmds[0] == 'exploits':
            color.cprint("[*] show exploits",GREEN)
            website = getWebsiteExp()
            server = getServerExp()
            info = '''Exploits
================

   Name                                         Type
   ----                                         ----
'''
            color.cprint(info,CYAN)
            for name in website:
                info = "   " + name + ((45-len(name))*' ')+"website"
                color.cprint(info,CYAN)
            for name in server:
                info = "   " + name + ((45-len(name))*' ')+"server"
                color.cprint(info,CYAN)
            print "\n"
        elif cmds[0] == 'options':
            info = '''Options
================

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
'''
            color.cprint(info,CYAN)
            info = '   ip  '+ '     ' +self.ip + ((15-len(self.ip))*' ')+'  No        ip Address'
            info += '\n   ips '+ '     ' +self.ips + ((15-len(self.ips))*' ')+'  No        ip File Path'
            info += '\n   url '+ '     ' +self.url + ((15-len(self.url))*' ')+'  No        url'
            info += '\n   urls'+ '     ' +self.urls + ((15-len(self.urls))*' ')+'  No        url File Path'
            info += '\n   exploit'+ '  ' +self.exploit + ((15-len(self.exploit))*' ')+'  Yes       exploit'
            info += '\n   thread '+ '  ' +self.thread + ((15-len(self.thread))*' ')+'  Yes       thread num'
            color.cprint(info,CYAN)
            print "\n"
    def lset(self,cmds):
        if len(cmds) <2 or cmds[0] not in ['ip','ips','url','urls','exploit','thread']:
            color.cprint("[-] Usage:set (ip|ips|url|urls|exploit|thread) (value)",RED)
        elif cmds[0] == 'ip':
            self.ip = cmds[1]
            info = 'ip => ='+cmds[1]
            color.cprint(info,CYAN)
        elif cmds[0] == 'ips':
            self.ips = cmds[1]
            info = 'ips => ='+cmds[1]
            color.cprint(info,CYAN)
        elif cmds[0] == 'url':
            self.url = cmds[1]
            info = 'url => ='+cmds[1]
            color.cprint(info,CYAN)
        elif cmds[0] == 'urls':
            self.urls = cmds[1]
            info = 'urls => ='+cmds[1]
            color.cprint(info,CYAN)
        elif cmds[0] == 'exploit':
            self.url = cmds[1]
            info = 'exploit => ='+cmds[1]
            color.cprint(info,CYAN)
        elif cmds[0] == 'thread':
            self.thread = cmds[1]
            info = 'thread => ='+cmds[1]
            color.cprint(info,CYAN)
    def lexploit(self,cmds):
        filename = os.path.split(os.path.realpath(__file__))[0].replace('lib','result\\') + datetime.now().date().strftime('%Y%m%d') + "_"+ str(random.randint(1, 88888)) + ".html"
        saveHead(filename)
        website = getWebsiteExp()
        servers = getServerExp()
        webque = Queue.Queue()
        servque = Queue.Queue()
        for url in website:
            webque.put(url)
        for server in servers:
            servque.put(server)
        if len(cmds) == 0:
            color.cprint("[*] Started Exploits...",CYAN)
            if self.url != '':
                obj = Work('website',self.thread,webque,[self.url],filename)
                obj.start()
            if self.ip != '':
                obj = Work('server',self.thread,servque,[self.ip],filename)
                obj.start()
        elif cmds[0] == '-a':
            color.cprint("[*] Started Exploits...",CYAN)
            if self.urls != '':
                try:
                    result = []
                    fd = file(self.urls, "r" )  
                    for line in fd.readlines():  
                        result.append(line.strip())  
                    obj = Work('website',self.thread,webque,result,filename)
                    obj.start()
                except Exception,e:
                    print e
            if self.ips != '':
                try:
                    result = []
                    fd = file(self.ips, "r" )  
                    for line in fd.readlines():  
                        result.append(line.strip())  
                    obj = Work('server',self.thread,servque,result,filename)
                    obj.start()
                except Exception,e:
                    print e
            saveFoot(filename)
            color.cprint("[*] Scan finished Result file and save to %s\n" % filename,PURPLE)
 