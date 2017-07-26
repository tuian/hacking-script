#-*- coding:utf-8 -*-
import urllib2
import ssl
import json
__author=jamesj
#servers=服务器
#username=用户名
#pw=sha256加密后的密码
#以上内容请批量替换，然后把要添加的url列表保存成testawvs.txt文件，放在该脚本下运行该脚本。
ssl._create_default_https_context = ssl._create_unverified_context
url_login="https://servers:3443/api/v1/me/login"
send_headers_login={
'Host': 'servers:3443',
'Accept': 'application/json, text/plain, */*',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate, br',
'Content-Type': 'application/json;charset=utf-8'
}

data_login='{"email":"--------username-------","password":"------pw------","remember_me":false}'
#data_login里面的密码加密方式为sha256,通过burp抓包可获取,也可以使用(http://tool.oschina.net/encrypt?type=2)把密码进行加密之后填入
req_login = urllib2.Request(url_login,headers=send_headers_login)
response_login = urllib2.urlopen(req_login,data_login)
xauth = response_login.headers['X-Auth']
COOOOOOOOkie = response_login.headers['Set-Cookie']
print COOOOOOOOkie,xauth
#以上代码实现登录（获取cookie）和校验值

url="https://servers:3443/api/v1/targets"

urllist=open('testawvs.txt','r')#这是要添加的url列表
formaturl=urllist.readlines()
send_headers2={	
'Host':'servers:3443',
'Accept': 'application/json, text/plain, */*',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Content-Type':'application/json;charset=utf-8',
'X-Auth':xauth,
'Cookie':COOOOOOOOkie,
}	
try:
	for i in formaturl:
		target_url='http://'+i.strip()
		data='{"description":"222","address":"'+target_url+'","criticality":"10"}'
		#data = urllib.urlencode(data)由于使用json格式所以不用添加
		req = urllib2.Request(url,headers=send_headers2)
		response = urllib2.urlopen(req,data)
		jo=eval(response.read())
		target_id=jo['target_id']#获取添加后的任务ID

#以上代码实现批量添加

		url_scan="servers:3443/api/v1/scans"
		headers_scan={
'Host': 'servers:3443',
'Accept': 'application/json, text/plain, */*',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate, br',
'Content-Type': 'application/json;charset=utf-8',
'X-Auth':xauth,
'Cookie':COOOOOOOOkie,
		}
		data_scan='{"target_id":'+'\"'+target_id+'\"'+',"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false},"ui_session_id":"66666666666666666666666666666666"}'
		req_scan=urllib2.Request(url_scan,headers=headers_scan)
		response_scan=urllib2.urlopen(req_scan,data_scan)
		print response_scan.read()
#以上代码实现批量加入扫描

except Exception,e:
	print e
