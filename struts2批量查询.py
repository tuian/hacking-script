#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
a = open("ip.txt","r")
b = ("/index.action","/index.do","/login.do","/login.action")
x = open("success.txt","w")
for c in a:
        d = c.strip()
        for e in b:
                g = requests.get(str(d) + str(e))
                print g.url
                if g.status_code == 200:
                        print>>x,g.url        
a.close()
x.close()
