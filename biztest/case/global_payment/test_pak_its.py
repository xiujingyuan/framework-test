# -*- coding: utf-8 -*-
import pytest

from biztest.config.easymock.easymock_config import global_payment_mock
from biztest.function.global_payment.global_payment_check_function import check_withdraw_data, check_data, \
    check_withhold_data
from biztest.function.global_payment.global_payment_db_function import update_withhold_receipt_expired_at, \
    update_task_by_task_order_no
from biztest.interface.payment_global.payment_global_interface import auto_withdraw, auto_pay, its_ebank_payment
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_pak import PaymentPakMock
from biztest.util.task.task import TaskGlobalPayment
from biztest.util.tools.tools import get_date


class TestPakIts:

    sign_company = "goldlion"
    withdraw_channel = "its_goldlion_withdraw"

    def setup_class(self):
        self.mock = PaymentPakMock(global_payment_mock)
        self.task = TaskGlobalPayment()
        self.mock.update_fk_user_info()
        # 登录
        task_order_no = "its_goldlion_withdraw_39288244755590416"
        update_task_by_task_order_no(task_order_no, "open")
        self.task.run_task(task_order_no, "Login", excepts={"code": 0})

    def teardown_class(self):
        self.mock.update_fk_user_info()
        DataBase.close_connects()

    @pytest.mark.its
    def test_withdraw_success(self):
        req, resp = auto_withdraw(self.sign_company, channel_name=self.withdraw_channel, card_uuid="900000000000000014", user_uuid="900000000000000014")
        merchant_key = req["merchant_key"]
        self.task.run_task(merchant_key, "withdrawRegister", excepts={"code": 0, "message": "开户成功，已创建代付任务"})
        self.task.run_task(merchant_key, "withdraw", excepts={"code": 0, "message": "WITHDRAW success"})
        check_withdraw_data(merchant_key, 2, 2, "WT_0000")

    @pytest.mark.its
    def test_withhold_callback_success(self):
        req, resp = auto_pay(self.sign_company, payment_type="ebank", payment_option="wallet", amount=1030)
        merchant_key = req["merchant_key"]
        channel_key = resp["data"]["channel_key"]
        resp = its_ebank_payment(channel_key, "11.00")
        check_data(resp, status="success")
        self.task.run_task(channel_key, "withholdCallback", excepts={"code": 0})
        self.task.run_task(merchant_key, "withholdUpdate", excepts={"code": 0})
        self.task.run_task(merchant_key, "withholdChargeQuery", excepts={"code": 0})
        check_withhold_data(merchant_key, 2, 2, "callback success")

    @pytest.mark.its
    def test_withhold_query_success(self):
        req, resp = auto_pay(self.sign_company, payment_type="ebank", payment_option="wallet", amount=1030)
        merchant_key = req["merchant_key"]
        channel_key = resp["data"]["channel_key"]
        self.mock.its_withhold_query_success(amount=11)
        self.task.run_task(merchant_key, "withholdChargeQuery", excepts={"code": 0})
        self.task.run_task(merchant_key, "withholdUpdate", excepts={"code": 0})
        check_withhold_data(merchant_key, 2, 2, "WHQ_0000_success")

    @pytest.mark.its
    def test_withhold_time_out_fail(self):
        req, resp = auto_pay(self.sign_company, payment_type="ebank", payment_option="wallet")
        merchant_key = req["merchant_key"]
        update_withhold_receipt_expired_at(merchant_key, expired_at=get_date(hour=-1))
        self.mock.its_withhold_query_not_exist()
        self.task.run_task(merchant_key, "withholdChargeQuery", excepts={"code": 1})
        self.task.run_task(merchant_key, "withholdUpdate", excepts={"code": 0})
        check_withhold_data(merchant_key, 3, 3, "KN_TIMEOUT_CLOSE_ORDER")
