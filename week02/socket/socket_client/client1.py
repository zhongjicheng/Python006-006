"""
用http协议访问网页
"""
import requests
# pip3 install requests

r = requests.get('http://www.httpbin.org')
print(r.status_code)
print(r.headers)
#print(r.text)
