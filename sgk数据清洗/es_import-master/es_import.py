# coding=utf-8
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import csv
import traceback


def csv_import():
    try:
        es = Elasticsearch()
        actions = []
        i = 1
        with open('xiaomi_com.csv') as reader:
            for line in reader:
                action = {
                    "_index": "xiaomi_",
                    "_type": "xiaomi_user",
                    "_id": i,
                    "_source": {
                        u"id": line[0].decode('utf8'),
                        u"账户名": line[1].decode('utf8'),
                        u"密码": line[2].decode('utf8'),
                        u"email": line[3].decode('utf8'),
                        u"ip地址": line[4].decode('utf8'),
                        u"号码": line[5].decode('utf8'),
                        u"身份证号": line[6].decode('utf8'),
                        u"年龄": line[7].decode('utf8'),
                        u"月份": line[8].decode('utf8'),
                        u"年份": line[9].decode('utf8'),
                        u"姓氏": line[10].decode('utf8')
                    }
                }
                i += 1
                actions.append(action)
                if len(actions) == 500:
                    helpers.bulk(es, actions)
                    del actions[0:len(actions)]
            if len(actions) > 0:
                helpers.bulk(es, actions)
    except:
        traceback.print_exc()


if __name__ == '__main__':
    csv_import()