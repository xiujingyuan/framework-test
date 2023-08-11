# -*- coding: utf-8 -*-
# @Time    : 公元18-11-27 上午9:09
# @Author  : 张廷利
# @Site    : 
# @File    : ConnUtils.py
# @Software: IntelliJ IDEA



import pymysql as MySQLdb
from common.tools.CommUtils import CommUtils
from DBUtils.PooledDB import PooledDB

'''
    语句块初始化数据库连接，会将配置文件中所有的数据库配置读取出来初始化。
    默认每个配置初始化5个连接
'''
pools = {}


def __init_config__(dbserver=None):
    try:
        configs = []
        DataBaseUtils = CommUtils()
        if dbserver != None:
            configs = DataBaseUtils.get_special_database(dbserver)
        else:
            configs = DataBaseUtils.get_database_config()
        if configs != None:
            for config in configs:
                host = config["config"]["host"]
                user = config["config"]["username"]
                password = config["config"]["password"]
                database = config["config"]["database"]
                port = config["config"]["port"]
                pool = PooledDB(MySQLdb, 5, host=host,
                                user=user,
                                passwd=password,
                                db=database,
                                port=port)
                pools[config['dbserver']] = pool

    except Exception as e:

        raise Exception("数据库初始化失败，请检查配置或者网络环境！host={},user={},password={},database={},port ={}".format(host,user,password,database,port) )


def get_connection(dbserver):
    ''' 返回一个数据库连接'''

    if (dbserver in pools) == False:
        __init_config__(dbserver)
        return pools[dbserver].connection()
    else:
        return pools[dbserver].connection()
