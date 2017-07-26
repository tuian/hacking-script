#!/usr/bin/env python
# coding=utf-8

import argparse
import sys
from conf import url_txt


def parse_args():
    parser = argparse.ArgumentParser(prog='Awvs', usage="Awvs.py [Option]",
                                     description="* Awvs scanning by python *",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-u', metavar='UrlPath', type=str, default=url_txt,
                        help="The url list for scanning")
    parser.add_argument('-t', metavar='ThreadNum', type=int, default=3,
                        help='The wvs_console number, should be a int between 1 and 10')

    if len(sys.argv) == 1:
        sys.argv.append('-h')

    args = parser.parse_args()
    check_args(args)
    return args


def check_args(args):

    if not (args.t >= 1 and args.t <= 10):
        raise Exception('-t must be an integer between 1 and 10')
