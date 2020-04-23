dict = {}

all_cookies = 

all_cookies = all_cookies.split("; ")
num_cookies = len(all_cookies)
for c in range(num_cookies):
    tmp_list = all_cookies[c].split("=", 1)
    dict[tmp_list[0]] = tmp_list[1]
print(dict)
