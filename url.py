#! usr/bin/env python
#coding = UTF-8

import os
import re

print '''
        ==================================================================
        =                        By: Barrett                             =
        =                       QQ: 2463917215                           =
        =                   Oursite:bbs.blackbap.org                     =
        ==================================================================
        '''

if __name__ == '__main__':
    try:
        url = open('url.txt', 'r')
    except:
        print 'you do not have the file url.txt'
    else:
        tmp = [tmp.split('?')[0] for tmp in url]
        tmp = {}.fromkeys(tmp).keys()
        nex = '\n'
        result = open('result.txt', 'w')
        result.write(nex.join(tmp))
        result.close()
        
    