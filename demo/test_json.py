# -*- coding: utf-8 -*-
import json
import requests
import re
#
# response = requests.get("https://jsonplaceholder.typicode.com/todos")
# todos = json.loads(response.text)
#
# print todos[0]
#
# print todos[0]["title"]



# xs=re.findall(r'\d+', '261课，5198词')
# print xs

def test():
    for x in range(6):
        yield x


for a in test():
    print a