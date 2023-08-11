#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time

import pytest

from biztest.config.payment_global.global_payment_kv_config import update_fusing_config
from biztest.function.global_payment.global_payment_check_function import check_fusing_data, check_withdraw_data
from biztest.function.global_payment.global_payment_db_function import update_fusing_all_close, update_withdraw_status, \
    update_fusing_create_at
from biztest.interface.payment_global.payment_global_interface import auto_withdraw, global_run_job
from biztest.util.db.db_util import DataBase
from biztest.util.task.task import TaskGlobalPayment
from biztest.util.tools.tools import get_date


class TestFusing:
    task = TaskGlobalPayment()
    # phl
    sign_company = "coperstone"
    withdraw_channel = "paycools_copperstone_withdraw"
    channel_resp_code = "1009"
    channel_resp_message = "amount:must be greater than or equal to 100"

    # mex
    # sign_company = "alibey"
    # withdraw_channel = "pandapay_alibey_withdraw"
    # channel_resp_code = "-1"
    # channel_resp_message = "Importe no válido"

    # tha
    # sign_company = "amberstar1"
    # withdraw_channel = "gbpay_amberstar1_withdraw"
    # channel_resp_code = "WD_90"
    # channel_resp_message = "Error"

    def setup_class(cls):
        update_fusing_all_close()

    def teardown_class(cls):
        update_fusing_config()
        update_fusing_all_close()
        DataBase.close_connects()

    @pytest.mark.fusing
    def test_error_fusing(self):
        """
        错误信息熔断
        """
        update_fusing_config({self.withdraw_channel: [self.channel_resp_message]})
        req, resp = auto_withdraw(self.sign_company, channel_name=self.withdraw_channel, amount=1)
        merchant_key = req["merchant_key"]
        self.task.run_task(merchant_key, "withdraw", excepts={"code": 2})
        check_withdraw_data(merchant_key, 1, 1, self.channel_resp_code, self.channel_resp_message)
        # 熔断触发
        fusing_trace_no = check_fusing_data(self.withdraw_channel, "error", "open")
        # 新进订单挂起
        req, resp = auto_withdraw(self.sign_company, channel_name=self.withdraw_channel)
        merchant_key = req["merchant_key"]
        check_withdraw_data(merchant_key, 1, 0, "KN_CHANNEL_FUSING", "KN_CHANNEL_FUSING")
        self.task.run_task(merchant_key, "withdraw", excepts={"code": 2, "message": "fusing suspend.*"})
        # 手动恢复
        global_run_job("fusingRestoreJob", {"traceNo": fusing_trace_no, "fusingStatus":"close"})
        check_fusing_data(self.withdraw_channel, "error", "close")

    @pytest.mark.fusing
    def test_exception_fusing(self):
        """
        成功率熔断，渐进式恢复
        """
        update_fusing_config()
        # 熔断触发
        req, resp = auto_withdraw(self.sign_company, channel_name=self.withdraw_channel)
        self.task.run_task(req["merchant_key"], "withdraw", excepts={"code": 2})
        req, resp = auto_withdraw(self.sign_company, channel_name=self.withdraw_channel)
        self.task.run_task(req["merchant_key"], "withdraw", excepts={"code": 2})
        global_run_job("fusingSuccessRateJob", {})
        check_fusing_data(self.withdraw_channel, "exception", "open")
        # 白名单放行
        req, resp = auto_withdraw(self.sign_company, channel_name=self.withdraw_channel)
        merchant_key_1 = req["merchant_key"]
        req, resp = auto_withdraw(self.sign_company, channel_name=self.withdraw_channel)
        merchant_key_2 = req["merchant_key"]
        global_run_job("fusingRestoreJob", {})
        time.sleep(1)
        check_withdraw_data(merchant_key_2, 1, 0, "KN_FUSING_RESTORE", "KN_FUSING_RESTORE")
        self.task.run_task(merchant_key_1, "withdraw", excepts={"code": 2})
        self.task.run_task(merchant_key_2, "withdraw", excepts={"code": 2})
        # 成功率未达标，继续熔断中
        global_run_job("fusingRestoreJob", {})
        check_fusing_data(self.withdraw_channel, "exception", "open")
        # 成功率达标，熔断恢复
        update_withdraw_status(merchant_key_1, "success")
        update_withdraw_status(merchant_key_2, "success")
        global_run_job("fusingRestoreJob", {})
        check_fusing_data(self.withdraw_channel, "exception", "close")

    @pytest.mark.fusing
    def test_exception_fusing_time_out_restore(self):
        """
        熔断时长到了自动恢复（这个用例可能跑不通，有数据干扰）
        执行前确保没有 resp_code=KN_FUSING_RESTORE 的订单
        """
        update_fusing_config()
        # 熔断触发
        req, resp = auto_withdraw(self.sign_company, channel_name=self.withdraw_channel)
        self.task.run_task(req["merchant_key"], "withdraw", excepts={"code": 2})
        req, resp = auto_withdraw(self.sign_company, channel_name=self.withdraw_channel)
        self.task.run_task(req["merchant_key"], "withdraw", excepts={"code": 2})
        global_run_job("fusingSuccessRateJob", {})
        fusing_trace_no = check_fusing_data(self.withdraw_channel, "exception", "open")
        # 时间到了，熔断恢复
        update_fusing_create_at(fusing_trace_no, get_date(hour=-3))
        global_run_job("fusingRestoreJob", {})
        check_fusing_data(self.withdraw_channel, "exception", "close")
