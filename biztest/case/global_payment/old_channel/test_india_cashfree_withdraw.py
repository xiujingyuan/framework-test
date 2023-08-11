# -*- coding: utf-8 -*-

import json

import pytest

from biztest.config.payment_global.global_payment_kv_config import update_cashfree_withdraw, update_razorpay_withdraw
from biztest.function.global_payment.global_payment_check_function import check_withdraw_receipt, check_withdraw, \
    check_binding
from biztest.function.global_payment.global_payment_db_operation import delete_binding, get_binding, \
    update_channel_error, get_available_uuid, update_provider, update_sign_company_provider_product, update_channel
from biztest.interface.payment_global.payment_global_interface import global_withdraw_balance, auto_withdraw, \
    run_task_by_order_no
from biztest.util.asserts.assert_util import Assert
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_cashfree import CashfreeMock
from biztest.util.easymock.global_payment.global_payment_razorpay import RazorpayMock


class TestIndiaCashfreeWithdraw:
    def setup_class(self):
        self.env_test = pytest.config.getoption("--env") if hasattr(pytest, "config") else 1
        self.sign_company = "yomoyo5"
        self.channel = "cashfree_%s_withdraw" % self.sign_company
        update_channel(self.channel, channel_status="1", channel_sign_company_code=self.sign_company)
        self.cashfree_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
        self.razorpay_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
        update_provider("razorpay", "close")
        update_sign_company_provider_product(self.sign_company, "cashfree", "withdraw", "open")
        update_cashfree_withdraw(self.sign_company, "5e9807281718270057767a3e")
        update_razorpay_withdraw(self.sign_company, "5e9807281718270057767a3e")

    def teardown_class(self):
        update_provider("razorpay", "open")
        update_cashfree_withdraw(self.sign_company)
        update_razorpay_withdraw(self.sign_company)
        DataBase.close_connects()

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_withdraw
    @pytest.mark.global_cashfree
    def test_withdraw_balance_fail(self):
        # 更新easymock余额查询为失败,cashfree和razorpay均查询失败
        self.cashfree_mock.update_cashfree_withdraw_balance_fail()
        self.razorpay_mock.update_razorpay_withdraw_balance_fail()
        # 发起余额查询请求
        req, resp = global_withdraw_balance(self.sign_company)
        Assert.assert_match_json({"code": 1, "message": "余额查询失败", "data": None}, resp, "代付余额查询失败")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_withdraw
    @pytest.mark.global_cashfree
    def test_withdraw_balance_success(self):
        # razorpay查询失败，只有cashfree查询成功
        self.cashfree_mock.update_cashfree_withdraw_balance_success()
        self.razorpay_mock.update_razorpay_withdraw_balance_fail()
        # 发起余额查询请求
        req, resp = global_withdraw_balance(self.sign_company)
        Assert.assert_match_json({"code": 0,
                                  "message": "余额查询成功",
                                  "data": {"total": 123478,
                                           "available": 19979478,
                                           "data": [{"total": 123478,
                                                     "available": 19979478,
                                                     "channel_name": self.channel}]}},
                                 resp, "余额查询成功")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_withdraw
    def test_withdraw_fail_addBeneficiary_fail(self):
        # 更新easymock放款请求返回失败
        account = get_available_uuid("account", 1)[0]
        card_num = account["account_card_num"]
        card_uuid = account["account_card_uuid"]
        delete_binding(card_num, self.channel)

        self.cashfree_mock.update_cashfree_withdraw_balance_success()
        self.cashfree_mock.update_cashfree_query_Beneficiary_not_exit(card_num)
        self.cashfree_mock.update_cashfree_add_Beneficiary_fail()

        # 发起代付请求
        req, resp = auto_withdraw(self.sign_company, card_uuid)
        # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
        Assert.assert_match_json({"code": 2,
                                  "message": "订单.*交易正在处理中！",
                                  "data": {
                                      "amount": 200,
                                      "platform_code": "E20002",
                                      "platform_message": "PROCESSING",
                                      "channel_name": self.channel,
                                      "channel_code": "",
                                      "channel_message": "",
                                      "status": 0}},
                                 resp,
                                 "代付处理中")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "放款开户绑卡失败"})
        check_binding(card_uuid, "account", 2, self.channel)
        check_withdraw(req["merchant_key"], account, 3, self.channel)
        check_withdraw_receipt(req["merchant_key"], account, 3, self.channel, "KN_BINDING_UNVALID", "failed")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_withdraw
    def test_withdraw_fail_queryBeneficiary_exit(self):
        # 更新easymock放款请求返回失败
        update_channel_error("cashfree", "400", "", 1, "WITHDRAW")
        account = get_available_uuid("account", 1)[0]
        card_num = account["account_card_num"]
        card_uuid = account["account_card_uuid"]
        delete_binding(card_num, self.channel)

        self.cashfree_mock.update_cashfree_withdraw_balance_success()
        self.cashfree_mock.update_cashfree_query_Beneficiary_exit(card_num)
        self.cashfree_mock.update_cashfree_add_Beneficiary_fail()
        self.cashfree_mock.update_cashfree_withdraw_fail()

        # 发起代付请求
        req, resp = auto_withdraw(self.sign_company, card_uuid)
        # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
        Assert.assert_match_json({"code": 2,
                                  "message": "订单.*交易正在处理中！",
                                  "data": {
                                      "amount": 200,
                                      "platform_code": "E20002",
                                      "platform_message": "PROCESSING",
                                      "channel_name": self.channel,
                                      "channel_code": "",
                                      "channel_message": "",
                                      "status": 0}},
                                 resp,
                                 "代付处理中")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现失败"})
        bind = get_binding(card_num, self.channel)[0]
        Assert.assert_equal(json.loads(bind["binding_protocol_info"])["bene_id"], card_num, "联系人开户信息保存")

        check_binding(card_uuid, "account", 1, self.channel)
        check_withdraw(req["merchant_key"], account, 3, self.channel)
        check_withdraw_receipt(req["merchant_key"], account, 3, self.channel, "400",
                               "Transfer amount is less than minimum amount of Rs.1")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_withdraw
    def test_withdraw_fail(self):
        # 更新easymock放款请求返回失败
        update_channel_error("cashfree", "400", "", 1, "WITHDRAW")
        account = get_available_uuid("account", 1)[0]
        card_num = account["account_card_num"]
        card_uuid = account["account_card_uuid"]
        delete_binding(card_num, self.channel)

        self.cashfree_mock.update_cashfree_withdraw_balance_success()
        self.cashfree_mock.update_cashfree_query_Beneficiary_not_exit(card_num)
        self.cashfree_mock.update_cashfree_add_Beneficiary_success()
        self.cashfree_mock.update_cashfree_withdraw_fail()

        # 发起代付请求
        req, resp = auto_withdraw(self.sign_company, card_uuid)
        # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
        Assert.assert_match_json({"code": 2,
                                  "message": "订单.*交易正在处理中！",
                                  "data": {
                                      "amount": 200,
                                      "platform_code": "E20002",
                                      "platform_message": "PROCESSING",
                                      "channel_name": self.channel,
                                      "channel_code": "",
                                      "channel_message": "",
                                      "status": 0}},
                                 resp,
                                 "代付处理中")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现失败"})
        bind = get_binding(card_num, self.channel)[0]
        Assert.assert_equal(json.loads(bind["binding_protocol_info"])["bene_id"], card_num, "联系人开户信息保存")

        check_binding(card_uuid, "account", 1, self.channel)
        check_withdraw(req["merchant_key"], account, 3, self.channel)
        check_withdraw_receipt(req["merchant_key"], account, 3, self.channel, "400",
                               "Transfer amount is less than minimum amount of Rs.1")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_withdraw
    def test_withdraw_query_reversed(self):
        # 更新easymock放款查询返回放款失败
        # 1.查询受益人失败+添加受益人更新为成功，2.放款请求接口更新为成功，3.查询更新为失败
        account = get_available_uuid("account", 1)[0]
        card_num = account["account_card_num"]
        card_uuid = account["account_card_uuid"]
        delete_binding(card_num, self.channel)

        self.cashfree_mock.update_cashfree_withdraw_balance_success()
        self.cashfree_mock.update_cashfree_query_Beneficiary_not_exit(card_num)
        self.cashfree_mock.update_cashfree_add_Beneficiary_success()
        self.cashfree_mock.update_cashfree_withdraw_success()
        self.cashfree_mock.update_cashfree_withdraw_query_reversed()

        # 发起代付请求
        req, resp = auto_withdraw(self.sign_company, card_uuid)
        # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
        Assert.assert_match_json({"code": 2,
                                  "message": "订单.*交易正在处理中！",
                                  "data": {
                                      "amount": 200,
                                      "platform_code": "E20002",
                                      "platform_message": "PROCESSING",
                                      "channel_name": self.channel,
                                      "channel_code": "",
                                      "channel_message": "",
                                      "status": 0}},
                                 resp,
                                 "代付处理中")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询撤销"})
        bind = get_binding(card_num, self.channel)[0]
        Assert.assert_equal(json.loads(bind["binding_protocol_info"])["bene_id"], card_num, "联系人开户信息保存")

        check_binding(card_uuid, "account", 1, self.channel)
        check_withdraw(req["merchant_key"], account, 3, self.channel)
        check_withdraw_receipt(req["merchant_key"], account, 3, self.channel, "REVERSED",
                               "Details of transfer with transferId a927a2ecfdc64601bc76c1ede05f37a1")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_withdraw
    def test_withdraw_query_fail(self):
        # 更新easymock放款查询返回放款失败，外层status=SUCCESS且内部Status=FAILED，为放款失败
        # 1.添加受益人更新为成功，2.放款请求接口更新为成功，3.查询更新为失败
        account = get_available_uuid("account", 1)[0]
        card_num = account["account_card_num"]
        card_uuid = account["account_card_uuid"]
        delete_binding(card_num, self.channel)

        self.cashfree_mock.update_cashfree_withdraw_balance_success()
        self.cashfree_mock.update_cashfree_query_Beneficiary_not_exit(card_num)
        self.cashfree_mock.update_cashfree_add_Beneficiary_success()
        self.cashfree_mock.update_cashfree_withdraw_success()
        self.cashfree_mock.update_cashfree_withdraw_query_fail()

        # 发起代付请求
        req, resp = auto_withdraw(self.sign_company, card_uuid)
        # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
        Assert.assert_match_json({"code": 2,
                                  "message": "订单.*交易正在处理中！",
                                  "data": {
                                      "amount": 200,
                                      "platform_code": "E20002",
                                      "platform_message": "PROCESSING",
                                      "channel_name": self.channel,
                                      "channel_code": "",
                                      "channel_message": "",
                                      "status": 0}},
                                 resp,
                                 "代付处理中")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询失败"})
        bind = get_binding(card_num, self.channel)[0]
        Assert.assert_equal(json.loads(bind["binding_protocol_info"])["bene_id"], card_num, "联系人开户信息保存")

        check_binding(card_uuid, "account", 1, self.channel)
        check_withdraw(req["merchant_key"], account, 3, self.channel)
        check_withdraw_receipt(req["merchant_key"], account, 3, self.channel, "FAILED",
                               "BENEFICIARY_BANK_NODE_OFFLINE")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_withdraw
    def test_withdraw_query_fail_not_exists(self):
        # 更新easymock放款查询返回交易不存在，置为放款失败
        account = get_available_uuid("account", 1)[0]
        card_num = account["account_card_num"]
        card_uuid = account["account_card_uuid"]
        delete_binding(card_num, self.channel)

        self.cashfree_mock.update_cashfree_withdraw_balance_success()
        self.cashfree_mock.update_cashfree_query_Beneficiary_not_exit(card_num)
        self.cashfree_mock.update_cashfree_add_Beneficiary_success()
        self.cashfree_mock.update_cashfree_withdraw_success()
        self.cashfree_mock.update_cashfree_withdraw_query_fail_not_exists()

        # 发起代付请求
        req, resp = auto_withdraw(self.sign_company, card_uuid)
        # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
        Assert.assert_match_json({"code": 2,
                                  "message": "订单.*交易正在处理中！",
                                  "data": {
                                      "amount": 200,
                                      "platform_code": "E20002",
                                      "platform_message": "PROCESSING",
                                      "channel_name": self.channel,
                                      "channel_code": "",
                                      "channel_message": "",
                                      "status": 0}},
                                 resp,
                                 "代付处理中")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询订单不存在"})
        bind = get_binding(card_num, self.channel)[0]
        Assert.assert_equal(json.loads(bind["binding_protocol_info"])["bene_id"], card_num, "联系人开户信息保存")

        check_binding(card_uuid, "account", 1, self.channel)
        check_withdraw(req["merchant_key"], account, 3, self.channel)
        check_withdraw_receipt(req["merchant_key"], account, 3, self.channel, "KN_ORDER_NOT_EXISTS",
                               "transferId is invalid or doesnot exist")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_withdraw
    def test_withdraw_query_process_out_status_error(self):
        # 更新easymock放款查询返回放款处理中
        # 1.添加受益人更新为成功，2.放款请求接口更新为成功，3.查询更新为处理中
        account = get_available_uuid("account", 1)[0]
        card_num = account["account_card_num"]
        card_uuid = account["account_card_uuid"]
        delete_binding(card_num, self.channel)

        self.cashfree_mock.update_cashfree_withdraw_balance_success()
        self.cashfree_mock.update_cashfree_query_Beneficiary_not_exit(card_num)
        self.cashfree_mock.update_cashfree_add_Beneficiary_success()
        self.cashfree_mock.update_cashfree_withdraw_success()
        self.cashfree_mock.update_cashfree_withdraw_query_out_status_error()

        # 发起代付请求
        req, resp = auto_withdraw(self.sign_company, card_uuid)

        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现查询订单不存在"})
        bind = get_binding(card_num, self.channel)[0]
        Assert.assert_equal(json.loads(bind["binding_protocol_info"])["bene_id"], card_num, "联系人开户信息保存")

        check_binding(card_uuid, "account", 1, self.channel)
        check_withdraw(req["merchant_key"], account, 1, self.channel)
        check_withdraw_receipt(req["merchant_key"], account, 1, self.channel, "200",
                               "Transfer completed successfully")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_withdraw
    def test_withdraw_query_process_pending(self):
        # 更新easymock放款查询返回放款处理中，cashfree通道返回status=SUCCESS且data.status=PENDING，置为放款处理中
        # 1.添加受益人更新为成功，2.放款请求接口更新为成功，3.查询更新为处理中
        account = get_available_uuid("account", 1)[0]
        card_num = account["account_card_num"]
        card_uuid = account["account_card_uuid"]
        delete_binding(card_num, self.channel)

        self.cashfree_mock.update_cashfree_withdraw_balance_success()
        self.cashfree_mock.update_cashfree_query_Beneficiary_not_exit(card_num)
        self.cashfree_mock.update_cashfree_add_Beneficiary_success()
        self.cashfree_mock.update_cashfree_withdraw_success()
        self.cashfree_mock.update_cashfree_withdraw_query_pending()

        # 发起代付请求
        req, resp = auto_withdraw(self.sign_company, card_uuid)

        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        bind = get_binding(card_num, self.channel)[0]
        Assert.assert_equal(json.loads(bind["binding_protocol_info"])["bene_id"], card_num, "联系人开户信息保存")

        check_binding(card_uuid, "account", 1, self.channel)
        check_withdraw(req["merchant_key"], account, 1, self.channel)
        check_withdraw_receipt(req["merchant_key"], account, 1, self.channel, "200",
                               "Transfer completed successfully")

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_withdraw
    def test_withdraw_success(self):
        # 更新easymock放款查询返回放款成功
        # 1.查询受益人失败+创建受益人成功，2.放款请求接口更新为成功，3.查询更新为成功
        account = get_available_uuid("account", 1)[0]
        card_num = account["account_card_num"]
        card_uuid = account["account_card_uuid"]
        delete_binding(card_num, self.channel)

        self.cashfree_mock.update_cashfree_withdraw_balance_success()
        self.cashfree_mock.update_cashfree_query_Beneficiary_not_exit(card_num)
        self.cashfree_mock.update_cashfree_add_Beneficiary_success()
        self.cashfree_mock.update_cashfree_withdraw_success()
        self.cashfree_mock.update_cashfree_withdraw_query_success()

        # 发起代付请求
        req, resp = auto_withdraw(self.sign_company, card_uuid)

        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
        bind = get_binding(card_num, self.channel)[0]
        Assert.assert_equal(json.loads(bind["binding_protocol_info"])["bene_id"], card_num, "联系人开户信息保存")

        check_binding(card_uuid, "account", 1, self.channel)
        check_withdraw(req["merchant_key"], account, 2, self.channel)
        check_withdraw_receipt(req["merchant_key"], account, 2, self.channel, "SUCCESS",
                               "Details of transfer with transferId a927a2ecfdc64601bc76c1ede05f37a1")
