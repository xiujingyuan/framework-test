# import pytest
#
# from biztest.config.payment.url_config import global_sign_company_yomoyo3, user_operator, payment_type_ebank, \
#     global_amount, global_razorpay_ebank_payment_mode, global_razorpay_ebank_channel_key, \
#     global_withhold_successed_msg, global_paymentMode, global_cashfree_ebank_channel_key, \
#     global_razorpay_ebank_success_message, global_razorpay_collect_channel_option_upi, \
#     global_razorpay_ebank_service_fee, global_razorpay_ebank_service_tax
# from biztest.function.global_payment.global_payment_db_assert import \
#     assert_check_withhold_withholdreceipt, assert_check_razorpay_channelrequestlog, \
#     assert_check_cashfree_channelrequestlog, assert_withhold_success, run_task_by_merchantkey_channelkey
# from biztest.function.global_payment.global_payment_db_operation import update_global_channel_ebank_only_razorpay, \
#     update_channel_status_allusable, \
#     get_withhold_receipt_by_merchant_key, update_kv_mockrazorpay, undo_update_kv_mockrazorpay, \
#     update_kv_mockcashfree, undo_update_kv_mockcashfree, update_global_channel_ebank_only_cashfree, \
#     get_withhold_by_merchant_key, get_none_carduuid, \
#     get_none_cardandaccount_bycarduuid
# from biztest.function.payment.common import get_mobile, get_bank_account, get_english_name
# from biztest.interface.payment.payment_interface import get_timestamp, global_withhold_autopay_no_carduuid, \
#     global_encrypt
# from biztest.util.db.db_util import DataBase, time
# from biztest.util.easymock.global_payment.global_payment_cashfree import CashfreeMock
# from biztest.util.easymock.global_payment.global_payment_razorpay import RazorpayMock
#
#
# # 无卡支付
# class TestIndiaNocardpay:
#     """
#     global nocard pay
#     author: fangchangfang
#     date: 2020
#     """
#
#     @classmethod
#     def setup_class(self):
#         self.env_test = pytest.config.getoption("--env") if hasattr(pytest, "config") else 1
#         self.db_test_payment = DataBase("global_payment_test%s" % self.env_test)
#         update_kv_mockrazorpay(self.db_test_payment)
#         update_kv_mockcashfree(self.db_test_payment)
#
#     def teardown_class(self):
#         undo_update_kv_mockrazorpay(self.db_test_payment)
#         undo_update_kv_mockcashfree(self.db_test_payment)
#         update_channel_status_allusable(self.db_test_payment)
#         DataBase.close_connects()
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_nocardpay
#     def test_nocard_razorpay_ebank_success(self):
#         # 无卡支付：走razorpay通道
#         update_channel_status_allusable(self.db_test_payment)
#         update_global_channel_ebank_only_razorpay(self.db_test_payment)
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_success_003()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.upi_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.email_encrypt = self.upi_encrypt  # 用upi作为email
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay_no_carduuid(merchant_key, global_sign_company_yomoyo3,
#                                                                     self.user_name_encrypt, self.mobile_encrypt,
#                                                                     self.email_encrypt, user_operator,
#                                                                     payment_type_ebank)
#         # ebank是网关支付，请求成功一定是返回code=2处理中
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"
#         # 手动执行task
#         run_task_by_merchantkey_channelkey(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 无法统一的断言，cashfree的mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         withhold_info = get_withhold_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "paid", '代扣成功'
#         assert withhold_receipt_info[0][
#                    "withhold_receipt_channel_resp_message"] == global_razorpay_ebank_success_message, '超时关单失败原因'
#         assert withhold_receipt_info[0][
#                    "withhold_receipt_payment_option"] == global_razorpay_collect_channel_option_upi, '支付方式'
#         assert withhold_receipt_info[0]["withhold_receipt_payment_mode"] == '', '支付方式'
#         assert withhold_receipt_info[0][
#                    "withhold_receipt_channel_inner_key"] == global_razorpay_ebank_channel_key, '通道流水号'
#         assert withhold_receipt_info[0][
#                    "withhold_receipt_service_charge"] == global_razorpay_ebank_service_fee - global_razorpay_ebank_service_tax, '通道流水号'
#         assert withhold_receipt_info[0]["withhold_receipt_service_tax"] == global_razorpay_ebank_service_tax, '通道流水号'
#         # 无卡支付会生成临时卡
#         card_account_info = get_none_cardandaccount_bycarduuid(self.db_test_payment,
#                                                                withhold_info[0]["withhold_card_uuid"])
#         assert card_account_info[0]['card_auth_mode'] == "none"
#         assert card_account_info[0]['account_auth_mode'] == "none"
#         assert card_account_info[0]['card_mobile'] == self.mobile_encrypt
#         assert card_account_info[0]['card_username'] == self.user_name_encrypt
#         assert card_account_info[0]['card_email'] == self.email_encrypt
#         assert card_account_info[0]['card_num'] == withhold_receipt_info[0]["withhold_receipt_card_num"]
#         assert card_account_info[0]['account_card_num'] == withhold_receipt_info[0]["withhold_receipt_card_num"]
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key,
#                                 resp_withhold_autopay['content']['data']['channel_key'],
#                                 resp_withhold_autopay['content']['data']['channel_name'],
#                                 withhold_info[0]["withhold_card_uuid"], global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, withhold_info[0]["withhold_card_uuid"],
#                                               merchant_key,
#                                               withhold_receipt_info[0]["withhold_receipt_card_num"],
#                                               resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#         update_channel_status_allusable(self.db_test_payment)  # 还原环境，下一步可能会用
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_nocardpay
#     def test_nocard_havecarduuid_razorpay_ebank_success(self):
#         # 无卡支付：已有card_uuid的无卡支付，走razorpay通道
#         update_channel_status_allusable(self.db_test_payment)
#         update_global_channel_ebank_only_razorpay(self.db_test_payment)
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_success_003()
#         # 选已有card_uuid的数据再次无卡支付
#         card_account_info = get_none_carduuid(self.db_test_payment)
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay_no_carduuid(merchant_key, global_sign_company_yomoyo3,
#                                                                     card_account_info[0]["card_username"],
#                                                                     card_account_info[0]["card_mobile"],
#                                                                     card_account_info[0]["card_email"], user_operator,
#                                                                     payment_type_ebank)
#         # cashfree_ebank是网关支付，请求成功一定是返回code=2处理中
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"
#         # 手动执行task
#         run_task_by_merchantkey_channelkey(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 无法统一的断言，cashfree的mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         withhold_info = get_withhold_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "paid", '代扣成功'
#         assert withhold_receipt_info[0][
#                    "withhold_receipt_channel_resp_message"] == global_razorpay_ebank_success_message, '超时关单失败原因'
#         assert withhold_receipt_info[0][
#                    "withhold_receipt_payment_option"] == global_razorpay_collect_channel_option_upi, '支付方式'
#         assert withhold_receipt_info[0]["withhold_receipt_payment_mode"] == '', '支付方式'
#         assert withhold_receipt_info[0][
#                    "withhold_receipt_channel_inner_key"] == global_razorpay_ebank_channel_key, '通道流水号'
#         assert withhold_receipt_info[0][
#                    "withhold_receipt_service_charge"] == global_razorpay_ebank_service_fee - global_razorpay_ebank_service_tax, '通道流水号'
#         assert withhold_receipt_info[0]["withhold_receipt_service_tax"] == global_razorpay_ebank_service_tax, '通道流水号'
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key,
#                                 resp_withhold_autopay['content']['data']['channel_key'],
#                                 resp_withhold_autopay['content']['data']['channel_name'],
#                                 withhold_info[0]["withhold_card_uuid"], global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_account_info[0]["account_card_uuid"],
#                                               merchant_key,
#                                               card_account_info[0]["account_card_num"], resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#         update_channel_status_allusable(self.db_test_payment)  # 还原环境，下一步可能会用
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_nocardpay
#     def test_nocard_cashfree_ebank_success(self):
#         # 无卡支付：走cashfree通道
#         update_channel_status_allusable(self.db_test_payment)
#         update_global_channel_ebank_only_cashfree(self.db_test_payment)
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_cashfree_withhold_query_success()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.upi_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.email_encrypt = self.upi_encrypt  # 用upi作为email
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay_no_carduuid(merchant_key, global_sign_company_yomoyo3,
#                                                                     self.user_name_encrypt, self.mobile_encrypt,
#                                                                     self.email_encrypt, user_operator,
#                                                                     payment_type_ebank)
#         # cashfree_ebank是网关支付，请求成功一定是返回code=2处理中
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"
#         # 手动执行task
#         run_task_by_merchantkey_channelkey(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 无法统一的断言，cashfree的mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         withhold_info = get_withhold_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "PAID-SUCCESS", '代扣成功'
#         assert withhold_receipt_info[0][
#                    "withhold_receipt_channel_resp_message"] == global_withhold_successed_msg, '代扣超时'
#         assert withhold_receipt_info[0]["withhold_receipt_payment_mode"] == global_paymentMode, '支付方式'
#         assert withhold_receipt_info[0][
#                    "withhold_receipt_channel_inner_key"] == global_cashfree_ebank_channel_key, '通道流水号'
#         # 无卡支付会生成临时卡
#         card_account_info = get_none_cardandaccount_bycarduuid(self.db_test_payment,
#                                                                withhold_info[0]["withhold_card_uuid"])
#         assert card_account_info[0]['card_auth_mode'] == "none"
#         assert card_account_info[0]['account_auth_mode'] == "none"
#         assert card_account_info[0]['card_mobile'] == self.mobile_encrypt
#         assert card_account_info[0]['card_username'] == self.user_name_encrypt
#         assert card_account_info[0]['card_email'] == self.email_encrypt
#         assert card_account_info[0]['card_num'] == withhold_receipt_info[0]["withhold_receipt_card_num"]
#         assert card_account_info[0]['account_card_num'] == withhold_receipt_info[0]["withhold_receipt_card_num"]
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key,
#                                 resp_withhold_autopay['content']['data']['channel_key'],
#                                 resp_withhold_autopay['content']['data']['channel_name'],
#                                 withhold_info[0]["withhold_card_uuid"], global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, withhold_info[0]["withhold_card_uuid"],
#                                               merchant_key,
#                                               withhold_receipt_info[0]["withhold_receipt_card_num"],
#                                               resp_withhold_autopay)
#         assert_check_cashfree_channelrequestlog(self.db_test_payment, merchant_key)
#         update_channel_status_allusable(self.db_test_payment)  # 还原环境，下一步可能会用
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_nocardpay
#     def test_nocard_havecarduuid_cashfree_ebank_success(self):
#         # 无卡支付：已有card_uuid的无卡支付，走cashfree通道
#         update_channel_status_allusable(self.db_test_payment)
#         update_global_channel_ebank_only_cashfree(self.db_test_payment)
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_cashfree_withhold_query_success()
#         # 选已有card_uuid的数据再次无卡支付
#         card_account_info = get_none_carduuid(self.db_test_payment)
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay_no_carduuid(merchant_key, global_sign_company_yomoyo3,
#                                                                     card_account_info[0]["card_username"],
#                                                                     card_account_info[0]["card_mobile"],
#                                                                     card_account_info[0]["card_email"], user_operator,
#                                                                     payment_type_ebank)
#         # cashfree_ebank是网关支付，请求成功一定是返回code=2处理中
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"
#         # 手动执行task
#         run_task_by_merchantkey_channelkey(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 无法统一的断言，cashfree的mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         withhold_info = get_withhold_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "PAID-SUCCESS", '代扣成功'
#         assert withhold_receipt_info[0][
#                    "withhold_receipt_channel_resp_message"] == global_withhold_successed_msg, '代扣超时'
#         assert withhold_receipt_info[0]["withhold_receipt_payment_mode"] == global_paymentMode, '支付方式'
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key,
#                                 resp_withhold_autopay['content']['data']['channel_key'],
#                                 resp_withhold_autopay['content']['data']['channel_name'],
#                                 withhold_info[0]["withhold_card_uuid"], global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_account_info[0]["account_card_uuid"],
#                                               merchant_key, card_account_info[0]["account_card_num"], resp_withhold_autopay)
#         assert_check_cashfree_channelrequestlog(self.db_test_payment, merchant_key)
#         update_channel_status_allusable(self.db_test_payment)  # 还原环境，下一步可能会用
