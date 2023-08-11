# -*- coding: utf-8 -*-
import pytest

from biztest.config.easymock.easymock_config import global_payment_easy_mock
from biztest.config.payment.url_config import global_amount
from biztest.config.payment_global.global_payment_nacos import PaymentNacos
from biztest.function.global_payment.global_payment_check_function import check_autopay_response, \
    assert_withdrawandreceipt_process, \
    assert_check_withdraw_withdrawreceipt_initinfo, assert_withdrawandreceipt_success, assert_withdrawandreceipt_fail, \
    assert_check_withhold_withholdreceipt_initinfo, assert_withholdandreceipt_process, assert_withholdandreceipt_fail, \
    assert_withholdandreceipt_success
from biztest.function.global_payment.global_payment_db_function import update_provider_score, \
    update_task_by_task_order_no, update_channel_error, update_receipt_created_at
from biztest.interface.payment_global.payment_global_interface import run_task_by_order_no, auto_withdraw, \
    auto_pay, clear_cache, pandapay_withdraw_callback, global_autoWithdraw_retry
from biztest.interface.payment_global.payment_global_qrcode import pandapay_inquiry_confirm, mongopay_withdraw
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_pandapay_mock import PandapayMock
from biztest.util.tools.tools import get_sysconfig, get_date

env = get_sysconfig("--env")
country = get_sysconfig("--country")
provider = "pandapay"
sign_company = "alibey"
channel_name_withdraw = "pandapay_alibey_withdraw"
channel_name_barcode = "pandapay_alibey_barcode"
card_uuid = "6667561750979944"
user_uuid = "6663756175099944"
switch_card_uuid = "6667561750979955"
amount = 2022
project_id = "5b9a3ddd3a0f7700206522eb"  # mock
nacos_domain = "nacos-test-mex.starklotus.com"  # nacos


class TestThailandPandapay:

    # 每个类的前置条件
    def setup_class(cls):
        # 修改kv，使走到mock
        cls.global_payment_nacos = PaymentNacos(nacos_domain)
        cls.global_payment_nacos.update_pandapay_withdraw(project_id=project_id)
        # mock使fk返回用户信息和卡信息与本地库数据一致
        cls.global_payment_mock = PandapayMock(global_payment_easy_mock)
        # 修改mock 墨西哥没有card表相关信息了
        cls.account = {
            "account_card_uuid": card_uuid,
            "account_user_uuid": user_uuid,
            "account_card_num": "enc_03_2917886558479065088_754"
        }
        # cls.global_payment_mock.update_fk_userinfo(
        #     cls.account["card_id_num"], cls.account["card_username"], cls.account["card_account"])
        # 修改渠道的评分为最高，使一定路由到该通道
        update_provider_score(1000, provider, sign_company)
        clear_cache()  # 有时候直接修改数据库配置，会有缓存的问题

    # 每个类的最后需要还原之前的修改，并关闭数据库链接
    @classmethod
    def teardown_class(cls):
        cls.global_payment_nacos.update_pandapay_withdraw()
        update_provider_score(60, provider, sign_company)
        DataBase.close_connects()

    @pytest.mark.global_payment_pandapay
    @pytest.mark.global_payment_pandapay_withdraw
    @pytest.mark.parametrize("getpay_status,createpay_status,case_code,case_msg,task_demo",
                             [("not_exit", "success", "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS", {"code": 2, "message": "代付提现处理中"}),
                              ("not_exit", "fail", "-11", "El tipo de cuenta 3 es invalido", {"code": 2, "message": "代付提现处理中"}),
                              ("not_exit", "500", "KN_NO_CHANNEL_CODE", "response data is null", {"code": 2, "message": "代付提现处理中"}),
                              ("not_exit", "no_enough", "-1", "Insufficient partner balance", {"code": 2, "message": "代付提现处理中"}),
                              ("cancel", "", "Cancel", "Cancel", {"code": 2, "message": "exception order，pls query"}),
                              ("success",  "success", "KN_REPEAT_ORDER", "KN_REPEAT_ORDER", {"code": 2, "message": "exception order，pls query"}),
                              ("500",  "success", "KN_NO_CHANNEL_CODE", "", {"code": 2, "message": "代付提现处理中"}),
                              ("not_exit",  "maximum", "-403", "Maximum request limit", {"code": 2, "message": "代付提现处理中"})
                              ],
                             ids=["success", "fail", "500", "no_enough", "exit_fail", "exit_success", "pre_500", "maximum"])
    # 参数说明：前置查询接口code，下单接口code，数据库存储code，数据库存储msg，task_memo
    # 场景说明：下单成功，下单失败，下单接口500，下单余额不足，已失败的订单重复下单，已成功的订单重复下单，前置查询接口500，下单接口限流
    def test_pandapay_withdraw(self, getpay_status, createpay_status, case_code, case_msg, task_demo):
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid)
        # 1、修改mock，使代付能够成功，代付时：先查询一下订单是否存在
        self.global_payment_mock.update_withdraw_getPay(resp["data"]["channel_key"], getpay_status)
        self.global_payment_mock.update_withdraw_createPay(createpay_status)
        # 执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json=task_demo)
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], case_code, case_msg)
        # 关闭未完成的task
        update_task_by_task_order_no(req["merchant_key"], "close")

    @pytest.mark.global_payment_pandapay
    @pytest.mark.global_payment_pandapay_withdraw
    @pytest.mark.parametrize("getpay_status,case_code,case_msg,task_demo",
                             [("success", "Success", "Success", {"code": 0, "message": "代付提现查询成功"}),
                              ("refund", "Refund", "Refund", {"code": 1, "message": "代付提现查询退款"}),
                              ("cancel", "Cancel", "Cancel", {"code": 1, "message": "代付提现查询取消"}),
                              ("fail", "Fail", "KN_REQUEST_SUCCESS", {"code": 1, "message": "代付提现查询失败"}),
                              ("process", "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS", {"code": 1, "message": "代付订单正在处理中！需要重试！"}),
                              ("500", "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS", {"code": 2, "message": "代付订单正在处理中！需要重试！"}),
                              ("not_exit", "-1_Invalid id or claveRastreo", "KN_REQUEST_SUCCESS", {"code": 2, "message": "代付订单正在处理中！需要重试！"}),
                              ("maximum", "-403_Maximum request limit", "Maximum request limit", {"code": 2, "message": "代付订单正在处理中！需要重试！"})
                              ],
                             ids=["success", "refund", "cancel", "fail", "process", "500", "not_exit", "maximum"])
    # 参数说明：订单查询接口code，数据库存储code，数据库存储msg，task_memo
    # 场景说明：查询到成功，查询到退款(失败)，查询到取消(失败)，查询到失败，未查询到终态，查询接口500，查询到订单不存在，查询接口限流
    # 注意订单不存在配置的是处理中还是失败，另外还需要处理msg覆盖的配置
    def test_pandapay_withdraw_Query(self, getpay_status, case_code, case_msg, task_demo):
        # 1、修改mock使下单成功
        self.global_payment_mock.update_withdraw_getPay("", "not_exit")
        self.global_payment_mock.update_withdraw_createPay("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid)
        # 执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        update_channel_error("pandapay", "-1_Invalid id or claveRastreo", 2, "WITHDRAW_QUERY,IGNORE_MESSAGE")
        # 检查withdraw／withdraw_receipt，上一条用例检查了，这里就不检查了
        # assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")
        # 执行代付task#withdrawQuery
        self.global_payment_mock.update_withdraw_getPay(resp["data"]["channel_key"], getpay_status)
        # run_task_by_order_no(req["merchant_key"], except_json=task_demo)
        run_task_by_order_no(req["merchant_key"])
        # 检查withdraw／withdraw_receipt
        if getpay_status == "process" or getpay_status == "500" or getpay_status == "maximum":
            assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], case_code, case_msg)
        else:
            assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                           card_uuid, channel_name_withdraw,
                                                           withdraw_type="online")
        if getpay_status == "success":
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], case_code, case_msg, None)
        if getpay_status == "refund" or getpay_status == "cancel" or getpay_status == "fail":
            assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], case_code, case_msg)
        if getpay_status == "not_exit":  # 现在把订单不存在配置为处理中
            assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], case_code, case_msg)
        # 关闭未完成的task
        run_task_by_order_no(req["merchant_key"])
        update_task_by_task_order_no(req["merchant_key"], "close")

    @pytest.mark.global_payment_pandapay
    @pytest.mark.global_payment_pandapay_withdraw
    def test_pandapay_withdraw_fail_retry_success(self):
        # 1、修改mock使下单成功
        self.global_payment_mock.update_withdraw_getPay("", "not_exit")
        self.global_payment_mock.update_withdraw_createPay("no_enough")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid)
        ## 2021年10月11日修改代码，该code需要一定配置为代付失败
        ## 为了解决tv总是提示，ChannelError不存在，providerCode[pandapay],channelErrorCode[-1]
        # update_channel_error("pandapay", "-1_Invalid id or claveRastreo", 1, "WITHDRAW_QUERY,IGNORE_MESSAGE")
        # 2022年6月15日修改代码，该code不一定需要一直配置为失败了，故屏蔽上面的代码
        # 执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "-1", "Insufficient partner balance")
        # 4、需要修改一下查询的mock
        # 2022年6月15日修改代码，该code不一定需要一直配置为失败了，故屏蔽上面的代码，用另外的code来使订单失败
        self.global_payment_mock.update_withdraw_getPay(resp["data"]["channel_key"], "not_exit")
        # 配置错误码（此时我们修改一下错误码配置，确保其为处理中）
        update_channel_error("pandapay", "-1_Invalid id or claveRastreo", 2, "WITHDRAW_QUERY,IGNORE_MESSAGE")
        # 执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "-1_Invalid id or claveRastreo", "Insufficient partner balance")
        # 将刚刚修改的错误码，配置为失败
        update_channel_error("pandapay", "-1_Invalid id or claveRastreo", 1, "WITHDRAW_QUERY,IGNORE_MESSAGE")
        # 执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询失败"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "-1_Invalid id or claveRastreo", "Insufficient partner balance")
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       card_uuid, channel_name_withdraw,
                                                       withdraw_type="online")
        # 1、修改mock使下单成功
        self.global_payment_mock.update_withdraw_getPay("", "not_exit")
        self.global_payment_mock.update_withdraw_createPay("success")
        # 2、只换 trade_no 重新发起代付
        req2, resp2 = global_autoWithdraw_retry(sign_company, switch_card_uuid, user_uuid, merchant_key=req["merchant_key"])
        # 执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"])
        # 检查withdraw_receipt
        assert_withdrawandreceipt_process(req2["trade_no"], req["merchant_key"], "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")
        # 执行代付task#withdrawQuery，订单号不一致
        # 执行代付task#withdrawQuery，金额不一致，不检查金额
        self.global_payment_mock.update_withdraw_getPay(resp["data"]["channel_key"], "success")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 执行代付task#withdrawQuery
        self.global_payment_mock.update_withdraw_getPay(resp2["data"]["channel_key"], "success")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
        # 检查withdraw_receipt
        assert_withdrawandreceipt_success(req2["trade_no"], req["merchant_key"], "Success", "Success", None)
        assert_check_withdraw_withdrawreceipt_initinfo(req2["trade_no"], req["merchant_key"], user_uuid,
                                                       switch_card_uuid, channel_name_withdraw,
                                                       withdraw_type="online")
        # 还原配置
        update_channel_error("pandapay", "-1_Invalid id or claveRastreo", 2, "WITHDRAW_QUERY,IGNORE_MESSAGE")

    @pytest.mark.global_payment_pandapay
    @pytest.mark.global_payment_pandapay_withdraw
    @pytest.mark.parametrize("callback_status,getpay_status,case_code,case_msg,task_demo",
                             [("Success", "cancel", "Success", "Success,自动化回调", {"code": 0, "message": "处理成功", "data": None}),
                              ("Cancel", "cancel", "Cancel", "Cancel,自动化回调", {"code": 0, "message": "处理成功", "data": None}),
                              ("Cancel", "success", "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS", {"code": 2, "message": "查询补偿结果与回调结果不一致，重试", "data": None})
                              ],
                             ids=["success", "cancel", "cancel_success"])
    # 参数说明：回调状态code，补偿查询code，数据库存储code，数据库存储msg，task_memo
    # 场景说明：回调成功(补偿查询取消但是此时不会查询所以最终结果还是成功)，回调取消(补偿查询取消)，回调取消(补偿查询成功)
    def test_pandapay_withdraw_callback(self, callback_status, getpay_status, case_code, case_msg, task_demo):
        # 1、修改mock使下单成功
        self.global_payment_mock.update_withdraw_getPay("", "not_exit")
        self.global_payment_mock.update_withdraw_createPay("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")
        # 4、回调，回调之前需要为补充查询准备数据
        update_task_by_task_order_no(req["merchant_key"], "close")
        self.global_payment_mock.update_withdraw_getPay(resp["data"]["channel_key"], getpay_status)
        c_req, c_resp = pandapay_withdraw_callback(channel_name_withdraw, resp["data"]["channel_key"], callback_status)
        # print("##################", c_resp)
        # Assert.assert_equal("b'Success'", c_resp, "给通道的code正确")
        # 执行查询task#withholdCallback
        run_task_by_order_no(resp["data"]["channel_key"], except_json=task_demo)
        run_task_by_order_no(req["merchant_key"])  # 此时有两个task，暂时不检查task执行情况
        # 检查withdraw／withdraw_receipt
        if callback_status == "Cancel" and getpay_status == "success":  # 只有失败的回调会执行补充查询
            assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], case_code, case_msg)
        else:
            assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                           card_uuid, channel_name_withdraw,
                                                           withdraw_type="online")
        if callback_status == "Success":  # 只有失败的回调会执行补充查询
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], case_code, case_msg, None)
        if callback_status == "Cancel" and getpay_status == "cancel":
            assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], case_code, case_msg)
        # 关闭未完成的task
        update_task_by_task_order_no(resp["data"]["channel_key"], "close")

    @pytest.mark.global_payment_pandapay
    @pytest.mark.global_payment_pandapay_withdraw
    def test_pandapay_withdraw_callback_next_run_at(self):
        # 1、修改mock，是代付能够成功，代付时：先查询一下订单是否存在
        self.global_payment_mock.update_withdraw_getPay("", "not_exit")
        self.global_payment_mock.update_withdraw_createPay("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")
        # 4、回调
        pandapay_withdraw_callback(channel_name_withdraw, resp["data"]["channel_key"], "Success")
        pandapay_withdraw_callback(channel_name_withdraw, resp["data"]["channel_key"], "Cancel")
        pandapay_withdraw_callback(channel_name_withdraw, resp["data"]["channel_key"], "Refund")
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")
        # 关闭未完成的tas，观察task的下次执行时间
        update_task_by_task_order_no(resp["data"]["channel_key"], "close")
        update_task_by_task_order_no(req["merchant_key"], "close")

    @pytest.mark.global_payment_pandapay
    @pytest.mark.global_payment_pandapay_withdraw
    @pytest.mark.parametrize("callback_status,getpay_status,case_code,case_msg,task_demo",
                             [("Refund", "refund", "KN_REVERSE_ORDER", "Refund,自动化回调", {"code": 0, "message": "处理成功", "data": None}),
                              ("Refund", "success", "Success", "Success,自动化回调", {"code": 2, "message": "查询补偿结果与回调结果不一致，重试", "data": None}),
                              ("Refund", "cancel", "KN_REVERSE_ORDER", "Refund,自动化回调", {"code": 0, "message": "处理成功", "data": None})
                              ],
                             ids=["refund", "refund_success", "refund_cancel"])
    # 参数说明：回调状态code，补偿查询code，数据库存储code，数据库存储msg，task_memo
    # 场景说明：回调退款(补偿查询退款)，回调退款(补偿查询成功)，回调退款(补偿查询取消)
    def test_pandapay_withdraw_callback_refund(self, callback_status, getpay_status, case_code, case_msg, task_demo):
        # 1、修改mock，是代付能够成功，代付时：先查询一下订单是否存在
        self.global_payment_mock.update_withdraw_getPay("", "not_exit")
        self.global_payment_mock.update_withdraw_createPay("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "KN_REQUEST_SUCCESS",
                                          "KN_REQUEST_SUCCESS")
        # 4、第一次回调成功
        c_req, c_resp = pandapay_withdraw_callback(channel_name_withdraw, resp["data"]["channel_key"], "Success")
        # print("##################", c_resp)
        # Assert.assert_equal("b'Success'", c_resp, "给通道的code正确")
        # 执行查询task#withholdCallback
        run_task_by_order_no(resp["data"]["channel_key"], except_json={"code": 0, "message": "处理成功", "data": None})
        run_task_by_order_no(req["merchant_key"])  # 此时有两个task，暂时不检查task执行情况
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], "Success", "Success,自动化回调", None)
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                           card_uuid, channel_name_withdraw,
                                                           withdraw_type="online")
        # 4、第二次回调退款
        update_task_by_task_order_no(req["merchant_key"], "close")
        self.global_payment_mock.update_withdraw_getPay(resp["data"]["channel_key"], getpay_status)
        pandapay_withdraw_callback(channel_name_withdraw, resp["data"]["channel_key"], callback_status)
        # 执行查询task#withholdCallback
        run_task_by_order_no(resp["data"]["channel_key"], except_json=task_demo)
        run_task_by_order_no(req["merchant_key"])  # 此时有两个task，暂时不检查task执行情况
        # 检查withdraw／withdraw_receipt
        if getpay_status == "success":
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], case_code, case_msg, None)
        else:
            assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], case_code, case_msg)
            assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                           card_uuid, channel_name_withdraw,
                                                           withdraw_type="online")
        # 关闭未完成的task
        update_task_by_task_order_no(resp["data"]["channel_key"], "close")

    @pytest.mark.global_payment_pandapay_test
    @pytest.mark.global_payment_mongopay
    def test_mongopay_withdraw_success(self):
        # # 1、该通道无法mock；2、使用固定的 card_uuid 发起代付，直接使用channelname，不走路由
        # req, resp = global_autoWithdraw(sign_company, card_uuid, user_uuid, "mongopay_alibey_withdraw")
        # # 执行代付task#withdraw
        # run_task_by_order_no(req["merchant_key"], except_json='{"code": 2, "message": "代付提现处理中"}')
        # # 检查withdraw／withdraw_receipt
        # assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "SUCCESS", "Request success")
        # # 关闭未完成的task
        # update_task_by_task_order_no(req["merchant_key"], "close")

        # 继续下一单
        req2, resp2 = auto_withdraw(sign_company, card_uuid, user_uuid, "mongopay_alibey_withdraw")
        # 执行代付task#withdraw
        run_task_by_order_no(req2["merchant_key"], except_json='{"code": 2, "message": "代付提现处理中"}')
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req2["trade_no"], req2["merchant_key"], "SUCCESS", "Request success")
        # 使用通道提供的工具，使订单成功
        req22, resp22 = mongopay_withdraw(resp2["data"]["channel_key"], "2")
        print(req22, resp22)
        run_task_by_order_no(req2["merchant_key"])
        assert_withdrawandreceipt_success(req2["trade_no"], req2["merchant_key"], "2", "SUCCESS", None)
        assert_check_withdraw_withdrawreceipt_initinfo(req2["trade_no"], req2["merchant_key"], user_uuid,
                                                       card_uuid, "mongopay_alibey_withdraw",
                                                       withdraw_type="online")

        # 继续下一单
        req3, resp3 = auto_withdraw(sign_company, card_uuid, user_uuid, "mongopay_alibey_withdraw")
        # 执行代付task#withdraw
        run_task_by_order_no(req3["merchant_key"], except_json='{"code": 2, "message": "代付提现处理中"}')
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req3["trade_no"], req3["merchant_key"], "SUCCESS", "Request success")
        # 使用通道提供的工具，使订单成功
        update_task_by_task_order_no(req3["merchant_key"], "close")
        mongopay_withdraw(resp3["data"]["channel_key"], "2")
        run_task_by_order_no(resp3["data"]["channel_key"])
        run_task_by_order_no(req3["merchant_key"])
        assert_withdrawandreceipt_success(req3["trade_no"], req3["merchant_key"], "2", "SUCCESS", None)
        assert_check_withdraw_withdrawreceipt_initinfo(req3["trade_no"], req3["merchant_key"], user_uuid,
                                                       card_uuid, "mongopay_alibey_withdraw",
                                                       withdraw_type="online")




    @pytest.mark.global_payment_pandapay
    @pytest.mark.global_payment_pandapay_barcode
    @pytest.mark.parametrize("payment_type, payment_option, channel_name",
                             [("barcode", "oxxo_cash", channel_name_barcode)])
    def test_pandapay_barcode(self, payment_type, payment_option, channel_name):
        # 1、使用 user_uuid 发起代扣，不用mock
        autopay_req, autopay_resp = auto_pay(sign_company, payment_type, payment_option, "", "", user_uuid)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name, global_amount, "KN_REQUEST_SUCCESS", "success", "", payment_type)
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name,
                                                       user_uuid=user_uuid, card_uuid="5200000000000000000", card_num="enc_03_2917886558479065088_754",
                                                       payment_option=payment_option, payment_mode="", channel_inner_key=autopay_resp["data"]["payment_data"]["wh_number"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")
        # 关闭未完成的task
        update_task_by_task_order_no(autopay_req["merchant_key"], "close")

    @pytest.mark.global_payment_pandapay
    @pytest.mark.global_payment_pandapay_barcode
    @pytest.mark.parametrize("payment_type, payment_option, channel_name",
                             [("barcode", "oxxo_cash", channel_name_barcode)])
    def test_pandapay_barcodeQuery_close(self, payment_type, payment_option, channel_name):
        # 1、使用 user_uuid 发起代扣，不用mock
        autopay_req, autopay_resp = auto_pay(sign_company, payment_type, payment_option, "", "", user_uuid)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name, global_amount, "KN_REQUEST_SUCCESS", "success", "", payment_type)
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name,
                                                       user_uuid=user_uuid, card_uuid="5200000000000000000", card_num="enc_03_2917886558479065088_754",
                                                       payment_option=payment_option, payment_mode="", channel_inner_key=autopay_resp["data"]["payment_data"]["wh_number"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")
        # 修改订单，使超时关单，有时差，这个函数是用的北京时间，和墨西哥差了10多个小时，而且数据库和程序还差1个小时
        update_receipt_created_at(autopay_req["merchant_key"], get_date(day=-2))
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 1, "message": "支付订单查询失败"})
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 0, "message": "代扣订单[%s]状态更新成功！" % autopay_req["merchant_key"]})
        # 检查代扣超时后数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name,
                                                       user_uuid=user_uuid, card_uuid="5200000000000000000", card_num="enc_03_2917886558479065088_754",
                                                       payment_option=payment_option, payment_mode="", channel_inner_key=autopay_resp["data"]["payment_data"]["wh_number"])
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "KN_TIMEOUT_CLOSE_ORDER", "none")

    @pytest.mark.global_payment_pandapay
    @pytest.mark.global_payment_pandapay_barcode
    @pytest.mark.parametrize("payment_type, payment_option, channel_name",
                             [("barcode", "oxxo_cash", channel_name_barcode)])
    def test_pandapay_barcodeQuery_revers(self, payment_type, payment_option, channel_name):
        # 1、使用 user_uuid 发起代扣，不用mock
        autopay_req, autopay_resp = auto_pay(sign_company, payment_type, payment_option, "", "", user_uuid)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name, global_amount, "KN_REQUEST_SUCCESS", "success", "", payment_type)
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name,
                                                       user_uuid=user_uuid, card_uuid="5200000000000000000", card_num="enc_03_2917886558479065088_754",
                                                       payment_option=payment_option, payment_mode="", channel_inner_key=autopay_resp["data"]["payment_data"]["wh_number"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")
        # 修改订单，使超时关单，有时差，这个函数是用的北京时间，和墨西哥差了10多个小时，而且数据库和程序还差1个小时
        update_receipt_created_at(autopay_req["merchant_key"], get_date(day=-2))
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 1, "message": "支付订单查询失败"})
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 0, "message": "代扣订单[%s]状态更新成功！" % autopay_req["merchant_key"]})
        # 检查代扣超时后数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name,
                                                       user_uuid=user_uuid, card_uuid="5200000000000000000", card_num="enc_03_2917886558479065088_754",
                                                       payment_option=payment_option, payment_mode="", channel_inner_key=autopay_resp["data"]["payment_data"]["wh_number"])
        assert_withholdandreceipt_fail(autopay_req["merchant_key"], "KN_TIMEOUT_CLOSE_ORDER", "none")

        # 执行回调
        pandapay_inquiry_confirm("lookup", autopay_resp["data"]["payment_data"]["wh_number"])
        pandapay_inquiry_confirm("payment_attempt", autopay_resp["data"]["payment_data"]["wh_number"], global_amount)
        pandapay_inquiry_confirm("paid", autopay_resp["data"]["payment_data"]["wh_number"], global_amount)
        # 执行回调 task
        run_task_by_order_no(autopay_resp["data"]["channel_key"], except_json={"code": 0, "message": "处理成功"})
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 0, "message": "代扣订单[%s]状态更新成功！" % autopay_req["merchant_key"]})
        # 检查代扣回调成功后数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name,
                                                       user_uuid=user_uuid, card_uuid="5200000000000000000", card_num="enc_03_2917886558479065088_754",
                                                       payment_option=payment_option, payment_mode="",
                                                       description="61d59a2b86a71f6f8a24d18d", channel_inner_key=autopay_resp["data"]["payment_data"]["wh_number"])
        assert_withholdandreceipt_success(autopay_req["merchant_key"], "KN_REVERSE_ORDER", "paid", "oxxo", "OXXO", "KN_REVERSE_ORDER")

    @pytest.mark.global_payment_pandapay
    @pytest.mark.global_payment_pandapay_barcode
    @pytest.mark.parametrize("payment_type, payment_option, channel_name",
                             [("barcode", "oxxo_cash", channel_name_barcode)])
    def test_pandapay_barcodeCallback_success(self, payment_type, payment_option, channel_name):
        # 1、使用 user_uuid 发起代扣，不用mock
        autopay_req, autopay_resp = auto_pay(sign_company, payment_type, payment_option, "", "", user_uuid)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name, global_amount, "KN_REQUEST_SUCCESS", "success", "", payment_type)
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name,
                                                       user_uuid=user_uuid, card_uuid="5200000000000000000", card_num="enc_03_2917886558479065088_754",
                                                       payment_option=payment_option, payment_mode="", channel_inner_key=autopay_resp["data"]["payment_data"]["wh_number"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")
        # 执行回调
        pandapay_inquiry_confirm("lookup", autopay_resp["data"]["payment_data"]["wh_number"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_INQUIRY_SUCCESS", "inquiry success")

        pandapay_inquiry_confirm("payment_attempt", autopay_resp["data"]["payment_data"]["wh_number"], global_amount)
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_CONFIRM_SUCCESS", "confirm success")

        pandapay_inquiry_confirm("paid", autopay_resp["data"]["payment_data"]["wh_number"], global_amount)
        # 执行回调 task
        run_task_by_order_no(autopay_resp["data"]["channel_key"], except_json={"code": 0, "message": "处理成功"})
        run_task_by_order_no(autopay_req["merchant_key"])
        # 检查代扣回调成功后数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name,
                                                       user_uuid=user_uuid, card_uuid="5200000000000000000", card_num="enc_03_2917886558479065088_754",
                                                       payment_option=payment_option, payment_mode="",
                                                       description="61d59a2b86a71f6f8a24d18d", channel_inner_key=autopay_resp["data"]["payment_data"]["wh_number"])
        assert_withholdandreceipt_success(autopay_req["merchant_key"], "paid", "paid", "oxxo", "OXXO")

    # 查询时需要mock
    @pytest.mark.parametrize("payment_type, payment_option, channel_name",
                             [("barcode", "oxxo_cash", channel_name_barcode)])
    def test_pandapay_barcodeQuery_success(self, payment_type, payment_option, channel_name):
        # 1、使用 user_uuid 发起代扣，不用mock
        autopay_req, autopay_resp = auto_pay(sign_company, payment_type, payment_option, "", "", user_uuid)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name, global_amount, "KN_REQUEST_SUCCESS", "success", "", payment_type)
        # 检查发起代扣数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name,
                                                       user_uuid=user_uuid, card_uuid="5200000000000000000", card_num="enc_03_2917886558479065088_754",
                                                       payment_option=payment_option, payment_mode="", channel_inner_key=autopay_resp["data"]["payment_data"]["wh_number"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")
        # 执行回调
        pandapay_inquiry_confirm("lookup", autopay_resp["data"]["payment_data"]["wh_number"])
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_INQUIRY_SUCCESS", "inquiry success")

        pandapay_inquiry_confirm("payment_attempt", autopay_resp["data"]["payment_data"]["wh_number"], global_amount)
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "KN_CONFIRM_SUCCESS", "confirm success")

        pandapay_inquiry_confirm("paid", autopay_resp["data"]["payment_data"]["wh_number"], global_amount)
        update_task_by_task_order_no(autopay_resp["data"]["channel_key"], "close")
        # 执行查询 task#withholdChargeQuery ，查询的时候需要mock
        run_task_by_order_no(autopay_req["merchant_key"])
        # 检查代扣回调成功后数据库中的数据
        assert_check_withhold_withholdreceipt_initinfo(merchant_key=autopay_req["merchant_key"], channel_name=channel_name,
                                                       user_uuid=user_uuid, card_uuid="5200000000000000000", card_num="enc_03_2917886558479065088_754",
                                                       payment_option=payment_option, payment_mode="",
                                                       description="61d59a2b86a71f6f8a24d18d", channel_inner_key=autopay_resp["data"]["payment_data"]["wh_number"])
        assert_withholdandreceipt_success(autopay_req["merchant_key"], "paid", "paid", "oxxo", "OXXO")
