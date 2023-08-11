# -*- coding: utf-8 -*-
import pytest

from biztest.config.easymock.easymock_config import global_payment_easy_mock
from biztest.config.payment_global.global_payment_nacos import PaymentNacos
from biztest.function.global_payment.global_payment_check_function import \
    assert_check_withdraw_withdrawreceipt_initinfo, \
    assert_withdrawandreceipt_process, assert_withdrawandreceipt_success, assert_withdrawandreceipt_fail
from biztest.function.global_payment.global_payment_db_function import get_carduuid_bycardnum, \
    update_task_by_task_order_no, update_channel_error
from biztest.interface.payment_global.payment_global_interface import run_task_by_order_no, auto_withdraw, \
    global_autoWithdraw_retry
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_scb_mock import ScbMock
from biztest.util.tools.tools import get_sysconfig

env = get_sysconfig("--env")
country = get_sysconfig("--country")
provider = "scb"
sign_company = "amberstar1"
channel_name_withdraw = "scb_amberstar1_withdraw"
channel_name_qrcode = "scb_amberstar1_qrcode"
card_uuid = "6621102700001270802"
user_uuid = "197222248434630658"
project_id = "5b9a3ddd3a0f7700206522eb"  # mock
nacos_domain = "nacos-test-tha.starklotus.com"  # nacos


# class TestThailandScb:
#
#     # 每个类的前置条件
#     def setup_class(cls):
#         # 使用固定的 card_uuid+user_uuid
#         cls.account = get_carduuid_bycardnum("account", "enc_03_3513454134508920832_259")[0]
#         # 修改kv，使走到mock
#         cls.global_payment_nacos = PaymentNacos(nacos_domain)
#         #默认nacos配置usercenter.properties中用户中心一直是mock地址
#         # cls.global_payment_nacos.update_user_center_config(project_id=project_id)
#         cls.global_payment_nacos.update_scb_withdraw(project_id=project_id)
#         # mock使fk返回用户信息和卡信息与本地库数据一致
#         cls.global_payment_mock = ScbMock(global_payment_easy_mock)
#         # 修改mock
#         cls.global_payment_mock.update_fk_userinfo(
#             cls.account["card_id_num"], cls.account["card_username"], cls.account["card_account"])
#         # 修改渠道的评分为最高，使一定路由到该通道
#         update_provider_score(1000, provider, sign_company)
#         clear_cache()  # 有时候直接修改数据库配置，会有缓存的问题
#
#     # 每个类的最后需要还原之前的修改，并关闭数据库链接
#     @classmethod
#     def teardown_class(cls):
#         # cls.global_payment_nacos.update_user_center_config()  # 不管是日常测试还是自动化测试，用户中心都暂时先一直使用mock
#         cls.global_payment_nacos.update_scb_withdraw()
#         update_provider_score(60, provider, sign_company)
#         update_provider("scb", "open")
#         DataBase.close_connects()
#
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withdraw
#     def test_scb_withdraw_success(self):
#         # 1、修改mock，是代付能够成功
#         # 代付时：调用gettoken，再调用initiate； 查询到付时：调用gettoken，再调用inquiry
#         self.global_payment_mock.update_gettoken("success")
#         self.global_payment_mock.update_withdraw_initiate("success")
#         self.global_payment_mock.update_withdraw_inquiry("success")  # 该接口返回成功则代付成功
#         # 2、使用固定的 card_uuid 发起代付
#         req, resp = global_autoWithdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
#         # 执行代付task#withdraw
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
#         # 检查withdraw／withdraw_receipt基础信息
#         assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid, channel_name_withdraw)
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "1000", "Success")
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
#         # 检查withdraw／withdraw_receipt的终态信息
#         assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], "ACCC", "Accepted Settlement Completed on creditor account")
#
#     @pytest.mark.global_payment_thailand_auto
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withdraw
#     def test_scb_withdraw_confirmsuccess(self):
#         # 1、修改mock，是代付能够成功
#         # 代付时：调用gettoken，再调用initiate； 查询到付时：调用gettoken，再调用inquiry
#         self.global_payment_mock.update_gettoken("success")
#         self.global_payment_mock.update_withdraw_initiate("success")
#         self.global_payment_mock.update_withdraw_inquiry("process")  # 该接口返回非成功则需要调用confirm
#         self.global_payment_mock.update_withdraw_confirm("success")
#         # 2、使用固定的 card_uuid 发起代付
#         req, resp = global_autoWithdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
#         # 执行代付task#withdraw
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
#         # 检查withdraw／withdraw_receipt基础信息
#         assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
#                                                        channel_name_withdraw)
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "1000", "Success")
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
#         # 检查withdraw／withdraw_receipt（9.16的分支要记录此时的中间状态）
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "PDNG", "Pending")
#
#         # 查询的时候继续调用inquiry
#         self.global_payment_mock.update_withdraw_inquiry("success")  # 该接口返回成功则代付成功
#
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
#         # 检查withdraw／withdraw_receipt的终态信息
#         assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], "ACCC", "Accepted Settlement Completed on creditor account")
#
#     @pytest.mark.global_payment_thailand_auto
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withdraw
#     def test_scb_withdraw_process(self):
#         # 1、修改mock，是代付能够成功
#         # 代付时：调用gettoken，再调用initiate； 查询到付时：调用gettoken，再调用inquiry
#         self.global_payment_mock.update_gettoken("success")
#         self.global_payment_mock.update_withdraw_initiate("success")
#         self.global_payment_mock.update_withdraw_inquiry("process")  # 该接口返回非成功则需要调用confirm
#         self.global_payment_mock.update_withdraw_confirm("success")
#         # 2、使用固定的 card_uuid 发起代付
#         req, resp = global_autoWithdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
#         # 执行代付task#withdraw
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
#         # 检查withdraw／withdraw_receipt基础信息
#         assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
#                                                        channel_name_withdraw)
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "1000", "Success")
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
#         # 检查withdraw／withdraw_receipt（9.16的分支要记录此时的中间状态）
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "PDNG", "Pending")
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
#         # 需要把查询task关闭，方便后续观察数据
#         update_task_by_task_order_no(req["merchant_key"], "close")
#
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withdraw
#     def test_scb_withdraw_process2(self):
#         # 1、修改mock，是代付能够成功
#         # 代付时：调用gettoken，再调用initiate； 查询到付时：调用gettoken，再调用inquiry
#         self.global_payment_mock.update_gettoken("success")
#         self.global_payment_mock.update_withdraw_initiate("success")
#         # 2、使用固定的 card_uuid 发起代付
#         req, resp = global_autoWithdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
#         # 执行代付task#withdraw
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
#         # 检查withdraw／withdraw_receipt基础信息
#         assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
#                                                        channel_name_withdraw)
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "1000", "Success")
#         # 需要把查询task关闭，方便后续观察数据，可以观察task#withdrawQuery是否被挂起
#         update_task_by_task_order_no(req["merchant_key"], "close")
#
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withdraw
#     def test_scb_withdraw_gettokenfail(self):
#         # 1、修改mock，是代付能够成功
#         # 代付时：调用gettoken，再调用initiate； 查询到付时：调用gettoken，再调用inquiry
#         self.global_payment_mock.update_gettoken("fail")  # 该接口若失败，流程停止
#         # 2、使用固定的 card_uuid 发起代付
#         req, resp = global_autoWithdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
#         # 执行代付task#withdraw
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
#         # 检查withdraw／withdraw_receipt基础信息
#         assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
#                                                        channel_name_withdraw)
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "", "")
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "TokenizerId is null"})
#         # 检查withdraw／withdraw_receipt
#         assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "KN_NO_CHANNEL_CODE", "TokenizerId is null")
#
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withdraw
#     def test_scb_withdraw_initiatefail(self):
#         # 1、修改mock，是代付能够成功
#         # 代付时：调用gettoken，再调用initiate； 查询到付时：调用gettoken，再调用inquiry
#         self.global_payment_mock.update_gettoken("success")
#         self.global_payment_mock.update_withdraw_initiate("fail")  # 从日志上看，查询的时候没有再调用任何接口，订单直接失败
#         # 2、使用固定的 card_uuid 发起代付
#         req, resp = global_autoWithdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
#         # 执行代付task#withdraw
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
#         # 检查withdraw／withdraw_receipt基础信息
#         assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
#                                                        channel_name_withdraw)
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "401", "FAILED")
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "TokenizerId is null"})
#         # 检查withdraw／withdraw_receipt
#         assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "KN_NO_CHANNEL_CODE", "TokenizerId is null")
#
#     @pytest.mark.global_payment_thailand_auto
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withdraw
#     @pytest.mark.global_payment_scb_test
#     def test_scb_withdraw_fail_errorcode(self):
#         # 1、修改mock，是代付能够成功
#         # 代付时：调用gettoken，再调用initiate； 查询到付时：调用gettoken，再调用inquiry
#         self.global_payment_mock.update_gettoken("success")
#         self.global_payment_mock.update_withdraw_initiate("success")
#         self.global_payment_mock.update_withdraw_inquiry("process")  # 该接口返回非成功则需要调用confirm
#         self.global_payment_mock.update_withdraw_confirm("success")
#         # 2、使用固定的 card_uuid 发起代付
#         req, resp = global_autoWithdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
#         # 执行代付task#withdraw
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
#         # 检查withdraw／withdraw_receipt基础信息
#         assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
#                                                        channel_name_withdraw)
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "1000", "Success")
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
#         # 检查withdraw／withdraw_receipt（9.16的分支要记录此时的中间状态）
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "PDNG", "Pending")
#         # 查询的时候继续调用inquiry
#         self.global_payment_mock.update_withdraw_inquiry("fail")  # 该接口返回成功则代付成功
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
#         # 检查withdraw／withdraw_receipt（9.16的分支要记录此时的中间状态）
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "RJCT", "Payment has been rejected")
#
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
#         # 配置错误码
#         update_channel_error("scb", "001", 1, "WITHDRAW_QUERY")
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询失败"})
#         # 检查withdraw／withdraw_receipt
#         assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "RJCT", "Payment has been rejected")
#
#         # 最后需要把配置的错误码移除，方便后续观察数据
#         update_channel_error("scb", "001", 1, "WITHDRAW_QUERY", "delete")
#
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withdraw
#     @pytest.mark.global_payment_scb_500
#     def test_scb_withdraw_initiate500(self):
#         # 1、修改mock，是代付能够成功
#         # 代付时：调用gettoken，再调用initiate； 查询到付时：调用gettoken，再调用inquiry
#         self.global_payment_mock.update_gettoken("success")
#         self.global_payment_mock.update_withdraw_initiate("500")
#         # 2、使用固定的 card_uuid 发起代付
#         req, resp = global_autoWithdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
#         # 执行代付task#withdraw
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
#         # 检查withdraw／withdraw_receipt基础信息
#         assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
#                                                        channel_name_withdraw)
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "", "")
#         # 需要把查询task关闭，方便后续观察数据，可以观察task#withdrawQuery是否被挂起
#         update_task_by_task_order_no(req["merchant_key"], "close")
#
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withdraw
#     def test_scb_withdraw_inquiry500(self):
#         # 1、修改mock，是代付能够成功
#         # 代付时：调用gettoken，再调用initiate； 查询到付时：调用gettoken，再调用inquiry
#         self.global_payment_mock.update_gettoken("success")
#         self.global_payment_mock.update_withdraw_initiate("success")
#         self.global_payment_mock.update_withdraw_inquiry("500")  # 该接口返回不通，则流程停止
#         # 2、使用固定的 card_uuid 发起代付
#         req, resp = global_autoWithdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
#         # 执行代付task#withdraw
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
#         # 检查withdraw／withdraw_receipt基础信息
#         assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
#                                                        channel_name_withdraw)
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "1000", "Success")
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
#         # 检查withdraw／withdraw_receipt
#         assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "1000", "Success")
#         # 执行代付task#withdrawQuery
#         run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
#         # 需要把查询task关闭，方便后续观察数据
#         update_task_by_task_order_no(req["merchant_key"], "close")
#
#     @pytest.mark.global_payment_thailand_auto
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withhold
#     def test_scb_qrcode_success(self):
#         # 1、这个通道不需要 mock
#         # 1、使用固定的 card_uuid 发起代扣
#         autopay_req, autopay_resp = global_withhold_autopay(sign_company, "qrcode", card_uuid=card_uuid)
#         # 检查autopay的response
#         check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, payment_type="qrcode")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_GENERATE_QR_CODE", "KN_GENERATE_QR_CODE")
#
#         # 4、模拟通道发起payment_inquiry
#         inquiry_req, inquiry_resp = scb_payment_inquiry_confirm("payment_inquiry", autopay_resp["data"]["channel_key"], global_amount/100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("0000", inquiry_resp["resCode"], "给通道的code正确")
#         Assert.assert_equal("Success", inquiry_resp["resMesg"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_INQUIRY_SUCCESS", "KN_INQUIRY_SUCCESS")
#
#         # 5、模拟通道发起payment_confirm
#         confirm_req, confirm_resp = scb_payment_inquiry_confirm("payment_confirm", autopay_resp["data"]["channel_key"], global_amount/100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("0000", confirm_resp["resCode"], "给通道的code正确")
#         Assert.assert_equal("Success", confirm_resp["resMesg"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_INQUIRY_SUCCESS", "KN_INQUIRY_SUCCESS")
#
#         # 6、执行回调task#withholdCallback
#         run_task_by_order_no(autopay_resp["data"]["channel_key"], except_json={"code": 0, "message": "处理成功"})
#         run_task_by_order_no(autopay_req["merchant_key"])
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 2, channel_name_qrcode,
#                                "KN_TRANSFER_SUCCESS", "KN_TRANSFER_SUCCESS")
#
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withhold
#     def test_scb_qrcode_amountfail(self):
#         # 1、这个通道不需要 mock
#         # 1、使用固定的 card_uuid 发起代扣
#         autopay_req, autopay_resp = global_withhold_autopay(sign_company, "qrcode", card_uuid=card_uuid, amount=global_amount)
#         # 检查autopay的response
#         check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, payment_type="qrcode")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_GENERATE_QR_CODE", "KN_GENERATE_QR_CODE")
#
#         # 4、模拟通道发起payment_inquiry
#         inquiry_req, inquiry_resp = scb_payment_inquiry_confirm("payment_inquiry", autopay_resp["data"]["channel_key"], global_amount/10)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("1004", inquiry_resp["resCode"], "给通道的code正确")
#         Assert.assert_equal("Invalid amount", inquiry_resp["resMesg"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_ORDER_AMOUNT_NOT_MATCH", "KN_ORDER_AMOUNT_NOT_MATCH")
#
#         # 5、修改订单时间，使其超时关单（这个时间其实还可以细化）
#         update_receipt_created_at(autopay_req["merchant_key"], get_date(day=-1))
#
#         # 6、执行查询task#withholdChargeQuery
#         run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 1, "message": "支付订单查询失败，订单过期"})
#         run_task_by_order_no(autopay_req["merchant_key"])  # 代扣订单[Auto_WH_31169890226934]状态更新成功！
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 3)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode,
#                                "KN_TIMEOUT_CLOSE_ORDER", "KN_ORDER_AMOUNT_NOT_MATCH")
#
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withhold
#     def test_scb_qrcode_reversefail(self):
#         # 1、这个通道不需要 mock，本条用例测试，已经成功的订单，再次还款
#         # 1、使用固定的 card_uuid 发起代扣
#         autopay_req, autopay_resp = global_withhold_autopay(sign_company, "qrcode", card_uuid=card_uuid, amount=global_amount)
#         # 检查autopay的response
#         check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, payment_type="qrcode")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_GENERATE_QR_CODE", "KN_GENERATE_QR_CODE")
#
#         # 4、模拟通道发起payment_inquiry
#         inquiry_req, inquiry_resp = scb_payment_inquiry_confirm("payment_inquiry", autopay_resp["data"]["channel_key"],
#                                                                 global_amount / 100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("0000", inquiry_resp["resCode"], "给通道的code正确")
#         Assert.assert_equal("Success", inquiry_resp["resMesg"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_INQUIRY_SUCCESS", "KN_INQUIRY_SUCCESS")
#
#         # 5、模拟通道发起payment_confirm
#         confirm_req, confirm_resp = scb_payment_inquiry_confirm("payment_confirm", autopay_resp["data"]["channel_key"],
#                                                                 global_amount / 100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("0000", confirm_resp["resCode"], "给通道的code正确")
#         Assert.assert_equal("Success", confirm_resp["resMesg"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_INQUIRY_SUCCESS", "KN_INQUIRY_SUCCESS")
#
#         # 6、执行回调task#withholdCallback
#         run_task_by_order_no(autopay_resp["data"]["channel_key"], except_json={"code": 0, "message": "处理成功"})
#         run_task_by_order_no(autopay_req["merchant_key"])
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 2, channel_name_qrcode,
#                                "KN_TRANSFER_SUCCESS", "KN_TRANSFER_SUCCESS")
#
#         # 7、再次模拟通道发起payment_inquiry
#         inquiry_req, inquiry_resp = scb_payment_inquiry_confirm("payment_inquiry", autopay_resp["data"]["channel_key"],
#                                                                 global_amount / 100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("2001", inquiry_resp["resCode"], "给通道的code正确")
#         Assert.assert_equal("Duplicate transaction", inquiry_resp["resMesg"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 2, channel_name_qrcode,
#                                "KN_TRANSFER_SUCCESS", "KN_TRANSFER_SUCCESS")
#
#     @pytest.mark.global_payment_thailand_auto
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withhold
#     def test_scb_qrcode_reverse(self):
#         # 1、这个通道不需要 mock，本条用例测试，已经失败的订单，再次还款
#         # 1、使用固定的 card_uuid 发起代扣
#         autopay_req, autopay_resp = global_withhold_autopay(sign_company, "qrcode", card_uuid=card_uuid, amount=global_amount)
#         # 检查autopay的response
#         check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, payment_type="qrcode")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_GENERATE_QR_CODE", "KN_GENERATE_QR_CODE")
#
#         # 4、模拟通道发起payment_inquiry
#         inquiry_req, inquiry_resp = scb_payment_inquiry_confirm("payment_inquiry", autopay_resp["data"]["channel_key"],
#                                                                 global_amount / 10)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("1004", inquiry_resp["resCode"], "给通道的code正确")
#         Assert.assert_equal("Invalid amount", inquiry_resp["resMesg"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_ORDER_AMOUNT_NOT_MATCH", "KN_ORDER_AMOUNT_NOT_MATCH")
#
#         # 5、修改订单时间，使其超时关单（这个时间其实还可以细化）
#         update_receipt_created_at(autopay_req["merchant_key"], get_date(day=-1))
#
#         # 6、执行查询task#withholdChargeQuery
#         run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 1, "message": "支付订单查询失败，订单过期"})
#         run_task_by_order_no(autopay_req["merchant_key"])  # 代扣订单[Auto_WH_31169890226934]状态更新成功！
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 3)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode,
#                                "KN_TIMEOUT_CLOSE_ORDER", "KN_ORDER_AMOUNT_NOT_MATCH")
#
#         # 7、再次模拟通道发起payment_inquiry
#         inquiry_req, inquiry_resp = scb_payment_inquiry_confirm("payment_inquiry", autopay_resp["data"]["channel_key"],
#                                                                 global_amount / 100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("0000", inquiry_resp["resCode"], "给通道的code正确")
#         Assert.assert_equal("Success", inquiry_resp["resMesg"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 3)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode,
#                                "KN_TIMEOUT_CLOSE_ORDER", "KN_ORDER_AMOUNT_NOT_MATCH")
#
#         # 8、再次模拟通道发起payment_confirm
#         confirm_req, confirm_resp = scb_payment_inquiry_confirm("payment_confirm", autopay_resp["data"]["channel_key"],
#                                                                 global_amount / 100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("0000", confirm_resp["resCode"], "给通道的code正确")
#         Assert.assert_equal("Success", confirm_resp["resMesg"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 3)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode,
#                                "KN_TIMEOUT_CLOSE_ORDER", "KN_ORDER_AMOUNT_NOT_MATCH")
#
#         # 6、执行回调task#withholdCallback
#         run_task_by_order_no(autopay_resp["data"]["channel_key"], except_json={"code": 0, "message": "处理成功"})
#         run_task_by_order_no(autopay_req["merchant_key"])
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 2, channel_name_qrcode,
#                                "KN_REVERSE_ORDER", "KN_TRANSFER_SUCCESS")
#
#     @pytest.mark.global_payment_scb
#     @pytest.mark.global_payment_scb_withhold
#     def test_scb_qrcode_amountfail2(self):
#         # 1、这个通道不需要 mock
#         # 1、使用固定的 card_uuid 发起代扣
#         autopay_req, autopay_resp = global_withhold_autopay(sign_company, "qrcode", card_uuid=card_uuid, amount=global_amount)
#         # 检查autopay的response
#         check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, payment_type="qrcode")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_GENERATE_QR_CODE", "KN_GENERATE_QR_CODE")
#
#         # 4、模拟通道发起payment_inquiry
#         inquiry_req, inquiry_resp = scb_payment_inquiry_confirm("payment_inquiry", autopay_resp["data"]["channel_key"],
#                                                                 global_amount / 100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("0000", inquiry_resp["resCode"], "给通道的code正确")
#         Assert.assert_equal("Success", inquiry_resp["resMesg"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_INQUIRY_SUCCESS", "KN_INQUIRY_SUCCESS")
#
#         # 5、模拟通道发起payment_confirm
#         confirm_req, confirm_resp = scb_payment_inquiry_confirm("payment_confirm", autopay_resp["data"]["channel_key"],
#                                                                 global_amount / 10)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("0000", confirm_resp["resCode"], "给通道的code正确")
#         Assert.assert_equal("Success", confirm_resp["resMesg"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_INQUIRY_SUCCESS", "KN_INQUIRY_SUCCESS")
#
#         # 6、执行回调task#withholdCallback
#         # {"code":2,"message":"代扣回调异常！收据[411035588611715]金额[9403]与回调金额[9003]不一致，回调任务无法继续执行","data":null}
#         run_task_by_order_no(autopay_resp["data"]["channel_key"])
#         # run_task_by_order_no(autopay_req["merchant_key"])
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_INQUIRY_SUCCESS", "KN_INQUIRY_SUCCESS")
#
#         # 7、修改订单时间，使其超时关单（这个时间其实还可以细化）
#         update_receipt_created_at(autopay_req["merchant_key"], get_date(day=-1))
#
#         # 6、执行查询task#withholdChargeQuery
#         run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 1, "message": "支付订单查询失败，订单过期"})
#         run_task_by_order_no(autopay_req["merchant_key"])  # 代扣订单[Auto_WH_31169890226934]状态更新成功！
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 3)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode,
#                                "KN_TIMEOUT_CLOSE_ORDER", "KN_INQUIRY_SUCCESS")


print()
# 这段用例测试用，自动化的时候不跑，但是也不要删除，就留在这里
class TestThailandGbpay:
    # 每个类的前置条件
    def setup_class(cls):
        # 使用固定的 card_uuid+user_uuid
        cls.account = get_carduuid_bycardnum("account", "enc_03_3513454134508920832_259")[0]
        # 修改kv，使走到mock
        cls.global_payment_nacos = PaymentNacos(nacos_domain)
        cls.global_payment_nacos.update_scb_withdraw(project_id=project_id)
        # mock使fk返回用户信息和卡信息与本地库数据一致
        cls.global_payment_mock = ScbMock(global_payment_easy_mock)
        # 修改mock
        cls.global_payment_mock.update_fk_userinfo(
            cls.account["card_id_num"], cls.account["card_username"], cls.account["card_account"])

    # 每个类的最后需要还原之前的修改，并关闭数据库链接
    @classmethod
    def teardown_class(cls):
        cls.global_payment_nacos.update_scb_withdraw()
        DataBase.close_connects()

    @pytest.mark.global_payment_gbpay_test
    def test_scb_withdraw_Query(self):
        # 1、使用固定的 card_uuid 发起代付
        self.global_payment_mock.update_gettoken("success")
        self.global_payment_mock.update_withdraw_initiate("success")
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name="scb_amberstar1_withdraw")
        # 2、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid, channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "1000", "Success")

        # 没有订单不存在的场景，修改mock使订单处理中
        self.global_payment_mock.update_withdraw_inquiry("process")  # 该接口返回非成功则需要调用confirm
        self.global_payment_mock.update_withdraw_confirm("success")  # 确认放款结果，返回成功则代表放款成功
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "PDNG", "Pending")

        # 再次查询，会查询到成功（此时假设查询到失败）
        self.global_payment_mock.update_withdraw_inquiry("fail")
        # 4、将订单错误码配置为处理中
        update_channel_error("scb", "RJCT", 2, "WITHDRAW_QUERY,IGNORE_MESSAGE")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "RJCT", "Pending")
        # 4、将订单错误码配置为失败
        update_channel_error("scb", "RJCT", 1, "WITHDRAW_QUERY,IGNORE_MESSAGE")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询失败"})
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "RJCT", "Pending")
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid, "scb_amberstar1_withdraw")

        # 1、修改mock，使重新下单成功
        self.global_payment_mock.update_gettoken("success")
        self.global_payment_mock.update_withdraw_initiate("success")
        # 2、只换 trade_no 重新发起代付
        req2, resp2 = global_autoWithdraw_retry(sign_company, card_uuid, user_uuid, "scb_amberstar1_withdraw", merchant_key=req["merchant_key"])
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json='{"code": 2, "message": "代付提现处理中"}')
        assert_withdrawandreceipt_process(req2["trade_no"], req["merchant_key"], "1000", "Success")
        # 4、执行代付task#withdrawQuery，接口500
        self.global_payment_mock.update_withdraw_inquiry("500")
        run_task_by_order_no(req["merchant_key"])
        run_task_by_order_no(req["merchant_key"])
        # 4、执行代付task#withdrawQuery，无法检查订单号，也无法检查金额
        self.global_payment_mock.update_withdraw_inquiry("success")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
        assert_withdrawandreceipt_success(req2["trade_no"], req["merchant_key"], "ACCC", "Accepted Settlement Completed on creditor account", None)

    @pytest.mark.global_payment_gbpay_test
    @pytest.mark.parametrize("token_status,withdraw_status,case_code,case_msg,task_demo",
                             [("fail", "", "KN_NO_CHANNEL_CODE", "response data is null", {"code": 2, "message": "代付提现处理中"}),
                              ("success", "success", "1000", "Success", {"code": 2, "message": "代付提现处理中"}),
                              ("success", "500", "KN_NO_CHANNEL_CODE", "response data is null", {"code": 2, "message": "代付提现处理中"}),
                              ("success", "fail", "401", "FAILED", {"code": 2, "message": "代付提现处理中"})
                              ],
                             ids=["token_fail", "success", "500", "fail"])
    # 参数说明：token接口code，下单接口code，数据库存储code，数据库存储msg，task_memo
    # 场景说明：token获取失败，下单成功，下单接口500，下单失败
    def test_scb_withdraw(self, token_status, withdraw_status, case_code, case_msg, task_demo):
        # 1、修改mock，是代付能够成功
        # 代付时：调用gettoken，再调用initiate； 查询到付时：调用gettoken，再调用inquiry
        self.global_payment_mock.update_gettoken(token_status)
        self.global_payment_mock.update_withdraw_initiate(withdraw_status)
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name="scb_amberstar1_withdraw")
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json=task_demo)
        # 4、检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid, "scb_amberstar1_withdraw")
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], case_code, case_msg)
        # 5、需要把查询task关闭，方便后续观察数据，可以观察task#withdrawQuery是否有延迟
        update_task_by_task_order_no(req["merchant_key"], "close")



