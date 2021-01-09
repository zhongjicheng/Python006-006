import requests
from lxml import etree
from queue import Queue
import threading
import json


class CrawlThread(threading.Thread):
    """
    爬虫类
    """

    def __init__(self, crawl_thread_id, queue):
        super().__init__()
        self.thread_id = crawl_thread_id
        self.queue = queue
        self.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }

    def run(self):
        """
        重写run方法
        """
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
            print(f'下载线程:{self.thread_id}, 下载页面:{page+1}')
            url = f'https://movie.douban.com/top250?start={page*25}&filter='
            print(f'url:{url}')

            try:
                # downloader 下载器
                response = requests.get(url, headers=self.headers)
                dataQueue.put(response.text)
            except Exception as e:
                print('下载出现异常:', e)


class ParserThread(threading.Thread):
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
                firm_data.append(res)
            except Exception as e:
                print('book error:', e)

            self.lock.release()

            # for book in books:
            #     try:
            #         title = book.xpath('./a/span[1]/text()')
            #         link = book.xpath('./a/@href')
            #         # response = {
            #         #     'title': title,
            #         #     'link': link
            #         # }
            #         # 解析方法和scrapy相同，再构造一个json
            #         # json.dump(response, fp=self.file, ensure_ascii=False)
            #     except Exception as e:
            #         print('book error:', e)

        except Exception as e:
            print('page error:', e)


if __name__ == '__main__':
    # 定义存放网页的任务队列
    pageQueue = Queue(20)
    for page_num in range(0, 10):
        pageQueue.put(page_num)

    # 定义存放解析数据的任务队列
    dataQueue = Queue()

    # 爬虫线程
    crawl_threads = []
    crawl_name_list = ['crasl_1', 'crasl_2', 'crasl_3']
    for thread_id in crawl_name_list:
        thread = CrawlThread(thread_id, pageQueue)
        thread.start()
        crawl_threads.append(thread)

    # 结束crawl线程
    [t.join() for t in crawl_threads]

    # 将结果保持到一个json文件中
    firm_data = []
    with open('book.json', 'a', encoding='utf-8') as pipeline_f:
        # 解析线程
        parse_thread = []
        parser_name_list = ['parse_1', 'parse_2', 'parse_3']
        flag = True
        for thread_id in parser_name_list:
            thread = ParserThread(thread_id, dataQueue, pipeline_f)
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

    print('退出主线程')
