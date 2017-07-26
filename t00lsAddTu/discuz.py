#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# author t0ols

import re
import requests
import config
import hashlib
from bs4 import BeautifulSoup
import time
import random


class Discuz(object):
    def __init__(self):
        self.nowDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.operate = ''  # response的对象（不含read）
        self.formhash = ''  # 没有formhash不能发帖

        self.s = requests.session()
        # self.formhash_pattern = re.compile(r'<input type="hidden" name="formhash" value="([0-9a-zA-Z]+)" />')
        self.formhash_pattern = re.compile(r'<input type="hidden" name="formhash" value="(.*?)">')
        UA = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
        self.header = {"User-Agent": UA,
                       "Referer": "https://www.t00ls.net/",
                       }
        self.url = 'https://www.t00ls.net/logging.php?action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'

    def login(self, username, password, questionid, answer):
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()
        getFormhashHtml = self.s.get(self.url, headers=self.header)
        formhashBS4 = BeautifulSoup(getFormhashHtml.text, 'lxml')
        formhash = formhashBS4.find('input', {'name': 'formhash'})['value']

        loginData = {
            'formhas': formhash,
            'referer': self.url,
            'loginfield': config.LOGINFIELD,  # username or email
            'username': username,
            'password': password,
            'questionid': questionid,
            'answer': answer,
            'loginsubmit': 'true',
            'cookietime': config.COOKIETIME,
        }
        self.s.post(self.url, headers=self.header, data=loginData)
        Cookie = "UTH_cookietime=2592000; UTH_auth={UTH_auth}; UTH_sid={UTH_sid}".format(
            UTH_auth=self.s.cookies['UTH_auth'],
            UTH_sid=self.s.cookies['UTH_sid'])
        self.header['Cookie'] = Cookie

    def check(self):
        selectTB = self.s.get(config.CHECKURL, headers=self.header).content
        soup = BeautifulSoup(selectTB, 'lxml')
        tbody = soup.find('tbody')
        for item in tbody.findAll('tr'):
            # print item
            if self.nowDate in item.text and u'域名' in item.text:
                print '*' * 30
                print '今日土币已领完，请明日继续！'
                print '详细信息：'
                print item.text
                print '*' * 30
                exit()

    def cha(self, domain):
        print '[+] Checking {}'.format(domain)
        getFormhashHtml = self.s.get(config.HOMEURL, headers=self.header)
        formhashBS4 = BeautifulSoup(getFormhashHtml.text, 'lxml')
        formhash_cha = formhashBS4.findAll('input', {'name': 'formhash'})
        formhash_cha = formhash_cha[0]['value']
        # print formhash_cha

        data = {'querydomainsubmit': '\xe6\x9f\xa5\xe8\xaf\xa2', 'domain': u'Rockislandauction.com',
                'formhash': '31d70cec',}
        data['domain'] = domain
        data['formhash'] = formhash_cha
        data['querydomainsubmit'] = u'查询'

        html = self.s.post(config.HOMEURL, headers=self.header, data=data).text
        # print html
        if u'注册信息' in html:
            print '{} 查询成功!'.format(domain)

    def getDomain(self):
        url = 'http://www.alexa.com/topsites/category;{}/Top/Business/Business_Services'.format(random.randint(1, 19))
        # url='http://www.alexa.com/topsites/category;19/Top/Business/Business_Services/Communications'
        soup = BeautifulSoup(requests.get(url).content, 'lxml')
        domainList = []
        for item in soup.find_all('p', attrs={'class': 'desc-paragraph'}):
            doamin = item.a.get_text().replace('/', '').replace('Https:', '').replace('http:', '')
            domainList.append(doamin)
        return domainList
