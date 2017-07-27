#!/usr/bin/python

import binascii
import socket
import struct
import threading
import subprocess
import tempfile
import re
import Queue
import sys

def MyThread(urllist):
	threads = []
	queue = Queue.Queue()
	for i in range(len(urllist)):
		queue.put((i+1,urllist[i].strip()))
	for x in xrange(0, int(sys.argv[2])):
		threads.append(tThread(queue))

	for t in threads:
		t.start()
	for t in threads:
		t.join()


class tThread(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):

		while not self.queue.empty():
			num,host = self.queue.get()
			try:
				send2(host)
			except Exception,e:
				print '[%s/%s],%s,%s' %(num,nums,host,e)
				pass

def logout(msg):
	with open('smbresult.txt','a') as f:
		print >>f,msg

def send2(targetip):
	templist=[]
	templist.append(targetip)
	out_temp = tempfile.SpooledTemporaryFile(bufsize=10 * 1000)
	fileno = out_temp.fileno()
	run_cmd = 'Smbtouch-1.1.1.exe --TargetIp %s' % targetip.strip()
	app = subprocess.Popen(run_cmd, shell=True, stdout=fileno, stderr=fileno)
	app.wait()
	out_temp.seek(0)
	lines = out_temp.readlines()
	newlines = ''.join(lines)
	if "successfully" in newlines:
		info=re.findall("Target OS (Version.*?)\[",newlines,re.S)[0].strip().split("\r\n")
		vul=re.findall("\[Vulnerable\](.*?)\[",newlines,re.S)[0].strip().split("\r\n")
		for i in info:
			templist.append(i.strip())
		for j in vul:
			templist.append(re.sub("\s*","",j.strip()))
		print "----".join(templist)
		logout("----".join(templist))
	elif "Target OS" in newlines:
		info=re.findall("Target OS (Version.*?)\[",newlines,re.S)[0].strip().split("\r\n")
		for i in info:
			templist.append(i.strip())
		print "----".join(templist)
		logout("----".join(templist))
		#logout(newlines)
		
	if out_temp:
		out_temp.close()



if __name__=='__main__':
	if len(sys.argv)==3:
		with open(sys.argv[1]) as f:
			urls=f.readlines()
			nums=len(urls)
			MyThread(urls)
	else:
		print "Python file.py ips.txt thread"