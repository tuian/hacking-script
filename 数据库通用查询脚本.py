#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Forsaken

import getopt, mysql.connector, sys, time
from codecs import open

HTML_BEGIN = u'''<!DOCTYPE HTML>
<html>
    <head>
        <meta charset="UTF-8"/>
        <title>Social Engineering Database Query 0.1</title>
    </head>
    <body>
'''

HTML_END = u'''    </body>
</html>'''

timestamp = unicode(int(time.time()))
log_name = u'se_log_' + timestamp + u'.html'

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], u'hk:lv', [u'help', u'keyword=', u'like', u'version'])
        if opts == []:
            raise getopt.GetoptError(u'')
    except getopt.GetoptError as error:
        print(error)
        print_help()
        exit(2)

    keyword = unicode()
    like = False

    for o, p in opts:
        if o in (u'-h', u'--help'):
            print_help()
            exit(0)
        elif o in (u'-k', u'--keyword'):
            keyword = p
        elif o in (u'-l', u'--like'):
            like = True
        elif o in (u'-v', u'--version'):
            print_about()
            exit(0)
        else:
            pass

    conn = mysql.connector.connect(host = u'127.0.0.1', port = 3306, user = u'root', password = u'toor', database = u'se', use_unicode = True, charset = u'utf8')

    global cursor
    cursor = conn.cursor()

    print(u'Please wait...')

    with open(log_name, u'w', u'utf-8') as f:
        f.write(HTML_BEGIN)

    table_list = get_list(u'table')

    for table in table_list:
        data = list()
        column_list = get_list(u'index', table)
        for column in column_list:
            data.extend(get_data(table, column, keyword, like))
        if data != []:
            data = process_data(data)
            print_data(table, data)

    with open(log_name, u'a', u'utf-8') as f:
        f.write(HTML_END)

    cursor.close()
    conn.close()

    print(u'Please view ' + log_name)

def get_list(mode, table = u''):
    sql_table = u"SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'se';"
    sql_index = u"SELECT COLUMN_NAME FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = 'se' AND TABLE_NAME = '" + table + u"';"
    sql_column = u"SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'se' AND TABLE_NAME = '" + table + u"';"
    lst = list()
    if mode == u'table':
        cursor.execute(sql_table)
    elif mode == u'index':
        cursor.execute(sql_index)
    elif mode == u'column':
        cursor.execute(sql_column)
    else:
        pass
    for tmp in cursor.fetchall():
        lst.append(u''.join(tmp))
    return lst

def get_data(table, column, keyword, like):
    sql_exact = u"SELECT * FROM " + table + u" WHERE " + column + u" = '" + keyword + u"';"
    sql_like = u"SELECT * FROM " + table + u" WHERE " + column + u" LIKE '%" + keyword + u"%';"
    if like == False:
        cursor.execute(sql_exact)
    else:
        cursor.execute(sql_like)
    data = cursor.fetchall()
    return data

def process_data(data):
    result = list()
    for tmp in data:
        result.append(tup2str(tmp))
    result = list(set(result))
    return result

def tup2str(tup):
    s = unicode()
    for tmp in tup:
        tmp = unicode(tmp)
        s += tmp.strip() + u' | '
    return s

def print_data(table, data):
    table_name = u'Table: ' + table
    column_name = u' | '.join(get_list(u'column', table))
    with open(log_name, u'a', u'utf-8') as f:
        f.write(u'        <h3>' + table_name + u'</h3>\n' + u'        <h5>' + column_name + u'</h5>\n')
        for tmp in data:
            f.write(u'         <p>' + tmp + u'</p>\n')

def print_help():
    print(u'Usage: ' + sys.argv[0] + u' [options]')
    print(u'')
    print(u'Options:')
    print(u'  -h, --help:' + u'\t\t\t' + u'Show basic help message and exit')
    print(u'  -k, --keyword=KEYWORD:' + u'\t' + u'Target KEYWORD')
    print(u'  -l, --like:' + u'\t\t\t' + u'Use LIKE predicate')
    print(u'  -v, --version:' + u'\t\t' + u'Show program\'s version number and exit')

def print_about():
    print(u'Common Social Engineering Database Query 0.1')
    print(u'Author: Forsaken')

if __name__ == u'__main__':
    main()