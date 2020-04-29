# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 17:00:31 2020
@author: RML
"""
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import sublist3r
import requests

def test_site_cookies(target_url: str, login_pattern: str, verbose=False):
    '''Returns a dictionary of 5 lists
    {
        "all_sess_cookies": [],
        "no_secure_flag": [],
        "no_http_only: [],
        "all_secure_cookies": [],
        "all_http_cookies": []
    }

    Use verbose=True to see output, defaults to false
    '''
    #p = os.getcwd()
   # dPath = p + "\\chromedriver.exe"
    driver = webdriver.Firefox()
    # driver.maximize_window()
    driver.get(target_url)
    input("Hit enter when logged in.")  # manual login
    browser_cookies = driver.get_cookies()  # Saves initial cookies so we can reset state and use

    # Pattern looks for indicators of login. In our test case we look for our name and lastname.
    #   This could also be extended to look for a specific username
    searcher = re.compile(login_pattern, re.IGNORECASE)

    # Lists to be returned
    session_cookies = []
    nohttp = []
    notsecure = []
    allsecure = []
    allhttponly = []

    for c in range(len(browser_cookies)-10,len(browser_cookies)):
        # ensure all floats are ints so can be readded to browser
        # have to do as seperate for loop from below in case of log out
        # also pull out all secure and httponly cookies
        for key, value, in browser_cookies[c].items():
            if (type(value) == float):
                browser_cookies[c][key] = int(browser_cookies[c][key])
        if browser_cookies[c]['httpOnly']:
            allhttponly.append(browser_cookies[c])
        if browser_cookies[c]['secure']:
            allsecure.append(browser_cookies[c])

    for c in range(len(browser_cookies)-10,len(browser_cookies)):
        # delete cookies 1 by 1 and check if logs you out
        driver.delete_cookie(browser_cookies[c]['name'])
        if verbose:
            print("Deleting {}.".format(browser_cookies[c]['name']))
        driver.refresh()

        # Searcher will return None if pattern is not found (if we aren't logged in)
        m = searcher.search(driver.page_source)

        if (m != None):
            if verbose:
                print("still logged in")
        else:
            if verbose:
                print("we got jebooted")
            session_cookies.append(browser_cookies[c])
            if (not browser_cookies[c]['httpOnly']):
                nohttp.append(browser_cookies[c])
            if (not browser_cookies[c]['secure']):
                notsecure.append(browser_cookies[c])
            break

        for cookie in browser_cookies:  # Reset cookies in jar
            driver.add_cookie(cookie)

    driver.close()
    return {
        "all_sess_cookies": session_cookies,
        "no_secure_flag": notsecure,
        "no_http_only": nohttp,
        "all_secure_cookies": allsecure,
        "all_http_cookies": allhttponly
    }


if __name__ == "__main__":  # Just running this file runs this. Use for demo/Testing
    import pprint

    targ = "http://banggood.com"

    found_cookies = test_site_cookies(targ, "(Pizzaman)|(Pizzaboy)|(bucyber2020@gmail.com)|(sign out)", verbose=True)

    # Print out results
   # print("Num Session Cookies:\t{}".format(len(found_cookies['all_sess_cookies'])))
    #print("Cookie name/values:")
    print("Found our authenticating cookie")
    for cook in found_cookies['all_sess_cookies']:
        print((cook['name'], cook['value'], "Secure?" + (" Yes" if cook['secure'] else " Nope")))


    # Attempt login from fresh browser
    print("Let's pull up a logged-in session")
    newDriver = webdriver.Firefox()
    newDriver.get(targ)
    for cookie in found_cookies['all_sess_cookies']:
        newDriver.add_cookie(cookie)
    newDriver.refresh()
    #input("Hit enter when done")
    #newDriver.close()

    print("Finding subdomains of target...")
    subdomains = sublist3r.main("banggood.com", 40, 'some_subdomains.txt', ports=None, silent=True, verbose=False,
                                enable_bruteforce=False, engines=None)
    insecure = []
    first = 0
    print("Iterating through list for subdomains that allow http access")
    for website in subdomains:
        # print('checking http://' + website)
        try:
            r = requests.get('http://' + website, timeout=5)
        except:
            continue
        if not 'https' in r.url:
            print("Found potential site, " + website)
            insecure.append(website)
            #newDriver.execute_script("window.open('{}');".format(website))
            #print(newDriver.window_handles)
            if first == 0:
                newDriver.execute_script("window.open();")
                newDriver.switch_to.window(newDriver.window_handles[1])
            newDriver.get("http://" + website)
            if 'https' in newDriver.current_url:
                print("nah")
                continue
            try:
                newDriver.get_cookie(found_cookies['all_sess_cookies'][0]['name'])
            except:
                print("nah")
                continue
            print("Subdomain http://" + website + " will give session cookie" )
            print("target domain is vulnerable")
            exit()

    print("No subdomains will give desired cookie")


            #newDriver.switch_to_window()

