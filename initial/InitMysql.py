# -*- coding: utf-8 -*-
# @Time    : 公元19-02-25 下午3:59
# @Author  : 张廷利
# @Site    : 
# @File    : InitMysql.py
# @Software: IntelliJ IDEA


from elixir import *

def init_mysql(ip, port, user, pwd, database):
    try:
        # metadata.bind = "mysql://root:Coh8Beyiusa7@127.0.0.1:3317/zhangtingli"
        metadata.bind = "mysql://{0}:{1}@{2}:{3}/{4}".format(user, pwd, ip, port, database)
        session.bind = metadata.bind
        setup_all(True)
        session.commit()
    except Exception as err:
        raise ValueError("can not connect the database with err is:{0}".format(err))
    else:
        print("init mysql ok!")
