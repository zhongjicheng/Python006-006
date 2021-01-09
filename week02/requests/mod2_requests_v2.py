# ！/usr/bin/env python

import sys
import requests
from pathlib import *

# 浏览器的头
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
header = {'user-agent': user_agent}
myurl = 'https://movie.douban.com/top250'

try:
    response = requests.get(myurl, headers=header)
except requests.exceptions.ConnectTimeout as e:
    print('requests 库超时')
    sys.exit(1)

# 将网页内容改为存入文件
# print(response.text)

# 获得python脚本的绝对路径
p = Path(__file__)
pyfile_path = p.resolve().parent
# 建立新的目录html
html_path = pyfile_path.joinpath('html')
if not html_path.is_dir():
    Path.mkdir(html_path)
page = html_path.joinpath('douban.html')

# 上下文管理器
try:
    with open(page, 'w', encoding='utf-8') as f:
        f.write(response.text)
except FileNotFoundError as e:
    print(f'文件无法打开， {e}')
except IOError as e:
    print(f'读写文件出错， {e}')
except Exception as e:
    print(e)
