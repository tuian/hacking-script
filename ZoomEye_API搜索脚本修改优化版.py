#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Forsaken

import getopt
import requests
import sys
import time

USER = ''
PASS = ''

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hu:p:m:q:l:f:', ['help', 'user=', 'pass=', 'mode=', 'query=', 'limit=', 'facets='])
    except getopt.GetoptError as e:
        print('[-] %s' % str(e))
        usage()
        sys.exit(2)

    username = USER
    password = PASS
    mode = 'host'
    query = ''
    limit = 2048
    facets = ''

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-u', '--user'):
            username = a
        elif o in ('-p', '--pass'):
            password = a
        elif o in ('-m', '--mode'):
            if a in ('host', 'web'):
                mode = a
            else:
                print('[-] Unknown Mode!')
                usage()
                sys.exit(2)
        elif o in ('-q', '--query'):
            query = a
        elif o in ('-l', '--limit'):
            try:
                limit = int(a)
            except ValueError as e:
                print('[-] %s' % str(e))
                usage()
                sys.exit(2)
        elif o in ('-f', '--facets'):
            facets = a
        else:
            pass

    if not query:
        print('[-] Query Keyword Not Found!')
        usage()
        sys.exit(2)

    print('[!] Mode: %s' % mode)
    print('[!] Query: %s' % query)
    print('[!] Limit: %s' % str(limit))
    print('[!] Facets: %s' % facets)

    try:
        choice = raw_input('Start Query? [Y/n] ')
    except NameError as e:
        choice = input('Start Query? [Y/n] ')

    if choice in ('n', 'N'):
        sys.exit()

    authorization = get_authorization(username, password)
    if not authorization:
        sys.exit(1)

    resources_info = get_resources_info(authorization)
    if not resources_info:
        sys.exit(1)
    else:
        print('[*] Plan: %s' % resources_info['plan'])
        print('[*] Resources: Host %s Web %s' % (resources_info['resources']['host-search'], resources_info['resources']['web-search']))

    result = list()
    page = 1
    while page <= limit:
        temp = search(authorization, mode, query, str(page), facets)
        if not temp:
            break
        result.extend(extract(mode, temp))
        print('Download Page: %s' % str(page))
        page += 1
    result = set(result)

    log = 'ZoomEye_' + str(time.time()) + '.txt'
    with open(log, 'w') as f:
        f.writelines(result)

    print('Please Check The %s' % log)

def usage():
    print('Usage: python %s [options]' % sys.argv[0])
    print('')
    print('Options:')
    print('  -h, --help                        Show Help Message And Exit')
    print('  -u USER, --user=USER              ZoomEye E-Mail')
    print('  -p PASS, --pass=PASS              ZoomEye Password')
    print('  -m MODE, --mode=MODE              host || web (Default: host)')
    print('  -q QUERY, --query=QUERY           Query Keyword')
    print('  -l LIMIT, --limit=LIMIT           Page Limit (Default: 2048)')
    print('  -f FACETS, --facets=FACETS        Facets Keyword')

def get_authorization(username, password):
    authorization = dict()
    access_token = get_access_token(username, password)
    if access_token:
        authorization['Authorization'] = 'JWT ' + access_token['access_token']
    else:
        pass
    return authorization

def get_access_token(username, password):
    try:
        r = requests.post('https://api.zoomeye.org/user/login', json={'username': username, 'password': password})
    except requests.RequestException as e:
        print('[-] %s' % str(e))
        print('[-] Get Access Token Failed!')
    else:
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('[-] %s %s \n[-] %s' % (str(r.status_code), r.json()['error'], r.json()['message']))
            print('[-] Get Access Token Failed!')

def get_resources_info(authorization):
    try:
        r = requests.get('https://api.zoomeye.org/resources-info', headers=authorization)
    except requests.RequestException as e:
        print('[-] %s' % str(e))
        print('[-] Get Resources Info Failed!')
    else:
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('[-] %s %s \n[-] %s' % (str(r.status_code), r.json()['error'], r.json()['message']))
            print('[-] Get Resources Info Failed!')

def search(authorization, mode='host', query='', page='1', facets=''):
    try:
        url = 'https://api.zoomeye.org/' + mode + '/search?query=' + query + '&page=' + page + '&facets=' + facets
        print('GET %s' % url)
        r = requests.get(url, headers=authorization)
    except requests.RequestException as e:
        print('[-] %s' % str(e))
        print('[-] %s Search Failed!' % mode.capitalize())
    else:
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('[-] %s %s \n[-] %s' % (str(r.status_code), r.json()['error'], r.json()['message']))
            print('[-] %s Search Failed!' % mode.capitalize())

def extract(mode, temp):
    result = list()
    if mode == 'host':
        for line in temp['matches']:
            result.append(line['ip'] + ':' + str(line['portinfo']['port']) + '\n')
    else:
        for line in temp['matches']:
            result.append(line['site'] + '\n')
    return result

if __name__ == '__main__':
    main()