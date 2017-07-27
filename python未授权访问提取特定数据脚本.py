import urllib.request
import urllib.error
from bs4 import BeautifulSoup

x=0
for i in range(1,1000):
    url = 'http://xxx.xxx.xxx?id='+str(i)
    x+=1
    try:
        html = urllib.request.urlopen(url)  #定义地址
        soup = BeautifulSoup(html,"lxml") #使用BeautifulSoup接受url参数
        soup1 = soup.find(id="nsrsbh")#查找标签id值为nsrsbh
        nsbr = (soup1.get('value')) #获取标签内value属性的字符串
        print("获取到第"+str(i)+"条数据:"+nsbr)
    except urllib.error.URLError as e:   #异常捕获
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)