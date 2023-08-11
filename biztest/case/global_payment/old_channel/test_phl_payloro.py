# -*- coding: utf-8 -*-

import pytest

from biztest.config.easymock.easymock_config import global_payment_easy_mock_phl
from biztest.config.payment.url_config import global_amount, payloro_resp_payment_mode, \
    global_withhold_failed_link_expired
from biztest.config.payment_global.global_payment_nacos import PaymentNacos
from biztest.function.global_payment.global_payment_check_function import check_autopay_response, \
    assert_check_withhold_withholdreceipt_initinfo, assert_withholdandreceipt_process, \
    assert_withholdandreceipt_success, check_autopay_response_fail, assert_withholdandreceipt_fail
from biztest.function.global_payment.global_payment_db_function import get_carduuid_bycardnum, \
    update_withhold_receipt_expired_at, update_channel_error
from biztest.function.global_payment.global_payment_db_operation import \
    insert_payloro_plwn_success_callback_task
from biztest.interface.payment_global.payment_global_interface import run_task_by_order_no, auto_pay, \
    clear_cache, global_withhold_close_order
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_phl_payloro import PayloroMock
from biztest.util.tools.tools import get_sysconfig
from foundation_test.util.asserts.assert_util import Assert

env = get_sysconfig("--env")
country = get_sysconfig("--country")
provider = "payloro"
sign_company = "copperstone"
channel_name_ebank = "payloro_copperstone_ebank"
user_uuid = "58042740327317418"
project_id = "5e9807281718270057767a3e"  # mock
nacos_domain = "nacos-test-phl.starklotus.com"  # nacos

# 备注：payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
# payloro_ebank_palawan 发起代扣成功、后查询到支付成功
# payloro_ebank_palawan 发起代扣失败
# payloro_ebank_palawan 查询到支付中、查询返回异常、查询返回500
# payloro_ebank_palawan 查询到超时关单
# payloro_ebank_palawan 查询到支付失败（channel_error配置为失败）
# payloro_ebank_palawan 查询到订单不存在
# payloro_ebank_palawan 手动关单成功
# payloro_ebank_palawan 手动关单失败、1.已经是失败状态   2.已经是成功状态   3.配置为不支持关单
# payloro_ebank_palawan 回调支付成功，回调有验签暂无法模拟，手动insert回调任务
# payloro_ebank_palawan 失败后收到回调代扣成功---补单

class TestPhilippinesPayloro:

    # 每个类的前置条件
    def setup_class(self):
        # 菲律宾使用默认卡
        self.account = get_carduuid_bycardnum("card", "enc_04_4106612382062092288_439")[0]
        self.global_payment_nacos = PaymentNacos(nacos_domain)
        # 修改kv，使走到mock
        self.global_payment_nacos.update_payloro_ebank(project_id=project_id)
        self.global_payment_mock = PayloroMock(global_payment_easy_mock_phl)
        clear_cache()  # 有时候直接修改数据库配置，会有缓存的问题

    # 每个类的最后需要还原之前的修改，并关闭数据库链接
    @classmethod
    def teardown_class(cls):
        # 恢复到通道测试环境
        cls.global_payment_nacos.update_payloro_ebank()
        DataBase.close_connects()

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_payloro_ebank_palawan
    def test_payloro_ebank_palawan_query_success(self):
        # payloro_ebank_palawan 查询到支付成功
        # 1、发起代扣、payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败  TODO 修改为优先获取通道返回的过期时间expiredDate，可以mock了
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank", payment_option="store",
                                             payment_mode="Palawan Pawnshop", user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response  payment_mode="7-11"是因为目前路由的都是7-11
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "PENDING", codes="success", payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name_ebank, user_uuid=user_uuid,
                                                       channel_redirect=autopay_resp["data"]["payment_data"]["redirect_url"], operator="USER",
                                                       payment_option="store", payment_mode="Palawan Pawnshop", channel_key=autopay_resp["data"]["channel_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        # 2、修改mock，使代扣查询到成功
        self.global_payment_mock.update_payloro_ebank_query("success", autopay_resp["data"]["channel_key"])
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_success(autopay_req["merchant_key"], "SUCCESS", "SUCCESS", mode=payloro_resp_payment_mode)

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_payloro_ebank_palawan
    def test_payloro_ebank_palawan_chrage_fail(self):
        # 发起直接支付失败，代扣金额小于50泰铢，payloro返回外层status<>200
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank", payment_option="store",
                                             payment_mode="Palawan Pawnshop", user_uuid=user_uuid, amount=1)
        # 检查autopay的response
        check_autopay_response_fail(autopay_resp, channel_name_ebank, 1, "416", "param payAmount invalid, more than 49")
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "416", "param payAmount invalid, more than 49")


    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_payloro_ebank_palawan
    def test_payloro_ebank_palawan_query_process(self):
        # payloro_ebank_palawan 查询到支付中、查询返回异常、查询返回500
        # 1、发起代扣、payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank", payment_option="store",
                                             payment_mode="Palawan Pawnshop", user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response  payment_mode="7-11"是因为目前路由的都是7-11
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "PENDING", codes="success", payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name_ebank, user_uuid=user_uuid,
                                                       channel_redirect=autopay_resp["data"]["payment_data"]["redirect_url"], operator="USER",
                                                       payment_option="store", payment_mode="Palawan Pawnshop", channel_key=autopay_resp["data"]["channel_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        # 执行查询任务、查询到支付中
        self.global_payment_mock.update_payloro_ebank_query("process", autopay_resp["data"]["channel_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        # 2、修改mock，使代扣查询异常
        self.global_payment_mock.update_payloro_ebank_query("error", autopay_resp["data"]["channel_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        # 2、修改mock，查询返回500
        self.global_payment_mock.update_payloro_ebank_query("500", autopay_resp["data"]["channel_key"])
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")


    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_payloro_ebank_palawan
    def test_payloro_ebank_palawan_query_timeout(self):
        # payloro_ebank_palawan 查询到支付超时关单
        # 1、发起代扣、payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank", payment_option="store",
                                             payment_mode="Palawan Pawnshop", user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response  payment_mode="7-11"是因为目前路由的都是7-11
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "PENDING", codes="success", payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name_ebank, user_uuid=user_uuid,
                                                       channel_redirect=autopay_resp["data"]["payment_data"]["redirect_url"], operator="USER",
                                                       payment_option="store", payment_mode="Palawan Pawnshop", channel_key=autopay_resp["data"]["channel_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        # 2、修改mock，使代扣查询到支付超时关单
        self.global_payment_mock.update_payloro_ebank_query("expired", autopay_resp["data"]["channel_key"])
        # payloro过期时间是根据withhold_receipt_expired_at判断的
        update_withhold_receipt_expired_at(autopay_req["merchant_key"], "2022-05-24 00:00:00")
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "KN_TIMEOUT_CLOSE_ORDER", global_withhold_failed_link_expired)


    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_payloro_ebank_palawan
    def test_payloro_ebank_palawan_query_fail(self):
        # payloro_ebank_palawan 查询到支付失败（channel_error需要配置为失败状态）
        # 1、发起代扣、payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank", payment_option="store",
                                             payment_mode="Palawan Pawnshop", user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response  payment_mode="7-11"是因为目前路由的都是7-11
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "PENDING", codes="success", payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name_ebank, user_uuid=user_uuid,
                                                       channel_redirect=autopay_resp["data"]["payment_data"]["redirect_url"], operator="USER",
                                                       payment_option="store", payment_mode="Palawan Pawnshop", channel_key=autopay_resp["data"]["channel_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        # 2、修改mock，使代扣查询到支付失败
        self.global_payment_mock.update_payloro_ebank_query("fail", autopay_resp["data"]["channel_key"])
        update_channel_error("payloro", "FAILED", 1,  "CHARGE_QUERY")
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "FAILED", "FAILED")


    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_payloro_ebank_palawan
    def test_payloro_ebank_palawan_manual_close_success(self):
        # payloro_ebank_palawan 查询到支付失败（channel_error需要配置为可关单状态）
        # 1、发起代扣、payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank", payment_option="store",
                                             payment_mode="Palawan Pawnshop", user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "PENDING", codes="success", payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name_ebank, user_uuid=user_uuid,
                                                       channel_redirect=autopay_resp["data"]["payment_data"]["redirect_url"], operator="USER",
                                                       payment_option="store", payment_mode="Palawan Pawnshop", channel_key=autopay_resp["data"]["channel_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        # 2、修改mock，使代扣查询到支付中
        self.global_payment_mock.update_payloro_ebank_query("process", autopay_resp["data"]["channel_key"])
        # channel_error需要PENIDNG配置为可关单状态
        update_channel_error("payloro", "PENIDNG", 2,  "CHARGE_QUERY,MANUAL_CLOSE")
        close_req, close_resp = global_withhold_close_order(autopay_req["merchant_key"])
        Assert.assert_equal(0, close_resp["code"], "给前端的code正确")
        Assert.assert_equal("关闭订单成功", close_resp["message"], "给前端说关闭订单成功")
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "KN_MANUAL_CLOSE_ORDER", "pending")


    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_payloro_ebank_palawan
    def test_payloro_ebank_palawan_query_not_exsit(self):
        # payloro_ebank_palawan 查询到支付失败（channel_error需要配置为失败状态）
        # 1、发起代扣、payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank", payment_option="store",
                                             payment_mode="Palawan Pawnshop", user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response  payment_mode="7-11"是因为目前路由的都是7-11
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "PENDING", codes="success", payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name_ebank, user_uuid=user_uuid,
                                                       channel_redirect=autopay_resp["data"]["payment_data"]["redirect_url"], operator="USER",
                                                       payment_option="store", payment_mode="Palawan Pawnshop", channel_key=autopay_resp["data"]["channel_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        # 2、修改mock，使代扣查询到支付超时关单
        self.global_payment_mock.update_payloro_ebank_query("not_exsit", autopay_resp["data"]["channel_key"])
        update_channel_error("payloro", "404", 1,  "CHARGE_QUERY")
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "404", "order not exist")


    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_payloro_ebank_palawan
    def test_payloro_ebank_palawan_manual_close_fail_1(self):
        # payloro_ebank_palawan 查询到支付失败（channel_error需要配置为可关单状态 1.已经是失败状态）
        # 1、发起代扣、payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank", payment_option="store",
                                             payment_mode="Palawan Pawnshop", user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "PENDING", codes="success", payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name_ebank, user_uuid=user_uuid,
                                                       channel_redirect=autopay_resp["data"]["payment_data"]["redirect_url"], operator="USER",
                                                       payment_option="store", payment_mode="Palawan Pawnshop", channel_key=autopay_resp["data"]["channel_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        # channel_error需要配置为已失败状态
        update_channel_error("payloro", "FAILED", 1,  "CHARGE_QUERY")
        # 3、修改mock，使代扣查询到失败，此时再来关单
        self.global_payment_mock.update_payloro_ebank_query("fail", autopay_resp["data"]["channel_key"])
        close_req, close_resp = global_withhold_close_order(autopay_req["merchant_key"])
        Assert.assert_equal(1, close_resp["code"], "给前端的code正确")
        Assert.assert_equal("订单已经成为终态，关闭订单失败", close_resp["message"], "给前端说关单失败")
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "FAILED", "FAILED")


    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_payloro_ebank_palawan
    def test_payloro_ebank_palawan_manual_close_fail_2(self):
        # payloro_ebank_palawan 查询到支付失败（channel_error需要配置为可关单状态 2.已经是成功状态）
        # 1、发起代扣、payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank", payment_option="store",
                                             payment_mode="Palawan Pawnshop", user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "PENDING", codes="success", payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name_ebank, user_uuid=user_uuid,
                                                       channel_redirect=autopay_resp["data"]["payment_data"]["redirect_url"], operator="USER",
                                                       payment_option="store", payment_mode="Palawan Pawnshop", channel_key=autopay_resp["data"]["channel_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        # 3、修改mock，使代扣查询到成功，此时再来关单
        self.global_payment_mock.update_payloro_ebank_query("success", autopay_resp["data"]["channel_key"])
        close_req, close_resp = global_withhold_close_order(autopay_req["merchant_key"])
        Assert.assert_equal(1, close_resp["code"], "给前端的code正确")
        Assert.assert_equal("订单已经成为终态，关闭订单失败", close_resp["message"], "给前端说关单失败")
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_success(autopay_req["merchant_key"], "SUCCESS", "SUCCESS", mode=payloro_resp_payment_mode)


    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_payloro_ebank_palawan
    def test_payloro_ebank_palawan_manual_close_fail_3(self):
        # payloro_ebank_palawan  3.配置为不支持关单
        # 1、发起代扣、payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank", payment_option="store",
                                             payment_mode="Palawan Pawnshop", user_uuid=user_uuid, amount=global_amount)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "PENDING", codes="success", payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name_ebank, user_uuid=user_uuid,
                                                       channel_redirect=autopay_resp["data"]["payment_data"]["redirect_url"], operator="USER",
                                                       payment_option="store", payment_mode="Palawan Pawnshop", channel_key=autopay_resp["data"]["channel_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        self.global_payment_mock.update_payloro_ebank_query("no_close", autopay_resp["data"]["channel_key"])
        # channel_error需要配置为不可关单状态
        update_channel_error("payloro", "no_close", 2,  "CHARGE_QUERY")
        update_channel_error("payloro", "no_close", 2,  "CHARGE_QUERY", "delete")
        close_req, close_resp = global_withhold_close_order(autopay_req["merchant_key"])
        Assert.assert_equal(1, close_resp["code"], "给前端的code正确")
        Assert.assert_equal("订单处理中，关闭订单失败", close_resp["message"], "给前端说关单失败")
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_payloro_ebank_palawan
    def test_payloro_ebank_palawan_callback_success(self):
        # payloro_ebank_palawan 回调支付成功
        # 1、发起代扣、payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank",
                                             payment_option="store",
                                             payment_mode="Palawan Pawnshop", user_uuid=user_uuid,
                                             amount=global_amount)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "PENDING", codes="success",
                               payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_ebank, user_uuid=user_uuid,
                                                       channel_redirect=autopay_resp["data"]["payment_data"][
                                                           "redirect_url"], operator="USER",
                                                       payment_option="store", payment_mode="Palawan Pawnshop",
                                                       channel_key=autopay_resp["data"]["channel_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        self.global_payment_mock.update_payloro_ebank_query("process", autopay_resp["data"]["channel_key"])
        # 手动插入回调任务withholdCallback
        insert_callback_task_no = insert_payloro_plwn_success_callback_task(autopay_req["merchant_key"], channel_name_ebank)
        run_task_by_order_no(insert_callback_task_no, {"code": 0, "message": "处理成功"})
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_success(autopay_req["merchant_key"], "SUCCESS", "SUCCESS", mode=payloro_resp_payment_mode)

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_payloro_ebank_palawan
    def test_payloro_ebank_palawan_query_fail_callback_success(self):
        # payloro_ebank_palawan 回调支付成功
        # 1、发起代扣、payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
        autopay_req, autopay_resp = auto_pay(channel_name=channel_name_ebank, payment_type="ebank",
                                             payment_option="store",
                                             payment_mode="Palawan Pawnshop", user_uuid=user_uuid,
                                             amount=global_amount)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_ebank, global_amount, "PENDING", codes="success",
                               payment_type="ebank")
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"],
                                                       channel_name=channel_name_ebank, user_uuid=user_uuid,
                                                       channel_redirect=autopay_resp["data"]["payment_data"][
                                                           "redirect_url"], operator="USER",
                                                       payment_option="store", payment_mode="Palawan Pawnshop",
                                                       channel_key=autopay_resp["data"]["channel_key"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "PENDING", "PENDING")
        self.global_payment_mock.update_payloro_ebank_query("fail", autopay_resp["data"]["channel_key"])
        update_channel_error("payloro", "FAILED", 1,  "CHARGE_QUERY")
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "FAILED", "FAILED")
        # 回调成功进行补单- 手动插入回调任务withholdCallback
        insert_callback_task_no = insert_payloro_plwn_success_callback_task(autopay_req["merchant_key"], channel_name_ebank)
        run_task_by_order_no(insert_callback_task_no, {"code": 0, "message": "处理成功"})
        # 执行查询任务
        run_task_by_order_no(autopay_req["merchant_key"])
        run_task_by_order_no(autopay_req["merchant_key"])
        # 支付成功-检查数据库中的数据
        assert_withholdandreceipt_success(autopay_req["merchant_key"], "KN_REVERSE_ORDER", "SUCCESS", mode=payloro_resp_payment_mode)



