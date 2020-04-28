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

driver = webdriver.Chrome(r'C:\Users\RML\Documents\EC521\project\chromedriver.exe')
#driver.maximize_window()
session_cookies = []
nohttpOnly = []
nosecure = []
driver.get('https://facebook.com')
input("Press Enter to continue...")
print("continuing")
#time.sleep(40) #manual login
browser_cookies = driver.get_cookies()
 

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
    ret = driver.find_elements_by_xpath("(//*[contains(translate(text(), 'LOG OUT', 'log out'), 'log out')])")
    ret2 = driver.find_elements_by_xpath("(//*[contains(translate(text(), 'SIGN OUT', 'sign out'), 'sign out')])")
    ret3 = driver.find_elements_by_xpath("(//*[contains(translate(text(), 'LOG IN', 'log in'), 'log in')])")
    ret4 = driver.find_elements_by_xpath("(//*[contains(translate(text(), 'SIGN IN', 'sign in'), 'sign in')])")
  #  ret5 = driver.find_elements_by_xpath("(//*[contains(text(), 'logout')])")
  #  ret6 = driver.find_elements_by_xpath("(//*[contains(text(), 'login')])")
    if((ret != [] or ret2 != [] ) or (ret3 == [] and ret4 == [])): #or ret5 != [], and ret6 == [])
        #log/sign out option avial or neither log/sign in avail
        print("Still logged IN")
#        print(ret); print("ret: log out present\n")
#        print(ret2); print("ret2: sign out present\n")
#        print(ret5); print("ret5: logout is present\n")
#        print(ret3); print("ret3: log in not present\n")
#        print(ret4); print("ret4: sign in not present\n")
#        print(ret6); print("ret6: login not present\n")
#        
    else:
        print("Logged OUT")
        session_cookies.append(browser_cookies[c]['name'])
        if(browser_cookies[c]['httpOnly'] == False):
            nohttpOnly.append(browser_cookies[c]['name'])
        if(browser_cookies[c]['secure'] == False):
            nosecure.append(browser_cookies[c]['name'])
        #log back in
        for i in range(len(browser_cookies)):
            driver.add_cookie(browser_cookies[i])
print("Potential session cookies: ")
print(session_cookies)
print("Session cookies without httpOnly flag:")
print(nohttpOnly)
print("Session cookies without secure flag:")
print(nosecure)
    
            
'''       
        continue
    elif((ret == [] and ret2 == [] ) or (ret3 != [] or ret4 != [] )): #and ret5 == [], or ret6 != [])
        print("Logged OUT")      
#        print(ret); print("ret: log out not present\n")
#        print(ret2); print("ret2: sign out not present\n")
#        print(ret5); print("ret5: logout not present\n")
#        print(ret3); print("ret3: log in is present\n")
#        print(ret4); print("ret4: sign is present\n")
#        print(ret6); print("ret6: login is present\n")


        session_cookies.append(browser_cookies[c]['name'])
        #log back in
        for i in range(len(browser_cookies)):
            driver.add_cookie(browser_cookies[i])
    else:
        print("not right")
        #log back in
        for i in range(len(browser_cookies)):
            driver.add_cookie(browser_cookies[i])
        
print("Potential session cookies: ")
print(session_cookies)
'''
    

'''  
Process for automating finding if a site is vulnerable or not
    1) find valid http subdomain (sublister code)
    2) if available, open host url
    3) manual login/create account
    4) get cookies delete 1 by 1 
    5) check if logged in or not
    6) identify if session cookies have httpOnly/secure flags
'''