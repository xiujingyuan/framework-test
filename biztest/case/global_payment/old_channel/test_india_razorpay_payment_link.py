# -*- coding: utf-8 -*-

import pytest

from biztest.config.payment_global.global_payment_kv_config import update_razorpay_ebank
from biztest.function.global_payment.global_payment_check_function import check_resp_data, \
    check_withhold_receipt, check_withhold, check_withhold_channel_request, check_withhold_sendmsg
from biztest.function.global_payment.global_payment_db_operation import get_available_uuid, \
    update_withhold_receipt_clear_inner_key, update_channel_error, \
    insert_global_withhold_razorpay_success_callback_task, update_withhold_receipt_create_at, update_provider, \
    update_channel
from biztest.interface.payment_global.payment_global_interface import auto_pay, run_task_by_order_no, \
    global_withhold_close_order
from biztest.util.asserts.assert_util import Assert
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_razorpay import RazorpayMock


class TestIndiaRazorpayPaymentLink:
    def setup_class(self):
        # get available account info for auto_withhold
        # self.card_uuid = "1020120815836284293"
        # self.available_account_info = {"account_card_uuid": self.card_uuid}
        self.available_account_info = get_available_uuid("account", "1")[0]
        self.card_uuid = self.available_account_info["account_card_uuid"]
        self.global_payment_mock = RazorpayMock("carltonliu", "lx19891115", "5f33abd683be280020b70ad8")
        self.sign_company = "yomoyo"
        self.payment_type = "ebank"
        self.payment_option = ""
        self.channel_name = "razorpay_%s_ebank" % self.sign_company
        update_channel(self.channel_name, channel_status="1", channel_sign_company_code=self.sign_company)
        update_razorpay_ebank(self.sign_company, "5f33abd683be280020b70ad8")
        update_provider("cashfree", "close")
        update_provider("paytm", "close")

    @classmethod
    def teardown_class(cls):
        update_razorpay_ebank()
        update_provider("cashfree", "open")
        update_provider("paytm", "open")
        DataBase.close_connects()

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_success(self):
        # 发起代扣成功 -> 查询到交易成功并更新状态
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        self.global_payment_mock.update_razorpay_standard_payment_link_query_success()

        # 发起代扣并检查api返回值
        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)
        expected_resp_data = {
            "platform_code": "E20002",
            "platform_message": "created",
            "channel_name": self.channel_name,
            "channel_code": "created",
            "channel_message": "created",
            "need_bind": 0,
            "need_sms": 0,
            "amount": req["amount"],
            "status": 1,
            "payment_type": "ebank",
            "payment_option": ""
        }
        check_resp_data(resp, 2, "交易进行中", expected_resp_data)

        # 查询代扣订单初始状态
        check_withhold_channel_request(req["merchant_key"], "payment_links", "CHARGE")
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 1, self.channel_name, "created", "")
        check_withhold(req["merchant_key"], self.available_account_info, 1)

        # 查询到代扣订单成功并更新withhold_receipt表
        run_task_by_order_no(req["merchant_key"], {"code": 0, "message": "支付订单查询处理成功"})
        check_withhold_channel_request(req["merchant_key"], "orders", "CHARGE_QUERY")
        expected_withhold_receipt_data = {
            "withhold_receipt_amount": req["amount"],
            "withhold_receipt_payment_option": "Debit Card",
            "withhold_receipt_payment_mode": "Visa",
            "withhold_receipt_service_charge": 800,
            "withhold_receipt_service_tax": 144
        }
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 2, self.channel_name, "paid", "{\"attempts\":1}",
                               expected_withhold_receipt_data)

        # 代扣订单成功后更新withhold表
        message = "代扣订单[%s]状态更新成功！" % req["merchant_key"]
        run_task_by_order_no(req["merchant_key"], {"code": 0, "message": message})
        check_withhold(req["merchant_key"], self.available_account_info, 2)

        # 检查Sendmsg
        expected_sendmsg_data = {
            "platform_code": "E20000",
            "platform_message": "{\"attempts\":1}",
            "channel_name": self.channel_name,
            "channel_code": "paid",
            "channel_message": "{\"attempts\":1}",
            "status": 2
        }
        check_withhold_sendmsg(req["merchant_key"], expected_sendmsg_data)

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_request_failed(self):
        # 发起代扣失败
        self.global_payment_mock.update_razorpay_standard_payment_link_failed()
        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)
        expected_resp_data = {
            "platform_code": "E20001",
            "platform_message": "FAILED",
            "channel_name": self.channel_name,
            "channel_code": "failed",
            "need_bind": 0,
            "need_sms": 0,
            "amount": req["amount"],
            "status": 3,
            "payment_type": "ebank",
            "payment_option": ""
        }
        check_resp_data(resp, 1, "交易失败", expected_resp_data)
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 3, self.channel_name, "failed", "")
        check_withhold(req["merchant_key"], self.available_account_info, 3)

        expected_sendmsg_data = {
            "platform_code": "E20001",
            "platform_message": "FAILED",
            "channel_name": self.channel_name,
            "channel_code": "failed",
            "channel_message": "",
            "status": 3
        }
        check_withhold_sendmsg(req["merchant_key"], expected_sendmsg_data)

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_process_not_attempted(self):
        # 发起代扣成功 -> 用户尚未打开链接 -> 查询到交易进行中
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        self.global_payment_mock.update_razorpay_standard_payment_link_query_not_attempted()

        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)
        run_task_by_order_no(req["merchant_key"], {"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 1, self.channel_name, "created", "")
        check_withhold(req["merchant_key"], self.available_account_info, 1)

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_process_attempted(self):
        # 发起代扣成功 -> 用户打开链接尚未支付完成 -> 查询到交易进行中
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        self.global_payment_mock.update_razorpay_standard_payment_link_query_attempted()

        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)
        run_task_by_order_no(req["merchant_key"], {"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 1, self.channel_name, "created", "")
        check_withhold(req["merchant_key"], self.available_account_info, 1)

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_process_not_attempted(self):
        # 发起代扣成功 -> innerkey置为空 -> 查询到订单不存在
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        self.global_payment_mock.update_razorpay_standard_payment_link_query_not_attempted()

        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)
        update_withhold_receipt_clear_inner_key(req["merchant_key"])
        run_task_by_order_no(req["merchant_key"], {"code": 1, "message": "支付订单查询交易不存在"})
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 3, self.channel_name, "KN_ORDER_NOT_EXISTS", "")
        run_task_by_order_no(req["merchant_key"], {"code": 0, "message": "代扣订单[%s]状态更新成功！" % req["merchant_key"]})
        check_withhold(req["merchant_key"], self.available_account_info, 3)

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_callback_when_processing(self):
        # 发起代扣成功 -> 回调成功 -> 更新订单状态到成功
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        self.global_payment_mock.update_razorpay_standard_payment_link_query_success()
        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)
        insert_callback_task_no = insert_global_withhold_razorpay_success_callback_task(req["merchant_key"],
                                                                                        self.channel_name)
        run_task_by_order_no(insert_callback_task_no, {"code": 0, "message": "处理成功"})
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 2, self.channel_name, "captured", "")
        run_task_by_order_no(req["merchant_key"], {"code": 0, "message": "代扣收据[%s]为最终状态！直接返回！" % req["merchant_key"]})
        check_withhold(req["merchant_key"], self.available_account_info, 2)

    params = ["payment_option", "method", "payment_mode"]
    values = [("Debit Card", "card", "Visa"),
              ("Net Banking", "netbanking", "FDRL"),
              ("Wallet", "wallet", "airtelmoney"),
              ("Upi", "upi", "")]
    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    @pytest.mark.parametrize(params, values)
    def test_razorpay_auto_withhold_payment_type(self, payment_option, method, payment_mode):
        # 发起代扣成功 -> -> 回调成功 -> 更新本地状态并记录payment相关信息
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        self.global_payment_mock.update_razorpay_standard_payment_link_query_not_attempted()
        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)

        insert_callback_task_no = insert_global_withhold_razorpay_success_callback_task(req["merchant_key"],
                                                                                        self.channel_name, method)
        run_task_by_order_no(insert_callback_task_no, {"code": 0, "message": "处理成功"})
        expected_withhold_receipt_data = {
            "withhold_receipt_amount": req["amount"],
            "withhold_receipt_payment_option": payment_option,
            "withhold_receipt_payment_mode": payment_mode,
            "withhold_receipt_service_charge": 1100,
            "withhold_receipt_service_tax": 198
        }
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 2, self.channel_name, "captured", "",
                               expected_withhold_receipt_data)
        run_task_by_order_no(req["merchant_key"], {"code": 0, "message": "代扣收据[%s]为最终状态！直接返回！" % req["merchant_key"]})
        check_withhold(req["merchant_key"], self.available_account_info, 2)

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_timeout_close_order(self):
        # 发起代扣成功 -> 查询到已超时(razorpay超时不看本地时间，看通道方的创建时间来算过期时间) -> 订单置为失败
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        self.global_payment_mock.update_razorpay_standard_payment_link_query_attempted(True)

        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)
        run_task_by_order_no(req["merchant_key"], {"code": 1, "message": "支付订单查询失败"})
        run_task_by_order_no(req["merchant_key"], {"code": 0, "message": "代扣订单[%s]状态更新成功！" % req["merchant_key"]})
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 3, self.channel_name, "KN_TIMEOUT_CLOSE_ORDER", "Payment failed")
        check_withhold(req["merchant_key"], self.available_account_info, 3)
        expected_sendmsg_data = {
            "platform_code": "E20010",
            "platform_message": "Payment failed",
            "channel_name": self.channel_name,
            "channel_code": "KN_TIMEOUT_CLOSE_ORDER",
            "channel_message": "Payment failed",
            "status": 3
        }
        check_withhold_sendmsg(req["merchant_key"], expected_sendmsg_data)

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_callback_order_not_exist(self):
        # 回调订单不存在 -> 不处理
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)
        insert_callback_task_no = insert_global_withhold_razorpay_success_callback_task(req["merchant_key"],
                                                                                        self.channel_name, "netbanking",
                                                                                        "false")
        run_task_by_order_no(insert_callback_task_no, {"code": 1, "message": "代扣订单不存在"})

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_callback_when_failed(self):
        # 发起代扣成功 -> 查询到超时并关单 -> 回调成功 -> 更新本地订单到成功
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)
        update_withhold_receipt_create_at(req["merchant_key"], day=-1)

        update_razorpay_ebank(self.sign_company)
        run_task_by_order_no(req["merchant_key"], {"code": 1, "message": "支付订单查询失败"})
        run_task_by_order_no(req["merchant_key"], {"code": 0, "message": "代扣订单[%s]状态更新成功！" % req["merchant_key"]})
        insert_callback_task_no = insert_global_withhold_razorpay_success_callback_task(req["merchant_key"],
                                                                                        self.channel_name)
        run_task_by_order_no(insert_callback_task_no, {"code": 0, "message": "处理成功"})
        run_task_by_order_no(req["merchant_key"], {"code": 0, "message": "代扣订单[%s]状态更新成功！" % req["merchant_key"]})
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 2, self.channel_name, "KN_REVERSE_ORDER", "")
        check_withhold(req["merchant_key"], self.available_account_info, 2)
        update_razorpay_ebank(self.sign_company, "5f33abd683be280020b70ad8")

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_close_order_when_channel_success(self):
        # 代扣订单通道为成功状态 -> 手动关单 -> 关单失败
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        self.global_payment_mock.update_razorpay_standard_payment_link_query_success()
        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)

        close_req, close_resp = global_withhold_close_order(req["merchant_key"])
        Assert.assert_match_json({"code": 1,
                                  "data": None,
                                  "message": "订单已经成为终态，关闭订单失败"},
                                 close_resp,
                                 "关单失败")
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 2, self.channel_name, "paid", "{\"attempts\":1}")

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_close_order_when_channel_failed(self):
        # 代扣订单通道为失败状态 -> 手动关单 -> 关单失败
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        self.global_payment_mock.update_razorpay_standard_payment_link_query_failed()

        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)

        close_req, close_resp = global_withhold_close_order(req["merchant_key"])
        Assert.assert_match_json({"code": 1,
                                  "data": None,
                                  "message": "订单处理中，关闭订单失败"},
                                 close_resp,
                                 "关单失败")
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 1, self.channel_name, "created", "")

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_close_order_success_channel_not_attempted(self):
        # 发起代扣但不打开链接 -> 手动关单 -> 关单成功
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        self.global_payment_mock.update_razorpay_standard_payment_link_query_not_attempted()

        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)

        close_req, close_resp = global_withhold_close_order(req["merchant_key"])
        Assert.assert_match_json({"code": 0,
                                  "message": "关闭订单成功",
                                  "data": {
                                      "platform_code": "E20010",
                                      "platform_message": "Order manual closed",
                                      "channel_name": self.channel_name,
                                      "channel_code": "KN_MANUAL_CLOSE_ORDER",
                                      "channel_message": "Order manual closed"}},
                                 close_resp,
                                 "关单成功")
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 3, self.channel_name, "KN_MANUAL_CLOSE_ORDER", "")

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_close_order_success_channel_is_processing(self):
        # 发起代扣并尝试支付一次失败 -> 手动关单 -> 关单成功
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        self.global_payment_mock.update_razorpay_standard_payment_link_query_attempted()
        update_channel_error("razorpay", "attempted", "attempted", 2, "MANUAL_CLOSE")

        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)

        close_req, close_resp = global_withhold_close_order(req["merchant_key"])
        Assert.assert_match_json({"code": 0,
                                  "message": "关闭订单成功",
                                  "data": {
                                      "platform_code": "E20010",
                                      "platform_message": "Payment failed",
                                      "channel_name": self.channel_name,
                                      "channel_code": "KN_MANUAL_CLOSE_ORDER",
                                      "channel_message": "Payment failed"}},
                                 close_resp,
                                 "关单成功")
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 3, self.channel_name, "KN_MANUAL_CLOSE_ORDER",
                               "Payment failed")

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_razorpay
    @pytest.mark.global_payment_razorpay_payment_link
    def test_razorpay_auto_withhold_process_query_failed(self):
        # 发起代扣成功 -> 查询失败 -> task保持为open, withhold/withhold_receipt状态不变
        self.global_payment_mock.update_razorpay_standard_payment_link_success()
        self.global_payment_mock.update_razorpay_standard_payment_link_query_failed()

        req, resp = auto_pay(self.sign_company, self.payment_type, self.payment_option, self.card_uuid)
        run_task_by_order_no(req["merchant_key"], {"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        check_withhold_receipt(req["merchant_key"], self.card_uuid, 1, self.channel_name, "created", "")
        check_withhold(req["merchant_key"], self.available_account_info, 1)
