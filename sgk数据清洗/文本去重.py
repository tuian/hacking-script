#coding=utf-8
import sys
def open_txt():  #打开TXT文本写入数组
    try:
        xxx = file(sys.argv[1], 'r')
        for xxx_line in xxx.readlines():
            passlist.append(xxx_line)
        xxx.close()
    except:
        return 0
         
def write_txt():  #打开TXT文本写入数组
    try:
        yyy = file(sys.argv[2], 'w')
        for i in list_passwed:
            yyy.write(i)
        yyy.close()
    except:
        return 0
         
         
global  passlist  #声明全局变量
passlist = []    #用户名：anonymous 密码为空
open_txt()   #TXT导入数组
#passlist = list(set(passlist))   #python 列表去重
global  list_passwed  #列表去重，不打乱原来的顺序
list_passwed=[]
for i in passlist:
    if i not in list_passwed:
        list_passwed.append(i)
write_txt()