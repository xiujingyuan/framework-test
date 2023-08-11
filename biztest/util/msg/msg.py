# -*- coding: utf-8 -*-
from biztest.util.db.db_util import DataBase
import time
from biztest.util.http.http_util import Http
from biztest.util.asserts.assert_util import Assert
from biztest.util.msgsender.msgsender import Msgsender
import common.global_const as gc


class Msg(object):
    def __init__(self, env):
        self.header = {"Content-Type": "application/json"}
        self.base_url = None
        self.db = None
        self.get_base_url(env)

    def get_base_url(self, env):
        if "gbiz" in env:
            self.base_url = gc.GRANT_URL
            self.db = gc.GRANT_DB
        elif "rbiz" in env:
            self.base_url = gc.REPAY_URL
            self.db = gc.REPAY_DB
        elif "contact" in env:
            self.base_url = gc.CONTRACT_URL
            self.db = gc.CONTRACT_DB
        elif "dcs" in env:
            self.base_url = gc.DCS_URL
            self.db = gc.DCS_DB
        else:
            raise Exception("url未配置，请配置")

    def run_msg(self, order_no, msg_type, wait_time=0, excepts=None):
        time.sleep(wait_time)
        task_id = self.get_msg_id_by_task_type(order_no, msg_type)
        self.db.update(
            "update sendmsg set sendmsg_next_run_at = DATE_SUB(now(), interval 80 minute) where sendmsg_order_no = "
            "'%s' ;" % order_no)
        url = self.base_url + "/msg/run?msgId=" + str(task_id)
        ret = Http.http_get(url, self.header)
        if excepts is not None:
            Assert.assert_match_json(excepts, ret[0], "msg运行结果校验不通过")

    def run_msg_by_order_no(self, order_no, wait_time=0):
        time.sleep(wait_time)
        self.db.update(
            "update sendmsg set sendmsg_next_run_at = DATE_SUB(now(), interval 80 minute) where sendmsg_order_no = "
            "'%s' ;" % order_no)
        url = self.base_url + "/msg/run?orderNo=" + str(order_no)
        Http.http_get(url, self.header)

    def get_msg_id_by_task_type(self, order_no, msg_type):
        msg_id = 0
        msg_list = \
            self.db.query("select * from sendmsg where sendmsg_order_no='%s' order by sendmsg_id desc" % order_no)
        for msg in msg_list:
            if msg["sendmsg_type"] == msg_type:
                msg_id = msg["sendmsg_id"]
                break
        if msg_id == 0:
            raise Exception("no msg found, order_no:%s, msg_type:%s" % (order_no, msg_type))
        return msg_id

    def run_msg_by_id(self, msg_id, excepts=None, wait_time=0):
        time.sleep(wait_time)
        self.db.update("update sendmsg set sendmsg_next_run_at = DATE_SUB(now(), interval 80 minute) where sendmsg_id "
                       "= '%s'" % msg_id)
        url = self.base_url + "/msg/run?msgId=" + str(msg_id)
        ret = Http.http_get(url, self.header)
        if excepts is not None:
            Assert.assert_match_json(excepts, ret[0], "msg运行结果校验不通过")

    def run_msg_by_id_and_search_by_order_no(self, order_no, excepts=None):
        msg_list = self.db.query(
            "select * from sendmsg where sendmsg_order_no='%s' and sendmsg_status='open'" % order_no)
        for msg in msg_list:
            self.run_msg_by_id(msg["sendmsg_id"], excepts)


class GbizMsg(Msg):
    def __init__(self):
        super().__init__("gbiz%s" % gc.ENV)

