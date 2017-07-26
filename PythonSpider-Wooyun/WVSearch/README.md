# WVSearch
**W**ooyun **V**ulnerabilites **Search**
## Usage
```
usage: WVSearch.py [options]

* Wooyun Vulnerabilities Search *

optional arguments:
  -h, --help    show this help message and exit
  -s StartPage  Start page for searching (default: 1)
  -e EndPage    End page for searching (default: 10)
  -t ThreadNum  Num of threads (default: 10)
  -k KeyWord    Keywords for searching (default: SQL|XSS|CSRF)
  --browser     Open web browser to view report after after search was
                finished. (default: False)
```
## Instruction
```
1. Python 2.7.x && BeautifulSoup4==4.3.2
2. 自定义搜索的起始页和终止页
3. 自定义线程数，默认10
4. 自定义搜索关键词，用 '|' 分隔，关键词用双引号包裹
5. 结果保存为html文件，可以在搜索结束自动打开
```
## Example
```
python WVSearch.py -s 10 -e 100 -t 20 -k "中国|SQL|XSS|xss" --browser
```
