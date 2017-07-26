#!/usr/bin/env python
# coding=utf-8

import argparse
import sys


# 设置命令行参数
def parse_args():
    # argparse.ArgumentDefaultsHelpFormatter 最常用的输出格式
    parser = argparse.ArgumentParser(prog='IVSpider', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="*Ingored Vulnerabilities Spider for Wooyun.*",
                                     usage="IVSpider.py [options]")
    # metavar 参数在帮助信息的名字
    parser.add_argument('-s', metavar='StartPage', type=int, default=1, help="The start page of Wooyun")
    parser.add_argument('-e', metavar='EndPage', type=int, default=2, help="The end page of Wooyun, Not including")
    parser.add_argument('-t', metavar='Threads', type=int, default=10, help="Num of threads for spider, 10 for default")

    # 如果cmd接受到的参数只有1，也就是只有一个脚本名，那么就添加一个 -h/-help 的命令
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    return args
