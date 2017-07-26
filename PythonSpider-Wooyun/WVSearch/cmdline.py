#!/usr/bin/env python
# coding=utf-8


import argparse
import sys

def parse_args():

    # 创建一个命令行参数对象
    parser = argparse.ArgumentParser(prog='WVSearch', usage="WVSearch.py [options]",
                                    description="* Wooyun Vulnerabilities Search *",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-s', metavar='StartPage', type=int, default=1, help='Start page for searching')
    parser.add_argument('-e', metavar='EndPage', type=int, default=10, help='End page for searching')
    parser.add_argument('-t', metavar='ThreadNum', type=int, default=10, help='Num of threads')
    parser.add_argument('-k', metavar='KeyWord', type=str, default='SQL|XSS|CSRF', help='Keywords for searching')
    parser.add_argument('--browser', default=False, action='store_true',
                        help="Open web browser to view report after after search was finished.")

    # 如果什么都没输入，就输入了一个脚本名，那么就是sys.argv只有一个参数
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    # 返回一个保存命令行参数的命名空间
    args = parser.parse_args()
    return args
