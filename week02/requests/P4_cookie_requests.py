import time
import requests
# from fake_useragent import UserAgent

# ua = UserAgent(verify_ssl=False)
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    'Referer': 'https://accounts.douban.com/passport/login?source=movie'
}

s = requests.Session()
# 会话对象： 在有一个Session 实例发出的所以请求之间保持 cookie
# 期间使用 urllib3 的 connection pooling 功能
# 向同一主机发出多个请求，层层的TCP 链接将会被重用，从而带来显著的性能提升
login_url = 'https://accounts.douban.com/j/mobile/login/basic'
form_data = {
    'ck': '',
    'name': '13794849195',
    'password': 'jczhong2017',
    'remember': 'false'
}

response = s.post(login_url, data=form_data, headers=headers)
print(response.json())
print(response.cookies)
print(response.text)

# 登录后可以进程后续的请求
# url2 = 'https://accounts.douban.com/passport/setting'

# response2 = s.get(url2, headers=headers)
# response3 = newseesion.get(url3, headers=headers, cookies=s.cookies)

# with open('profile.html', 'w+') as f:
#     f.write(response2.text)