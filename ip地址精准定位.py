# -*- coding:utf-8 -*-
# author:allen权
import sys
import urllib2
import json

def get_ip_information(ip):
    url='http://api.map.baidu.com/highacciploc/v1?qcip='+ip+'&qterm=pc&ak='你的密钥（AK）'&coord=bd09ll&extensions=3'
    poiss=''
    request = urllib2.Request(url)
    page = urllib2.urlopen(request, timeout=10)
    data_json = page.read()
    data_dic = json.loads(data_json)
    if(data_dic.has_key("content")):
        content=data_dic["content"]
        address_component=content["address_component"]
        formatted_address=content["formatted_address"]
        print "该IP地址的具体位置为："
        print address_component["country"]
        print formatted_address
        if (content.has_key("pois")):
            print "该IP地址附近POI信息如下："
            pois = content["pois"]
            for index in range(len(pois)):
                pois_name = pois[index]["name"]
                pois_address = pois[index]["address"]
                print pois_name, pois_address
    else:
        print 'IP地址定位失败！！！'
if __name__ == '__main__':
    get_ip_information('183.55.116.95')