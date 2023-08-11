# -*- coding: utf-8 -*-
# @Time    : 公元18-11-26 下午5:10
# @Author  : 张廷利
# @Site    : 
# @File    : SqlTools.py
# @Software: IntelliJ IDEA

import pymysql as MySQLdb
import traceback, datetime, decimal, json
import initial.connection.ConnUtils as Connection
from pprint import pprint


class SqlTools(object):

    def __init__(self):
        pass

    @classmethod
    def queryone(cls, dbserver, sql, params=None):
        '''
        查询单条记录
        :param dbserver: database.config 文件中配置的dbserver ，string
        :param sql: 需要查询的sql 语句 ，string
        :param params: 查询sql 语句中的参数，list
        :return:
        '''
        cursor = None
        connection = None
        try:
            connection = Connection.get_connection(dbserver)
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            result = ()
            if params == None:
                rs = cursor.execute(sql)
                result = cursor.fetchone()
            else:
                rs = cursor.execute(sql, params)
                result = cursor.fetchone()
            log_info = {"sql_info": str(sql),
                        "sql_return_info": str(rs),
                        "commit_info": str(result),
                        "name": "queryone"}
            #pprint(log_info)
            return cls.SerializerDict(result)
        except Exception as e:
            print("数据库执行异常" + str(e))
            traceback.print_exc()
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def queryoneBySqlEntity(cls, sqlentity, dbserver=None):
        '''
        查询单条记录，传入的参数为sqlentity
        :param sqlentity.dbserver: database.config 文件中配置的dbserver ，string
        :param sqlentity.sql: 需要查询的sql 语句 ，string
        :param sqlentity.params: 查询sql 语句中的参数，list
        :return:
        '''
        cursor = None
        connection = None
        try:
            if dbserver is None:
                connection = Connection.get_connection(sqlentity['database'])
            else:
                connection = Connection.get_connection(dbserver)
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            result = ()
            if sqlentity['params'] == None:
                rs = cursor.execute(sqlentity['sql'])
                result = cursor.fetchone()
            else:
                rs = cursor.execute(sqlentity['sql'], sqlentity['params'])
                result = cursor.fetchone()
            log_info = {"sql_info": str(sqlentity),
                        "sql_return_info": str(rs),
                        "commit_info": str(result),
                        "name": "queryoneBySqlEntity"}
            #pprint(log_info)
            return cls.SerializerDict(result)
        except Exception as e:
            print("数据库执行异常" + str(e))
            traceback.print_exc()
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def queryall(cls, dbserver, sql, params):
        '''
        查询多条记录
        :param dbserver: database.config 文件中配置的dbserver ，string
        :param sql: 需要查询的sql 语句 ，string
        :param params: 查询sql 语句中的参数，list
        :return:
        '''
        cursor = None
        connection = None
        try:
            connection = Connection.get_connection(dbserver)
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            result = ()
            if params == None:
                rs = cursor.execute(sql)
                result = cursor.fetchall()
            else:
                rs = cursor.execute(sql, params)
                result = cursor.fetchall()
            log_info = {"sql_info": str(sql),
                        "sql_return_info": str(rs),
                        "commit_info": str(result),
                        "name": "queryall"}
            #pprint(log_info)
            return cls.SerializerDict(result)
        except Exception as e:
            print("数据库执行异常" + str(e))
            traceback.print_exc()
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def queryallBySqlEntity(cls, sqlentity, dbserver=None):
        '''
        查询多条记录，传入的参数为sqlentity
        :param sqlentity.dbserver: database.config 文件中配置的dbserver ，string
        :param sqlentity.sql: 需要查询的sql 语句 ，string
        :param sqlentity.params: 查询sql 语句中的参数，list
        :return:
        '''
        connection = None
        if dbserver is None:
            connection = Connection.get_connection(sqlentity['database'])
        else:
            connection = Connection.get_connection(dbserver)
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        result = ()
        try:
            if sqlentity['params'] == None:
                rs = cursor.execute(sqlentity['sql'])
                result = cursor.fetchall()
            else:
                rs = cursor.execute(sqlentity['sql'], sqlentity['params'])
                result = cursor.fetchall()
            commit_info = connection.commit()
            log_info = {"sql_info": str(sqlentity),
                        "sql_return_info": str(rs),
                        "commit_info": str(commit_info),
                        "fetchall_info": str(result),
                        "name": "queryallBySqlEntity"}
            #pprint(log_info)
            return cls.SerializerDict(result)
        except Exception as e:
            print("数据库执行异常" + str(e))
            traceback.print_exc()
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def updateandinsert(cls, dbserver, sql, params):
        '''
           更新或者插入语句
           :param dbserver: database.config 文件中配置的dbserver ，string
           :param sql: 需要查询的sql 语句 ，string
           :param params: 查询sql 语句中的参数，list
           :return:
           '''
        cursor = None
        connection = None
        result = None
        try:
            connection = Connection.get_connection(dbserver)
            cursor = connection.cursor()
            if params is None:
                result = cursor.execute(sql)
            else:
                result = cursor.execute(sql, params)
            commit_info = connection.commit()
            log_info = {"sql_info": str(sql),
                        "sql_return_info": str(result),
                        "commit_info": str(commit_info),
                        "name": "updateandinsert"}
            #pprint(log_info)
            return cls.SerializerDict(result)
        except Exception as e:
            print("数据库执行异常" + str(e))
            traceback.print_exc()
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def uaiBySqlEntity(cls, sqlentity, dbserver=None):
        '''
           更新或者插入语句，传入的参数为sqlentity
           :param sqlentity.dbserver: database.config 文件中配置的dbserver ，string
           :param sqlentity.sql: 需要查询的sql 语句 ，string
           :param sqlentity.params: 查询sql 语句中的参数，list
           :return:
           '''
        cursor = None
        connection = None
        try:
            if dbserver is None:
                connection = Connection.get_connection(sqlentity['database'])
            else:
                connection = Connection.get_connection(dbserver)
            cursor = connection.cursor()
            rs = cursor.execute(sqlentity['sql'], sqlentity['params'])
            commit_info = connection.commit()
            log_info = {"sql_info": str(sqlentity),
                        "sql_return_info": str(rs),
                        "commit_info": str(commit_info),
                        "name": "uaiBySqlEntity"}
            #pprint(log_info)
            return cls.SerializerDict(rs)
        except Exception as e:
            print("数据库执行异常" + str(e))
            traceback.print_exc()
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def SerializerDict(cls, result):
        if isinstance(result, (list, tuple)):
            for r in result:
                for key, value in r.items():
                    if isinstance(value, datetime.datetime):
                        r[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                    elif isinstance(value, decimal.Decimal):
                        temp = str(value)
                        tem_value = temp.split(".")
                        if (len(tem_value) > 1 and int(tem_value[1]) == 0):
                            r[key] = tem_value[0]
                        else:
                            r[key] = temp
        elif isinstance(result, dict):
            for key, value in result.items():
                if isinstance(value, datetime.datetime):
                    result[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(value, decimal.Decimal):
                    temp = str(value)
                    tem_value = temp.split(".")
                    if (len(tem_value) > 1 and int(tem_value[1]) == 0):
                        result[key] = tem_value[0]
                    else:
                        result[key] = temp

        return result
