# 操作 string
# 用户量超过百万级可以用 string
# 如果超过百万级可以用哈希方式存储
# 不要贸然使用 keys* 指令，会造成redis短暂不响应
import redis

client = redis.Redis(host='localhost', password='testpass')

# 保存 value 值到 key 中
client.set('key', 'value')
result = client.get('key')
print(result.decode())

# 默认的情况会把原来 key 的值覆盖
client.set('key', 'value2')
result = client.get('key')
print(f"overwrite value:{result.decode()}")

# 如果不想覆盖原来的值，可以把 nx 参数设置为 True
client.set('key', 'value3', nx=True)
result = client.get('key')
print(f"not overwrite value:{result.decode()}")

# 在value3后面增加字符
client.append('key', "value4")
result = client.get('key')
print(f"append value:{result.decode()}")


client.set('key2', '100')
result = client.get('key2')
print(f"origin value:{result.decode()}")
# 对原有的值 +1
client.incr('key2')
result = client.get('key2')
print(f"increase value:{result.decode()}")
# 对原有的值 -1
client.decr('key2')
result = client.get('key2')
print(f"decrease value:{result.decode()}")

print(client.getrange())