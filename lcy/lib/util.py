#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lcy
# @Date:   2016-09-20 13:46:52
# @Last Modified by:   Lcy
# @Last Modified time: 2016-09-21 12:59:35
import os
from socket import gethostbyname
from urlparse import urlsplit
def getWebsiteExp():
    path = os.path.split(os.path.realpath(__file__))[0].replace('lib','')
    exps = os.listdir(path + '/exploits/website/')
    fil = lambda str:(True, False)[str[-3:] == 'pyc' or str.find('__init__.py') != -1]
    return filter(fil, exps)

def getServerExp():
    path = os.path.split(os.path.realpath(__file__))[0].replace('lib','')
    exps = os.listdir(path+ '/exploits/server/')
    fil = lambda str:(True, False)[str[-3:] == 'pyc' or str.find('__init__.py') != -1]
    return filter(fil, exps)
#生成扫描结果
def saveHead(filename):
    head = '''
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <title>LcyScan</title>
                </head>
                <style>
                    body{
                      background: green;
                    }
                    table { 
                    table-layout: fixed;
                    word-wrap:break-word;
                    border:1px solid #000;
                    font-size:11px;
                    }
                </style>
                <body>
                    <table border=1 style="width:100%;hegiht:100%;">
                        <thead>
                            <tr>
                              <th>url</th>
                              <th>存在漏洞的插件</th>
                              <th>插件名称</th>
                              <th>漏洞来源</th>
                              <th>执行结果</th>
                              <th>类型</th>
                            </tr>
                        </thead>
                        <tbody>
    '''
    f = open(filename,"a")
    f.write(head)
    f.close
def saveFoot(filename):
    head = '''
                        </tbody>
            </table>
        </body>
    </html>
    '''
    f = open(filename,"a")
    f.write(head)
    f.close
def saveResult(filename,result):
    html = "<tr>"
    html += '<td>' + result['target'] + '</td>'
    html += '<td>' + result['filename'] + '</td>'
    html += '<td>' + result['name'] + '</td>'
    html += '<td>' + result['ref'] + '</td>'
    html += '<td>' + result['info'] + '</td>'
    html += '<td>' + result['type'] + '</td>'
    html += '</tr>'
    f = open(filename,"a")
    f.write(html)
    f.close()
def url2ip(url):
    """
    works like turning 'http://baidu.com' => '180.149.132.47'
    """
    iport = urlsplit(url)[1].split(':')
    if len(iport) > 1:
        return gethostbyname(iport[0]), iport[1]
    return gethostbyname(iport[0])
