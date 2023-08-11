# -*- coding: utf-8 -*-
import pytest

from biztest.config.easymock.easymock_config import global_payment_mock
from biztest.function.global_payment.global_payment_check_function import check_withdraw_data, check_data, \
    check_withhold_data, check_binding_data
from biztest.function.global_payment.global_payment_db_function import update_withhold_receipt_expired_at, \
    update_task_by_task_order_no
from biztest.interface.payment_global.payment_global_interface import auto_withdraw, auto_pay, \
    onelink_paycode_inquiry, onelink_paycode_payment, auto_bind
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_pak import PaymentPakMock
from biztest.util.task.task import TaskGlobalPayment
from biztest.util.tools.tools import get_date, get_item_no


class TestPakOnelink:

    sign_company = "goldlion"
    withdraw_channel = "onelink_goldlion_withdraw"

    def setup_class(self):
        self.mock = PaymentPakMock(global_payment_mock)
        self.task = TaskGlobalPayment()
        self.mock.update_fk_user_info("account")
        # 登录
        task_order_no = "onelink_goldlion_withdraw_29110899957195637"
        update_task_by_task_order_no(task_order_no, "open")
        self.task.run_task(task_order_no, "Login", excepts={"code": 0})

    def teardown_class(self):
        self.mock.update_fk_user_info("account")
        DataBase.close_connects()

    @pytest.mark.onelink
    def test_withdraw_success(self):
        req, resp = auto_withdraw(self.sign_company, channel_name=self.withdraw_channel)
        merchant_key = req["merchant_key"]
        self.task.run_task(merchant_key, "withdrawRegister", excepts={"code": 0})
        self.task.run_task(merchant_key, "withdraw", excepts={"code": 0})
        check_withdraw_data(merchant_key, 2, 2, "WT_00", "PROCESSED OK")

    @pytest.mark.onelink
    def test_withhold_success(self):
        req, resp = auto_pay(self.sign_company, payment_type="paycode", payment_option="wallet", amount=1030)
        merchant_key = req["merchant_key"]
        channel_key = resp["data"]["channel_key"]
        resp = onelink_paycode_inquiry(channel_key)
        check_data(resp, response_Code="00", bill_status="U", amount_within_dueDate="+0000000001100")
        resp = onelink_paycode_payment(channel_key, "+0000000001100")
        check_data(resp, response_Code="00")
        self.task.run_task(channel_key, "withholdCallback", excepts={"code": 0})
        self.task.run_task(merchant_key, "withholdUpdate", excepts={"code": 0})
        self.task.run_task(merchant_key, "withholdChargeQuery", excepts={"code": 0})
        check_withhold_data(merchant_key, 2, 2, "KN_TRANSFER_SUCCESS", "callback confirm")

    @pytest.mark.onelink
    def test_withhold_time_out_fail(self):
        req, resp = auto_pay(self.sign_company, payment_type="paycode", payment_option="wallet")
        merchant_key = req["merchant_key"]
        update_withhold_receipt_expired_at(merchant_key, expired_at=get_date(minute=-1))
        self.task.run_task(merchant_key, "withholdChargeQuery", excepts={"code": 1})
        self.task.run_task(merchant_key, "withholdUpdate", excepts={"code": 0})
        check_withhold_data(merchant_key, 3, 3, "KN_TIMEOUT_CLOSE_ORDER", "KN_GENERATE_OFFLINE_CODE")

    @pytest.mark.onelink
    def test_bind_success(self):
        user_uuid = card_uuid = get_item_no()
        req, resp = auto_bind(self.sign_company, card_uuid, user_uuid)
        check_data(resp, code=0)
        merchant_key = req["merchant_key"]
        check_binding_data(card_uuid, merchant_key, 0, 0, 2, "V_00", "PROCESSED OK")
