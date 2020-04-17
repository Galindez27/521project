import sqlite3
import http.cookiejar
import requests
import sys

def get_cookies(cj, ff_cookies):
    con = sqlite3.connect(ff_cookies)
    cur = con.cursor()
    cur.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies")
    for item in cur.fetchall():
        c = http.cookiejar.Cookie(0, item[4], item[5],
            None, False,
            item[0], item[0].startswith('.'), item[0].startswith('.'),
            item[1], False,
            item[2],
            item[3], item[3]=="",
            None, None, {})
        print (c)
        cj.set_cookie(c)



if __name__ == "__main__":
    cj = http.cookiejar.CookieJar()
    ff_cookies = r"C:\Users\Daniel Work\AppData\Roaming\Mozilla\Firefox\Profiles\ftcmwbju.default-release\cookies.sqlite" #path to the cookies.sqlite file, has to be changed for each user, but keep the r at the begining
    get_cookies(cj, ff_cookies)
    s = requests.Session()
    s.cookies = cj
 
