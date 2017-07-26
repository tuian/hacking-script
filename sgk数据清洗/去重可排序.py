#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Forsaken

import getopt
import os
import sys

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hf:s', ['help', 'file=', 'sort'])
    except getopt.GetoptError as e:
        print('[-] %s' % e)
        usage()
        sys.exit(2)

    file = ''
    sort = False

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-f', '--file'):
            file = a
        elif o in ('-s', '--sort'):
            sort = True
        else:
            pass

    if not file:
        print('[-] File Arguments Not Found!')
        usage()
        sys.exit(2)

    if not os.path.exists(file):
        print('[-] File Not Found!')
        sys.exit(1)

    with open(file, 'r') as f:
        old = f.readlines()

    old_len = len(old)
    new = list()
    for o in old:
        if not o in new:
            new.append(o)
    new_len = len(new)
    delete = old_len - new_len

    if sort:
        new.sort()

    out = 'new_' + file
    with open(out, 'w') as f:
        f.writelines(new)

    print('Delete %s Line' % delete)
    print('Please Check %s' % out)

def usage():
    print('Usage: python %s [options]' % sys.argv[0])
    print('')
    print('Options:')
    print('  -h, --help                        Show Help Message And Exit')
    print('  -f FILE, --file=FILE              File')
    print('  -s, --sort                        Sort')

if __name__ == '__main__':
    main()