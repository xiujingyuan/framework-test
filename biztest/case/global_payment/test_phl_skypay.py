# -*- coding: utf-8 -*-
import time

import pytest

from biztest.config.easymock.easymock_config import global_payment_easy_mock_phl
from biztest.config.payment_global.global_payment_nacos import PaymentNacos
from biztest.function.global_payment.global_payment_check_function import \
    assert_check_withdraw_withdrawreceipt_initinfo, assert_withdrawandreceipt_process, \
    assert_withdrawandreceipt_success, assert_withdrawandreceipt_fail
from biztest.function.global_payment.global_payment_db_function import get_carduuid_bycardnum
from biztest.function.global_payment.global_payment_db_operation import get_global_withdraw_info_by_trade_no
from biztest.interface.payment_global.payment_global_interface import run_task_by_order_no, auto_withdraw, \
    clear_cache
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_phl_xendit import XenditMock
from biztest.util.tools.tools import get_four_element_global

provider = "skypay"
sign_company = "copperstone"
channel_name_withdraw = "skypay_copperstone_withdraw"
user_uuid = "58042740327317418"
card_uuid = "6621102700001270802"
nacos_domain = "nacos-test-phl.starklotus.com"  # nacos


class TestPhilippinesSkypay:

    # 每个类的前置条件
    def setup_class(cls):
        # 菲律宾使用默认卡
        cls.account = get_carduuid_bycardnum("card", "enc_03_2773064776828854272_908")[0]
        cls.global_payment_nacos = PaymentNacos(nacos_domain)
        # skypay不需要kv，因为有验签无法mock
        # mock用户中心的返回数据使得线上放款可以直接成功
        cls.global_payment_mock = XenditMock(global_payment_easy_mock_phl)
        # 修改mock
        four_element = get_four_element_global()
        cls.global_payment_mock.update_fk_userinfo(account_no=four_element['data']['card_num_encrypt'], bank_code="LBP")
        clear_cache()  # 有时候直接修改数据库配置，会有缓存的问题

    # 每个类的最后需要还原之前的修改，并关闭数据库链接
    @classmethod
    def teardown_class(cls):
        # 恢复用户中心原始数据
        cls.global_payment_mock = XenditMock(global_payment_easy_mock_phl)
        cls.global_payment_mock.update_fk_userinfo(account_no="enc_04_3383474380125773824_485", bank_code="LBP")
        DataBase.close_connects()

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_skypay
    @pytest.mark.global_payment_skypay_withdraw
    def test_skypay_withdraw_callback_success_or_fail(self):
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="KN_REQUEST_SUCCESS",
                                          message="KN_REQUEST_SUCCESS")
        # 4、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # skypay有验签无法mock，走通道真实环境，线上放款会直接收到回调代付成功，需要等待时间才能拿到结果(但是超过次数就会返回放款失败"Daily Transaction Times")，立马查询返回处理中pending
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="0", message="Pending")
        withdraw_info = get_global_withdraw_info_by_trade_no(req["trade_no"])
        # 等待通道的回调结果
        time.sleep(60)
        # 4、执行代付task#withdrawCallback
        run_task_by_order_no(withdraw_info[0]["withdraw_receipt_channel_key"],
                             except_json={"code": 0, "message": "处理成功"})
        # 4、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"])
        withdraw_info = get_global_withdraw_info_by_trade_no(req["trade_no"])
        # 检查withdraw／withdraw_receipt的终态信息,可能是成功，也可能是失败
        if withdraw_info[0]["withdraw_receipt_status"] == 2:
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="2",
                                              message="callback success", resp_transfer_mode="Bank (RT)")
        else:
            assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], code="4",
                                           message="Daily Transaction Times.")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_skypay
    @pytest.mark.global_payment_skypay_withdraw
    def test_skypay_withdraw_query_success_or_fail(self):
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="KN_REQUEST_SUCCESS",
                                          message="KN_REQUEST_SUCCESS")
        # 4、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # skypay有验签无法mock，走通道真实环境，线上放款会直接收到回调代付成功，需要等待时间才能拿到结果，立马查询返回处理中pending
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="0", message="Pending")
        # 等待通道的回调结果
        time.sleep(60)
        # 4、执行代付task#withdrawQuery,不执行callback
        run_task_by_order_no(req["merchant_key"])
        # 4、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"])
        # 检查withdraw／withdraw_receipt的终态信息,可能是成功，也可能是失败
        withdraw_info = get_global_withdraw_info_by_trade_no(req["trade_no"])
        if withdraw_info[0]["withdraw_receipt_status"] == 2:
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="1",
                                              message="Completed", resp_transfer_mode="Bank (RT)")
        else:
            assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], code="4", message="Failed")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_skypay
    @pytest.mark.global_payment_skypay_withdraw
    def test_skypay_withdraw_fail_retry_success(self):
        # 第一次代付失败，后只换trade_no重新发起代付
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})

        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")