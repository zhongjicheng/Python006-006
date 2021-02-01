# 生产者代码
import pika
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

# 声明交换机
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

# exchange 指定交换机
# routing_key 指定队列名
message = 'send message to fanout'
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)

# 关闭与rabbitmq server的链接
connection.close()
