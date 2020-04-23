# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 20:47
# @Author  : Alan
# @Email   : xiezhengwen2013@163.com
# @File    : load_dbdata.py
# @Software: PyCharm


import pymysql
import pandas as pd
from sqlalchemy import create_engine


def create_db():
    connect = pymysql.connect(  # 连接数据库服务器-*-*-
        user="root",
        password="123456",
        host="127.0.0.1",
        port=3306,
        charset="utf8"
    )
    conn = connect.cursor()  # 创建操作游标
    # 你需要一个游标 来实现对数据库的操作相当于一条线索

    #                          创建表
    conn.execute("drop database if exists KB_QA")  # 如果new_database数据库存在则删除
    conn.execute("create database KB_QA")  # 新创建一个数据库
    conn.execute("use KB_QA")  # 选择new_database这个数据库
    conn.execute("SET @@global.sql_mode=''")

    # sql 中的内容为创建一个名为 new_table 的表
    sql = """create table nlpccQA(entity VARCHAR(50) character set utf8 collate utf8_unicode_ci,
    attribute VARCHAR(50) character set utf8 collate utf8_unicode_ci, answer VARCHAR(255) character set utf8 
    collate utf8_unicode_ci)"""  # ()中的参数可以自行设置
    conn.execute("drop table if exists nlpccQA")  # 如果表存在则删除
    conn.execute(sql)  # 创建表

    #                           删除
    # conn.execute("drop table new_table")

    conn.close()  # 关闭游标连接
    connect.close()  # 关闭数据库服务器连接 释放内存


def loaddata():
    # 初始化数据库连接，使用pymysql模块
    db_info = {'user': 'root',
               'password': '123456',
               'host': '127.0.0.1',
               'port': 3306,
               'database': 'KB_QA'
               }

    engine = create_engine( # 导入模块中的create_engine，需要利用它来进行连接数据库
        'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8' % db_info, encoding='utf-8')
    # ("mysql+pymysql://【此处填用户名】:【此处填密码】@【此处填host】:【此处填port】/【此处填数据库的名称】?charset=utf8")
    # 直接使用这种形式也可以engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
    # 填写链接信息

    # 读取本地CSV文件
    df = pd.read_csv("./DB_Data/clean_triple.csv", sep=',', encoding='utf-8')
    print(df)
    # 将新建的DataFrame储存为MySQL中的数据表，不储存index列(index=False)
    # if_exists:
    # 1.fail:如果表存在，啥也不做
    # 2.replace:如果表存在，删了表，再建立一个新表，把数据插入
    # 3.append:如果表存在，把数据插入，如果表不存在创建一个表！！
    pd.io.sql.to_sql(df, 'nlpccQA', con=engine, index=False, if_exists='append', chunksize=10000)
    # df.to_sql('example', con=engine,  if_exists='replace')这种形式也可以
    print("Write to MySQL successfully!")


def upload_data(sql):
    connect = pymysql.connect(  # 连接数据库服务器
        user="root",
        password="123456",
        host="127.0.0.1",
        port=3306,
        db="kb_qa",
        charset="utf8"
    )
    cursor = connect.cursor()  # 创建操作游标
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


if __name__ == '__main__':
    # create_db()
    # loaddata()
    sql = "select * from nlpccqa where entity = '高等数学'"

    ret = upload_data(sql)
    print(list(ret))
    #