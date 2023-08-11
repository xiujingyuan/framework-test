# -*- coding: utf-8 -*-
from biztest.function.biz.biz_db_function import get_central_msg_id_by_order_no, \
    get_central_task_id_by_type, get_central_task_id_by_request_order_no, get_central_task_id_by_order_no
from biztest.util.asserts.assert_util import Assert
from biztest.util.http.http_util import Http
import common.global_const as global_const
from biztest.util.tools.tools import *


def get_timestamp():
    """
    获取20位的随机数
    :return:
    """
    return '2020' + str(datetime.now().timestamp()).replace('.', '')


"""
biz central系统的主要接口
"""

header = {"Content-Type": "application/json"}


def run_task_in_biz_central(order_no, excepts=None):
    task_list = get_central_task_id_by_order_no(order_no)
    if task_list:
        for task in task_list:
            run_task_in_biz_central_by_task_id(task["task_id"], excepts=excepts)


def run_task_in_biz_central_by_task_id(task_id, excepts=None):
    url = global_const.BIZ_CENTRAL_URL + "/job/runTaskById?id={0}".format(task_id)
    ret = Http.http_get(url, header)
    if excepts is not None:
        Assert.assert_match_json(excepts, ret, "task运行结果校验不通过，task_id:{0}".format(task_id))


def run_msg_in_biz_central(order_no, excepts=None):
    msg_list = get_central_msg_id_by_order_no(order_no)
    if msg_list:
        for msg in msg_list:
            url = global_const.BIZ_CENTRAL_URL + "/job/sendMsgById?id=" + str(msg["sendmsg_id"])
            ret = Http.http_get(url, header)
            if excepts is not None:
                Assert.assert_match_json(excepts, ret[0], "msg运行结果校验不通过")


def run_biz_central_task_by_count(order_no, count=2, wait_time=0.5):
    for c in range(count):
        run_task_in_biz_central(order_no)
        time.sleep(wait_time)


def run_type_task_biz_central(task_type, order_no, excepts=None):
    task_list = get_central_task_id_by_type(order_no, task_type)
    if task_list:
        for task in task_list:
            run_task_in_biz_central_by_task_id(task["task_id"], excepts=excepts)


def run_request_order_no_task_biz_central(order_no, excepts=None):
    task_list = get_central_task_id_by_request_order_no(order_no)
    if task_list:
        for task in task_list:
            run_task_in_biz_central_by_task_id(task["task_id"], excepts=excepts)
