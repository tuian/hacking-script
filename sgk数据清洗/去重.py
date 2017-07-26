#!/usr/bin/env python
# encoding: utf-8

#�ֵ�ȥ��С����
import sys
import os
import platform
try:
    pass 
except:
    print '''you have something wrong this is a simple jiaoben '''
    sys.exit()


why = 'why.txt'
for i in xrange(len(sys.argv)):
    if(i>=1):
        other = sys.argv[i]
        if os.path.exists(other):
            pass
        else:
            print other + ' file not find'
            sys.exit()
        if 'Windows' in platform.system():
            os.system("type "+other+" >> "+why)
        else:
            os.system("cat "+other+" >> "+why)

yuan = open('duowan_user.txt','r')
dirc = open('whynot.txt','w')
for line in set(yuan.readlines()):
    if line == '' or line == '\r\n':
        pass
    else:
        dirc.writelines(line)