#!/usr/bin/env python 

""" 
Copyright (c) 2006-2016 sqlmap developers (http://sqlmap.org/) 
See the file 'doc/COPYING' for copying permission 
""" 

import httplib 
import re 
import socket 
import urllib 
import urllib2 

from lib.core.common import getSafeExString 
from lib.core.common import getUnicode 
from lib.core.common import popValue 
from lib.core.common import pushValue 
from lib.core.common import readInput 
from lib.core.common import urlencode 
from lib.core.data import conf 
from lib.core.data import kb 
from lib.core.data import logger 
from lib.core.enums import CUSTOM_LOGGING 
from lib.core.enums import HTTP_HEADER 
from lib.core.enums import REDIRECTION 
from lib.core.exception import SqlmapBaseException 
from lib.core.exception import SqlmapConnectionException 
from lib.core.exception import SqlmapUserQuitException 
from lib.core.settings import DUMMY_SEARCH_USER_AGENT 
from lib.core.settings import DUCKDUCKGO_REGEX 
from lib.core.settings import DISCONNECT_SEARCH_REGEX 
from lib.core.settings import GOOGLE_REGEX 
from lib.core.settings import HTTP_ACCEPT_ENCODING_HEADER_VALUE 
from lib.core.settings import UNICODE_ENCODING 
from lib.request.basic import decodePage 
from thirdparty.socks import socks 


def _search(dork): 
    """ 
    This method performs the effective search on Google providing 
    the google dork and the Google session cookie 
    """ 
    retVal = [] 
    paths = [] 

    if not dork: 
        return None 

    headers = {} 

    headers[HTTP_HEADER.USER_AGENT] = dict(conf.httpHeaders).get(HTTP_HEADER.USER_AGENT, DUMMY_SEARCH_USER_AGENT) 
    headers[HTTP_HEADER.ACCEPT_ENCODING] = HTTP_ACCEPT_ENCODING_HEADER_VALUE 

    gpage = conf.googlePage if conf.googlePage > 1 else 1 

#polluted by xi4okv QQ£º48011203 

    for gpage in xrange(1,10): 
        logger.info("using search result page #%d" % gpage) 

        url = "https://m.baidu.com/s?" 
        url += "word=%s&" % urlencode(dork, convall=True) 
        url += "&pn=%d" % ((gpage - 1) * 10) 

        try: 
            req = urllib2.Request(url, headers=headers) 
            conn = urllib2.urlopen(req) 

            requestMsg = "HTTP request:\nGET %s" % url 
            requestMsg += " %s" % httplib.HTTPConnection._http_vsn_str 
            logger.log(CUSTOM_LOGGING.TRAFFIC_OUT, requestMsg) 

            page = conn.read() 
            code = conn.code 
            status = conn.msg 

            responseHeaders = conn.info() 
            page = decodePage(page, responseHeaders.get("Content-Encoding"), responseHeaders.get("Content-Type")) 
            #print page 

            responseMsg = "HTTP response (%s - %d):\n" % (status, code) 

            if conf.verbose <= 4: 
                responseMsg += getUnicode(responseHeaders, UNICODE_ENCODING) 
            elif conf.verbose > 4: 
                responseMsg += "%s\n%s\n" % (responseHeaders, page) 

            logger.log(CUSTOM_LOGGING.TRAFFIC_IN, responseMsg) 
        except urllib2.HTTPError, e: 
            pass 

        urls = [urllib.unquote(match.group(0) or match.group(1)) for match in re.finditer(GOOGLE_REGEX, page, re.I)] 
        #retVal = re.findall(GOOGLE_REGEX, page, re.I) 

        import urlparse 

        for url in urls: 
            urls_pat = re.compile(r"http://(.*)[^']") 
            aurl = re.findall(urls_pat, url) 
            if "?" in url and "baidu" not in url: 
                xpath = urlparse.urlparse(url).path 
                if xpath not in paths: 
                    paths.append(xpath) 
                    retVal.append(aurl[0]) 

    #print retVal 

    return retVal 

def search(dork): 
    pushValue(kb.redirectChoice) 
    kb.redirectChoice = REDIRECTION.YES 

    try: 
        return _search(dork) 
    except SqlmapBaseException, ex: 
        if conf.proxyList: 
            logger.critical(getSafeExString(ex)) 

            warnMsg = "changing proxy" 
            logger.warn(warnMsg) 

            conf.proxy = None 

            setHTTPHandlers() 
            return search(dork) 
        else: 
            raise 
    finally: 
        kb.redirectChoice = popValue() 

def setHTTPHandlers():  # Cross-linked function 
    raise NotImplementedError