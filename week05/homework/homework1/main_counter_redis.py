#!/usr/bin/env python

"""
作业一：使用 Python+redis 实现高并发的计数器功能
需求描述:
在社交类网站中，经常需要对文章、视频等元素进行计数统计功能，热点文章和视频多为高并发请求，因此采用 redis 做为文章阅读、视频播放的计数器。
请实现以下函数：

复制代码
counter()
def counter(video_id: int):
    ...
    return count_number
函数说明:

counter 函数为统计视频播放次数的函数，每调用一次，播放次数 +1
参数 video_id 每个视频的 id，全局唯一
基于 redis 实现自增操作，确保线程安全
期望执行结果：
conuter(1001) # 返回 1
conuter(1001) # 返回 2
conuter(1002) # 返回 1
conuter(1001) # 返回 3
conuter(1002) # 返回 2

遗留问题：
1，用户体验不好，存储64万条数据不同线程池的 max_workers 的性能如下：
max_workers=100，总耗时：30m14.907s
2，数据量太大，容易把 redis 搞挂
3，基于 Django+ redis 实现，使用 redis 作为 Django 后端可参考如下代码：
https://django-redis-chs.readthedocs.io/zh_CN/latest/
"""
import os
import threading
import redis
import random
from queue import Queue
from dbconfig import read_db_config
from record_log import RecordLog
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED


class RedisBase:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log = RecordLog().logger
        config = read_db_config()
        self.client = redis.Redis(**config)

    def hash_add(self, key, value, name='video'):
        """
        增加或者修改 value
        :param key:
        :param value:
        :param name:
        :return:
        """
        self.client.hset(name, key, value)

    def hash_get(self, key, name='video'):
        """
        获取 value
        :param key:
        :param name:
        :return:
        """
        value = self.client.hget(name, key)
        if value:
            return value.decode()
        self.log.error(f"get key:{key} from {name} failed, pls check it out.")

    def hash_getall(self, name):
        """
        返回数据库 哈希表中指定 name 的所有字段和值
        :param name:
        :return:
        """
        return self.client.hgetall(name)

    def hash_print_all(self, name):
        """
        打印数据库 哈希表中指定 name 的所有字段和值
        :param name:
        :return:
        """
        result = self.client.hgetall(name)
        for key, value in result.items():
            self.log.info(f"{key.decode()}:{value.decode()}")

    def hash_del(self, key, name='video'):
        """
        删除
        :param key:
        :param name:
        :return:
        """
        self.client.hdel(name, key)

    def hash_member_set(self, value_dic, name='video'):
        """
        批量添加
        :param value_dic:
        :param name:
        :return:
        """
        self.client.hmset(name, value_dic)

    def init_redis_by_keys(self, key_list, value, name='video'):
        """
        按 key 列表，批量初始化redis，value值为 0
        :param key_list:
        :param value:
        :param name:
        :return:
        """
        for key in key_list:
            if not self.client.hget(name, key):
                self.hash_add(key, value, name=name)


class VideoCounter(RedisBase):
    def __init__(self, v_num):
        super(VideoCounter).__init__()
        self.video_num = v_num
        self.group_name = "documentary"
        self.video_id_list = [f'video_{i}' for i in range(self.video_num)]

    def init_data(self):
        """
        初始化所有的视频播放量，默认为 0
        :return:
        """
        self.init_redis_by_keys(self.video_id_list, 0, self.group_name)

    def counter(self, video_id):
        """
        视频播放计数器
        :param video_id: 视频id
        :return:
        """
        if video_id not in self.video_id_list:
            self.video_id_list.append(video_id)
            self.hash_add(video_id, 0, name=self.group_name)
        else:
            views = self.hash_get(video_id, name=self.group_name)
            if views:
                views = int(views) + 1
                self.hash_add(video_id, views, name=self.group_name)
                return views
            else:
                return False


def get_video_id(total_video_num, total_views):
    """
    获取总随机 video_id
    :param total_video_num:
    :param total_views:
    :return:
    """
    for _ in range(total_views):
        yield f"video_{random.randint(0, total_video_num-1)}"   # -1 是为了确保随机数是在 0 - total_video_num，不包含 total_video_num


def main():
    total_views = 1000000  # 网站视频总播放量
    total_video_num = 10  # 网站总视频数

    # 初始化数据到redis
    count = VideoCounter(total_video_num)
    count.init_data()

    # 批量线程通过map提交
    executor = ThreadPoolExecutor(max_workers=10)
    for result in executor.map(count.counter, get_video_id(total_video_num, total_views)):
        pass

    # 打印各视频播放量
    count.hash_print_all(count.group_name)


if __name__ == '__main__':
    main()
