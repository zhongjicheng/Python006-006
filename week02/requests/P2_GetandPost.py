# http 协议的 GET 方法
import requests
r = requests.get('https://github.com')
r.status_code
r.headers['content-type']
# r.text
r.encoding
# r.json()

# http 协议 POST 方法
import requests
r = requests.post('http://httpbin.org/post', data={'key':'value'})
# 获取返回结果
r.json()
