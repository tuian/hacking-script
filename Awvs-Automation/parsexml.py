#!/usr/bin/env python
# coding=utf-8

from xml.dom import minidom
import sys


# 对扫描结果进行分析
def parse_xml(xml_name):
    result = []
    tmp_result = []
    color_list = {'red': 'High', 'orange': 'Medium', 'blue': 'Low', 'green': 'Info'}
    try:
        dom = minidom.parse(xml_name)
        root = dom.documentElement
        report_node = root.getElementsByTagName('ReportItem')
        # 只有一个节点所以用列表中的[0]取得其中的唯一一个，节点中的子节点的值
        result.append(root.getElementsByTagName("StartURL")[0].childNodes[0].nodeValue)
        result.append(root.getElementsByTagName("StartTime")[0].childNodes[0].nodeValue)
        result.append(root.getElementsByTagName("FinishTime")[0].childNodes[0].nodeValue)
        result.append(root.getElementsByTagName("ScanTime")[0].childNodes[0].nodeValue)
        if report_node:
            for node in report_node:
                # 获得color节点的属性值
                color = node.getAttribute('color')
                name = node.getElementsByTagName('Name')[0]
                if color in color_list:
                    # 因为color后面接漏洞名，需要空个tab
                    color_result = color_list[color] + '\t'
                else:
                    color_result = 'Other\t'
                for vul_node in name.childNodes:
                    tmp_result.append(color_result + vul_node.nodeValue)
        result2 = sortresultlist(tmp_result)
        result.append('Vulnerable Count:' + str(len(result2)))
        for n in xrange(len(result2)):
            result.append(result2[n])
    except Exception, e:
        sys.exit("Error in parse xml: %s" % e)

    return result


# 将扫描结果进行排序,这太渣了
def sortresultlist(List):
    Result = []
    for i in List:
        if i.startswith('High'):
            Result.append(i)
    for i in List:
        if i.startswith('Medium'):
            Result.append(i)
    for i in List:
        if i.startswith('Low'):
            Result.append(i)
    for i in List:
        if i.startswith('Info'):
            Result.append(i)
    for i in List:
        if i.startswith('Other'):
            Result.append(i)
    return Result
