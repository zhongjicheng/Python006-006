#!/usr/bin/env python

"""
作业内容：使用 requests 库抓取知乎任意一个话题下排名前 15 条的答案内容 (如果对前端熟悉请抓取所有答案)，并将内容保存到本地的一个文件。

说明：
本次作业并没有按要求实现，模拟知乎的登录功能。仅实现了作为游客，抓取前10条专栏名称和url，并保存到文件中的功能
后期需要优化点: 模拟知乎账号登录，并进行数据抓取

"""
import requests
from lxml import etree
from queue import Queue
import threading
import json


class CrawlThread(threading.Thread):
    """
    爬虫类
    """

    def __init__(self, crawl_thread_id):
        super().__init__()
        self.thread_id = crawl_thread_id
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
        url = f'https://www.zhihu.com/special/all'
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
        解析网页内容，并保存到文件中
        :param item:
        :return:
        """
        try:
            html = etree.HTML(item)
            self.lock.acquire()
            try:
                link = html.xpath('//div[@class="SpecialListCard-infos"]/a/@href')
                title = html.xpath('//div[@class="SpecialListCard-infos"]/a/text()')
                link_list = list(map(lambda x: "https://www.zhihu.com" + x, link))
                res = dict(zip(title, link_list))
                json.dump(res, fp=self.file, ensure_ascii=False)
            except IOError as e:
                print(f'Dump data to {self.file} failed:', e)

            self.lock.release()

        except Exception as e:
            print('page error:', e)


if __name__ == '__main__':

    # 定义存放解析数据的任务队列
    dataQueue = Queue()

    # 爬虫线程
    crawl_threads = []
    crawl_name_list = ['crawl_1']
    for thread_id in crawl_name_list:
        thread = CrawlThread(thread_id, )
        thread.start()
        crawl_threads.append(thread)

    # 结束crawl线程
    [t.join() for t in crawl_threads]

    # 将结果保持到一个json文件中
    firm_data = []
    with open('book.json', 'a', encoding='utf-8') as pipeline_f:
        # 解析线程
        parse_thread = []
        parser_name_list = ['parse_1']
        flag = True
        for thread_id in parser_name_list:
            thread = ParserThread(thread_id, dataQueue, pipeline_f)
            thread.start()
            parse_thread.append(thread)

        # 结束parse线程
        [j.join() for j in parse_thread]

    print('退出主线程')
