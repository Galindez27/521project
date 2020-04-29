import os
import sublist3r
import requests
# to install sublist3r, first install requests, dnspython and argparse python modules as you would any other module
# and then run pip install git+https://github.com/aboul3la/Sublist3r

def http_subdomains(domain, exhaustive=False):
    subdomains = sublist3r.main(domain, 40, 'some_subdomains.txt', ports=None, silent=True, verbose=False,
                                enable_bruteforce=False, engines=None)
    insecure = []
    for website in subdomains:
        #print('checking http://' + website)
        try:
            r = requests.get('http://'+website, timeout=5)
        except:
            continue
        if not 'https' in r.url:
            insecure.append(website)
            print(website)
            if not exhaustive and len(insecure) > 4:
                break
    return insecure
print(http_subdomains('banggood.com'))
