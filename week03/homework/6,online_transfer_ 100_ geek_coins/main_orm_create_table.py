# !/usr/bin/python3

"""
作业要求：
张三给李四通过网银转账 100 极客币，现有数据库中三张表：

一张为用户表，包含用户 ID 和用户名字，另一张为用户资产表，包含用户 ID 用户总资产，
第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。

请合理设计三张表的字段类型和表结构；
请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。

待优化点：
1，表的操作需要完善，并增加异常处理
2，创建表前未检查表是否存在，2次创建会报异常（因表使用了primary_key）

"""
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


class UserTable(Base):
    """
    用户表，包含用户 ID 和用户名字
    """
    __tablename__ = 'userTable'
    u_id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)

    def __repr__(self):
        return "userTable(u_id='{self.u_id}', name={self.name}".format(self=self)


class UserAssetTable(Base):
    """
    用户资产表，包含用户 ID 用户总资产
    """
    __tablename__ = 'UserAssetTable'
    u_id = Column(Integer(), primary_key=True, unique=True)
    total_assets = Column(Integer())

    def __repr__(self):
        return "UserAssetTable(u_id='{self.u_id}', total_assets={self.total_assets}".format(self=self)


class AuditTable(Base):
    """
    审计用表，记录了转账时间，转账 id，被转账 id，转账金额
    """
    __tablename__ = 'AuditTable'
    transfer_id = Column(Integer(), primary_key=True, unique=True)
    transferred_id = Column(Integer(), primary_key=True, unique=True)
    transfer_amount = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now)

    def __repr__(self):
        return "AuditTable(transfer_id='{self.transfer_id}', transferred_id={self.transferred_id}," \
               "transfer_amount={self.transfer_amount}, created_on={self.created_on}".format(self=self)


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

    def update(self, filter_column, condition_value, update_column, update_value):
        """
        更新表中的字段
        :return:
        """
        query = self.session.query(self.table)
        query = query.filter(filter_column == condition_value)
        query.update({update_column: update_value})
        print(query.first())
        self.query_all()

    def query_all(self):
        """
        查询表中所有的数据
        :return:
        """
        for data in self.session.query(self.table).all():
            print(data)

    def query_by_condition(self, condition_column, condition_value, *query_args):
        """
        按条件查询
        :param condition_column: 表的列名
        :param condition_value: 查询值
        :param query_args: 查询参数
        :return:
        """
        return self.session.query(*query_args).filter(condition_column == condition_value).first()

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


class Business:
    def __init__(self):
        # 初始化所有userTable
        self.user_table = TableBase(UserTable)
        # 初始化user asset table
        self.asset_table = TableBase(UserAssetTable)
        # 初始化 audit table
        self.audit_table = TableBase(AuditTable)

    def __del__(self):
        # Base.metadata.drop_all(tables=UserTable)
        # Base.metadata.drop_all(tables=UserAssetTable)
        # Base.metadata.drop_all(tables=AuditTable)
        pass

    def create_all_table(self):
        """
        生成所有table
        :return:
        """
        self.user_table.create_all_engine()

    def init_table_data(self):
        """
        初始化表格的数据
        :return:
        """
        self.init_data_from_json(self.user_table, 'user_data.json')
        self.init_data_from_json(self.asset_table, 'user_asset.json')

    def init_data_from_json(self, table, file):
        """
        读取json信息并插入表格
        :return:
        """
        # 读取所有user信息
        with open(file, 'r') as f:
            data_json = json.load(f)

        # 把所有的user信息添加到user表中
        for value in data_json.values():
            print(value)
            table.insert(**value)
            table.commit()

        # 查询表的所有信息
        table.query_all()

    def update_asset(self, table_column, condition_value, update_column, update_value):
        """
        更新 table
        :return:
        """
        self.asset_table.query_all()
        self.asset_table.update(table_column, condition_value, update_column, update_value)

    def query_asset_by_uid(self, query_uid):
        """
        按 u_id 查询资产
        :param query_uid:
        :return:
        """
        try:
            asset = self.asset_table.query_by_condition(UserAssetTable.u_id, query_uid, *(UserAssetTable.total_assets,))
            print(f'asset: {asset}')
        except Exception as e:
            print(f"Query failed by id{query_uid}, error info:{e}")
            return ""
        return asset[0]

    def bussiness_deal(self, a_uid1, b_uid2):
        """
        用户 A 向用户 B 转账 100 极客币
        :param a_uid1: 
        :param b_uid2: 
        :return: 
        """""
        if not isinstance(a_uid1, int) and a_uid1 > 3:
            return False
        if not isinstance(b_uid2, int) and b_uid2 > 3:
            return False
        # 查询用户资产
        a_uid1_asset = self.query_asset_by_uid(a_uid1)
        b_uid2_asset = self.query_asset_by_uid(b_uid2)
        if not b_uid2_asset or not a_uid1_asset:
            return False
        # 查询用户A的资产是否达到 100 极客币
        if a_uid1_asset < 100:
            return False
        # 交易
        a_uid1_asset -= 100
        b_uid2_asset += 100
        audit_info = {"transfer_id": a_uid1, "transferred_id": b_uid2, "transfer_amount": 100}
        try:
            # 用户A 向用户 B 转 100 极客币
            self.update_asset(UserAssetTable.u_id, a_uid1, UserAssetTable.total_assets, a_uid1_asset)
            self.update_asset(UserAssetTable.u_id, b_uid2, UserAssetTable.total_assets, b_uid2_asset)
            self.asset_table.session.commit()
            # 记录交易信息
            self.audit_table.insert(**audit_info)
            self.audit_table.session.commit()
        except Exception as e:
            # 回退到交易前的状态
            print(f"Something wrong with update table, error info:{e}")
            self.asset_table.session.rollback()
            self.audit_table.session.rollback()
        finally:
            self.asset_table.session.close()
            self.audit_table.session.close()


if __name__ == "__main__":
    buss = Business()
    buss.create_all_table()
    buss.init_table_data()
    buss.bussiness_deal(2, 3)
