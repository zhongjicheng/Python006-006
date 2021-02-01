# Ubuntu安装Redis及使用

# NoSQL简介
- NoSQL，全名为Not Only SQL，指的是非关系型的数据库
- 随着访问量的上升，网站的数据库性能出现了问题，于是nosql被设计出来
# 优点/缺点
- 优点:
    - 高可扩展性
    - 分布式计算
    - 低成本
    - 架构的灵活性，半结构化数据
    - 没有复杂的关系

- 缺点:
    - 没有标准化
    - 有限的查询功能（到目前为止）
    - 最终一致是不直观的程序
    

# 分类
|  类型   | 部分代表 | 特点 |
|  ----  | ----  | --- |
| 列存储  | Hbase 、 Cassandra 、 Hypertable | 顾名思义，是按列存储数据的。最大的特点是方便存储结构化和半结构化数据，方便做数据压缩，对针对某一列或者某几列的查询有非常大的IO优势。 | 
| 文档存储  | MongoDB 、CouchDB | 文档存储一般用类似json的格式存储，存储的内容是文档型的。这样也就有有机会对某些字段建立索引，实现关系数据库的某些功能。 |
| key-value 存储| TokyoCabinet/Tyrant、 BerkeleyDB、MemcacheDB 、 Redis | 可以通过key快速查询到其value。一般来说，存储不管value的格式，照单全收。（Redis包含了其他功能） |
| 图存储 | Neo4J、 FlockDB | 图形关系的最佳存储。使用传统关系数据库来解决的话性能低下，而且设计使用不方便。 |
| 对象存储 | db4o 、 Versant | 通过类似面向对象语言的语法操作数据库，通过对象的方式存取数据。 |
| xml数据库 | BerkeleyDB、 XML、 BaseX | 高效的存储XML数据，并支持XML的内部查询语法，比如XQuery,Xpath。 |

# redis相关资源：
[Redis 官网](https://redis.io/)

[Redis 在线测试](http://try.redis.io/)

[Redis菜鸟教程](https://www.runoob.com/redis/redis-tutorial.html)

# Redis安装
## 在线安装
直接输入命令 ``` sudo apt-get install redis-server ```
安装完成后，Redis服务器会自动启动。
使用```ps -aux|grep redis```命令可以看到服务器系统进程默认端口6379

redis      2890  0.2  0.1  41872  6064 ?        Ssl  14:17   0:07 /usr/bin/redis-server 127.0.0.1:6379     
hzlarm     3222  0.0  0.0  11324   780 pts/2    S+   15:02   0:00 grep --color=auto redis 

使用 ```netstat -nlt|grep 6379```命令可以看到redis服务器状态
tcp 0 0 127.0.0.1:6379 0.0.0.0:* LISTEN
使用```sudo /etc/init.d/redis-server status```命令可以看到Redis服务器状态在这里插入图片描述

## 下载安装包：
- 下载：打开redis官方网站，推荐下载稳定版本(stable)
```wget http://download.redis.io/releases/redis-5.0.5.tar.gz```
- 解压```tar xzf redis-5.0.5.tar.gz```
- 复制：推荐放到usr/local目录下```sudo mv redis-5.0.5 /usr/local/redis```
- 进入redis目录 ```cd /usr/local/redis/```
- 生成:```sudo make```失败则 使用 ```sudo make MALLOC=libc```后再```sudo make```
- 测试 ```sudo make test``` 这段运行时间会较长
- 安装：将redis的命令安装到/usr/bin/目录```sudo make install```
- 运行 redis-server 按ctrl+c停止

# Redis服务器基本配置
配置文件为```/etc/redis/redis.conf```(在线安装推荐)或者 ```/usr/local/redis/redis.conf```(手动安装)

首先```sudo vi /etc/redis/redis.conf```
## 添加Redis的访问账号
Redis服务器默认是不需要密码的，假设设置密码为hzlarm。
去掉requirepass 前面的注释#，在后面添加密码
```requirepass hzlarm```

## 开启Redis的远程连接
注释掉绑定地址#bind 127.0.0.1

## 修改Redis的默认端口
```port 6379```

## Redis以守护进程运行
如果以守护进程运行，则不会在命令行阻塞，类似于服务
如果以非守护进程运行，则当前终端被阻塞，无法使用
推荐改为yes，以守护进程运行
daemonize no|yes
Redis的数据文件
dbfilename dump.rdb

## 数据文件存储路径
dir /var/lib/redis

## 配置完成后重新启动服务器
```
sudo /etc/init.d/redis-server restart or
sudo service redis-server restart or
sudo redis-server /etc/redis/redis.conf
```

Redis安装 配置服务器 启动客户端 数据操作 发布订阅 主从配置 卸载Redis

# 启动客户端
安装Redis服务器，会自动地一起安装Redis命令行客户端程序。命令行输入 ```redis-cli``` 如果设置了密码hzlarm```redis-cli -a hzlarm```

## 常用命令： Redis命令不区分大小写
- ping返回PONG表示畅通
- help 命令行的帮助
- quit 或者Ctrl+d或者Ctrl+c退出

## 键的命令
- 查找键，参数支持正则KEYS pattern例如keys *查看所有的key列表
- 判断键是否存在，如果存在返回1，不存在返回0EXISTS key [key ...]
- 查看键对应的value的类型TYPE key
- 删除键及对应的值DEL key [key ...]
- 设置过期时间，以秒为单位
创建时没有设置过期时间则一直存在，直到使用使用DEL移除EXPIRE key seconds
- 查看有效时间，以秒为单位TTL key
- 修改 key 的名称RENAME key newkey

# 数据操作
- redis是key-value的数据，所以每个数据都是一个键值对
- 键的类型是字符串
- 值的类型分为五种：
    - 字符串string
    - 哈希hash
    - 列表list
    - 集合set
    - 有序集合zset
- 数据操作的全部命令，可以查看中文网站
- 接下来逐个介绍操作各类型的命令
- 各个数据类型应用场景：

| 类型 | 简介 | 特性 | 场景 |
|---|---|---|---|
| String(字符串) | 二进制安全 | 可以包含任何数据,比如jpg图片或者序列化的对象,一个键最大能存储512M | — |
| Hash(字典)	| 键值对集合,即编程语言中的Map类型 | 适合存储对象,并且可以像数据库中update一个属性一样只修改某一项属性值(Memcached中需要取出整个字符串反序列化成对象修改完再序列化存回去) | 存储、读取、修改用户属性|
| List(列表) | 链表(双向链表) | 增删快,提供了操作某一段元素的API | 1,最新消息排行等功能(比如朋友圈的时间线) 2,消息队列 |
| Set(集合) | 哈希表实现,元素不重复 | 1、添加、删除,查找的复杂度都是O(1) 2、为集合提供了求交集、并集、差集等操作 | 1、共同好友 2、利用唯一性,统计访问网站的所有独立ip 3、好友推荐时,根据tag求交集,大于某个阈值就可以推荐 |
| Sorted Set(有序集合) | 将Set中的元素增加一个权重参数score,元素按score有序排列 | 数据插入集合时,已经进行天然排序 | 1、排行榜 2、带权重的消息队列 |

## string
- string是redis最基本的类型,一个 key 对应一个 value
- 最大能存储512MB数据
- string类型是二进制安全的，即可以为任何数据，比如数字、图片、序列化对象等
###命令
#### 设置
- 设置键值```set key value```
- 设置键值及过期时间,以秒为单位```SETEX key seconds value```
- 设置键值及过期时间,以毫秒为单位```PSETEX key milliseconds value```
- 设置多个键值```MSET key value [key value ...]```
- 只有在 key 不存在时设置 key 的值。```SETNX key value```
- 同时设置一个或多个 key-value 对，当且仅当所有给定 key 都不存在。```MSETNX key value [key value ...]```
- 用 value 参数覆写给定 key 所储存的字符串值，从偏移量 offset 开始。```SETRANGE key offset value```

#### 获取
- 根据键获取值，如果不存在此键则返回nil```GET key```
- 根据多个键获取多个值```MGET key1 [key2 ...]```
- 返回 key 中字符串值的子字符```GETRANGE key start end```
- 将给定 key 的值设为 value ，并返回 key 的旧值(old value)。```GETSET key value```

#### 运算(要求:值是数字)
- 将key对应的value加1INCR key
- 将key对应的value加整数INCRBY key increment
- 将key对应的value减1DECR key
- 将key对应的value减整数DECRBY key decrement

#### 其它
- 追加值APPEND key value
- 获取值长度STRLEN key

## hash
- Redis hash 是一个string类型的field和value的映射表，hash特别适合用于存储对象。
- Redis 中每个 hash 可以存储 232 - 1 键值对（40多亿）。
### 命令
###设置
- 设置单个属性```HSET key field value```
- 设置多个属性```HMSET key field1 value [field2 value ...]```
- 只有在字段 field 不存在时，设置哈希表字段的值。```HSETNX key field value```

### 获取
- 获取一个属性的值```HGET key field```
- 获取多个属性的值```HMGET key field1 [field2 ...]```
- 获取所有属性和值```HGETALL key```
- 获取所有的属性```HKEYS key```
- 返回包含属性的个数```HLEN key```
- 获取所有值```HVALS key```

### 其它
- 判断属性是否存在```HEXISTS key field```
- 删除属性及值```HDEL key field [field ...]```
- 返回值的字符串长度```HSTRLEN key field``` ERR unknown command ‘HSTRLEN’
- 查看哈希表 key 中，指定的字段是否存在```HEXISTS key field```
- 为哈希表 key 中的指定字段的整数值加上增量 increment ```HINCRBY key field increment```
- 为哈希表 key 中的指定字段的浮点数值加上增量 increment ```HINCRBYFLOAT key field increment```
- 迭代哈希表中的键值对```HSCAN key cursor [MATCH pattern] [COUNT count]```

## list
- 列表是简单的string列表，按照插入顺序排序
- 可以在列表的头部或者尾部添加元素
### 命令
### 设置
- 在头部插入一个或多个数据```LPUSH key value1 [value2 ...]```
- 将一个值插入到已存在的列表头部```LPUSHX key value```
- 在尾部插入一个或多个数据```RPUSH key value1 [value2 ...]```
- 为已存在的列表添加值```RPUSHX key value```
- 在列表的元素前或后插入新元素```LINSERT key BEFORE|AFTER pivot value```
- 通过索引设置列表元素的值```LSET key index value```(索引是基于0的下标,索引可以是负数，表示偏移量是从list尾部开始计数，如-1表示列表的最后一个元素)

### 获取
- 移出并获取列表的第一个元素```LPOP key```
- 移出并返回列表最后一个元素```RPOP key```
- 移除列表元素```LREM key count value```(count > 0 : 从表头开始向表尾搜索，移除与 VALUE 相等的元素，数量为 COUNT 。count < 0 : 从表尾开始向表头搜索，移除与 VALUE 相等的元素，数量为 COUNT 的绝对值。count = 0 : 移除表中所有与 VALUE 相等的值。)
- 获取列表指定范围内的元素```LRANGE key start stop```
(start和stop偏移量都是基于0的下标,偏移量也可以是负数,表示偏移量是从list尾部开始计数,如-1表示列表的最后一个元素)
- 移出并获取列表的第一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。```BLPOP key1 [key2 ] timeout```
- 移出并获取列表的最后一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。```BRPOP key1 [key2 ] timeout```
- 从列表中弹出一个值，将弹出的元素插入到另外一个列表中并返回它； 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。BRPOPLPUSH source destination timeout
- 移除列表的最后一个元素，并将该元素添加到另一个列表并返回```RPOPLPUSH source destination```

### 其它
- 对一个列表进行修剪(trim),让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除```LTRIM key start stop```
(start 和 stop偏移量都是基于0的下标,偏移量也可以是负数，表示偏移量是从list尾部开始计数,如-1表示列表的最后一个元素)
- 获取列表长度```LLEN key```
- 通过索引获取列表中的元素```LINDEX key index```

## set
- Set 是 String 类型的无序集合。集合成员是唯一的，不能出现重复的数据。
- 集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是 O(1)。
### 命令
### 设置
- 添加元素```SADD key member [member ...]```

### 获取
- 返回key集合所有的元素SMEMBERS key
- 返回集合元素个数SCARD key

### 其它
- 求多个集合的交集```SINTER key [key ...]```
- 返回给定所有集合的交集并存储在集合destination 中```SINTERSTORE destination key1 [key2]```
- 求某集合与其它集合的差集```SDIFF key [key ...]```
- 返回给定所有集合的差集并存储在 集合destination 中```SDIFFSTORE destination key1 [key2]```
- 将 member 元素从 source 集合移动到 destination 集合```SMOVE source destination member```
- 求多个集合的合集```SUNION key [key ...]```
- 判断元素是否在集合中```SISMEMBER key member```
- 移除并返回集合中的一个随机元素```SPOP key```
- 返回集合中一个或多个随机数```SRANDMEMBER key [count]```
- 移除集合中一个或多个成员```SREM key member1 [member2]```
- 所有给定集合的并集存储在 destination 集合中```SUNIONSTORE destination key1 [key2]```
- 迭代集合中的元素```SSCAN key cursor [MATCH pattern] [COUNT count]```

## zset
- 有序集合和集合一样也是string类型元素的集合,且不允许重复的成员。
- 每个元素都会关联一个double类型的score，表示权重，通过权重将元素从小到大排序，元素的score可以相同
### 命令
### 设置
- 添加```ZADD key score member [score member ...]```

### 获取
- 返回指定范围内的元素```ZRANGE key start stop```
- 返回元素个数```ZCARD key```
- 返回有序集key中，score值在min和max之间的成员```ZCOUNT key min max```
- 返回有序集key中，成员member的score值```ZSCORE key member```

...

```ZINCRBY key increment member```
有序集合中对指定成员的分数加上增量 increment
```ZINTERSTORE destination numkeys key [key ...]```
计算给定的一个或多个有序集的交集并将结果集存储在新的有序集合 key 中
```ZLEXCOUNT key min max```
在有序集合中计算指定字典区间内成员数量
```ZRANGEBYLEX key min max [LIMIT offset count]```
通过字典区间返回有序集合的成员
```ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT]```
通过分数返回有序集合指定区间内的成员
```ZRANK key member```
返回有序集合中指定成员的索引
```ZREM key member [member ...]```
移除有序集合中的一个或多个成员
```ZREMRANGEBYLEX key min max```
移除有序集合中给定的字典区间的所有成员
```ZREMRANGEBYRANK key start stop```
移除有序集合中给定的排名区间的所有成员
```ZREMRANGEBYSCORE key min max```
移除有序集合中给定的分数区间的所有成员
```ZREVRANGE key start stop [WITHSCORES]```
返回有序集中指定区间内的成员，通过索引，分数从高到底
```ZREVRANGEBYSCORE key max min [WITHSCORES]```
返回有序集中指定分数区间内的成员，分数从高到低排序
```ZREVRANK key member```
返回有序集合中指定成员的排名，有序集成员按分数值递减(从大到小)排序
```ZUNIONSTORE destination numkeys key [key ...]```
计算给定的一个或多个有序集的并集，并存储在新的 key 中
```ZSCAN key cursor [MATCH pattern] [COUNT count]```
迭代有序集合中的元素（包括元素成员和元素分值）


# 发布订阅
- 发布者不是计划发送消息给特定的接收者（订阅者），而是发布的消息分到不同的频道，不需要知道什么样的订阅者订阅
- 订阅者对一个或多个频道感兴趣，只需接收感兴趣的消息，不需要知道什么样的发布者发布的
发布者和订阅者的解耦合可以带来更大的扩展性和更加动态的网络拓扑
- 客户端发到频道的消息，将会被推送到所有订阅此频道的客户端
- 客户端不需要主动去获取消息，只需要订阅频道，这个频道的内容就会被推送过来

## 消息的格式
- 推送消息的格式包含三部分
- 第一部分:消息类型，包含三种类型
    - subscribe，表示订阅成功
    - unsubscribe，表示取消订阅成功
    - message，表示其它终端发布消息
- 如果第一部分的值为subscribe，则第二部分是频道，第三部分是现在订阅的频道的数量
- 如果第一部分的值为unsubscribe，则第二部分是频道，第三部分是现在订阅的频道的数量，如果为0则表示当前没有订阅任何频道，当在Pub/Sub以外状态，客户端可以发出任何redis命令
- 如果第一部分的值为message，则第二部分是来源频道的名称，第三部分是消息的内容

## 命令
- 订阅SUBSCRIBE 频道名称 [频道名称 ...]
- 取消订阅,如果不写参数，表示取消所有订阅UNSUBSCRIBE 频道名称 [频道名称 ...]
- 将信息发送到指定的频道。PUBLISH 频道 消息

# 主从配置
- 一个master可以拥有多个slave，一个slave又可以拥有多个slave，如此下去，形成了强大的多级服务器集群架构
- 比如，将ip为192.168.1.10的机器作为主服务器，将ip为192.168.1.11的机器作为从服务器

## 设置主服务器的配置
```sudo vi /etc/redis/redis.conf```修改绑定ip
```bind 192.168.1.10``` 重启redis服务器

## 设置从服务器的配置
```sudo vi /etc/redis/redis.conf```注意：在slaveof后面写主机ip，再写端口，而且端口必须写
```bind 192.168.1.11```
```slaveof 192.168.1.10 6379```
重启redis服务器

启动客户端redis-cli -h修改后的ip
在master和slave分别执行info命令，查看输出信息
在master上写数据
set hello world
在slave上读数据
get hello

# 卸载redis
```sudo apt-get remove redis-server```
```sudo apt-get autoremove --purge redis-server```
