#!/usr/bin/env python
# encoding: utf-8
# [url]http://ldap3.readthedocs.io/tutorial.html#accessing-an-ldap-server[/url]
import ldap3
from fileutils import FileUtils
import os

def verify(host):
        
        try:
            print host
            server = ldap3.Server(host, get_info=ldap3.ALL, connect_timeout=30)
            conn = ldap3.Connection(server, auto_bind=True)
            #print server 
            if len(server.info.naming_contexts) > 0:
                for _ in server.info.naming_contexts:
                    if conn.search(_, '(objectClass=inetOrgPerson)'):
                        naming_contexts = _.encode('utf8')
                        f = open('ldap.txt','a')
                        f.write(host + '\n')
                        f.close()

        except Exception, e:
            pass
            #print e

if __name__ == '__main__':
    for host in FileUtils.getLines('ldap.lst'):
        verify(host)