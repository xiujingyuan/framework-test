#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pytest

from biztest.case.deposit.base_test_deposit import BaseTestDeposit
from biztest.function.deposit.deposit_check_function import check_trade_data, check_trade_order_data
from biztest.function.deposit.deposit_db_function import get_account_by_channel_code
from biztest.interface.deposit.deposit_interface import trade_tally, trade_transfer, trade_withdrawal, trade_loan
from biztest.util.asserts.assert_util import Assert
from biztest.util.tools.tools import get_item_no

"""
齐商存管功能：
1.账户相关：开户/绑卡
2.交易相关：1-记账（资金归集）/2-会员贷款清分（虚户间转账）/3-提现出金/4-会员放款
3.流水相关：余额同步/资金明细流水拉取
"""


class TestQishangDeposit(BaseTestDeposit):

    @pytest.fixture()
    def data(self):
        self.order_no = get_item_no()
        self.trade_no = "%s_1" % self.order_no
        self.amount = 500000

    @pytest.mark.deposit
    def test_trade_tally(self, data):
        """
        1-记账（资金归集）
        """
        channel_code = "v_qs_phtest002_qs_qianjingjing"
        pay_channel_code="qsq_cpcn_tq_quick"
        account = get_account_by_channel_code(channel_code)
        in_account_db = account[0]["number"]
        merchant_id = account[0]["merchant_id"]

        resp = trade_tally(self.order_no, self.trade_no, channel_code, pay_channel_code, self.amount)
        Assert.assert_equal(0, resp["code"], "接口调用异常")

        self.trade_task_process(self.order_no, self.trade_no)
        check_trade_data(self.trade_no, type=1, status=2, amount=self.amount, in_account=in_account_db, out_account="", merchant_id=merchant_id)
        check_trade_order_data(self.order_no, type=1, status=2, amount=self.amount, merchant_id=merchant_id)

    @pytest.mark.deposit
    def test_trade_transfer(self, data):
        """
        2-会员贷款清分（虚户间转账）
        """
        in_account_param = "v_qs_phtest002_qs_qianjingjing"
        out_account_param = "v_qs_phtest001_qs_qianjingjing"
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
        out_account_param = "v_qs_phtest001_qs_qianjingjing"
        out_account = get_account_by_channel_code(out_account_param)
        out_account_db = out_account[0]["number"]
        merchant_id = out_account[0]["merchant_id"]

        resp = trade_withdrawal(self.order_no, self.trade_no, out_account_param, self.amount)
        Assert.assert_equal(0, resp["code"], "接口调用异常")

        self.trade_task_process(self.order_no, self.trade_no)
        check_trade_data(self.trade_no, type=3, status=2, amount=self.amount, in_account="", out_account=out_account_db, merchant_id=merchant_id)
        check_trade_order_data(self.order_no, type=3, status=2, amount=self.amount, merchant_id=merchant_id)

    @pytest.mark.deposit
    def test_trade_loan(self, data):
        """
        4-会员放款
        """
        channel_code = "v_qs_phtest001_qs_qianjingjing"
        out_account = get_account_by_channel_code(channel_code)
        out_account_db = out_account[0]["number"]
        merchant_id = out_account[0]["merchant_id"]
        four_element = {"data": {
            "bank_code_encrypt": "enc_03_2690099239887308800_512",
            "phone_number_encrypt": "enc_01_2688957784028350464_954",
            "user_name_encrypt": "enc_04_2482837155136145408_767",
            "id_number_encrypt": "enc_02_2690099240105412608_752",
        }}
        # # 添加白名单
        # member_register(channel_code, four_element)
        # self.task.run_task(four_element['data']['bank_code_encrypt'], "MemberRegister", excepts={"code": 0})

        resp = trade_loan(self.order_no, self.trade_no, channel_code, four_element, self.amount)
        Assert.assert_equal(0, resp["code"], "接口调用异常")

        self.trade_task_process(self.order_no, self.trade_no)
        check_trade_data(self.trade_no, type=4, status=2, amount=self.amount, in_account=four_element['data']['bank_code_encrypt'], out_account=out_account_db, merchant_id=merchant_id)
        check_trade_order_data(self.order_no, type=4, status=2, amount=self.amount, merchant_id=merchant_id)

    @pytest.mark.deposit
    def test_account_balance(self):
        pass

    @pytest.mark.deposit
    def test_account_detail(self):
        pass

