#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lcy
# @Date:   2016-09-20 10:01:26
# @Last Modified by:   Lcy
# @Last Modified time: 2016-09-21 11:34:31
from lib.Color import *
from lib.framework import *
import os
lcy = framework()
lcy.lbanner()
if __name__=='__main__':
        try:
            while True:
                color.cprint("lcy",GREY,0)
                cmd=raw_input('>')
                cmds = lcy.formatCmd(cmd)
                if(len(cmds) == 0):
                    continue
                if cmds[0] == 'exit':
                    lcy.lexit()
                if cmds[0] == 'banner':
                    lcy.lbanner()
                elif cmds[0] == 'show':
                    lcy.lshow(cmds[1:])
                elif cmds[0] == 'set':
                    lcy.lset(cmds[1:])
                elif cmds[0] == 'exploit':
                    lcy.lexploit(cmds[1:])
                else:
                    os.system(cmd)
        except KeyboardInterrupt:
                exit()
        except Exception,e:
                print e
