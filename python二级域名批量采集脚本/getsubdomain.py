#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#version 0.1
#author：hehao
#qq:278563291
#python version:2.6.4
#lib:lxml
#
import urllib2
import os
import sys
import re
import getopt
import time
from urllib import urlencode
import simplejson

class getsubdomain(object):
	"""docstring for getsubdomain"""
	def __init__(self):
		super (getsubdomain, self).__init__()
		#self.arg = arg
	def getip(self,domain):
		#print domain
		'''函数功能：获取IP
	  	   参数：子域名
	       返回：ip地址，归属地
	       功能：利用IP138定位网站所属IP地址及归属地，可自行修改为其它方式获取'''
		opener = urllib2.build_opener()
		urllib2.install_opener(opener)
		url_data = urlencode({"q":domain})
		try:
			res = opener.open("http://domain.duapp.com", url_data).read().decode("gb18030")
			m=re.findall(r'<strong class="red">.*<br\s*/>',res)
			tmp=m[0].split(">>")
			remote_ip=tmp[1]
			location=tmp[2][0:-6]
		except:
			location=''
			remote_ip=''
		return remote_ip,location

	def print_progress(self,msg, progress):
		'''
		函数功能：打印进度条
		参数：msg 打印的消息  progress 进度显示 10.....%
		'''
		sys.stdout.write('%-71s%3d%%\r' % (msg.encode(sys.getfilesystemencoding()), progress))
		sys.stdout.flush()
		if progress >= 100:
			sys.stdout.write('\n')

	def google(self,domain,page=20):
		list_google=[]
		for x in range(page):
			url = ('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&rsz=8&start=%s') % ("site:"+domain,x)
			try:
				request = urllib2.Request(url)
				response = urllib2.urlopen(request)
				results = simplejson.load(response)
				URLinfo = results['responseData']['results']
			except Exception, e:
				print u"google 连不上了 GFW发飙了！！"
				raise e

			else:
				for info in URLinfo:
					visibleUrl=info['visibleUrl']
					title=info['title']
					ip,location=self.getip(info['visibleUrl'])
					list_google.append((visibleUrl,ip,location,title))
		return set(list_google)

	def baidu(self,domain,page=10):
		tmp=[]
		list_baidu=[]
		for x in range(page):
			i=x*10
			url='http://www.baidu.com/s?wd=site:'+domain+'&pn='+str(i)+'&ie=utf-8'
			try:
				req=urllib2.Request(url)
				res=urllib2.urlopen(req).read()
			except:
				print u"百度你都连不上，网络太不给力了！！！！！！，找李彦宏投诉去吧"
				sys.exit(2)
			progress=(x+1)*1.0/page*100
			p=re.compile(r'(?is)<span[^>]*?class=()\"g\"\1[^>]*>([^<]+)</span>')
			m=p.findall(res)
			self.print_progress(u'正在处理数据中,处理第(%d)页.    进度条---------------------->'%(x+1),progress)
			for x in m:
				subdomin=x[1].split("/")[0].strip()
				ip,location=self.getip(subdomin)
				#print subdomin,ip,location
				tmp.append((subdomin,ip,location))
			#print tmp
			list_baidu.extend(tmp)
			tmp=[]
		return set(list_baidu)
	
	def save(self,domain,str):
		'''
		函数功能：保存数据至csv文件
		参数：根域名 domain
		包含二级域名、IP地址、归属地、title的tuple str
		'''
		import csv
		writer=csv.writer(open(domain+'.csv','a'))
		writer.writerow(str)

	def usage(self):
		print u'-------------------------------------------------------------'
		print u'作者   : hehao            90sec_id: evildragon'
		print u'邮箱   : foxhack@qq.com   QQ      : 278563291\n'
		print u'此小程序主要用来获取指定域名的子域名，用于渗透测试前期收集信息,默认输出以域名为文件名的csv文件'
		print u'例子: python get-subdomain.py --module baidu --domain qq.com --num=30\n'
		print u'使用pyton get-subdomain -h 获取使用帮助信息\n'
		print u'python get-subdomain.py [options]'
		print u'[options:]'
		print u'-h --help       帮助信息'
		print u'-d --domain     指定需查询子域的根域名 例如qq.com'
		print u'-n --num        爬行页面数 默认值10页（每页10条）,建议值30,请依据网络条件设置' 
		print u'-m --module     指定搜索引擎 baidu google 默认是baidu'
		print u'-------------------------------------------------------------'

if __name__ == '__main__':
	d_flag=False
	n_flag=False
	m_flag=False
	url_list=[]
	subdomin=getsubdomain()
	try:
		opts,args=getopt.getopt(sys.argv[1:],"d:n:m:h")
	except getopt.GetoptError:
		subdomin.usage()
		sys.exit(2)
	if not len(opts):
		subdomin.usage()
		sys.exit(2)

	for o,a in opts:
		if o in ("-d","--domain"):
			domain=a
			if domain==None:
				subdomin.usage()
				sys.exit(2)
			else:
				d_flag=True
		if o in ("-m","--module"):
			module_str=a
			m_flag=True
		if o in ("-n","--num"):
			page=int(a)
			n_flag=True
		if o in ("-h","--help"):
			subdomin.usage()
			sys.exit(2)
	try:
		if os.path.exists(domain+'.csv'):
			os.remove(domain+'.csv')
	except:
		pass
	print u'-------------数据处理开始-----------------\n'
	if d_flag:
		if m_flag:
			if module_str in 'google':
				if n_flag:
					url_list=subdomin.google(domain,page)
				else:
					url_list=subdomin.google(domain)
			elif module_str in 'baidu':
				if n_flag:
					url_list=subdomin.baidu(domain,page)
				else:
					url_list=subdomin.baidu(domain)
		else:
			if n_flag:
				url_list=subdomin.baidu(domain,page)
			else:
				url_list=subdomin.baidu(domain)

	elif d_flag==False:
		subdomin.usage()
		sys.exit(2)
	#time.sleep(4)
	for x in url_list:
		if len(x)<4:
			print x[0],x[1],x[2]
			subdomin.save(domain,(x[0],x[1],x[2].encode(sys.getfilesystemencoding())))
		else:
			print x[0],x[1],x[2],x[3]
			subdomin.save(domain,(x[0],x[1],x[2].encode(sys.getfilesystemencoding()),x[3].encode(sys.getfilesystemencoding())))
	print u'数据已保存至'+domain+u'.csv中，请打开文件校验'
	print u'-------------数据处理结束-----------------'		

