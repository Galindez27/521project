# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 17:00:31 2020

@author: RML
"""
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

def test_site_cookies(target_url: str, login_pattern: str, verbose=False):
    '''Returns a dictionary of 3 lists
    {
        "all_sess_cookies": []
        "no_secure_flag": []
        "no_http_only: []
    }

    Use verbose=True to see output, defaults to false
    '''


    p = os.getcwd()
    dPath = p + "\\chromedriver.exe"
    driver = webdriver.Chrome(dPath)
    #driver.maximize_window()
    driver.get(target_url)
    input("Hit enter when logged in.") #manual login
    browser_cookies = driver.get_cookies() #Saves initial cookies so we can reset state and use

    # Pattern looks for indicators of login. In our test case we look for our name and lastname.
    #   This could also be extended to look for a specific username
    searcher = re.compile(login_pattern, re.IGNORECASE)

    for c in range(len(browser_cookies)):
        #ensure all floats are ints so can be readded to browser
        #have to do as seperate for loop from below in case of log out
        for key,value in browser_cookies[c].items():                                                                      
            if(type(value) == float):
                browser_cookies[c][key] = int(browser_cookies[c][key])

    # Lists to be returned
    session_cookies = []
    nohttp = []
    notsecure = []

    for c in range(len(browser_cookies)):
        # delete cookies 1 by 1 and check if logs you out
        driver.delete_cookie(browser_cookies[c]['name'])
        if verbose:
            print("Deleting {}.".format(browser_cookies[c]['name']))
        driver.refresh()

        #Searcher will return None if pattern is not found (if we aren't logged in)
        m = searcher.search(driver.page_source)

        if(m != None):
            if verbose:
                print("logged in")
        else:
            if verbose:
                print("Possible logout")
            session_cookies.append(browser_cookies[c])
            if (not browser_cookies[c]['httpOnly']):
                nohttp.append(browser_cookies[c])
            if (not browser_cookies[c]['secure']):
                notsecure.append(browser_cookies[c])
        
        for cookie in browser_cookies: #Reset cookies in jar
            driver.add_cookie(cookie)

    driver.close()
    return {
        "all_sess_cookies": session_cookies,
        "no_secure_flag": notsecure,
        "no_http_only": nohttp
    }

if __name__ == "__main__": # Just running this file runs this.
    import pprint
    targ = "http://wish.com"
    found_cookies = test_site_cookies(targ, "(Pizzaman)|(Pizzaboy)", verbose=True)
    pprint.pprint(found_cookies)
    newDriver = webdriver.Chrome(os.getcwd() + "\\chromedriver.exe")
    newDriver.get(targ)
    for cookie in found_cookies['all_sess_cookies']:
        newDriver.add_cookie(cookie)
    newDriver.refresh()
    input("Hit enter when done")
    newDriver.close()