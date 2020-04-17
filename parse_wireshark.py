# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 08:24:48 2020

@author: RML
"""
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

PATH = 'C:/Users/RML/Documents/EC521/project'
capture = PATH + '/test.pcap'


#offline read pcap file
def offline_parse(capture):
    packets = scapy.sniff(offline = capture, prn = parse_packet)


def live_capture():
    #https://stackoverflow.com/questions/10729116/adding-a-module-specifically-pymorph-to-spyder-python-ide
    interface = scapy.IFACES.dev_from_index(7) #7 is the index for the wifi interface on my computer
    scapy.sniff(iface= interface, store=False, prn = parse_packet)

def parse_packet(p): #callback function for each packet in capture   

    if(p.haslayer('HTTPRequest')):
        # if this packet is an HTTP Request
        # get the requested URL
        url = p.Host.decode() + p.Path.decode()
       # print(url)
        if(p.Cookie):
            all_cookies = p.Cookie.decode() #string type
            all_cookies = all_cookies.split("; ")
            num_cookies = len(all_cookies)
            for c in range(num_cookies):
                print(all_cookies[c])
      #  p.show() #will print entire contents of packet in readable form
    
    
offline_parse(capture)



