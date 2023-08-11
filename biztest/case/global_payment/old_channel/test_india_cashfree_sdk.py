# -*- coding: utf-8 -*-

import pytest

from biztest.config.payment_global.global_payment_kv_config import update_cashfree_sdk
from biztest.function.global_payment.global_payment_check_function import check_withhold, check_withhold_receipt
from biztest.function.global_payment.global_payment_db_operation import update_withhold_receipt_create_at, \
    update_provider, get_available_uuid
from biztest.interface.payment_global.payment_global_interface import auto_pay, \
    run_task_by_order_no, global_withhold_close_order
from biztest.util.asserts.assert_util import Assert
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_cashfree import CashfreeMock


class TestIndiaCashfreeSdk:
    def setup_class(self):
        self.sign_company = "yomoyo2"
        update_provider("razorpay", "close")
        update_cashfree_sdk(self.sign_company, "5e9807281718270057767a3e")
        self.cashfree_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")

    def teardown_class(self):
        update_provider("razorpay", "open")
        update_cashfree_sdk(self.sign_company)
        DataBase.close_connects()

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_sdk
    @pytest.mark.global_cashfree
    def test_cashfree_sdk_token_fail(self):
        # 发起代扣请求直接失败
        self.cashfree_mock.update_cashfree_sdk_gettoken_fail()
        account = get_available_uuid("upi", 1)[0]
        channel = "cashfree_%s_sdk" % self.sign_company

        # 发起代扣
        req, resp = auto_pay(self.sign_company, "sdk", "upi", account["account_card_uuid"])
        merchant_key = req["merchant_key"]
        Assert.assert_match_json({'code': 1,
                                  'data': {'amount': 1111,
                                           'channel_code': 'FAILED',
                                           'channel_message': 'Token generate failed',
                                           'channel_name': channel,
                                           'payment_option': 'upi',
                                           'payment_type': 'sdk',
                                           'platform_code': 'E20016',
                                           'platform_message': 'Token generate failed',
                                           'status': 3},
                                  'message': '交易失败'},
                                 resp,
                                 "代扣结果不正确")
        check_withhold(merchant_key, account, 3)
        check_withhold_receipt(merchant_key, account, 3, channel, "FAILED", "Token generate failed")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_sdk
    @pytest.mark.global_cashfree
    def test_cashfree_sdk_token_success(self):
        # 发起代扣请求直接失败
        self.cashfree_mock.update_cashfree_sdk_gettoken_success()
        account = get_available_uuid("upi", 1)[0]
        channel = "cashfree_%s_sdk" % self.sign_company

        # 发起代扣
        req, resp = auto_pay(self.sign_company, "sdk", "upi", account["account_card_uuid"])
        merchant_key = req["merchant_key"]
        Assert.assert_match_json({'code': 2,
                                  'data': {'amount': 1111,
                                           'channel_code': 'OK',
                                           'channel_message': 'Token generated',
                                           'channel_name': channel,
                                           'payment_data': {'sdk': 'cashfree',
                                                            'token': 'sdk_token'},
                                           'payment_option': 'upi',
                                           'payment_type': 'sdk',
                                           'platform_code': 'E20000',
                                           'platform_message': 'Token generated',
                                           'status': 1},
                                  'message': '交易进行中'},
                                 resp,
                                 "代扣结果不正确")
        check_withhold(merchant_key, account, 1)
        check_withhold_receipt(merchant_key, account, 1, channel, "OK", "Token generated")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_sdk
    @pytest.mark.global_cashfree
    def test_cashfree_sdk_query_success(self):
        self.cashfree_mock.update_cashfree_sdk_gettoken_success()
        self.cashfree_mock.update_cashfree_withhold_query_success()
        account = get_available_uuid("upi", 1)[0]
        channel = "cashfree_%s_sdk" % self.sign_company

        # 发起代扣
        req, resp = auto_pay(self.sign_company, "sdk", "upi", account["account_card_uuid"])
        merchant_key = req["merchant_key"]
        run_task_by_order_no(merchant_key, {"code": 0})
        run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        check_withhold(merchant_key, account, 2)
        check_withhold_receipt(merchant_key, account, 2, channel, "PAID-SUCCESS", "Transaction is Successful")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_sdk
    @pytest.mark.global_cashfree
    def test_cashfree_sdk_query_no_pay(self):
        self.cashfree_mock.update_cashfree_sdk_gettoken_success()
        self.cashfree_mock.update_cashfree_withhold_query_no_pay_no_expire()
        account = get_available_uuid("upi", 1)[0]
        channel = "cashfree_%s_sdk" % self.sign_company

        # 发起代扣
        req, resp = auto_pay(self.sign_company, "sdk", "upi", account["account_card_uuid"])
        merchant_key = req["merchant_key"]
        run_task_by_order_no(merchant_key, {"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        check_withhold(merchant_key, account, 1)
        check_withhold_receipt(merchant_key, account, 1, channel, "OK", "Token generated")

        self.cashfree_mock.update_cashfree_withhold_query_no_pay_expired()
        run_task_by_order_no(merchant_key, {"code": 1, "message": "支付订单查询 this link has expired"})
        run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        check_withhold(merchant_key, account, 3)
        check_withhold_receipt(merchant_key, account, 3, channel, "KN_TIMEOUT_CLOSE_ORDER", "this link has expired")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_sdk
    @pytest.mark.global_cashfree
    def test_cashfree_sdk_query_not_exist(self):
        # 用户一直没有操作，一直返回交易不存在，超过配置时间后置为代扣失败
        self.cashfree_mock.update_cashfree_sdk_gettoken_success()
        self.cashfree_mock.update_cashfree_withhold_query_not_exist()
        account = get_available_uuid("upi", 1)[0]
        channel = "cashfree_%s_sdk" % self.sign_company

        # 发起代扣
        req, resp = auto_pay(self.sign_company, "sdk", "upi", account["account_card_uuid"])
        merchant_key = req["merchant_key"]
        run_task_by_order_no(merchant_key, {"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        check_withhold(merchant_key, account, 1)
        check_withhold_receipt(merchant_key, account, 1, channel, "OK", "Token generated")

        update_withhold_receipt_create_at(merchant_key, day=-1)
        run_task_by_order_no(merchant_key, {'code': 1, 'message': '支付订单查询订单不存在'})
        run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        check_withhold(merchant_key, account, 3)
        check_withhold_receipt(merchant_key, account, 3, channel, "KN_ORDER_NOT_EXISTS", "Order Id does not exist")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_sdk
    @pytest.mark.global_cashfree
    def test_cashfree_sdk_query_not_expiry_time(self):
        # 用户一直没有操作，一直返回交易不存在，超过配置时间后置为代扣失败
        self.cashfree_mock.update_cashfree_sdk_gettoken_success()
        self.cashfree_mock.update_cashfree_withhold_query_process_no_exprie()
        account = get_available_uuid("upi", 1)[0]
        channel = "cashfree_%s_sdk" % self.sign_company

        # 发起代扣
        req, resp = auto_pay(self.sign_company, "sdk", "upi", account["account_card_uuid"])
        merchant_key = req["merchant_key"]
        run_task_by_order_no(merchant_key, {"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        check_withhold(merchant_key, account, 1)
        check_withhold_receipt(merchant_key, account, 1, channel, "OK", "Token generated")

        update_withhold_receipt_create_at(merchant_key, day=-1)
        run_task_by_order_no(merchant_key, {'code': 2, 'message': '代扣订单正在处理中！需要重试！'})
        check_withhold(merchant_key, account, 1)
        check_withhold_receipt(merchant_key, account, 1, channel, "OK", "Token generated")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_sdk
    @pytest.mark.global_cashfree
    def test_cashfree_sdk_query_fail_failed(self):
        self.cashfree_mock.update_cashfree_sdk_gettoken_success()
        self.cashfree_mock.update_cashfree_withhold_query_process_failed()
        account = get_available_uuid("upi", 1)[0]
        channel = "cashfree_%s_sdk" % self.sign_company

        # 发起代扣
        req, resp = auto_pay(self.sign_company, "sdk", "upi", account["account_card_uuid"])
        merchant_key = req["merchant_key"]
        run_task_by_order_no(merchant_key, {"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        check_withhold(merchant_key, account, 1)
        check_withhold_receipt(merchant_key, account, 1, channel, "OK", "Token generated")

        self.cashfree_mock.update_cashfree_withhold_query_fail_failed()
        run_task_by_order_no(merchant_key, {"code": 1, "message": "支付订单查询 this link has expired"})
        run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        check_withhold(merchant_key, account, 3)
        check_withhold_receipt(merchant_key, account, 3, channel, "KN_TIMEOUT_CLOSE_ORDER", "Transaction fail")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_sdk
    @pytest.mark.global_cashfree
    def test_cashfree_sdk_query_fail_user_dropped(self):
        self.cashfree_mock.update_cashfree_sdk_gettoken_success()
        self.cashfree_mock.update_cashfree_withhold_query_process_user_dropped()
        account = get_available_uuid("upi", 1)[0]
        channel = "cashfree_%s_sdk" % self.sign_company

        # 发起代扣
        req, resp = auto_pay(self.sign_company, "sdk", "upi", account["account_card_uuid"])
        merchant_key = req["merchant_key"]
        run_task_by_order_no(merchant_key, {"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        check_withhold(merchant_key, account, 1)
        check_withhold_receipt(merchant_key, account, 1, channel, "OK", "Token generated")

        self.cashfree_mock.update_cashfree_withhold_query_fail_user_dropped()
        run_task_by_order_no(merchant_key, {"code": 1, "message": "支付订单查询 this link has expired"})
        run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        check_withhold(merchant_key, account, 3)
        check_withhold_receipt(merchant_key, account, 3, channel, "KN_TIMEOUT_CLOSE_ORDER", "User dropped out of txn")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_sdk
    @pytest.mark.global_cashfree
    def test_cashfree_sdk_query_fail_pending(self):
        self.cashfree_mock.update_cashfree_sdk_gettoken_success()
        self.cashfree_mock.update_cashfree_withhold_query_process_pending()
        account = get_available_uuid("upi", 1)[0]
        channel = "cashfree_%s_sdk" % self.sign_company

        # 发起代扣
        req, resp = auto_pay(self.sign_company, "sdk", "upi", account["account_card_uuid"])
        merchant_key = req["merchant_key"]
        run_task_by_order_no(merchant_key, {"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        check_withhold(merchant_key, account, 1)
        check_withhold_receipt(merchant_key, account, 1, channel, "OK", "Token generated")

        self.cashfree_mock.update_cashfree_withhold_query_fail_pending()
        run_task_by_order_no(merchant_key, {"code": 1, "message": "支付订单查询 this link has expired"})
        run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        check_withhold(merchant_key, account, 3)
        check_withhold_receipt(merchant_key, account, 3, channel, "KN_TIMEOUT_CLOSE_ORDER", "this link has expired")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_sdk
    @pytest.mark.global_cashfree
    def test_cashfree_sdk_close_order_process(self):
        self.cashfree_mock.update_cashfree_sdk_gettoken_success()
        self.cashfree_mock.update_cashfree_withhold_query_process_pending()
        account = get_available_uuid("upi", 1)[0]
        channel = "cashfree_%s_sdk" % self.sign_company

        # 发起代扣
        req, resp = auto_pay(self.sign_company, "sdk", "upi", account["account_card_uuid"])
        merchant_key = req["merchant_key"]
        run_task_by_order_no(merchant_key, {"code": 2, "message": "代扣订单正在处理中！需要重试！"})

        close_req, close_resp = global_withhold_close_order(req["merchant_key"])
        Assert.assert_match_json({'code': 1, 'data': None, 'message': '订单处理中，关闭订单失败'},
                                 close_resp,
                                 "关单失败")

        update_withhold_receipt_create_at(merchant_key, day=-1)
        close_req, close_resp = global_withhold_close_order(req["merchant_key"])
        Assert.assert_match_json({'code': 1, 'data': None, 'message': '订单处理中，关闭订单失败'},
                                 close_resp,
                                 "关单失败")

        self.cashfree_mock.update_cashfree_withhold_query_fail_pending()
        close_req, close_resp = global_withhold_close_order(req["merchant_key"])
        Assert.assert_match_json({'code': 1, 'data': None, 'message': '订单已经成为终态，关闭订单失败'},
                                 close_resp,
                                 "关单失败")

        run_task_by_order_no(merchant_key, {"code": 0})
        check_withhold(merchant_key, account, 3)
        check_withhold_receipt(merchant_key, account, 3, channel, "KN_TIMEOUT_CLOSE_ORDER", "this link has expired")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_sdk
    @pytest.mark.global_cashfree
    def test_cashfree_sdk_close_order_not_exist(self):
        self.cashfree_mock.update_cashfree_sdk_gettoken_success()
        self.cashfree_mock.update_cashfree_withhold_query_not_exist()
        account = get_available_uuid("upi", 1)[0]
        channel = "cashfree_%s_sdk" % self.sign_company

        # 发起代扣
        req, resp = auto_pay(self.sign_company, "sdk", "upi", account["account_card_uuid"])
        merchant_key = req["merchant_key"]
        run_task_by_order_no(merchant_key, {"code": 2, "message": "代扣订单正在处理中！需要重试！"})

        close_req, close_resp = global_withhold_close_order(req["merchant_key"])
        Assert.assert_match_json({"code": 0,
                                  "message": "关闭订单成功",
                                  "data": {
                                      "platform_code": "E20010",
                                      "platform_message": "Order Id does not exist",
                                      "channel_name": channel,
                                      "channel_code": "KN_MANUAL_CLOSE_ORDER",
                                      "channel_message": "Order Id does not exist"}},
                                 close_resp,
                                 "关单失败")

        run_task_by_order_no(merchant_key, {"code": 0})
        check_withhold(merchant_key, account, 3)
        check_withhold_receipt(merchant_key, account, 3, channel, "KN_MANUAL_CLOSE_ORDER", "Order Id does not exist")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_sdk
    @pytest.mark.global_cashfree
    def test_cashfree_sdk_close_order_success(self):
        self.cashfree_mock.update_cashfree_sdk_gettoken_success()
        self.cashfree_mock.update_cashfree_withhold_query_success()
        account = get_available_uuid("upi", 1)[0]
        channel = "cashfree_%s_sdk" % self.sign_company

        # 发起代扣
        req, resp = auto_pay(self.sign_company, "sdk", "upi", account["account_card_uuid"])
        merchant_key = req["merchant_key"]

        close_req, close_resp = global_withhold_close_order(req["merchant_key"])
        Assert.assert_match_json({'code': 1, 'data': None, 'message': '订单已经成为终态，关闭订单失败'},
                                 close_resp,
                                 "关单失败")
        run_task_by_order_no(merchant_key, {"code": 0})
        check_withhold(merchant_key, account, 2)
        check_withhold_receipt(merchant_key, account, 2, channel, "PAID-SUCCESS", "Transaction is Successful")
