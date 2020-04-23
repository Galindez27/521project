import sqlite3
import http.cookiejar
import requests
import sys

def has_http_only(cookie):
    extra_args = cookie.__dict__.get('_rest')
    if extra_args:
        for key in extra_args.keys():
            if key.lower() == 'httponly':
                return True
    return False


def scan_site(sitename):
    #cj = http.cookiejar.CookieJar()
    s = requests.Session()
    #s.cookies = cj
    count = 0
    s.get(sitename);
    for cookie in s.cookies:
        count += 1
        if (not has_http_only(cookie) or not cookie.secure):
            print ('cookie domain = ' + cookie.domain)
            print('cookie name = ' + cookie.name)
            print('cookie secure = ' + str(cookie.secure))
            print('httponly? ' + str(has_http_only(cookie)))
    print(s.cookies)
 

#Usage: import tester5, and then call scan_site('url')
# it will output any cookies that are not secure or dont have httponly enabled
scan_site('https://slack.com/')

