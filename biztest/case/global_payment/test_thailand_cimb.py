# # -*- coding: utf-8 -*-
# import pytest
# from biztest.util.asserts.assert_util import Assert
# from biztest.util.easymock.global_payment.global_payment_cimb_mock import CimbMock
# from biztest.config.easymock.easymock_config import global_payment_easy_mock
# from biztest.config.payment_global.global_payment_nacos import PaymentNacos
# from biztest.interface.payment_global.payment_global_qrcode import cimb_payment_inquiry, cimb_payment_confirm
# from biztest.function.global_payment.global_payment_check_function import \
#     check_withhold, check_withhold_receipt, check_autopay_response
# from biztest.function.global_payment.global_payment_database import update_provider_score, get_carduuid_bycardnum, \
#     update_receipt_created_at
# from biztest.interface.payment_global.payment_global_interface import run_task_by_order_no, global_autoWithdraw, \
#     global_withhold_autopay, clear_cache
# from biztest.util.db.db_util import DataBase
# from biztest.util.tools.tools import get_sysconfig, get_date
#
# env = get_sysconfig("--env")
# country = get_sysconfig("--country")
# provider = "cimb"
# sign_company = "amberstar1"
# channel_name_withdraw = "cimb_amberstar1_withdraw"
# channel_name_qrcode = "cimb_amberstar1_qrcode"
# card_uuid = "6621102700001270802"
# user_uuid = "197222248434630658"
# amount = 929
# project_id = "5b9a3ddd3a0f7700206522eb"  # mock
# nacos_domain = "nacos-test-tha.starklotus.com"  # nacos
#
#
# class TestThailandCimb:
#
#     # 每个类的前置条件
#     def setup_class(cls):
#         # 使用固定的 card_uuid+user_uuid
#         cls.account = get_carduuid_bycardnum("account", "enc_03_3513454134508920832_259")[0]
#         # 修改kv，使走到mock
#         cls.global_payment_nacos = PaymentNacos(nacos_domain)
#         #默认nacos配置usercenter.properties中用户中心一直是mock地址
#         # cls.global_payment_nacos.update_user_center_config(project_id=project_id)
#         # mock使fk返回用户信息和卡信息与本地库数据一致
#         cls.global_payment_mock = CimbMock(global_payment_easy_mock)
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
#         update_provider_score(100, provider, sign_company)
#         DataBase.close_connects()
#
#     # cimb环境很不稳定，经常遇到Connection reset，故放款经常都会失败，并且无法mock
#     @pytest.mark.global_payment_cimb_withdraw
#     # def test_cimb_withdraw_success(self):
#         # 1、使用固定的 card_uuid 发起代付
#         # 这个通道要固定的用户才能放款成功／失败，这个稍后完善
#         # TODO 先屏蔽这个用例，然后找能成功的数据
#         # req, resp = global_autoWithdraw(sign_company, card_uuid, user_uuid, amount=amount)
#         # # 执行代付task#withdraw
#         # run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
#         # # 检查withdraw
#         # check_withdraw(req["merchant_key"], self.account, 1, channel_name_withdraw)
#         # # 执行代付task#withdraw
#         # run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
#         # # 检查withdraw／withdraw_receipt
#         # check_withdraw(req["merchant_key"], self.account, 2, channel_name_withdraw)
#         # check_withdraw_receipt(
#         #     req["merchant_key"], self.account, 2, channel_name_withdraw, "WDQ_00", "Complete/Success")
#
#     @pytest.mark.global_payment_thailand_auto
#     @pytest.mark.global_payment_cimb
#     @pytest.mark.global_payment_cimb_withhold
#     def test_cimb_qrcode_success(self):
#         # 1、这个通道不需要 mock
#         # 1、使用固定的 card_uuid 发起代扣
#         autopay_req, autopay_resp = global_withhold_autopay(sign_company, "qrcode", card_uuid=card_uuid, amount=amount)
#         # 检查autopay的response
#         check_autopay_response(autopay_resp, channel_name_qrcode, amount, payment_type="qrcode")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_GENERATE_QR_CODE", "KN_GENERATE_QR_CODE")
#
#         # 4、模拟通道发起payment_inquiry
#         inquiry_req, inquiry_resp = cimb_payment_inquiry(autopay_resp["data"]["channel_key"], amount / 100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("000", inquiry_resp["status"]["code"], "给通道的code正确")
#         Assert.assert_equal("Success", inquiry_resp["status"]["message"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_INQUIRY_SUCCESS", "KN_INQUIRY_SUCCESS")
#
#         # 5、模拟通道发起payment_confirm
#         confirm_req, confirm_resp = cimb_payment_confirm(autopay_resp["data"]["channel_key"], amount/100, "S")
#         # 检查payment_inquiry的response
#         Assert.assert_equal("000", confirm_resp["status"]["code"], "code正确")
#         Assert.assert_equal("Success", confirm_resp["status"]["message"], "给通道的msg正确")
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
#     @pytest.mark.global_payment_cimb
#     @pytest.mark.global_payment_cimb_withhold
#     def test_cimb_qrcode_amountfail(self):
#         # 1、这个通道不需要 mock
#         # 1、使用固定的 card_uuid 发起代扣
#         autopay_req, autopay_resp = global_withhold_autopay(sign_company, "qrcode", card_uuid=card_uuid, amount=amount)
#         # 检查autopay的response
#         check_autopay_response(autopay_resp, channel_name_qrcode, amount, payment_type="qrcode")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_GENERATE_QR_CODE", "KN_GENERATE_QR_CODE")
#
#         # 4、模拟通道发起payment_inquiry
#         inquiry_req, inquiry_resp = cimb_payment_inquiry(autopay_resp["data"]["channel_key"], amount / 10)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("999", inquiry_resp["status"]["code"], "给通道的code正确")
#         Assert.assert_equal("KN_ORDER_AMOUNT_NOT_MATCH", inquiry_resp["status"]["message"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "999", "KN_ORDER_AMOUNT_NOT_MATCH")
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
#     @pytest.mark.global_payment_thailand_auto
#     @pytest.mark.global_payment_cimb
#     @pytest.mark.global_payment_cimb_withhold
#     def test_cimb_qrcode_reversefail(self):
#         # 1、这个通道不需要 mock，本条用例测试，已经成功的订单，再次还款
#         # 1、使用固定的 card_uuid 发起代扣
#         autopay_req, autopay_resp = global_withhold_autopay(sign_company, "qrcode", card_uuid=card_uuid, amount=amount)
#         # 检查autopay的response
#         check_autopay_response(autopay_resp, channel_name_qrcode, amount, payment_type="qrcode")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_GENERATE_QR_CODE", "KN_GENERATE_QR_CODE")
#
#         # 4、模拟通道发起payment_inquiry
#         inquiry_req, inquiry_resp = cimb_payment_inquiry(autopay_resp["data"]["channel_key"], amount / 100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("000", inquiry_resp["status"]["code"], "给通道的code正确")
#         Assert.assert_equal("Success", inquiry_resp["status"]["message"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_INQUIRY_SUCCESS", "KN_INQUIRY_SUCCESS")
#
#         # 5、模拟通道发起payment_confirm
#         confirm_req, confirm_resp = cimb_payment_confirm(autopay_resp["data"]["channel_key"], amount/100, "S")
#         # 检查payment_inquiry的response
#         Assert.assert_equal("000", confirm_resp["status"]["code"], "code正确")
#         Assert.assert_equal("Success", confirm_resp["status"]["message"], "给通道的msg正确")
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
#         inquiry_req, inquiry_resp = cimb_payment_inquiry(autopay_resp["data"]["channel_key"], amount / 100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("999", inquiry_resp["status"]["code"], "给通道的code正确")
#         Assert.assert_equal("KN_REPEAT_ORDER", inquiry_resp["status"]["message"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 2, channel_name_qrcode,
#                                "KN_TRANSFER_SUCCESS", "KN_TRANSFER_SUCCESS")
#
#     @pytest.mark.global_payment_cimb
#     @pytest.mark.global_payment_cimb_withhold
#     def test_cimb_qrcode_reverse(self):
#         # 1、这个通道不需要 mock，本条用例测试，已经失败的订单，再次还款
#         # 1、使用固定的 card_uuid 发起代扣
#         autopay_req, autopay_resp = global_withhold_autopay(sign_company, "qrcode", card_uuid=card_uuid, amount=amount)
#         # 检查autopay的response
#         check_autopay_response(autopay_resp, channel_name_qrcode, amount, payment_type="qrcode")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_GENERATE_QR_CODE", "KN_GENERATE_QR_CODE")
#
#         # 4、模拟通道发起payment_inquiry
#         inquiry_req, inquiry_resp = cimb_payment_inquiry(autopay_resp["data"]["channel_key"], amount / 10)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("999", inquiry_resp["status"]["code"], "给通道的code正确")
#         Assert.assert_equal("KN_ORDER_AMOUNT_NOT_MATCH", inquiry_resp["status"]["message"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "999", "KN_ORDER_AMOUNT_NOT_MATCH")
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
#         inquiry_req, inquiry_resp = cimb_payment_inquiry(autopay_resp["data"]["channel_key"], amount / 100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("000", inquiry_resp["status"]["code"], "给通道的code正确")
#         Assert.assert_equal("Success", inquiry_resp["status"]["message"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 3)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode,
#                                "KN_TIMEOUT_CLOSE_ORDER", "KN_ORDER_AMOUNT_NOT_MATCH")
#
#         # 8、再次模拟通道发起payment_confirm
#         confirm_req, confirm_resp = cimb_payment_confirm(autopay_resp["data"]["channel_key"], amount / 100, "S")
#         # 检查payment_inquiry的response
#         Assert.assert_equal("000", confirm_resp["status"]["code"], "code正确")
#         Assert.assert_equal("Success", confirm_resp["status"]["message"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 3)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode,
#                                "KN_TIMEOUT_CLOSE_ORDER", "KN_ORDER_AMOUNT_NOT_MATCH")
#
#         # 9、执行回调task#withholdCallback
#         run_task_by_order_no(autopay_resp["data"]["channel_key"], except_json={"code": 0, "message": "处理成功"})
#         run_task_by_order_no(autopay_req["merchant_key"])
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 2, channel_name_qrcode,
#                                "KN_REVERSE_ORDER", "KN_TRANSFER_SUCCESS")
#
#     @pytest.mark.global_payment_thailand_auto
#     @pytest.mark.global_payment_cimb
#     @pytest.mark.global_payment_cimb_withhold
#     def test_cimb_qrcode_amountfail2(self):
#         # 1、这个通道不需要 mock
#         # 1、使用固定的 card_uuid 发起代扣
#         autopay_req, autopay_resp = global_withhold_autopay(sign_company, "qrcode", card_uuid=card_uuid, amount=amount)
#         # 检查autopay的response
#         check_autopay_response(autopay_resp, channel_name_qrcode, amount, payment_type="qrcode")
#         # 检查数据库中的数据
#         check_withhold(autopay_req["merchant_key"], self.account, 1)
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_GENERATE_QR_CODE", "KN_GENERATE_QR_CODE")
#
#         # 4、模拟通道发起payment_inquiry
#         inquiry_req, inquiry_resp = cimb_payment_inquiry(autopay_resp["data"]["channel_key"], amount / 100)
#         # 检查payment_inquiry的response
#         Assert.assert_equal("000", inquiry_resp["status"]["code"], "给通道的code正确")
#         Assert.assert_equal("Success", inquiry_resp["status"]["message"], "给通道的msg正确")
#         # 检查数据库中的数据
#         check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
#                                "KN_INQUIRY_SUCCESS", "KN_INQUIRY_SUCCESS")
#
#         # 5、模拟通道发起payment_confirm
#         confirm_req, confirm_resp = cimb_payment_confirm(autopay_resp["data"]["channel_key"], amount / 10, "S")
#         # 检查payment_inquiry的response
#         Assert.assert_equal("000", confirm_resp["status"]["code"], "code正确")
#         Assert.assert_equal("Success", confirm_resp["status"]["message"], "给通道的msg正确")
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
#
#
