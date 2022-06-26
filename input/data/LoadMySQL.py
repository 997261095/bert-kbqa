# -*- coding: utf-8 -*-

import pymysql
import pandas as pd
from sqlalchemy import create_engine

# 创建数据库, 默认使用 root 用户
def create_db():

    #创建连接，若账号密码不同请记得修改；
    connect = pymysql.connect(
        user="root",
        password="123456",
        host="127.0.0.1",
        port=3306,
        db="KB_QA",
        charset="utf8"
    )
    #创建操作游标
    conn = connect.cursor()

    # 如果 KB_QA 数据库存在则删除
    conn.execute("drop database if exists KB_QA")
    # 新创建一个数据库
    conn.execute("create database KB_QA")
    # 选择使用 KB_QA 数据库
    conn.execute("use KB_QA")
    conn.execute("SET @@global.sql_mode=''")

    # 如果表存在，则删除
    conn.execute("drop table if exists nlpccQA")
    conn.execute(sql)

    # 创建一个名为 nlpccQA 的表
    sql = """
    create table nlpccQA(entity VARCHAR(50) character set utf8 collate utf8_unicode_ci,
    attribute VARCHAR(50) character set utf8 collate utf8_unicode_ci, answer VARCHAR(255) character set utf8 
    collate utf8_unicode_ci)
    """

    #关闭游标
    conn.close()
    #关闭与数据库的连接
    connect.close()


def loaddata():
    #使用 pymysql，与数据库进行连接，同样，注意用户名和密码的设置。
    db_info = {'user': 'root',
               'password': 'root',
               'host': '127.0.0.1',
               'port': 3306,
               'database': 'KB_QA'
               }

    # 导入模块中的 create_engine, 需要利用它来进行连接数据库
    engine = create_engine(
        'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8' % db_info, encoding='utf-8')
    # ("mysql+pymysql://【此处填用户名】:【此处填密码】@【此处填host】:【此处填port】/【此处填数据库的名称】?charset=utf8")
    # 直接使用这种形式也可以engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
    # 填写链接信息

    # 读取本地CSV文件
    df = pd.read_csv("./DB_Data/clean_triple.csv", sep=',', encoding='utf-8')

    # 将新建的 DataFrame 储存到 MySQL 中的数据表, 不储存 index 列 (index=False)
    # if_exists 参数:
    #  - fail:      如果表存在，啥也不做
    #  - replace:   如果表存在，删了表，再建立一个新表，把数据插入
    #  - append:    如果表存在，把数据插入，如果表不存在创建一个表！！
    pd.io.sql.to_sql(df, 'nlpccQA', con=engine, index=False, if_exists='append', chunksize=10000)
    # df.to_sql('example', con=engine,  if_exists='replace')这种形式也可以
    print("Write to MySQL successfully!")


def upload_data(sql):
    #连接数据库服务器
    connect = pymysql.connect(
        user="root",
        password="root",
        host="127.0.0.1",
        port=3306,
        db="kb_qa",
        charset="utf8"
    )
    # 创建操作游标
    cursor = connect.cursor()
    results = None
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except Exception as e:
        print("Error: unable to fecth data: %s ,%s" % (repr(e), sql))
    finally:
        # 关闭数据库连接
        cursor.close()
        connect.close()
    return results


def insert_data(entity, attributes, answer):
    connect = pymysql.connect(
        user="root",
        password="123456",
        host="127.0.0.1",
        port=3306,
        db="kb_qa",
        charset="utf8"
    )

    # 创建操作游标
    cursor = connect.cursor()
    sql = "INSERT INTO nlpccQA(entity, attribute, answer) VALUES (%s, %s, %s)"
    cursor.execute(sql, (entity, attributes, answer))
    connect.commit()
    cursor.close()
    connect.close()


if __name__ == '__main__':
    # create_db()
    # loaddata()
    sql = "select * from nlpccqa where entity = '高等数学'"

    ret = upload_data(sql)
    print(list(ret))
