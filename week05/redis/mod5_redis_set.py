# 操作 list
import redis

client = redis.Redis(host='localhost', password='testpass')

# 添加一个数据
client.sadd('redis_set_demo', 'new_data')
# 弹出一个数据（随机的）
# client.spop()

# 查看所有的数据
# client.smembers('redis_set_demo')

# 集合运算
# 交接
client.sinter('set_a', 'set_b')

# 并集
client.sunion('set_a', 'set_b')

# 差集
client.sdiff('set_a', 'set_b')


