#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# author t0ols

# 域名
DOMAIN = r'https://www.t00ls.net/'  # 域名必须用/结束，不然与下面的拼接不成功
USERNAME = 'xxxxx' #用户名
PASSWORD = 'xxxx'  #密码
QUESTIONID = 5  # 0 空 1 母亲的名字 2 爷爷的名字 3 父亲出生的城市 4 您其中一位老师的名字 5您个人计算机的型号 6 您最喜欢的餐馆名称 7 驾驶执照的最后四位数字
ANSWER = 'xxxx'  #答案
LOGINFIELD = r'用户名' #用户名
COOKIETIME = 2592000

HOMEURL = DOMAIN + r't00ls_domain.php'
CHECKURL = DOMAIN + r'members-tubilog-xxxxx.html'  #这里记得一定要修改才行的
LOGINURL = DOMAIN + r'logging.php?action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
