#IVSpider
**I**gnored **V**ulnerabilities **S**pider for Wooyun
##Version
```
IVSpider.py  -------  单线程版本，舍弃
IVSpider02.py  -----  多线程版本，下载本地后重命名为IVSpider.py即可
```
##Usage
```
usage: IVSpider.py [options]

*Ingored Vulnerabilities Spider for Wooyun.*

optional arguments:
  -h, --help    show this help message and exit
  -s StartPage  The start page of Wooyun (default: 1)
  -e EndPage    The end page of Wooyun, Not including (default: 2)
  -t Threads    Num of threads for spider, 10 for default (default: 10)

```
##Instruction
```
1. Python 2.7.x && BeautifulSoup4==4.3.2
2. 自定义搜索起始页和终止页
3. 自定义线程数量
```
##Example
```
python IVSpider.py -s 10 -e 30 -t 20
```
##Bug
```
1. 可能会被评论区的忽略给误导了
2. 当数量大时，子线程可能会有几天不能正常关闭（原因未知，可能是Queue队列的Bug）
```
