import requests
from lxml import etree
from queue import Queue
import threading
import json
import os
import sys

# 定义存放网页的任务队列
pageQueue = Queue(20)
# 定义存放解析电影数据的任务队列
dataQueue = Queue()
# 定义存放解析电影评论数据的任务队列
reviewDataQueue = Queue()
# 将结果保存到一个json文件中
firm_data = {}


class CrawlDoubanTop250MoviesPagesThread(threading.Thread):
    """
    爬虫类
    """

    def __init__(self, crawl_thread_id, queue):
        super().__init__()
        self.thread_id = crawl_thread_id
        self.queue = queue
        self.seesion = requests.Session()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            'Referer': 'https://accounts.douban.com/passport/login?source=movie'
        }
        self.login_url = 'https://accounts.douban.com/j/mobile/login/basic'
        self.form_data = {
            'ck': '',
            'name': 'testaccount',
            'password': 'testpass',
            'remember': 'false'
        }

    def douban_login(self):
        """
        登陆豆瓣网页
        :return:
        """
        try:
            print("Login Doubaning ...")
            response = self.seesion.post(self.login_url, data=self.form_data, headers=self.headers)
            print(response.json())
            print(response.cookies)
            print(response.text)
        except Exception as e:
            print(f"connect douban failed:{e}")

    def run(self):
        """
        重写run方法
        """
        self.douban_login()
        print(f'启动线程：{self.thread_id}')
        self.scheduler()
        print(f'结束线程：{self.thread_id}')

    def scheduler(self):
        """
        模拟任务调度
        """
        while not self.queue.empty():
            # 队列为空不处理
            page = self.queue.get()
            print(f'下载线程:{self.thread_id}, 下载页面:{page + 1}')
            url = f'https://movie.douban.com/top250?start={page * 25}&filter='
            print(f'top movies url:{url}')

            try:
                # downloader 下载器
                # response = requests.get(url, headers=self.headers)
                response = self.seesion.get(url, headers=self.headers)
                dataQueue.put(response.text)
            except Exception as e:
                print('下载出现异常:', e)


class ParserMovieThread(threading.Thread):
    """
    页面内容分析
    """

    def __init__(self, parser_thread_id, queue, file):
        super().__init__()
        self.lock = threading.Lock()
        self.thread_id = parser_thread_id
        self.queue = queue
        self.file = file

    def run(self):
        print(f'启动线程:{self.thread_id}')
        # while flag:  # 这里有什么优化思路
        while not self.queue.empty():
            try:
                item = self.queue.get(False)  # 参数为false时队列为空，抛出异常
                print(f"item:{item}")
                if not item:
                    continue
                self.parse_data(item)
                self.queue.task_done()  # get之后检测释放会阻塞
            except Exception as e:
                pass
        print(f'结束线程:{self.thread_id}')

    def parse_data(self, item):
        """
        解析网页内容
        :param item:
        :return:
        """
        try:
            html = etree.HTML(item)
            # books = html.xpath('//div[@class="hd"]')
            self.lock.acquire()
            try:
                title = html.xpath('//div[@class="hd"]/a/span[1]/text()')
                link = html.xpath('//div[@class="hd"]/a/@href')
                res = dict(zip(title, link))
                firm_data.update(res)
            except Exception as e:
                print('book error:', e)

            self.lock.release()

        except Exception as e:
            print('page error:', e)


class CrawlDoubanMoviesReviewsThread(threading.Thread):
    """
    爬虫类
    """

    def __init__(self, crawl_thread_id):
        super().__init__()
        self.thread_id = crawl_thread_id
        self.seesion = requests.Session()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            'Referer': 'https://accounts.douban.com/passport/login?source=movie'
        }
        self.login_url = 'https://accounts.douban.com/j/mobile/login/basic'
        self.form_data = {
            'ck': '',
            'name': 'testaccount',
            'password': 'testpass',
            'remember': 'false'
        }

    def douban_login(self):
        """
        登陆豆瓣网页
        :return:
        """
        try:
            print("Login Doubaning ...")
            response = self.seesion.post(self.login_url, data=self.form_data, headers=self.headers)
            print(response.json())
            print(response.cookies)
            print(response.text)
        except Exception as e:
            print(f"connect douban failed:{e}")

    def run(self):
        """
        重写run方法
        """
        # 登陆豆瓣
        self.douban_login()
        print(f'启动线程：{self.thread_id}')
        self.scheduler()
        print(f'结束线程：{self.thread_id}')

    def scheduler(self):
        """
        模拟任务调度
        """
        page = 0
        with open("movies_url.json", 'r', encoding='utf-8') as f:
            movies_info = json.load(f)
            for movie_name, url in movies_info.items():
                review_url = f'{url}reviews?start={page * 20}'
                try:
                    # downloader 下载器
                    response = requests.get(review_url, headers=self.headers)
                    reviewDataQueue.put(response.text)
                except Exception as e:
                    print('下载出现异常:', e)


class ParserReviewThread(threading.Thread):
    """
    页面内容分析
    """

    def __init__(self, queue):
        super().__init__()
        self.lock = threading.Lock()
        self.queue = queue

    def run(self):
        try:
            item = self.queue.get(False)  # 参数为false时队列为空，抛出异常
            print(f"item is empty, item:{item}")
            self.parse_data(item)
            self.queue.task_done()  # get之后检测释放会阻塞
        except Exception as e:
            pass

        # while not self.queue.empty():
        #     try:
        #         item = self.queue.get(False)  # 参数为false时队列为空，抛出异常
        #         if not item:
        #             continue
        #         self.parse_data(item)
        #         self.queue.task_done()  # get之后检测释放会阻塞
        #     except Exception as e:
        #         pass

    def parse_data(self, item):
        """
        解析网页内容
        :param item:
        :return:
        """
        try:
            html = etree.HTML(item)
            # books = html.xpath('//div[@class="hd"]')
            self.lock.acquire()
            try:
                title = html.xpath('//header[@class="main-hd"]/span[1]/text()')
                link = html.xpath('//div[@class="review-content clearfix"]/text()')
                print(f"title:{title}")
                print(f"link:{link}")
                # res = dict(zip(title, link))
                # firm_data.update(res)
            except Exception as e:
                print('book error:', e)

            self.lock.release()

        except Exception as e:
            print('page error:', e)


def main():
    for page_num in range(0, 10):
        pageQueue.put(page_num)

    # 爬虫线程
    crawl_movies_threads = []
    crawl_name_list = ['crasl_1', 'crasl_2', 'crasl_3']
    for thread_id in crawl_name_list:
        thread = CrawlDoubanTop250MoviesPagesThread(thread_id, pageQueue)
        thread.start()
        crawl_movies_threads.append(thread)

    # 结束crawl线程
    [t.join() for t in crawl_movies_threads]

    # 删除 movies_url.json 文件
    if os.path.exists('movies_url.json'):
        os.remove('movies_url.json')

    with open('movies_url.json', 'a', encoding='utf-8') as pipeline_f:
        # 解析线程
        parse_thread = []
        parser_name_list = ['parse_1', 'parse_2', 'parse_3']
        flag = True
        for thread_id in parser_name_list:
            thread = ParserMovieThread(thread_id, dataQueue, pipeline_f)
            thread.start()
            parse_thread.append(thread)

        # flag = False
        # 结束parse线程
        [j.join() for j in parse_thread]

        try:
            # 解析方法和scrapy相同，再构造一个json
            json.dump(firm_data, fp=pipeline_f, ensure_ascii=False)
        except IOError as e:
            print('dump data failed:', e)

    if not os.path.isfile('movies_url.json'):
        print('movies_url.json not exist')
        sys.exit(1)

    # 抓取review页面信息
    crawl_reviews_threads = []
    crawl_name_list = ['crasl_movie_review_1', 'crasl_movie_review_2', 'crasl_movie_review_3']
    for thread_id in crawl_name_list:
        thread = CrawlDoubanMoviesReviewsThread(thread_id)
        thread.start()
        crawl_reviews_threads.append(thread)

    # 结束crawl线程
    [t.join() for t in crawl_reviews_threads]

    # 获取review评论和评分
    parser_reviews_threads = []
    thread = ParserReviewThread(reviewDataQueue)
    thread.start()
    parser_reviews_threads.append(thread)

    # 结束crawl线程
    [t.join() for t in parser_reviews_threads]


if __name__ == '__main__':
    main()
