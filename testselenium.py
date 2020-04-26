# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 17:00:31 2020

@author: RML
"""

import sys
import os
import scapy.all as scapy  #can use pip scapy install - be sure to add to path manager if using IDE
from scapy.layers import http as s_http #pip install scapy_http
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re


p = os.getcwd()
dPath = p + "\\chromedriver.exe"
driver = webdriver.Chrome(dPath)
#driver.maximize_window()
session_cookies = []
driver.get('http://www.wish.com')
input() #manual login
browser_cookies = driver.get_cookies()
 

 ## Create patterns to search for
# testPattern1 = "(logout)|(log out)|(signout)|(sign out)|(my account)|(username)"
# testPattern2 = "(sign in)|(login)|(log in)|(signin)"
# tester1 = re.compile(testPattern1, re.IGNORECASE)
# tester2 = re.compile(testPattern2, re.IGNORECASE)

for c in range(len(browser_cookies)):
    #ensure all floats are ints so can be readded to browser
    #have to do as seperate for loop from below in case of log out
    for key,value in browser_cookies[c].items():                                                                      
        if(type(value) == float):
            browser_cookies[c][key] = int(browser_cookies[c][key])

for c in range(len(browser_cookies)):
    #delete cookies 1 by 1 and check if logs you out
    driver.delete_cookie(browser_cookies[c]['name'])
    print("Deleting {}.".format(browser_cookies[c]['name']))
    driver.refresh()

    # matches1 = tester1.findall(driver.page_source)
    # matches2 = tester2.findall(driver.page_source)
    if (input("Logged out? (y/[n]):") != 'y'):
        # print("Logged in")
        # print(matches1)
        continue
    else:
        session_cookies.append(browser_cookies[c])
        # print(matches1)
        # print("Logged out")
        #log back in
    
    for cookie in browser_cookies:
        driver.add_cookie(cookie)
        
print("Potential session cookies: ")
print(session_cookies)
driver.close()
'''  
Process for automating finding if a site is vulnerable or not
    1) find valid http subdomain (sublister code)
    2) if available, open host url
    3) manual login/create account
    4) get cookies delete 1 by 1 
    5) check if logged in or not
    6) identify if session cookies have httpOnly/secure flags
'''