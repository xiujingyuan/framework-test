#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time

import pytest

from biztest.case.deposit.base_test_deposit import BaseTestDeposit
from biztest.function.deposit.deposit_check_function import check_trade_data, check_trade_order_data
from biztest.function.deposit.deposit_db_function import get_account_by_channel_code
from biztest.interface.deposit.deposit_interface import huatong_tq_balance_notify, huatong_qjj_balance_notify, \
    trade_transfer, trade_withdrawal, trade_loan
from biztest.util.asserts.assert_util import Assert
from biztest.util.tools.tools import get_item_no, get_date, get_timestamp

"""
华通存管功能：
1.账户相关：开户/绑卡
2.交易相关：7-入金回调（资金归集）/2-余额支付（虚户间转账）/3-提现出金/4-子账户付款（放款）
3.流水相关：余额同步/资金明细流水拉取
"""


class TestHuatongDeposit(BaseTestDeposit):

    @pytest.fixture()
    def data(self):
        self.order_no = get_item_no()
        self.trade_no = "%s_1" % self.order_no
        self.amount = 500000

    @pytest.mark.deposit
    def test_trade_transfer(self, data):
        """
        2-余额支付（虚户间转账）
        """
        in_account_param = "v_test_ht_005_ht_qianjingjing"
        out_account_param = "v_test_ht_004_ht_qianjingjing"
        in_account = get_account_by_channel_code(in_account_param)
        out_account = get_account_by_channel_code(out_account_param)
        in_account_db = in_account[0]["number"]
        out_account_db = out_account[0]["number"]
        merchant_id = out_account[0]["merchant_id"]

        resp = trade_transfer(self.order_no, self.trade_no, in_account_param, out_account_param, self.amount)
        Assert.assert_equal(0, resp["code"], "接口调用异常")

        self.trade_task_process(self.order_no, self.trade_no)
        check_trade_data(self.trade_no, type=2, status=2, amount=self.amount, in_account=in_account_db, out_account=out_account_db, merchant_id=merchant_id)
        check_trade_order_data(self.order_no, type=2, status=2, amount=self.amount, merchant_id=merchant_id)

    @pytest.mark.deposit
    def test_trade_withdrawal(self, data):
        """
        3-提现出金
        """
        out_account_param = "v_phtest_002_ht_tengqiao"
        out_account = get_account_by_channel_code(out_account_param)
        out_account_db = out_account[0]["number"]
        merchant_id = out_account[0]["merchant_id"]

        resp = trade_withdrawal(self.order_no, self.trade_no, out_account_param, self.amount)
        Assert.assert_equal(0, resp["code"], "接口调用异常")
        self.task.run_task(self.order_no, "TradeNew", excepts={"code": 0})
        self.task.run_task(self.trade_no, "TradeApply", excepts={"code": 0})
        time.sleep(30)
        self.task.run_task(self.trade_no, "WithdrawCallback", excepts={"code": 0})
        self.task.run_task(self.trade_no, "QueryTrade", excepts={"code": 0})
        self.task.run_task(self.trade_no, "AcctRecharge", excepts={"code": 0})
        self.task.run_task(self.order_no, "QueryOrder", excepts={"code": 0})
        check_trade_data(self.trade_no, type=3, status=2, amount=self.amount, in_account="", out_account=out_account_db, merchant_id=merchant_id)
        check_trade_order_data(self.order_no, type=3, status=2, amount=self.amount, merchant_id=merchant_id)

    @pytest.mark.deposit
    def test_trade_loan(self, data):
        """
        4-子账户付款（放款）
        """
        channel_code = "v_test_ht_004_ht_qianjingjing"
        out_account = get_account_by_channel_code(channel_code)
        out_account_db = out_account[0]["number"]
        merchant_id = out_account[0]["merchant_id"]
        four_element = {"data": {
            "bank_code_encrypt": "enc_03_3199134250318694400_325",
            "phone_number_encrypt": "enc_01_1711720_086",
            "user_name_encrypt": "enc_04_3555940_938",
            "id_number_encrypt": "enc_02_2684792680353368064_341",
        }}
        # # 添加白名单
        # member_register(channel_code, four_element)
        # self.task.run_task(four_element['data']['bank_code_encrypt'], "MemberRegister", excepts={"code": 0})

        resp = trade_loan(self.order_no, self.trade_no, channel_code, four_element, self.amount)
        Assert.assert_equal(0, resp["code"], "接口调用异常")

        self.task.run_task(self.order_no, "TradeNew", excepts={"code": 0})
        self.task.run_task(self.trade_no, "UploadPayFlow", excepts={"code": 0})
        self.task.run_task(self.trade_no, "QueryUploadPayFlow", excepts={"code": 0})
        self.task.run_task(self.trade_no, "TradeApply", excepts={"code": 0})
        self.task.run_task(self.trade_no, "QueryTrade", excepts={"code": 0})
        self.task.run_task(self.trade_no, "AcctRecharge", excepts={"code": 0})
        self.task.run_task(self.order_no, "QueryOrder", excepts={"code": 0})
        check_trade_data(self.trade_no, type=4, status=2, amount=self.amount, in_account=four_element['data']['bank_code_encrypt'], out_account=out_account_db, merchant_id=merchant_id)
        check_trade_order_data(self.order_no, type=4, status=2, amount=self.amount, merchant_id=merchant_id)

    @pytest.mark.deposit
    def test_balance_notify_tq(self, data):
        """
        7-入金回调（资金归集）
        """
        order_no = int(get_timestamp())
        trade_no = "%s1M%s" % (get_date(fmt="%Y%m%d"), order_no)
        pay_account = "6222009801155834470"
        channel_code = "v_test_ht_004_ht_tengqiao"
        account = get_account_by_channel_code(channel_code)
        in_account_db = account[0]["number"]
        merchant_id = account[0]["merchant_id"]

        resp = huatong_tq_balance_notify(order_no, trade_no, pay_account, self.amount)
        Assert.assert_equal(200, resp['status'])
        self.task.run_task(trade_no, "InMoneySync", excepts={"code": 0})
        self.task.run_task(order_no, "TradeNew", excepts={"code": 0})
        self.task.run_task(trade_no, "UploadPayFlow", excepts={"code": 0})
        self.task.run_task(trade_no, "QueryUploadPayFlow", excepts={"code": 0})
        self.task.run_task(trade_no, "SingleLedger", excepts={"code": 0})
        self.task.run_task(trade_no, "QueryTrade", excepts={"code": 0})
        self.task.run_task(trade_no, "AcctRecharge", excepts={"code": 0})
        self.task.run_task(order_no, "QueryOrder", excepts={"code": 0})

        check_trade_data(trade_no, type=7, status=2, amount=self.amount, in_account=in_account_db, out_account=pay_account, merchant_id=merchant_id)
        check_trade_order_data(order_no, type=7, status=2, amount=self.amount, merchant_id=merchant_id)

    @pytest.mark.deposit
    def test_balance_notify_qjj(self, data):
        """
        7-入金回调（资金归集）
        """
        order_no = int(get_timestamp())
        trade_no = "%s1M%s" % (get_date(fmt="%Y%m%d"), order_no)
        pay_account = "6232656718000028461"
        channel_code = "v_test_ht_004_ht_qianjingjing"
        account = get_account_by_channel_code(channel_code)
        in_account_db = account[0]["number"]
        merchant_id = account[0]["merchant_id"]

        resp = huatong_qjj_balance_notify(order_no, trade_no, pay_account, self.amount)
        Assert.assert_equal(200, resp['status'])
        self.task.run_task(trade_no, "InMoneySync", excepts={"code": 0})
        self.task.run_task(order_no, "TradeNew", excepts={"code": 0})
        self.task.run_task(trade_no, "UploadPayFlow", excepts={"code": 0})
        self.task.run_task(trade_no, "QueryUploadPayFlow", excepts={"code": 0})
        self.task.run_task(trade_no, "SingleLedger", excepts={"code": 0})
        self.task.run_task(trade_no, "QueryTrade", excepts={"code": 0})
        self.task.run_task(trade_no, "AcctRecharge", excepts={"code": 0})
        self.task.run_task(order_no, "QueryOrder", excepts={"code": 0})

        check_trade_data(trade_no, type=7, status=2, amount=self.amount, in_account=in_account_db, out_account=pay_account, merchant_id=merchant_id)
        check_trade_order_data(order_no, type=7, status=2, amount=self.amount, merchant_id=merchant_id)

    @pytest.mark.deposit
    def test_account_balance(self):
        pass

    @pytest.mark.deposit
    def test_account_detail(self):
        pass

