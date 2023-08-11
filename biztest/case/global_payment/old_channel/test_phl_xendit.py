# -*- coding: utf-8 -*-
import time

import pytest

from biztest.config.easymock.easymock_config import global_payment_easy_mock_phl
from biztest.config.payment.url_config import xendit_redirect_url, global_amount, xendit_resp_payment_mode, \
    xendit_ebank_resp_payment_mode
from biztest.config.payment_global.global_payment_nacos import PaymentNacos
from biztest.function.global_payment.global_payment_check_function import check_autopay_response, \
    check_autopay_response_fail, \
    assert_check_withhold_withholdreceipt_initinfo, assert_withholdandreceipt_process, \
    assert_withholdandreceipt_success, assert_withholdandreceipt_fail, assert_withdrawandreceipt_success, \
    assert_withdrawandreceipt_fail, assert_withdrawandreceipt_process, assert_check_withdraw_withdrawreceipt_initinfo
from biztest.function.global_payment.global_payment_db_function import get_carduuid_bycardnum, update_channel_error
from biztest.function.global_payment.global_payment_db_operation import update_xendit_withhold_receipt_create_at
from biztest.interface.payment_global.payment_global_interface import run_task_by_order_no, auto_withdraw, \
    auto_pay, xendit_paycode_callback, clear_cache, xendit_ebank_callback, xendit_withdraw_callback
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_phl_xendit import XenditMock
from biztest.util.tools.tools import get_sysconfig, get_four_element_global, get_guid

env = get_sysconfig("--env")
country = get_sysconfig("--country")
provider = "xendit"
sign_company = "copperstone"
channel_name_paycode = "xendit_copperstone_paycode"
channel_name_ebank = "xendit_copperstone_ebank"
channel_name_withdraw = "xendit_copperstone_withdraw"
card_uuid = "58042740327317418"
user_uuid = "58042740327317418"
# amount = 1021  # 不能改
project_id = "5e9807281718270057767a3e"  # mock
nacos_domain = "nacos-test-phl.starklotus.com"  # nacos


# update 20220630跑通全部

class TestPhilippinesXendit:

    # 每个类的前置条件
    def setup_class(cls):
        # 菲律宾使用默认卡
        cls.account = get_carduuid_bycardnum("card", "enc_04_4106612382062092288_439")[0]
        cls.four_element = get_four_element_global()
        cls.global_payment_nacos = PaymentNacos(nacos_domain)
        # 修改kv，使走到mock
        cls.global_payment_nacos.update_xendit_paycode(project_id=project_id)
        cls.global_payment_nacos.update_xendit_ebank(project_id=project_id)
        cls.global_payment_mock = XenditMock(global_payment_easy_mock_phl)
        cls.channel_inner_key = "pcode-991099b0-cb2a-4a40-bcf3-0c5deb4d7036"  # 先写死，TODO 看mock如何修改api
        cls.channel_inner_key_ebank = "ewc_c6bc052c-d724-4043-b73f-aa97ed72f1f0"  # 先写死，TODO 看mock如何修改api
        cls.payment_code = "xendit_wh_number" + get_guid()  # 取款码
        clear_cache()  # 有时候直接修改数据库配置，会有缓存的问题

    # 每个类的最后需要还原之前的修改，并关闭数据库链接
    @classmethod
    def teardown_class(cls):
        # 恢复到通道测试环境
        cls.global_payment_nacos.update_xendit_paycode()
        cls.global_payment_nacos.update_xendit_ebank()
        DataBase.close_connects()

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_paycode
    def test_xendit_paycode_chrage_and_query_success(self):
        # xendit_paycode 查询到支付成功
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_xendit_paycode_charge("success", self.channel_inner_key, self.payment_code)
        # 3、发起代扣  xendit付款码还款payment_type=paycode&payment_option=store&payment_mode可不传
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_paycode, payment_type="paycode",
                                             payment_option="store", user_uuid=user_uuid,
                                             amount=global_amount)
        # 检查autopay的response  payment_mode="7-11"是因为目前路由的都是7-11
        check_autopay_response(autopay_resp, channel_name_paycode, global_amount, "ACTIVE", codes="success",
                               description=self.payment_code, payment_type="paycode")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_paycode,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="store", payment_mode=""
                                                       , description=self.payment_code
                                                       , channel_inner_key=self.channel_inner_key)
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "ACTIVE", "ACTIVE,")
        # 2、修改mock，使代扣查询到成功
        self.global_payment_mock.update_xendit_paycode_query("success", self.channel_inner_key, self.payment_code)
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_success(autopay_req["merchant_key"], "COMPLETED", "payment simulation",
                                          mode=xendit_resp_payment_mode)

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_paycode
    def test_xendit_paycode_chrage_and_callback_success(self):
        # xendit_paycode 回调支付成功
        # 1、修改mock，使得发起代扣成功
        self.global_payment_mock.update_xendit_paycode_charge("success", self.channel_inner_key, self.payment_code)
        # 2、发起代扣  xendit付款码还款payment_type=paycode&payment_option=store&payment_mode可不传
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_paycode, payment_type="paycode",
                                             payment_option="store", user_uuid=user_uuid,
                                             amount=global_amount)
        # 检查autopay的response，payment_mode=7-11是现在因为在provider_payment_mode_id最小是7-11
        check_autopay_response(autopay_resp, channel_name_paycode, global_amount, "ACTIVE", codes="success",
                               description=self.payment_code,
                               payment_type="paycode")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_paycode,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="store", payment_mode=""
                                                       , description=self.payment_code
                                                       , channel_inner_key=self.channel_inner_key)
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "ACTIVE", "ACTIVE,")
        # 3、发起回调代扣成功
        xendit_paycode_callback(channel_name_paycode, global_amount, autopay_resp["data"]["channel_key"],
                                self.channel_inner_key)
        # 执行回调
        run_task_by_order_no(autopay_resp["data"]["channel_key"])
        time.sleep(1)
        run_task_by_order_no(autopay_req["merchant_key"])
        time.sleep(1)
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_success(autopay_req["merchant_key"], "COMPLETED", "callback COMPLETED",
                                          mode=xendit_ebank_resp_payment_mode)

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_paycode
    def test_xendit_paycode_chrage_fail(self):
        # xendit_paycode 查询到支付成功
        # 1、修改mock，使得发起代扣失败
        self.global_payment_mock.update_xendit_paycode_charge("fail", self.channel_inner_key, self.payment_code)
        # 2、发起代扣  xendit付款码还款payment_type=paycode&payment_option=store&payment_mode可不传
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_paycode, payment_type="paycode",
                                             payment_option="store", user_uuid=user_uuid,
                                             amount=global_amount)
        # 检查autopay的response
        check_autopay_response_fail(autopay_resp, channel_name_paycode, global_amount, "error_fail", "error_fail")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_paycode,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="store", payment_mode=""
                                                       , description=""
                                                       , channel_inner_key="")
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "error_fail", "error_fail,")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_paycode
    def test_xendit_paycode_chrage_500(self):
        # xendit_paycode 查询到支付成功
        # 1、修改mock，使得发起代扣失败
        self.global_payment_mock.update_xendit_paycode_charge("500", self.channel_inner_key, self.payment_code)
        # 2、发起代扣  xendit付款码还款payment_type=paycode&payment_option=store&payment_mode可不传
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_paycode, payment_type="paycode",
                                             payment_option="store", user_uuid=user_uuid,
                                             amount=global_amount)
        # 检查autopay的response
        check_autopay_response_fail(autopay_resp, channel_name_paycode, global_amount, "KN_NO_CHANNEL_CODE",
                                    "payment_codes返回错误HttpStatus500")
        # 支付失败-检查数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_paycode,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="store", payment_mode=""
                                                       , description=""
                                                       , channel_inner_key="")
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "KN_NO_CHANNEL_CODE",
                                       "CHARGE fail, http://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/5e9807281718270057767a3e/payment_codes返回错误HttpStatus500,{}")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_paycode
    def test_xendit_paycode_query_timeout_order_fail(self):
        # xendit_paycode 超时关单  1、返回明确过期"status"="EXPIRED"
        # 1、修改mock，使得发起代扣成功
        self.global_payment_mock.update_xendit_paycode_charge("success", self.channel_inner_key, self.payment_code)
        # 2、发起代扣  xendit付款码还款payment_type=paycode&payment_option=store&payment_mode可不传
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_paycode, payment_type="paycode",
                                             payment_option="store", user_uuid=user_uuid,
                                             amount=global_amount)
        # 检查autopay的response  payment_mode="7-11"是因为目前路由的都是7-11
        check_autopay_response(autopay_resp, channel_name_paycode, global_amount, "ACTIVE", codes="success",
                               description=self.payment_code, payment_type="paycode")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_paycode,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="store", payment_mode=""
                                                       , description=self.payment_code
                                                       , channel_inner_key=self.channel_inner_key)
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "ACTIVE", "ACTIVE,")
        # 3、修改mock，使超时关单
        self.global_payment_mock.update_xendit_paycode_query("expired", self.channel_inner_key, self.payment_code)
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付失败-检查数据库中的数据
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "EXPIRED", "payment simulation")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_paycode
    def test_xendit_paycode_query_timeout_order_fail_none(self):
        # xendit_paycode 超时关单  1、用户一直未支付，返回空： []
        # 1、修改mock，使得发起代扣成功
        self.global_payment_mock.update_xendit_paycode_charge("success", self.channel_inner_key, self.payment_code)
        # 2、发起代扣  xendit付款码还款payment_type=paycode&payment_option=store&payment_mode可不传
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_paycode, payment_type="paycode",
                                             payment_option="store", user_uuid=user_uuid,
                                             amount=global_amount)
        # 检查autopay的response  payment_mode="7-11"是因为目前路由的都是7-11
        check_autopay_response(autopay_resp, channel_name_paycode, global_amount, "ACTIVE", codes="success",
                               description=self.payment_code, payment_type="paycode")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_paycode,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="store", payment_mode=""
                                                       , description=self.payment_code
                                                       , channel_inner_key=self.channel_inner_key)
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "ACTIVE", "ACTIVE,")

        # 3、修改mock，使超时关单
        self.global_payment_mock.update_xendit_paycode_query("none", self.channel_inner_key, self.payment_code)
        # 修改收据表的创建时间，使超时
        update_xendit_withhold_receipt_create_at(autopay_req["merchant_key"], "2021-12-13 00:00:00")  # 传前一天的时间，使超时关单
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付失败-检查数据库中的数据
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "KN_TIMEOUT_CLOSE_ORDER",
                                       "channel response is null")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_paycode
    def test_xendit_paycode_query_process(self):
        # xendit_paycode 查询返回处理中
        # 1、修改mock，使得发起代扣成功
        self.global_payment_mock.update_xendit_paycode_charge("success", self.channel_inner_key, self.payment_code)
        # 2、发起代扣  xendit付款码还款payment_type=paycode&payment_option=store&payment_mode可不传
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_paycode, payment_type="paycode",
                                             payment_option="store", user_uuid=user_uuid,
                                             amount=global_amount)
        # 检查autopay的response  payment_mode="7-11"是因为目前路由的都是7-11
        check_autopay_response(autopay_resp, channel_name_paycode, global_amount, "ACTIVE", codes="success",
                               description=self.payment_code, payment_type="paycode")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_paycode,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="store", payment_mode=""
                                                       , description=self.payment_code
                                                       , channel_inner_key=self.channel_inner_key)
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "ACTIVE", "ACTIVE,")

        # 3、修改mock，使超时关单
        self.global_payment_mock.update_xendit_paycode_query("process", self.channel_inner_key, self.payment_code)
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付中-检查数据库中的数据
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "ACTIVE", "ACTIVE,")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_paycode
    def test_xendit_paycode_query_failed(self):
        # xendit_paycode channel_error表中将FAILED配置为失败
        # 1、修改mock，使得发起代扣成功
        self.global_payment_mock.update_xendit_paycode_charge("success", self.channel_inner_key, self.payment_code)
        # 2、发起代扣  xendit付款码还款payment_type=paycode&payment_option=store&payment_mode可不传
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_paycode, payment_type="paycode",
                                             payment_option="store", user_uuid=user_uuid,
                                             amount=global_amount)
        # 检查autopay的response  payment_mode="7-11"是因为目前路由的都是7-11
        check_autopay_response(autopay_resp, channel_name_paycode, global_amount, "ACTIVE", codes="success",
                               description=self.payment_code, payment_type="paycode")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_paycode,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="store", payment_mode=""
                                                       , description=self.payment_code
                                                       , channel_inner_key=self.channel_inner_key)
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "ACTIVE", "ACTIVE,")

        # 3、修改mock，使超时关单
        self.global_payment_mock.update_xendit_paycode_query("fail", self.channel_inner_key, self.payment_code)
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付失败-检查数据库中的数据
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "FAILED", "payment FAILED")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_ebank
    def test_xendit_ebank_chrage_and_query_success(self):
        # 1、修改mock，使能够成功
        self.global_payment_mock.update_xendit_ebank_charge("success", self.channel_inner_key_ebank)
        # 3、发起代扣
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank",
                                             payment_option="wallet", payment_mode="GCash",
                                             user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               description=self.payment_code, payment_type="ebank")
        # 2、修改mock，xendit_ebank 查询到支付成功
        self.global_payment_mock.update_xendit_ebank_query("success", self.channel_inner_key_ebank,
                                                           autopay_resp["data"]["channel_key"])
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_ebank,
                                                       user_uuid=user_uuid,
                                                       channel_redirect=xendit_redirect_url, operator="USER",
                                                       payment_option="wallet", payment_mode="GCash"
                                                       , description=""
                                                       , channel_inner_key=self.channel_inner_key_ebank)
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_REQUEST_SUCCESS", "PENDING")
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_success(autopay_req["merchant_key"], "SUCCEEDED",
                                          "Payment transaction for specified charge_id is successfully",
                                          mode=xendit_ebank_resp_payment_mode)

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_ebank
    def test_xendit_ebank_chrage_and_callback_success(self):
        # xendit_ebank 查询到支付成功
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_xendit_ebank_charge("success", self.channel_inner_key_ebank)
        # 2、发起代扣
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank",
                                             payment_option="wallet", payment_mode="GCash",
                                             user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               description=self.payment_code, payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_ebank,
                                                       user_uuid=user_uuid,
                                                       channel_redirect=xendit_redirect_url, operator="USER",
                                                       payment_option="wallet", payment_mode="GCash"
                                                       , description=""
                                                       , channel_inner_key=self.channel_inner_key_ebank)
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_REQUEST_SUCCESS", "PENDING")

        # 3、发起回调代扣成功
        xendit_ebank_callback(channel_name_ebank, global_amount, autopay_resp["data"]["channel_key"],
                              self.channel_inner_key_ebank)
        # 执行回调
        run_task_by_order_no(autopay_resp["data"]["channel_key"])
        time.sleep(1)
        run_task_by_order_no(autopay_req["merchant_key"])
        time.sleep(1)
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_success(autopay_req["merchant_key"], "SUCCEEDED",
                                          "callback Payment transaction for specified charge_id is successfully",
                                          mode=xendit_ebank_resp_payment_mode)

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_ebank
    def test_xendit_ebank_chrage_fail(self):
        # xendit_ebank 发起直接支付失败  status<>PENDING直接失败
        self.global_payment_mock.update_xendit_ebank_charge("fail", self.channel_inner_key_ebank)
        # 2、发起代扣
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank",
                                             payment_option="wallet", payment_mode="GCash",
                                             user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response_fail(autopay_resp, channel_name_ebank, global_amount, "FAILED", "FAILED")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_ebank,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="wallet", payment_mode="GCash"
                                                       , description=""
                                                       , channel_inner_key="")
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "FAILED", "FAILED")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_ebank
    def test_xendit_ebank_chrage_fail_not_supported_channelcode(self):
        # xendit_ebank 发起直接支付失败  ":  通道返回的channel_code只能是 PH_PAYMAYA和PH_GCASH还有PH_GRABPAY
        self.global_payment_mock.update_xendit_ebank_charge("not_supported_channelcode", self.channel_inner_key_ebank)
        # 2、发起代扣
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank",
                                             payment_option="wallet", payment_mode="GCash",
                                             user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response_fail(autopay_resp, channel_name_ebank, global_amount, "KN_NO_CHANNEL_CODE",
                                    "not supported channel:PH_GCASH23")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_ebank,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="wallet", payment_mode="GCash"
                                                       , description=""
                                                       , channel_inner_key="")
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "KN_NO_CHANNEL_CODE",
                                       "not supported channel:PH_GCASH23")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_ebank
    def test_xendit_ebank_chrage_fail_no_inner_key(self):
        # xendit_ebank 发起直接支付失败-没有返回channel_inner_key
        self.global_payment_mock.update_xendit_ebank_charge("no_inner_key", self.channel_inner_key_ebank)
        # 2、发起代扣
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank",
                                             payment_option="wallet", payment_mode="GCash",
                                             user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response_fail(autopay_resp, channel_name_ebank, global_amount, "KN_NO_CHANNEL_CODE",
                                    "CHARGE fail:channelInnerKey is null")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_ebank,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="wallet", payment_mode="GCash"
                                                       , description=""
                                                       , channel_inner_key="")
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "KN_NO_CHANNEL_CODE",
                                       "CHARGE fail:channelInnerKey is null")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_ebank
    def test_xendit_ebank_chrage_fail_no_redirect_url(self):
        # xendit_ebank 发起直接支付失败-没有返回redirect_url
        self.global_payment_mock.update_xendit_ebank_charge("no_redirect_url", self.channel_inner_key_ebank)
        # 2、发起代扣
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank",
                                             payment_option="wallet", payment_mode="GCash",
                                             user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response_fail(autopay_resp, channel_name_ebank, global_amount, "KN_NO_CHANNEL_CODE",
                                    "redirect url is null")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_ebank,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="wallet", payment_mode="GCash"
                                                       , description=""
                                                       , channel_inner_key="")
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "KN_NO_CHANNEL_CODE", "redirect url is null")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_ebank
    def test_xendit_ebank_chrage_500(self):
        # xendit_paycode 查询到支付成功
        # 1、修改mock，使得发起代扣失败
        self.global_payment_mock.update_xendit_ebank_charge("500", self.channel_inner_key_ebank)
        # 2、发起代扣
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank",
                                             payment_option="wallet", payment_mode="GCash",
                                             user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response_fail(autopay_resp, channel_name_ebank, global_amount, "KN_NO_CHANNEL_CODE",
                                    "返回错误HttpStatus500")
        # 支付失败-检查数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_ebank,
                                                       user_uuid=user_uuid,
                                                       channel_redirect="", operator="USER",
                                                       payment_option="wallet", payment_mode="GCash"
                                                       , description=""
                                                       , channel_inner_key="")
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "KN_NO_CHANNEL_CODE",
                                       "CHARGE fail, http://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/5e9807281718270057767a3e/ewallets/charges返回错误HttpStatus500,{}")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_ebank
    def test_xendit_ebank_charge_success_query_fail(self):
        # 1、修改mock，查询到支付失败FAILED需要配置在channel_error中，且不能超时
        # 使用通道返回的created(这里要注意时区的转化)+通道配置中的expire_time时间作为过期时间和当前时间比较，所以created要设置大点
        self.global_payment_mock.update_xendit_ebank_charge("success", self.channel_inner_key_ebank)
        # 3、发起代扣
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank",
                                             payment_option="wallet", payment_mode="GCash",
                                             user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               description=self.payment_code, payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_ebank,
                                                       user_uuid=user_uuid,
                                                       channel_redirect=xendit_redirect_url, operator="USER",
                                                       payment_option="wallet", payment_mode="GCash"
                                                       , description=""
                                                       , channel_inner_key=self.channel_inner_key_ebank)
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_REQUEST_SUCCESS", "PENDING")

        # 2、修改mock，xendit_ebank 查询到支付失败FAILED
        self.global_payment_mock.update_xendit_ebank_query("fail", self.channel_inner_key_ebank,
                                                           autopay_resp["data"]["channel_key"])
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 检查支付失败的数据
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "FAILED", "INSUFFICIENT_BALANCE")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_ebank
    def test_xendit_ebank_charge_success_query_timeout(self):
        # 1、修改mock，查询到支付中PENDING且需要返回超时
        # 使用通道返回的created(这里要注意时区的转化)+通道配置中的expire_time时间作为过期时间和当前时间比较，所以created要设置小点
        self.global_payment_mock.update_xendit_ebank_charge("success", self.channel_inner_key_ebank)
        # 3、发起代扣
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank",
                                             payment_option="wallet", payment_mode="GCash",
                                             user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               description=self.payment_code, payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_ebank,
                                                       user_uuid=user_uuid,
                                                       channel_redirect=xendit_redirect_url, operator="USER",
                                                       payment_option="wallet", payment_mode="GCash"
                                                       , description=""
                                                       , channel_inner_key=self.channel_inner_key_ebank)
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_REQUEST_SUCCESS", "PENDING")
        # 2、修改mock，xendit_ebank 查询到支付失败FAILED
        self.global_payment_mock.update_xendit_ebank_query("pending_timeout", self.channel_inner_key_ebank,
                                                           autopay_resp["data"]["channel_key"])
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 检查发起代扣数据库中的数据
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "KN_TIMEOUT_CLOSE_ORDER",
                                       "Payment transaction for specified charge_id is awaiting payment attempt by end user")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_withdraw
    def test_xendit_withdraw_query_process_to_fail(self):
        # 1、mock用户中心的返回的是电子钱包Gcash
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="GCash", withdraw_type="Gcash")
        # 2、让withdraw走mock
        self.global_payment_nacos.update_xendit_withdraw(project_id=project_id)
        # 4、使用固定的 card_uuid 发起代付，此时receipt_status=0
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、修改mock，查询交易不存在-发起代付成功
        self.global_payment_mock.update_xendit_withdraw_query("not_exit", resp["data"]["channel_key"])
        self.global_payment_mock.update_xendit_withdraw("PENDING", resp["data"]["channel_key"])
        # 5、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "WITHDRAW processing"})
        # 检查发起代付数据库中的数据
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "wallet", "GCash")
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "PENDING", "KN_REQUEST_SUCCESS")

        # 修改mock，xendit查询到代付失败
        self.global_payment_mock.update_xendit_withdraw_query("fail", resp["data"]["channel_key"])
        # channel_error中配置为处理中
        update_channel_error("xendit", "FAILED", 2, "WITHDRAW_QUERY")
        # 执行查询任务
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 处理中也会更新code和message
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "FAILED", "FAILED_INSUFFICIENT_BALANCE")

        # 再将处理中的在channel_error中配置为失败
        update_channel_error("xendit", "FAILED", 1, "WITHDRAW_QUERY")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "WITHDRAW_QUERY fail"})
        # 放款失败-检查数据库中的数据
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "FAILED", "FAILED_INSUFFICIENT_BALANCE")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_withdraw
    def test_xendit_withdraw_query_success(self):
        # 1、mock用户中心的返回的是电子钱包Gcash
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="GCash", withdraw_type="Gcash")
        # 2、让withdraw走mock
        self.global_payment_nacos.update_xendit_withdraw(project_id=project_id)
        # 4、使用固定的 card_uuid 发起代付，此时receipt_status=0
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、修改mock，查询交易不存在-发起代付成功
        self.global_payment_mock.update_xendit_withdraw_query("not_exit", resp["data"]["channel_key"])
        self.global_payment_mock.update_xendit_withdraw("PENDING", resp["data"]["channel_key"])
        # 5、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "WITHDRAW processing"})
        # 检查发起代付数据库中的数据
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "wallet", "GCash")
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "PENDING", "KN_REQUEST_SUCCESS")

        # 修改mock，xendit查询到代付成功
        self.global_payment_mock.update_xendit_withdraw_query("success", resp["data"]["channel_key"])
        # 执行查询任务
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "WITHDRAW_QUERY success"})
        run_task_by_order_no(req["merchant_key"])
        # 放款失败-检查数据库中的数据
        assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], "COMPLETED", "COMPLETED", "PH_GCASH")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_withdraw
    def test_xendit_withdraw_query_notexsit(self):
        # 1、mock用户中心的返回的是电子钱包Gcash
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="GCash", withdraw_type="Gcash")
        # 2、让withdraw走mock
        self.global_payment_nacos.update_xendit_withdraw(project_id=project_id)
        # 3、使用固定的 card_uuid 发起代付，此时receipt_status=0
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 4、修改mock，查询交易不存在-发起代付成功
        self.global_payment_mock.update_xendit_withdraw_query("not_exit", resp["data"]["channel_key"])
        self.global_payment_mock.update_xendit_withdraw("500", resp["data"]["channel_key"])
        # 5、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "WITHDRAW processing"})
        # 检查发起代付数据库中的数据
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "wallet", "GCash")
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "", "")

        # channel_error中将交易不存在配置为失败和忽略消息
        update_channel_error("xendit", "KN_ORDER_NOT_EXISTS", 1, "WITHDRAW_QUERY,IGNORE_MESSAGE")
        # 修改mock，xendit查询到交易不存在
        self.global_payment_mock.update_xendit_withdraw_query("not_exit", resp["data"]["channel_key"])
        # 执行查询任务
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "WITHDRAW_QUERY fail"})
        run_task_by_order_no(req["merchant_key"])
        # 放款失败-检查数据库中的数据
        # TODO 这里应该有个bug，当channel_error配置了message，交易不存在的时没有更新withdraw_receipt_channel_resp_message但是回调gbiz的channel_message却有值
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "KN_ORDER_NOT_EXISTS", "")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_xendit
    @pytest.mark.global_payment_xendit_withdraw
    def test_xendit_withdraw_callback_success(self):
        # 1、mock用户中心的返回的是银行账户
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="LBP", withdraw_type="bank")
        # 2、让withdraw走mock
        self.global_payment_nacos.update_xendit_withdraw(project_id=project_id)
        # 4、使用固定的 card_uuid 发起代付，此时receipt_status=0
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、修改mock，查询交易不存在-发起代付成功
        self.global_payment_mock.update_xendit_withdraw_query("not_exit", resp["data"]["channel_key"])
        self.global_payment_mock.update_xendit_withdraw("PENDING", resp["data"]["channel_key"])
        # 5、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "WITHDRAW processing"})
        # 检查发起代付数据库中的数据
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "account", "LBP")
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "PENDING", "KN_REQUEST_SUCCESS")

        # 手动模拟回调-代付成功
        xendit_withdraw_callback(channel_name_withdraw, global_amount/100, resp["data"]["channel_key"])
        # 执行回调
        run_task_by_order_no(resp["data"]["channel_key"], except_json={"code": 0, "message": "处理成功"})
        run_task_by_order_no(req["merchant_key"])
        # 放款失败-检查数据库中的数据
        assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], "COMPLETED", "callback callback_COMPLETED", "PH_GCASH")