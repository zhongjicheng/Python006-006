# !/usr/bin/python3
import abc
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Float, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import desc, asc
from dbconfig import read_db_config

# 打开数据库连接
# mysql> create database testdb;
# mysql> update user set host='%' where user='testuser';
# mysql> GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'%' IDENTIFIED BY 'testpass';
Base = declarative_base()


def parse_config():
    """
    解析 database 配置，并返回配置信息
    :return:
    """
    config = read_db_config()
    sql = config.get('sql')
    eng = config.get('engine')
    user = config.get('user')
    password = config.get('password')
    host = config.get('host')
    port = config.get('port')
    database = config.get('database')
    charset = config.get('charset')

    return sql, eng, user, password, host, port, database, charset


class DatabaseEngine:
    def __init__(self):
        self.engine = self.create_db_engine()
        self.session = self.create_session(self.engine)

    def create_all_engine(self):
        """
        创建表格
        """
        try:
            Base.metadata.create_all(self.engine)
        except Exception as e:
            print(f"create table error:{e}")
            assert False

    def create_db_engine(self):
        """
        创建数据库引擎
        :return:
        """
        # 创建数据库引擎
        sql, eng, user, password, host, port, database, charset = parse_config()
        # dburl = "mysql+pymysql://testuser:testpass@server1:3306/testdb?charset=utf8mb4"
        dburl = f"{sql}+{eng}://{user}:{password}@{host}:{port}/{database}?charset={charset}"
        engine = create_engine(dburl, echo=True, encoding="utf-8")

        return engine

    def create_session(self, engine):
        """
        创建 session
        :return:
        """
        SessionClass = sessionmaker(bind=engine)
        session = SessionClass()
        return session

    @abc.abstractmethod
    def insert(self, user_dict):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def delete(self):
        pass

    @abc.abstractmethod
    def query_all(self):
        pass

    @abc.abstractmethod
    def commit(self):
        pass


class UserTable(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), index=True)
    age = Column(Integer())
    birthday = Column(String(50))
    gender = Column(String(10))
    education = Column(String(100))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "user(id='{self.id}', name={self.name}, age={self.age}, birthday={self.birthday}," \
               "gender={self.gender}, education={self.education}, created_on={self.created_on}," \
               "updated_on={self.updated_on})".format(self=self)


class TableBase(DatabaseEngine):
    def __init__(self, tb):
        super().__init__()
        self.table = tb

    def insert(self, **kwargs):
        """
        插入数据到表中
        :return:
        """
        user = self.table(**kwargs)
        self.session.add(user)

    def update(self):
        """
        更新表中的字段
        :return:
        """
        pass

    def query_all(self):
        """
        查询表中所有的数据
        :return:
        """
        for data in self.session.query(self.table).all():
            print(data)

    def query_by_column(self, *query_args, order="asc"):
        """
        按列查询
        :param query_args: 查询关键字
        :param order: （asc:升序；desc:降序）
        :return:
        """
        if order == "asc":
            for data in self.session.query(*query_args).order_by(asc(self.table.id)):
                print(data)
        else:
            for data in self.session.query(*query_args).order_by(desc(self.table.id)):
                print(data)

    def query_by_filter(self, column, condition, condition_value, *query_args):
        """
        按过滤条件查询
        TODO filter 部分未完成
        :param column:列名
        :param condition: 条件（>,<,=）
        :param condition_value: 参考值
        :param query_args: 查询关键字
        :return:
        """
        # cnd = f"id > 2"
        cnd = f"{column} {condition} {condition_value}"
        for data in self.session.query(*query_args).filter(cnd):
            print(data)

    def delete(self):
        """
        删除表中的数据
        :return:
        """
        pass

    def commit(self):
        """
        提交数据
        :return:
        """
        self.session.commit()


if __name__ == "__main__":
    # 初始化userTable
    table = TableBase(UserTable)
    table.create_all_engine()

    # 读取所有user信息
    with open('user_data.json', 'r') as f:
        all_user_data = json.load(f)

    # 把所有的user信息添加到user表中
    for value in all_user_data.values():
        print(value)
        table.insert(**value)
        table.commit()

    # 查询表的所有信息
    table.query_all()

    # 按列查询表的信息
    args = (table.table.name, table.table.age)
    table.query_by_column(*args)

    # 按条件查询
    # TODO 未完成
    # args = (table.table.name, table.table.age)
    # table.query_by_filter(table.table.age, ">", 25, *args)
