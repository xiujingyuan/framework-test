# -*- coding: utf-8 -*-
import time

from tenacity import retry, stop_after_attempt, wait_fixed

import common.global_const as gc
from biztest.util.asserts.assert_util import Assert
from biztest.util.http.http_util import Http
from biztest.util.log.log_util import LogUtil
from biztest.util.tools.tools import generate_sql


class Task(object):
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
        elif "payment" in env:
            self.base_url = gc.PAYMENT_URL
            self.db = gc.PAYMENT_DB
        elif "deposit" in env:
            self.base_url = gc.DEPOSIT_URL
            self.db = gc.DEPOSIT_DB
        else:
            raise Exception("url未配置，请配置")

    def wait_task_appear(self, order_no, task_type, timeout=60):
        result = False
        time_start = time.time()
        while (time.time() - time_start) < timeout:
            task_list = self.db.query("select task_id, task_type, task_status "
                                      "from task where task_order_no='%s' order by task_id desc" % order_no)
            for task in task_list:
                if task["task_type"] == task_type:
                    result = True
                    break
            if result:
                break
            else:
                time.sleep(0.2)
        if not result:
            raise Exception("no task found, task_order_no:%s, task_type:%s" % (order_no, task_type))

    def get_task_id_by_task_type(self, order_no, task_type):
        self.wait_task_appear(order_no, task_type, timeout=10)
        task_id = 0
        task_list = self.db.query("select task_id, task_type, task_status "
                                  "from task where task_order_no='%s' order by task_id desc" % order_no)
        for task in task_list:
            if task["task_type"] == task_type:
                task_id = task["task_id"]
                break
        if task_id == 0:
            raise Exception("no task found, task_order_no:%s, task_type:%s" % (order_no, task_type))
        return task_id

    def update_task_next_run_at_forward(self, order_no):
        self.db.update("update task set task_next_run_at = DATE_SUB(now(), "
                       "interval 80 minute) where task_order_no = '%s' " % order_no)

    def update_task_next_run_at_forward_grant_use(self, order_no, task_id):
        self.db.update("update task set task_next_run_at = DATE_SUB(now(), "
                       "interval 80 minute) where task_order_no = '%s' and task_id= %s" % (order_no, task_id))

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(5))


    def run_task_by_id(self, task_id, excepts=None):
        self.db.update("update task set task_next_run_at = DATE_SUB(now(), "
                       "interval 80 minute) where task_id = '%s'" % task_id)
        url = self.base_url + "/task/run?taskId=" + str(task_id)
        ret = Http.http_get(url, self.header)
        if "任务正在执行，请稍后重试" in str(ret):
            raise Exception("task正在执行，进行重试")
        if excepts is not None:
            Assert.assert_match_json(excepts, ret[0], "task运行结果校验不通过，order_id:%s" % task_id)
        return ret

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(5))
    def run_task(self, order_no, task_type, excepts=None):
        task_id = self.get_task_id_by_task_type(order_no, task_type)
        self.update_task_next_run_at_forward_grant_use(order_no, task_id)
        url = self.base_url + "/task/run?taskId=" + str(task_id)
        ret = Http.http_get(url, self.header)
        if "任务正在执行，请稍后重试" in str(ret):
            raise Exception("task正在执行，进行重试")
        if excepts is not None:
            Assert.assert_match_json(excepts, ret[0], "task运行结果校验不通过，order_no:%s, task_type:%s" % (order_no, task_type))
        return ret

    def run_task_by_order_no(self, order_no, excepts=None):
        self.update_task_next_run_at_forward(order_no)
        url = self.base_url + "/task/run?orderNo=" + str(order_no)
        ret = Http.http_get(url, self.header)
        if excepts is not None:
            Assert.assert_match_json(excepts, ret, "task运行结果校验不通过，order_no:%s" % order_no)
        return ret

    def run_task_by_order_no_count(self, order_no, count=2):
        tasks = self.get_task(task_order_no=order_no, task_status="open")
        if tasks is None or len(tasks) == 0:
            LogUtil.log_info("order_no:%s 不存在open状态的task" % order_no)
            return
        for c in range(count):
            self.run_task_by_order_no(order_no)

    def get_task(self, **kwargs):
        sql_param = generate_sql(kwargs, 'and')
        return self.db.query("select * from task where " + sql_param)

    def get_task_by_order_no_list(self, order_no_list):
        sql_param = "select * from task where task_order_no in (%s) and task_status='open'" % (str(order_no_list)[1:-1])
        return self.db.do_sql(sql_param)

    def update_task(self, task_id, **kwargs):
        sql_param = generate_sql(kwargs, ',')
        self.db.do_sql("update task set %s where task_id=%s" % (sql_param, task_id))

    def wait_task_stable(self, **kwargs):
        task_list = self.get_task(**kwargs)
        if task_list is None or len(task_list) == 0:
            return
        for task in task_list:
            if task["task_status"] in ["open", "close", "terminated"]:
                continue
            count = 0
            while True:
                task_temp = self.get_task(task_id=task["task_id"])[0]
                if task_temp["task_status"] not in ["open", "close", "terminated"]:
                    LogUtil.log_info("task仍在运行中，请关注，task_id：%s，order_no：%s，task_type：%s，status：%s" %
                                     (task_temp["task_id"], task_temp["task_order_no"],
                                      task_temp["task_type"], task_temp["task_status"]))
                    count = count + 1
                    time.sleep(0.5)
                else:
                    break
                if count > 60:
                    break

    def check_task_stable(self, order_no_list):
        task_list = self.db.query("select * from task where task_order_no in (%s)" % str(order_no_list)[1:-1])
        if task_list is None or len(task_list) == 0:
            return
        for task in task_list:
            if task["task_status"] not in ["close", "open", "terminated"]:
                self.wait_task_stable(task_id=task["task_id"])

    def run_task_until_close_or_timeout(self, item_no, times=30):
        """
        反复多次执行task，直到task全部close或者超过最大次数
        :param item_no:
        :param times:
        :return:
        """
        open_tasks = None
        for x in range(0, times):
            ret = self.run_task_by_order_no(item_no)
            open_tasks = self.get_task(task_order_no=item_no, task_status="open")
            if len(open_tasks) == 0:
                return
            time.sleep(1)
        if len(open_tasks) > 0:
            raise Exception("task执行%s次后仍未完全关闭，原因：%s" % (times, ret))


class GbizTask(Task):
    def __init__(self):
        super().__init__("gbiz%s" % gc.ENV)


class TaskContract(Task):
    def __init__(self):
        super().__init__("contact%s" % gc.ENV)

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(5))
    def run_task(self, order_no, task_type, excepts=None):
        task_id = self.get_task_id_by_task_type(order_no, task_type)
        url = self.base_url + "/task/run?taskId=" + str(task_id)
        ret = Http.http_get(url, self.header)
        if "任务正在执行，请稍后重试" in str(ret):
            raise Exception("task正在执行，进行重试")
        if excepts is not None:
            Assert.assert_match_json(excepts, ret, "task运行结果校验不通过，order_no:%s, task_type:%s" % (order_no, task_type))


class DepositTask(Task):
    def __init__(self):
        super().__init__("deposit%s" % gc.ENV)

    def run_task(self, order_no, task_type, excepts=None):
        self.update_task_next_run_at_forward(order_no)
        task_id = self.get_task_id_by_task_type(order_no, task_type)
        url = self.base_url + "/task/run?taskId=" + str(task_id)
        ret = Http.http_get(url, self.header)
        if "任务正在执行，请稍后重试" in str(ret):
            raise Exception("task正在执行，进行重试")
        if excepts is not None:
            Assert.assert_match_json(excepts, ret, "task运行结果校验不通过，order_no:%s, task_type:%s" % (order_no, task_type))
        return ret


class TaskGlobal(Task):
    def __init__(self):
        super(TaskGlobal, self).__init__("global_gbiz%s_%s" % (gc.ENV, gc.COUNTRY))


class TaskGlobalRepay(Task):
    def __init__(self):
        super(TaskGlobalRepay, self).__init__("global_rbiz%s_%s" % (gc.ENV, gc.COUNTRY))


class TaskGlobalPayment(Task):
    def __init__(self):
        super(TaskGlobalPayment, self).__init__("global_payment%s_%s" % (gc.ENV, gc.COUNTRY))

    def run_task(self, order_no, task_type, excepts=None):
        self.update_task_next_run_at_forward(order_no)
        task_id = self.get_task_id_by_task_type(order_no, task_type)
        url = self.base_url + "/task/runTaskById"
        req_data = {"id": task_id}
        ret = Http.http_post(url, req_data, self.header)
        if "任务正在执行，请稍后重试" in str(ret):
            raise Exception("task正在执行，进行重试")
        if excepts is not None:
            Assert.assert_match_json(excepts, ret, "task运行结果校验不通过，order_no:%s, task_type:%s" % (order_no, task_type))
        return ret

    def run_task_by_id(self, task_id, excepts=None):
        self.db.update("update task set task_next_run_at = DATE_SUB(now(), "
                       "interval 80 minute) where task_id = '%s'" % task_id)
        url = self.base_url + "/task/runTaskById"
        req_data = {"id": task_id}
        ret = Http.http_post(url, req_data, self.header)
        if excepts is not None:
            Assert.assert_match_json(excepts, ret, "task运行结果校验不通过，order_id:%s" % task_id)
        return ret

    def run_task_by_order_no(self, order_no, excepts=None):
        self.update_task_next_run_at_forward(order_no)
        url = gc.PAYMENT_URL + "/task/runTaskByOrderNo"
        req_data = {"orderNo": order_no}
        ret = Http.http_post(url, req_data, self.header)
        if excepts is not None:
            Assert.assert_match_json(excepts, ret, "task运行结果校验不通过，order_no:%s" % order_no)
        return ret
