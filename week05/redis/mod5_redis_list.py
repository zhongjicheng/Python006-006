# 操作 list
import redis

client = redis.Redis(host='localhost', password='testpass')

# 列表左侧存入数据
client.lpush('list_redis_demo', 'python')
# 列表右侧存入数据
client.rpush('list_redis_demo', 'java')

# 查看长度
print(client.llen('list_redis_demo'))

# 弹出数据
# lpop()  rpop()
data = client.lpop('list_redis_demo')
print(data)

# 查看一定范围的list数据
data = client.lrange('list_redis_demo', 0, -1)
print(data)

"""
列表的主要功能：左侧、右侧弹出和左侧、右侧添加，一般工作中我们会把它当成队列使用；
列表使用场景：
比如，批量地对某一类用户或某一类产品，相同的角色做相同的事情；
比如，对网站里的所有用户下发一个通知，发放优惠券，请用户来访问我们的服务器；
那么对多个用户去发送这些数据的时候，网关是有并发限制的，我们做不到把百万级的数据同时丢给网关，
一般我们会取出网关的最大并发链接，比如说10个，然后把我们的所有的用户，存入到我们的redis的列表中，
然后在列表中从左侧或者右侧按照顺序取出10个用户，然后发送短信；如果发送成功则继续发送下10个用户，
如果发送失败，我们再把这些失败的用户加入到新的列表当中，等所有的用户都发送完成后，没有发送成功的用户可以再发送一次；
有一些短信平台只能一个用户一个用户传，我们可以使用右侧的 rpop，把右侧的用户弹出，
如果发送失败，我们用 lpush 把这个失败的用户从同一个列表左侧插入；
"""
while True:
    phone = client.rpop('list_redis_demo')
    if not phone:
        print('发送完毕')
        break

    # sendsms(phone)
    # result_times = retry_once(phone)
    # if result_times >= 5:
    #     client.lpush('list_redis_demo', phone)

