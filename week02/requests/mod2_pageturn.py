"""
实现功能：
1、实现网页翻页处理
2、获取豆瓣的top 250电影名称和地址
"""
import sys
import requests
from lxml import etree
# 控制请求的频率，引入了time模块
from time import sleep


# 使用def 定义函数，myurl是函数的参数
def get_url_name(myurl):
    ua = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    header = {'user-agent': ua}
    try:
        response = requests.get(myurl, headers=header)
    except requests.exceptions.ConnectTimeout as e:
        print('requests 库超时')
        sys.exit(1)

    selector = etree.HTML(response.text)
    # 电影名称列表
    film_name = selector.xpath('//div[@class="hd"]/a/span[1]/text()')

    # 电影链接列表
    film_link = selector.xpath('//div[@class="hd"]/a/@href')
    # 遍历对应关系字典
    film_info = dict(zip(film_name, film_link))
    for i in film_info:
        print(f'电影名称:{i} \t\t 电影链接: {film_info[i]}')


if __name__ == '__main__':
    # 生成包含所以页面的元祖
    urls = tuple(f'https://movie.douban.com/top250?start={page * 25}&filter=' for page in range(10))
    for page in urls:
        get_url_name(page)
        sleep(5)
