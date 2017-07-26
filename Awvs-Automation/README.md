##Usage
```
usage: Awvs.py [Option]

* Awvs scanning by python *

optional arguments:
  -h, --help    show this help message and exit
  -u UrlPath    The url list for scanning (default: H:\Awvs\Url\1_url.txt)
  -t ThreadNum  The wvs_console number, should be a int between 1 and 10
                (default: 3)

```
##Instruction
```
1. 自行设置具体路径等内容
2. 利用wvs_console.exe来实现扫描txt文本内的url列
3. 多开wvs_console.exe来实现多线程的同时扫描
4. 扫描后xml分析结果，有漏洞发送指定邮箱报告
```
##Example
```
python Awvs.py -u H:\url.txt -t 2
```
##Bug
```
1. 多线程可能不是线程池的方式，有时候会出现错误，询问是否保存
2. 太占网络带宽了，用一下就根本无法流量其他网页了
```
