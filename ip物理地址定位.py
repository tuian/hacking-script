#!/usr/bin/python
# coding:utf-8
import requests
import json

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'}   

list_info = {

1:'服务器内部错误',

167:'定位失败',

101:'AK参数不存在',

200:'应用不存在，AK有误请检查重试',

201:'应用被用户自己禁止',

202:'应用被管理员删除',

203:'应用类型错误',

210:'应用IP校验失败',

211:'应用SN校验失败',

220:'应用Refer检验失败',

240:'应用服务被禁用',

251:'用户被自己删除',

252:'用户被管理员删除',

260:'服务不存在',

261:'服务被禁用',

301:'永久配额超限，禁止访问',

302:'当天配额超限，禁止访问',

401:'当前并发超限，限制访问',

402:'当前并发和总并发超限'
}


def handle_traffic(url):
    http_res = {}
    res = requests.get(url,timeout=100,headers=headers)
    http_res['code'] = res.status_code
    http_res['text'] = res.text
    return http_res

def ip_chk(ip,equ):
        #注意需要ak！
    url = 'http://api.map.baidu.com/highacciploc/v1?qcip={ip}&qterm={equ}&ak=ak&coord=bd09ll&extensions=3'.format(ip=ip,equ=equ)
    #注意需要ak！
    a = handle_traffic(url)
    res = a['text']
    res = json.loads(res)
    c_code = res['result']['error']
    if c_code == 161:
            d = res['content']['formatted_address']
            f = res['content']['address_component']['admin_area_code']
            w = res['content']['location']['lat']
            j = res['content']['location']['lng']
            print '该IP的地址为：',d
            print '该地区身份证前6位：'+str(f)
            print '经度：',j
            print '纬度：',w
            print 'Full :('+str(j)+','+str(w)+')'
    else:
            for i in list_info:
                    if c_code == i:
                            print list_info[i]


if __name__ == '__main__':
        ip = raw_input('Enter ip addr: ')
        equ = raw_input('PC or MOBILE <p/m> :')
        if equ == 'p' or equ == 'P':
                equ = 'pc'
                ip_chk(ip,equ)
        elif equ == 'm' or equ == 'M':
                equ = 'mb'
                ip_chk(ip,equ)