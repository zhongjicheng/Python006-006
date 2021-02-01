# 链接 Redis
import redis
# pip install redis

client = redis.Redis(host='localhost', password='testpass')

# 读取 redis 的所有 key，生产环境不建议这么用，因为生产环境中redis有大量的数据，会有一定的开销
print(client.keys())

for key in client.keys():
    print(key.decode())
