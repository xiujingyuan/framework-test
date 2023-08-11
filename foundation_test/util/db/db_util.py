# -*- coding: utf-8 -*-
import traceback


import decimal

try:
    from DBUtils.PooledDB import PooledDB
except:
    from dbutils.pooled_db import PooledDB

from foundation_test.util.tools.tools import *
import pymysql
import os
from sshtunnel import SSHTunnelForwarder
import socket
from foundation_test.util.log.log_util import logger


def trans_data(result):
    if isinstance(result, (list, tuple)):
        for r in result:
            for key, value in r.items():
                if isinstance(value, datetime):
                    r[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(value, decimal.Decimal):
                    temp = str(value)
                    tem_value = temp.split(".")
                    if len(tem_value) > 1 and int(tem_value[1]) == 0:
                        r[key] = tem_value[0]
                    else:
                        r[key] = temp
    elif isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, decimal.Decimal):
                temp = str(value)
                tem_value = temp.split(".")
                if len(tem_value) > 1 and int(tem_value[1]) == 0:
                    result[key] = tem_value[0]
                else:
                    result[key] = temp
    return result


def get_port():
    port = 0
    for i in range(10):
        ip = '127.0.0.1'
        port = random.randint(20000, 31000)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        s.close()
        if result == 0:
            logger.info("port:%s already been used" % port)
        else:
            logger.info("port:%s already been choiced" % port)
            break
        if i == 9:
            raise Exception("未选到合适的端口")
    return port


class DataBase(object):
    sshrunnel = []
    pools = {}

    def __init__(self, env, environment=os.environ.get('environment')):
        self.env = env
        self.environment = environment
        self.dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                                'resource')

    def connect(self, env):
        if env in DataBase.pools.keys():
            pass
        else:
            if self.environment == "dev":
                # fd = open("./resource/database_dev.config")
                fd = open(os.path.join(self.dir, "database_dev.config"))
            elif self.environment == "test":
                fd = open(os.path.join(self.dir, "database.config"))
            elif self.environment == "prod":
                fd = open(os.path.join(self.dir, "database_prod.config"))
            elif self.environment is None:
                fd = open(os.path.join(self.dir, "database_dev.config"))
            else:
                fd = None

            configs = fd.read()
            fd.close()
            configs = json.loads(configs)
            for config in configs['databases']:
                if config["dbserver"] == env:
                    host = config["config"]["host"]
                    user = config["config"]["username"]
                    password = config["config"]["password"]
                    database = config["config"]["database"]
                    port = config["config"]["port"]
                    if "ssh" in config.keys():
                        port = get_port()
                        server = SSHTunnelForwarder(
                            ssh_address_or_host=(config["ssh"]["sshproxyhost"], 22),
                            ssh_username=config["ssh"]["sshusername"],
                            ssh_pkey=config["ssh"]["sshprivatekey"],
                            remote_bind_address=(config["ssh"]["sshremotehost"], 3306),
                            local_bind_address=('127.0.0.1', port))
                        server.start()

                        pool = PooledDB(pymysql, 5,
                                        host=host,
                                        user=user,
                                        passwd=password,
                                        db=database,
                                        port=port)
                        DataBase.pools[config["dbserver"]] = pool
                        LogUtil.log_info("connect to %s with port %s" % (self.env, port))
                        # Log.log_debug(pprint(inspect.stack()[:5]))
                        DataBase.sshrunnel.append(server)
                    else:
                        pool = PooledDB(pymysql, 5,
                                        host=host,
                                        user=user,
                                        passwd=password,
                                        db=database,
                                        port=port)
                        DataBase.pools[config["dbserver"]] = pool
                        LogUtil.log_info("connect to %s with port %s" % (self.env, port))
                        # Log.log_debug(pprint(inspect.stack()[:5]))
                    break

    def get_connect(self):
        if self.env in DataBase.pools.keys():
            pass
        else:
            self.connect(self.env)
        return DataBase.pools[self.env].connection()

    def do_sql(self, sql):
        start = time.time()
        try:
            connection = self.get_connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
            log_info = {"db": self.env,
                        "sql request": sql,
                        "sql time": round(time.time() - start, 2)
                        # ,"sql response": trans_data(result)
                        }
            # Log.log_debug(log_info)
            logger.info(log_info)
            return trans_data(result)
        except Exception as e:
            logger.info("数据库执行异常，sql：%s" % sql)
            logger.info("数据库执行异常：%s" % str(e))
            traceback.print_exc()

    def query(self, sql):
        return self.do_sql(sql)

    def delete(self, sql):
        return self.do_sql(sql)

    def update(self, sql):
        return self.do_sql(sql)

    def insert(self, sql):
        return self.do_sql(sql)

    @classmethod
    def close_connects(cls):
        for db, pool in DataBase.pools.items():
            pool.connection().close()
            pool.close()
            logger.info("关闭数据库链接：%s" % db)
        DataBase.pools.clear()
        for server in DataBase.sshrunnel:
            logger.info("关闭隧道：%s" % server.local_bind_addresses)
            server.close()
            logger.info("关闭隧道成功")
        DataBase.sshrunnel.clear()


class PyMysql:

    def __init__(self, env, country="CN", **kwargs):
        self.dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                                'resource')
        self.env = env
        self.country = country
        self.kwargs = kwargs
        self.file = None
        self.server = None

        if "environment" in kwargs:
            self.environment = kwargs["environment"]
        else:
            self.environment = get_sysconfig("--environment")

        if self.environment == "dev":
            self.file = os.path.join(self.dir, "database_dev.config")
        elif self.environment == "test":
            self.file = os.path.join(self.dir, "database.config")
        elif self.environment == "prod":
            self.file = os.path.join(self.dir, "database_prod.config")
        with open(self.file) as f:
            content = f.read()
        configs = json.loads(content, strict=False)
        # CN中国、TH泰国、PH菲律宾、MX墨西哥、PK巴基斯坦、IN印度
        if self.country == "CN":
            dbserver_name = "qsq_fox1"
        elif self.country == "TH":
            dbserver_name = "arcticfox-thailand"
        elif self.country == "PH":
            dbserver_name = "arcticfox-philippines"
        elif self.country == "MX":
            dbserver_name = "arcticfox-mexico"
        elif self.country == "PK":
            dbserver_name = "arcticfox-pakistan"
        elif self.country == "IN":
            dbserver_name = "arcticfox-india"
        else:
            raise ValueError("not found the country :{0}".format(self.country))
        for config in configs['databases']:
            if config["dbserver"] == dbserver_name:
                self.host = config["config"]["host"]
                self.user = config["config"]["username"]
                self.password = config["config"]["password"]
                self.database = config["config"]["database"]
                self.port = config["config"]["port"]
                if "ssh" in config.keys():
                    ssh_pkey = os.path.join(self.dir, "dx_ssh_proxy")
                    self.port = get_port()
                    self.server = SSHTunnelForwarder(
                        (config["ssh"]["sshproxyhost"], 22),
                        ssh_username=config["ssh"]["sshusername"],
                        ssh_pkey=ssh_pkey,
                        remote_bind_address=(config["ssh"]["sshremotehost"], 3306),
                        local_bind_address=('127.0.0.1', self.port))
                    self.server.start()
                    self.py_mysql = pymysql.connect(user=self.user,
                                                    host=self.host,
                                                    password=self.password,
                                                    port=int(self.port),
                                                    db=self.database)
                    self.py_mysql.set_charset('utf8')
                    self.cur = self.py_mysql.cursor()
                    self.cur.execute('SET NAMES utf8;')
                    self.cur.execute('SET CHARACTER SET utf8;')
                    self.cur.execute('SET character_set_connection=utf8;')
                else:
                    self.py_mysql = pymysql.connect(user=self.user,
                                                    host=self.host,
                                                    password=self.password,
                                                    port=int(self.port),
                                                    db=self.database)
                    self.py_mysql.set_charset('utf8')
                    self.cur = self.py_mysql.cursor()
                    self.cur.execute('SET NAMES utf8;')
                    self.cur.execute('SET CHARACTER SET utf8;')
                    self.cur.execute('SET character_set_connection=utf8;')

                # Log.log_debug("conect to %s with port %s by PyMysql" % (env, self.port))
                # Log.log_debug(pprint(inspect.stack()[:5]))
                break

    def execute_mysql(self, sql, param=None):
        """
            执行增删改类的sql, 如果插入多条数据可以填写param参数为list中存放元祖参数
            eg: excute_sql("insert into user(name,password) values('%s','%s')",[('aaa','aaa'),('bbb','bbb')])
        :param sql:
        :param param:
        :return:
        """
        try:
            if param:
                rows_count = self.cur.executemany(sql, param)
            else:
                rows_count = self.cur.execute(sql)
            self.py_mysql.commit()
            return rows_count
        except Exception as e:
            self.py_mysql.rollback()
            raise Exception("fail to execute sql:{}".format(e))

    def query_mysql(self, sql):
        try:
            self.cur.execute(sql)
            rows = self.cur.fetchall()
            if rows:
                return list(rows)
            else:
                return []
        except Exception as e:
            raise Exception("query sql exception：{}".format(e))

    def fetchone(self, sql):
        try:
            self.cur.execute(sql)
            rows = self.cur.fetchone()
            if rows:
                return list(rows)
            else:
                return []
        except Exception as e:
            raise Exception("query sql exception：{}".format(e))

    def commit_mysql(self):
        self.py_mysql.commit()

    def close_conn(self):
        try:
            if self.cur:
                self.cur.close()
            if self.py_mysql:
                logger.info("PyMysql关闭链接：%s" % self.py_mysql.bind_address)
                self.py_mysql.close()
            if self.server:
                logger.info("PyMysql关闭隧道：%s" % self.server.local_bind_addresses)
                self.server.close()
                logger.info("关闭隧道成功")
        except Exception as e:
            raise Exception('close db session exception:{}'.format(e))


if __name__ == "__main__":
    # port = get_port()
    # server = SSHTunnelForwarder(
    #     ("47.116.2.104", 22),
    #     ssh_username="ssh-proxy",
    #     ssh_pkey="./../../resource/dx_ssh_proxy",
    #     remote_bind_address=("rm-uf60ec1554fou12qk33150.mysql.rds.aliyuncs.com", 3306),
    #     local_bind_address=('127.0.0.1', port))
    # server.start()
    # pool = PooledDB(pymysql, 5,
    #                 host="127.0.0.1",
    #                 user="biz_test",
    #                 passwd="1Swb3hAN0Hax9p",
    #                 db="global_gbiz1",
    #                 port=port)
    #
    # port1 = get_port()
    # server1 = SSHTunnelForwarder(
    #     ("47.116.2.104", 22),
    #     ssh_username="ssh-proxy",
    #     ssh_pkey="./../../resource/dx_ssh_proxy",
    #     remote_bind_address=("rm-uf60ec1554fou12qk33150.mysql.rds.aliyuncs.com", 3306),
    #     local_bind_address=('127.0.0.1', port1))
    # server1.start()
    # pool1 = PooledDB(pymysql, 5,
    #                  host="127.0.0.1",
    #                  user="biz_test",
    #                  passwd="1Swb3hAN0Hax9p",
    #                  db="global_payment_test1",
    #                  port=port1)
    #
    # cursor = pool.connection().cursor(pymysql.cursors.DictCursor)
    # print(cursor.execute("select * from asset"))
    # print(cursor.fetchall())
    # cursor1 = pool.connection().cursor(pymysql.cursors.DictCursor)
    # print(cursor1.execute("select * from withdraw"))
    # print(cursor1.fetchall())
    # pool.close()
    # pool1.close()
    # server.close()
    # server1.close()
    pass
