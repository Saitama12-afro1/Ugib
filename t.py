# import requests
# url = "http://cloud.tsnigri.ru/apps/files/?dir=/01-01-ФОНДОВЫЕМАТЕРИАЛЫЦНИГРИ/4625-ФеофилактовГ.А.,1970"
# resp  = requests.get(url)
# print(resp.request.headers, resp.status_code)

import collections
st = "You're on the right track! Keep going."
st = st.replace(' ', '')
st = st.replace('\'', '')
st = st.lower()
print(st)
a = max(collections.Counter(st).values())

print(a)


