"""
作业二：在使用短信群发业务时，公司的短信接口限制接收短信的手机号，每分钟最多发送五次，请基于 phone 和 redis 实现如下的短信发送接口：
已知有如下函数：

def sendsms(telephone_number: int, content: string, key=None)：
    # 短信发送逻辑, 作业中可以使用 print 来代替
    pass
    # 请实现每分钟相同手机号最多发送五次功能, 超过 5 次提示调用方,1 分钟后重试稍后
    pass
    print("发送成功")
期望执行结果：

sendsms(12345654321, content=“hello”) # 发送成功
sendsms(12345654321, content=“hello”) # 发送成功
…
sendsms(88887777666, content=“hello”) # 发送成功
sendsms(12345654321, content=“hello”) # 1 分钟内发送次数超过 5 次, 请等待 1 分钟
sendsms(88887777666, content=“hello”) # 发送成功

待完成
选做：
1.content 为短信内容，超过 70 个字自动拆分成两条发送
2. 为 sendsms() 函数增加装饰器 send_times()，通过装饰器方式实现限制手机号最多发送次数，如：

@send_times(times=5)
sendsms()
"""

import os
import redis
import random
from dbconfig import read_db_config
from record_log import RecordLog


class RedisBase:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log = RecordLog().logger
        config = read_db_config()
        self.client = redis.Redis(**config)

    def set_phone_num(self, phone_num, op_time=0):
        """
        右侧存入电话号码到表中
        :param phone_num: 电话号码
        :param op_time: 操作次数
        :return: 
        """
        self.client.set(phone_num, op_time)


class SmsSys(RedisBase):
    def __init__(self):
        super(SmsSys, self).__init__()
        self.max_phone_num = 1000

    def init_data(self):
        """
        初始化电话名单
        :return: 
        """
        for phone_num in self.generate_phone_num_list(self.max_phone_num):
            self.set_phone_num(phone_num)

    def generate_phone_num_list(self, max_phone_num):
        """
        生成电话号码列表（不保证电话号码不重复）
        :param max_phone_num: 生成电话号码个数
        :return:
        """
        for _ in range(max_phone_num):
            yield self.generate_phone_num()

    def generate_phone_num(self):
        """
        生成随机电话号码
        :return:
        """
        phone_start = random.choice(['137', '135', '138'])
        phone_end = ''.join(random.sample('0123456789', 8))

        return phone_start + phone_end

    def sendsms(self, telephone_number: int, content: str, key=None):
        """
        实现每分钟相同手机号最多发送五次功能, 超过 5 次提示调用方,1 分钟后重试稍后
        :param telephone_number:
        :param content:
        :param key:
        :return:
        """
        if not self.client.get(telephone_number):
            self.client.set(telephone_number, 1, 60, nx=True)
            print(f"send [{content}] success")
        elif self.client.get(telephone_number).decode() < 5:
            self.client.incr(telephone_number)
            print(f"send [{content}] success")
        else:
            print('1 分钟内发送次数超过 5 次, 请等待 1 分钟')


def main():
    # 初始化电话号码数据
    smssys = SmsSys()
    smssys.init_data()

    # 发送sms
    body = "[极客邦科技]周日晚19点大型直播《如何一步步从工程师成长为架构师》：" \
           "前资深人员分享他们的进阶方法论，帮助想成为架构师的你，快速找到突破口，戳此预约"
    phone_num = 13344455567
    smssys.sendsms(phone_num, body)


if __name__ == '__main__':
    main()
