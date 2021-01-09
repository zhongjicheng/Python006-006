#！/usr/bin/env python
import requests

# 浏览器的头
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
header = {'user-agent':user_agent}
myurl = 'https://movie.douban.com/top250'
response = requests.get(myurl, headers=header)
print(response.text)
print(f'返回码是: {response.status_code}')
