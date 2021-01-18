# 在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。
```
# 安装MySQL server
sudo apt-get install mysql-server
# 登陆mysql
mysql -u -root -p
# 创建数据库
mysql> create database testdb;
# 使用数据库
mysql> use testdb;
```

# 将修改字符集的配置项、验证字符集的 SQL 语句作为作业内容提交
```
mysql> alter database testdb character set utf8mb4;
```

# 将增加远程用户的 SQL 语句作为作业内容提交
```buildoutcfg
# mysql8增加远程用户并赋予权限需要修改host
mysql> update user set host='%' where user='testuser';
# 给指定的数据库（testdb）授予所以的权限，并把这个权限给到 testuser 用户，并通过 % 匹配所有的远程ip地址，密码是 testpass
mysql> GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'%' IDENTIFIED BY 'testpass';
```

# 删除数据库
```
mysql> drop database testdb;
```