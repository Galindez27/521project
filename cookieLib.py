import requests as req
from copy import deepcopy
from pathlib import Path
import sqlite3

def cookiePing(url: str):
    '''Pings a site URL and returns all the cookies
    the sire returns'''
    sess = req.sessions.Session()
    resp = sess.get(url)
    if resp.status_code == 200:
        return sess.cookies

def cookiesFromJar(pathObj: Path) -> req.cookies.RequestsCookieJar:
    '''Pulls cookies from a cookie jar given the path to 
    the sqlite. Returns a request session cookie jar.
    
    Currently only works on Firefox cookie jars

    TODO: Add support for google chrome and a way
    to decide which cookie jar is being read'''
    temp = req.cookies.RequestsCookieJar()
    jarData = sqlite3.connect(pathObj)
    curs = jarData.cursor()
    curs.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies")
    for cookie in curs.fetchall():
        result = { # Default cookie dictionary is filled in with the cookie's data we need
            'version': 0,
            'name': cookie[4],
            'value': cookie[5],
            'port': None,
            'domain': cookie[0],
            'path': cookie[1],
            'secure': cookie[2],
            'expires': None,
            'discard': True,
            'comment': None,
            'comment_url': None,
            'rest': {'HttpOnly': None},
            'rfc2109': False,
            'port_specified': None,
            'domain_specified': None,
            'domain_initial_dot': None,
            'path_specified': None
        }
        newCookie = req.cookies.cookielib.Cookie(**result) # Create cookie
        temp.set_cookie(newCookie)

    return temp
    #     reqCookie = req.cookies.cookielib.Cookie(*cookie)
    #     req.cookies.merge_cookies(temp, reqCookie)
    # return temp
