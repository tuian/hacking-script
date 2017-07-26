#!/usr/bin/env python

"""


"""

from lib.core.enums import PRIORITY

__priority__ = PRIORITY.LOW

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Replaces space character (' ') with plus ('/**)*/')

    >>> tamper('SELECT id FROM users')
    'SELECT/**)*/id/**)*/FROM/**)*/users'
        
    """

    retVal = payload

    if payload:
        retVal = ""
        quote, doublequote, firstspace = False, False, False

        for i in xrange(len(payload)):
            if not firstspace:
                if payload<i>.isspace():
                    firstspace = True
                    retVal += "/**)*/"
                    continue

            elif payload<i> == '\'':
                quote = not quote

            elif payload<i> == '"':
                doublequote = not doublequote

            elif payload<i> == " " and not doublequote and not quote:
                retVal += "/**)*/"
                continue

            retVal += payload<i>

    return retVal</i></i></i></i></i>