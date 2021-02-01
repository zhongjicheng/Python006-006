# 操作 list
import redis
import time

client = redis.Redis(host='localhost', password='testpass')

# 增加
client.hset('vip_user', '1001', 1)
client.hset('vip_user', '1002', 1)

# 删除
client.hdel('vip_user', '1002')

# 查询key是否存在
print(client.hexists('vip_user', '1002'))

# 批量添加 键值对(hmset可能在新版本会不使用)
client.hmset('vip_user', {'1003': 1, '1004': 1})

# 读取key值
# hkeys hget hmget hgetall
field = client.hkeys('vip_user')
print(field)
print(client.hget('vip_user', '1001').decode())
print(client.hgetall('vip_user'))

print("checking 1000 if exist")
# 设置过期时间
client.expire('1001', 2)
time.sleep(3)
# 查询key是否存在
print(client.hexists('vip_user', '1001'))
print(client.hget('vip_user', '1001'))
