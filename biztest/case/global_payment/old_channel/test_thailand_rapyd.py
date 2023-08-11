# -*- coding: utf-8 -*-

import pytest

from biztest.config.easymock.easymock_config import global_payment_mock
from biztest.config.payment.url_config import global_amount
from biztest.config.payment_global.global_payment_nacos import PaymentNacos
from biztest.function.global_payment.global_payment_check_function import check_withhold_receipt, check_withhold
from biztest.function.global_payment.global_payment_db_operation import update_sign_company_provider_product, \
    get_available_uuid, get_withhold_receipt_by_merchant_key, update_withhold_receipt_create_at, update_channel_error, \
    update_channel_otherclose
from biztest.interface.payment_global.payment_global_interface import run_task_by_order_no, auto_pay
from biztest.util.asserts.assert_util import Assert
from biztest.util.db.db_util import DataBase, time
from biztest.util.easymock.global_payment.global_payment_tha_rapyd import RapydMock
from biztest.util.tools.tools import get_sysconfig

env = get_sysconfig("--env")
country = get_sysconfig("--country")
sign_company = "amberstar1"
nacos_domain = "nacos-test-tha.starklotus.com"  # nacos
project_id = "5f9640cc62081c0020d7f560"  # mock


class TestThailandRapyd:
    def setup_class(self):
        # 修改nacos，使走到mock
        self.global_payment_nacos = PaymentNacos(nacos_domain)
        # 首先默认nacos配置usercenter.properties中用户中心一直是mock地址，如果被改了会导致自动化失败
        self.global_payment_nacos.update_rapyd_qrcode(project_id=project_id)
        # rapyd-easymock更新
        self.global_payment_mock = RapydMock(global_payment_mock)
        update_sign_company_provider_product(sign_company, "rapyd", "qrcode", "open")
        update_channel_otherclose(sign_company, "rapyd", "qrcode", "open")
        update_channel_otherclose(sign_company, "rapyd", "qrcode", "close")

    @classmethod
    def teardown_class(self):
        update_channel_otherclose(sign_company, "rapyd", "qrcode", "open")
        DataBase.close_connects()
        self.global_payment_nacos.update_rapyd_qrcode()

    @pytest.mark.global_payment_thailand
    @pytest.mark.global_payment_rapyd
    @pytest.mark.global_payment_rapyd_qrcode
    def test_rapyd_qrcode_query_success(self):
        account = get_available_uuid("account", 1)[0]
        channel = "rapyd_%s_qrcode" % sign_company
        self.global_payment_mock.update_qrcode_withhold_success()
        req, resp = auto_pay(sign_company, "qrcode", card_uuid=account["account_card_uuid"],
                                            channel_name="rapyd_amberstar1_qrcode")
        merchant_key = req["merchant_key"]
        withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        # 检查返回给rbiz的参数以及代扣表的状态
        Assert.assert_match_json({"code": 2,
                                  "data": {"amount": global_amount,
                                           "balance_not_enough": 0,
                                           "channel_code": "ACT",
                                           "channel_message": "Active and awaiting payment. Can be updated.",
                                           "channel_name": channel,
                                           "payment_data": {"image_dat": "data:image/png;base64.*"},
                                           "payment_option": "",
                                           "payment_type": "qrcode",
                                           "platform_code": "E20002",
                                           "platform_message": "PROCESSING",
                                           "status": 1},
                                  "message": "交易进行中"},
                                 resp,
                                 "代扣请求成功")
        check_withhold(merchant_key, account, 1)
        check_withhold_receipt(merchant_key, account, 1, channel, "ACT", "Active and awaiting payment. Can be updated.")
        self.global_payment_mock.update_qrcode_query_success(withhold_receipt, "1651334400")
        run_task_by_order_no(merchant_key, {"code": 0, "message": "二维码支付查询成功", "data": None})
        run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        check_withhold(merchant_key, account, 2)
        check_withhold_receipt(merchant_key, account, 2, channel, "CLO", "Closed and paid.")

    @pytest.mark.global_payment_thailand
    @pytest.mark.global_payment_rapyd
    @pytest.mark.global_payment_rapyd_qrcode
    def test_rapyd_qrcode_charge_fail(self):
        # 发起代扣异常，直接代扣失败
        account = get_available_uuid("account", 1)[0]
        channel = "rapyd_%s_qrcode" % sign_company
        self.global_payment_mock.update_qrcode_withhold_fail()
        req, resp = auto_pay(sign_company, "qrcode", card_uuid=account["account_card_uuid"])
        merchant_key = req["merchant_key"]
        check_withhold(merchant_key, account, 3)
        check_withhold_receipt(merchant_key, account, 3, channel, "ERROR_CREATE_PAYMENT",
                               "The request tried to create a payment, but the payment method was not found.")

    @pytest.mark.global_payment_thailand
    @pytest.mark.global_payment_rapyd
    @pytest.mark.global_payment_rapyd_qrcode
    def test_rapyd_qrcode_charge_500(self):
        account = get_available_uuid("account", 1)[0]
        channel = "rapyd_%s_qrcode" % sign_company
        self.global_payment_mock.update_qrcode_withhold_500()
        req, resp = auto_pay(sign_company, "qrcode", card_uuid=account["account_card_uuid"])
        Assert.assert_match_json({"code": 1,
                                  "data": {"amount": global_amount,
                                           "balance_not_enough": 0,
                                           "channel_code": "KN_NO_CHANNEL_CODE",
                                           "channel_name": channel,
                                           "platform_code": "E20001",
                                           "platform_message": "FAILED",
                                           "status": 3},
                                  "message": "交易失败"},
                                 resp,
                                 "代扣请求成功")
        merchant_key = req["merchant_key"]
        check_withhold(merchant_key, account, 3)
        check_withhold_receipt(merchant_key, account, 3, channel, "KN_NO_CHANNEL_CODE", "")

    @pytest.mark.global_payment_thailand
    @pytest.mark.global_payment_rapyd
    @pytest.mark.global_payment_rapyd_qrcode
    def test_rapyd_qrcode_query_fail(self):
        account = get_available_uuid("account", 1)[0]
        channel = "rapyd_%s_qrcode" % sign_company
        self.global_payment_mock.update_qrcode_withhold_success()
        req, resp = auto_pay(sign_company, "qrcode", card_uuid=account["account_card_uuid"])
        merchant_key = req["merchant_key"]

        withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        self.global_payment_mock.update_qrcode_query_fail(withhold_receipt, "1651334400")
        update_channel_error("rapyd", "CAN", "", 1, "CHARGE_QUERY,CHARGE,CHARGE_QR_CODE,CHARGE_QR_CODE_QUERY")
        run_task_by_order_no(merchant_key, {"code": 1, "message": "二维码支付查询失败"})
        run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        check_withhold(merchant_key, account, 3)
        check_withhold_receipt(merchant_key, account, 3, channel, "CAN",
                               "Canceled by the merchant or the customer's bank.")

    @pytest.mark.global_payment_thailand
    @pytest.mark.global_payment_rapyd
    @pytest.mark.global_payment_rapyd_qrcode
    def test_rapyd_qrcode_query_process(self):
        account = get_available_uuid("account", 1)[0]
        channel = "rapyd_%s_qrcode" % sign_company
        self.global_payment_mock.update_qrcode_withhold_success()
        req, resp = auto_pay(sign_company, "qrcode", card_uuid=account["account_card_uuid"])
        merchant_key = req["merchant_key"]

        withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        self.global_payment_mock.update_qrcode_query_process(withhold_receipt, "1984895205")  # 传一个未过期的时间
        update_channel_error("rapyd", "ACT", "", 2, "CHARGE_QUERY,CHARGE,CHARGE_QR_CODE,CHARGE_QR_CODE_QUERY")
        run_task_by_order_no(merchant_key, {"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        check_withhold(merchant_key, account, 1)
        check_withhold_receipt(merchant_key, account, 1, channel, "ACT", "Active and awaiting payment. Can be updated.")

    @pytest.mark.global_payment_thailand
    @pytest.mark.global_payment_rapyd
    @pytest.mark.global_payment_rapyd_qrcode
    def test_rapyd_qrcode_query_timeout_order_fail(self):
        account = get_available_uuid("account", 1)[0]
        channel = "rapyd_%s_qrcode" % sign_company
        self.global_payment_mock.update_qrcode_withhold_success()
        req, resp = auto_pay(sign_company, "qrcode", card_uuid=account["account_card_uuid"])
        merchant_key = req["merchant_key"]

        withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        self.global_payment_mock.update_qrcode_query_process(withhold_receipt, "1588262400")  # 传一个过期的时间
        update_channel_error("rapyd", "ACT", "", 2, "CHARGE_QUERY,CHARGE,CHARGE_QR_CODE,CHARGE_QR_CODE_QUERY")
        run_task_by_order_no(merchant_key, {"code": 1, "message": "二维码支付查询失败，订单过期"})
        run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        time.sleep(2)
        check_withhold(merchant_key, account, 3)
        check_withhold_receipt(merchant_key, account, 3, channel, "KN_TIMEOUT_CLOSE_ORDER", "KN_TIMEOUT_CLOSE_ORDER")

    @pytest.mark.global_payment_thailand
    @pytest.mark.global_payment_rapyd
    @pytest.mark.global_payment_rapyd_qrcode
    def test_rapyd_qrcode_query_timeout_order_success(self):
        account = get_available_uuid("account", 1)[0]
        channel = "rapyd_%s_qrcode" % sign_company
        self.global_payment_mock.update_qrcode_withhold_success()
        req, resp = auto_pay(sign_company, "qrcode", card_uuid=account["account_card_uuid"])
        merchant_key = req["merchant_key"]

        withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        self.global_payment_mock.update_qrcode_query_success(withhold_receipt, "1588262400")  # 传一个过期的时间
        update_withhold_receipt_create_at(merchant_key, day=-1)

        run_task_by_order_no(merchant_key, {"code": 0, "message": "二维码支付查询成功", "data": None})
        run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        check_withhold(merchant_key, account, 2)
        check_withhold_receipt(merchant_key, account, 2, channel, "CLO", "Closed and paid.")
