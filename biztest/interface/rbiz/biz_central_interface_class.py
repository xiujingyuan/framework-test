# -*- coding: utf-8 -*-
from biztest.function.biz.biz_db_class import BizDbBase, RepayDbBase
from biztest.function.rbiz.database_operation import *
from biztest.util.asserts.assert_util import Assert
from biztest.util.http.http_util import Http
import common.global_const as gc

"""
biz central系统的主要接口
"""


class BizInterfaceBase(object):
    central_base_url = gc.BIZ_CENTRAL_URL
    header = {"Content-Type": "application/json"}
    db = BizDbBase()
    repay_db = RepayDbBase()

    def run_task_in_biz_central(self, order_no, excepts=None):
        task_list = self.get_central_task_id_by_order_no(order_no)
        for task in task_list:
            self.run_task_in_biz_central_by_task_id(task["task_id"], excepts=excepts)

    def run_task_in_biz_central_by_task_id(self, task_id, excepts=None):
        url = self.central_base_url + "/job/runTaskById?id={0}".format(task_id)
        ret = Http.http_get(url, self.header)
        if excepts is not None:
            Assert.assert_match_json(excepts, ret, "task运行结果校验不通过，task_id:{0}".format(task_id))

    def run_msg_in_biz_central(self, order_no, excepts=None):
        msg_list = self.get_central_msg_id_by_order_no(order_no)
        for msg in msg_list:
            url = self.central_base_url + "/job/sendMsgById?id==" + str(msg["sendmsg_id"])
            ret = Http.http_get(url, self.header)
            if excepts is not None:
                Assert.assert_match_json(excepts, ret[0], "msg运行结果校验不通过")

    def run_task_by_count(self, order_no, count=2):
        for c in range(count):
            self.run_task_in_biz_central(order_no)

    def run_job_by_api(self, job_type, job_params):
        job_url = self.central_base_url + "/job/run"
        params = {"jobType": job_type,
                  "param": json.dumps(job_params)}
        return Http.http_get(job_url, params=params)
