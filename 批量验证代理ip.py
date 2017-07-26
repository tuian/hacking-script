
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys,requests,lxml,re
#设置 utf8 字符流处理
reload(sys)
sys.setdefaultencoding('utf-8')

#设置头信息
headers={       "User-Agent":"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36",
                "Accept":"*/*",
                "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding":"gzip, deflate",
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With":"XMLHttpRequest",
                "Connection":"keep-alive"
        }

#代理验证,proxies() #传入一个字典
def proxies(urls = {"http":"http://124.240.187.78:81"} ):
    proxies = urls
    # timeout=60 设置超时时间60秒
    # res.status_code 查看返回网页状态码
    # verify = False 忽略证书
    try:
        res = requests.get(url = "http://1212.ip138.com/ic.asp",proxies = proxies, verify = False,timeout=60,headers = headers)
        #print u"访问畅通!!!"
        #print res.content
        if res.status_code == 200 :
            #print u"代理可用!"
            #print res.content
            ##with open("1.txt",'wb') as f:
            ##    f.write(res.content)
            print urls
            print u"访问没有问题,返回1"
            return proxies
        else:
            print urls
            print u"访问不可用,返回0"
            return False
    except Exception, e:
        print urls
        print u"访问异常,返回0"
        return False

#获取列表页数 并 生成列表超链接
def get_list_page(listurl = "http://www.xicidaili.com/nt/"):
    #获取列表页数
    doc = requests.get(url = listurl,headers = headers).text
    soup = BeautifulSoup(doc,'lxml')
    page_html = soup.find("div",class_="pagination")
    page_list = re.findall(r"\d+",str(page_html))
    page_max = int(page_list[-2])
    #生成列表超链接
    list_all = []
    for i in xrange(1,page_max+1):
        url =  re.sub('/\d+','/%d'%i,listurl+"1",re.S)
        #print url
        list_all.append(url)
    else :
        #print list_all
                return list_all


#抓取页面字段
def page_data(url = "http://www.xicidaili.com/nn/1"):
    resule = []
    html = requests.get(url,headers = headers).text
    soup = BeautifulSoup(html,'lxml')
    table = soup.select('table tr')
    for tr in table:
                #print tr
                td = tr.select('td')
                iplist = []
                for ip in td:
                    #print ip.string
                    iplist.append(ip.string)
                #print iplist
                if iplist :
                    resule.append(iplist[5].lower() + ':' + iplist[5].lower() + '://' + iplist[1] + ':' + iplist[2])
    return resule
    #获取数据

#追加保存数据
def save_ip(ip):
        with open('ip.txt', 'a') as f:
                f.writelines(ip)
                f.close()


#proxies()
#print get_list_page("http://www.xicidaili.com/nn/")
#print page_data()


list_url = get_list_page(listurl = "http://www.xicidaili.com/nt/")
for url in list_url:
        iplist = page_data(url)
        #print iplist
        #exit()
        for ip in iplist:
                arr = re.split(':',ip)
                #print type(arr),arr,arr[0],arr[1],arr[2],arr[3]
                parame = {arr[0]:arr[1]+':'+arr[2]+':'+arr[3]}
                res = proxies(parame)
                if res :
                        #print u"file_put" #写入文件
                        save_ip(str(arr[1]+':'+arr[2]+':'+arr[3])+"\r\n")
                else:
                        #访问不可用时走这里的流程
                        pass




if __name__ == '__main__':
        #print "main"
        pass