# 消费者代码
import pika
import time

# pip install pika

# 用户和密码
credentials = pika.PlainCredentials('admin', 'admin')

# 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
parameters = pika.ConnectionParameters(host='localhost',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)

# 阻塞方法
connection = pika.BlockingConnection(parameters)

# 建立信道
channel = connection.channel()

# 声明消息队列(队列不存在就创建，存在就直接使用)
# 如不存在自动创建
# durable = True 队列持久化
channel.queue_declare(queue='task_queue', durable=True)


# 定义一个回调函数来处理消息队列中的消息
def callback(ch, method, properties, body):
    """
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    time.sleep(1)
    # 实现如何处理消息
    print(body.decode())
    # 手动发送消息确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 如果该消费者的channel上未确认的消息数达到了 prefetch_count 数，则不向该消费者发送消息
channel.basic_qos(prefetch_count=1)

# 消费者使用队列和那个回调函数处理消息
channel.basic_consume('task_queue', on_message_callback=callback)

# 开始接收信息，并进入阻塞状态
channel.start_consuming()
