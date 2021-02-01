# 操作 list
import redis

client = redis.Redis(host='localhost', password='testpass')

# 添加一个数据
client.zadd('rank', {'a': 4, 'b': 3, 'c': 1, 'd': 2, 'e': 5})

# 修改数据(把 e 的数据 -2，结果是3)
client.zincrby('rank', -2, 'e')

# 查看集合，从小到大排序
print("zrangebyscore: ", client.zrangebyscore('rank', 1, 5))

# 查看集合，从大到小 zrevrank
print("zrevrank: ", client.zrevrank('rank', 1))

# 查询多少个元素（基card）
print("zcard: ", client.zcard('rank'))

# 显示评分(从小到大)
print("zrange: ", client.zrange('rank', 0, -1, withscores=True))

# 显示评分(从大到小)
print("zrevrange: ", client.zrevrange('rank', 0, -1, withscores=True))

