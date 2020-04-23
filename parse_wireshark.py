'''
parses live stream or user input pcap file.
Finds HTTPRequest packets.
Identfies the URL and idividual cookies within packet.
Still need to:
    1) Call browser from corresponding URL
    2) Import cookies
    3) Call live capture and filter for http authorization response from that URL
    4) Notify user if successful login
'''

##couldn't get pyshark to work correctly without errors.
##A lot of recent stack overflow posts about the same issue. Developer states he has trouble keeping up with it.
#import pyshark 
#started off with this tutorial for live capture function: https://www.youtube.com/watch?v=WMmVheaE0xE

#scapy -> more documentation
import sys
import os
import scapy.all as scapy  #can use pip scapy install - be sure to add to path manager if using IDE
from scapy.layers import http as s_http #pip install scapy_http
#import httplib2
from selenium import webdriver
import http.cookiejar
import requests




PATH = 'C:/Users/RML/Documents/EC521/project'
capture = PATH + '/test.pcap'
driver = webdriver.Chrome(r'C:\Users\RML\Documents\EC521\project\chromedriver.exe')
#driver.maximize_window()

#def live_capture():
#    #https://stackoverflow.com/questions/10729116/adding-a-module-specifically-pymorph-to-spyder-python-ide
#    interface = scapy.IFACES.dev_from_index(7) #7 is the index for the wifi interface on my computer
#    scapy.sniff(iface= interface, store=False, prn = parse_packet)


#offline read pcap file
def offline_parse(capture):
    packets = scapy.sniff(offline = capture, prn = parse_packet)



def parse_packet(p): #callback function for each packet in capture   
    if(p.haslayer('HTTPRequest')): 
        
        # if this packet is an HTTP Request
        # get the requested URL
        url = p.Host.decode() + p.Path.decode()
       # print(url)
        if(p.Cookie):
            pkt_cookies = p.Cookie.decode() #string type
            pkt_cookies = pkt_cookies.split("; ")
            num_cookies = len(pkt_cookies)
            print(pkt_cookies)
            print(type(pkt_cookies))
            driver.get('http://' + url)
            browser_cookies = driver.get_cookies()
#            
'''
still working on parsing the cookies from packets here

            num_bcookies = len(browser_cookies)
            for c in range(num_bcookies):
                for i in range(num_cookies):
                    for key,value in browser_cookies[c].items(): 
                        if(key == 'expiry'):
                            browser_cookies[c]['expiry'] = int(browser_cookies[c]['expiry'])
                        if(browser_cookies[c]['name'] == pkt_cookies(i)):
'''
            
            driver.delete_all_cookies()
            for c in range(num_cookies):
                print(c)
                driver.add_cookie(cookies[c])
            driver.refresh()
            


    
    
offline_parse(capture)
    
#netflix example: replace "netflixid" and "secure_id" with your session values
#driver.get('https://www.netflix.com')
#cookies = driver.get_cookies()
##
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