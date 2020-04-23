dict = {}

all_cookies = "_ga=GA1.2.1335192507.1585581283; nmstat=1585581342667; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22c644349f-1f5e-45af-b7f0-39a1a5ca3cbe%22; _gid=GA1.2.361457333.1586893284; _mkto_trk=id:131-AQO-225&token:_mch-washington.edu-1586893290213-65575; _d2i_id.7a490682-d908-4153-b1b4-ba39c8085050=cc72bb1f-21de-4e4f-b614-bf2945038383; _d2i_ses.7a490682-d908-4153-b1b4-ba39c8085050=70bf99e0-6167-4b4c-b1e6-5c76b6d2ea4c; _d2i_po.7a490682-d908-4153-b1b4-ba39c8085050=2 "


all_cookies = all_cookies.split("; ")
num_cookies = len(all_cookies)
for c in range(num_cookies):
    tmp_list = all_cookies[c].split("=", 1)
    dict[tmp_list[0]] = tmp_list[1]
print(dict)
