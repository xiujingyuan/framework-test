# import pytest
# from biztest.config.payment.url_config import user_operator, global_amount, \
#     taiguo_sign_company_cymo2, payment_mode_promptpay, payment_option_qrcode, payment_type_qrcode, payment_type_ebank, \
#     global_sign_company_cymo1
# from biztest.function.global_payment.global_payment_db_assert import assert_withhold_success, \
#     assert_check_withhold_withholdreceipt, assert_withhold_fail, autobind_result_fail_query, \
#     assert_verify_check_card_account_binding_bindingrequest, assert_accountverify_check_cardandaccount_auth_mode, \
#     assert_verify_fail, autobind_result_success_query, assert_verify_success
# from biztest.function.global_payment.global_payment_db_operation import update_channel_status_allusable, \
#     get_withhold_receipt_by_merchant_key, get_withhold_by_merchant_key, \
#     insert_kser_qrcode_callback, update_withhold_receipt_create_at, update_kuainiu_cymo1_verify_check, \
#     update_kuainiu_cymo1_verify_uncheck, update_kuainiu_cymo1_verify_check_fail
# from biztest.function.payment.common import get_mobile, get_bank_account, get_english_name
# from biztest.interface.payment.payment_interface import get_timestamp, global_withhold_autopay_no_carduuid, \
#     run_task_by_task_order_no, global_encrypt, global_autobind
# from biztest.util.db.db_util import DataBase
# from biztest.util.tools.tools import get_sysconfig, get_four_element_global
#
#
# # ksher没有用mock，依赖通道测试环境，可能随时会失败
# class TestThailandKsher:
#     """
#     global thailand ksher
#     author: liutianbao
#     date: 2020
#     """
#
#     @classmethod
#     def setup_class(self):
#         self.env_test = get_sysconfig("--env")
#         self.db_test_payment = DataBase("taiguo_global_payment_test%s" % self.env_test)
#         # 初始化一些基础信息
#         self.ifsc = "mock_test_0001"
#         self.email_encrypt = "enc_05_2752999188760895488_191"  # 随意邮箱
#         self.address_encrypt = "enc_06_2752832664892874752_745"  # 随意邮箱
#
#     @classmethod
#     def teardown_class(self):
#         # 还原环境
#         update_kuainiu_cymo1_verify_check(self.db_test_payment)
#         DataBase.close_connects()
#
#     @pytest.mark.global_payment_thailand
#     @pytest.mark.global_taiguo_nocardpay
#     def test_autobind_fail001_kuainiu_account(self):
#         # 绑卡失败（泰国默认绑卡通道是同步的，不存在处理中）
#         update_kuainiu_cymo1_verify_check_fail(self.db_test_payment)
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_cymo1, self.bank_account_encrypt,
#                                         upi_encrypt, self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         assert resp_autobind["content"]["code"] == 1, "绑卡验证失败"
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autobind_result_fail_query(self.merchant_key)
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.bank_account_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_accountverify_check_cardandaccount_auth_mode(self.db_test_payment, self.bank_account_encrypt)
#         assert_verify_fail(self.db_test_payment, self.bank_account_encrypt)
#
#     @pytest.mark.global_payment_thailand
#     @pytest.mark.global_taiguo_nocardpay
#     def test_autobind_success_kuainiu_account(self):
#         # 绑卡失败（泰国默认绑卡通道是同步的，不存在处理中）
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # 更新KV不验证三要素的正确性，全部返回绑卡成功
#         update_kuainiu_cymo1_verify_uncheck(self.db_test_payment)
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_cymo1, self.bank_account_encrypt,
#                                         upi_encrypt, self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         assert resp_autobind["content"]["code"] == 0, "绑卡验证失败"
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autobind_result_success_query(self.merchant_key)
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.bank_account_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_accountverify_check_cardandaccount_auth_mode(self.db_test_payment, self.bank_account_encrypt)
#         assert_verify_success(self.db_test_payment, self.bank_account_encrypt)
#
#     @pytest.mark.global_payment_thailand
#     @pytest.mark.global_taiguo_nocardpay
#     def test_nocard_ksher_qrcode_success(self):
#         # 无卡支付：走ksher通道
#         update_channel_status_allusable(self.db_test_payment)
#         # 三要素数据进行海外global_payment_yinni加密处理，海外不需要传身份证
#         self.four_element = get_four_element_global()
#         self.mobile_encrypt = self.four_element["data"]["user_name_encrypt"]
#         self.user_name_encrypt = self.four_element["data"]["user_name_encrypt"]
#         self.email_encrypt = self.four_element["data"]["user_name_encrypt"]  # 用upi作为email
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay_no_carduuid(merchant_key, taiguo_sign_company_cymo2,
#                                                                     self.user_name_encrypt, self.mobile_encrypt,
#                                                                     self.email_encrypt, user_operator,
#                                                                     payment_type_qrcode, payment_option_qrcode,
#                                                                     payment_mode_promptpay)
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"  # 依赖于通道代扣请求的返回
#         # 调用通道模拟代扣成功的接口
#         insert_kser_qrcode_callback(self.db_test_payment, withhold_receipt_info[0]["withhold_receipt_channel_key"])
#
#         # 手动执行callback
#         run_task_by_task_order_no(**{"orderNo": withhold_receipt_info[0]["withhold_receipt_channel_key"]})
#         run_task_by_task_order_no(**{"orderNo": merchant_key})
#
#         # 无法统一的断言，kuainiu的mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         withhold_info = get_withhold_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "SUCCESS", '代扣成功'
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_message"] == "SUCCESS", '代扣成功'
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key,
#                                 resp_withhold_autopay['content']['data']['channel_key'],
#                                 resp_withhold_autopay['content']['data']['channel_name'],
#                                 withhold_info[0]["withhold_card_uuid"], global_amount)
#         # 数据断言
#         assert_check_withhold_withholdreceipt(self.db_test_payment, withhold_info[0]["withhold_card_uuid"],
#                                               merchant_key,
#                                               withhold_receipt_info[0]["withhold_receipt_card_num"],
#                                               resp_withhold_autopay)
#
#     @pytest.mark.global_payment_thailand
#     @pytest.mark.global_taiguo_nocardpay
#     def test_nocard_ksher_qrcode_timeout(self):
#         # 无卡支付：走ksher通道
#         update_channel_status_allusable(self.db_test_payment)
#         # 三要素数据进行海外global_payment_yinni加密处理，海外不需要传身份证
#         self.four_element = get_four_element_global()
#         self.mobile_encrypt = self.four_element["data"]["user_name_encrypt"]
#         self.user_name_encrypt = self.four_element["data"]["user_name_encrypt"]
#         self.email_encrypt = self.four_element["data"]["user_name_encrypt"]  # 用upi作为email
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay_no_carduuid(merchant_key, taiguo_sign_company_cymo2,
#                                                                     self.user_name_encrypt, self.mobile_encrypt,
#                                                                     self.email_encrypt, user_operator,
#                                                                     payment_type_qrcode, payment_option_qrcode,
#                                                                     payment_mode_promptpay)
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"  # 依赖于通道代扣请求的返回
#         # 调用通道模拟代扣成功的接口
#         update_withhold_receipt_create_at(self.db_test_payment, merchant_key, month=-1)
#
#         # 手动执行callback
#         run_task_by_task_order_no(**{"orderNo": merchant_key})
#         run_task_by_task_order_no(**{"orderNo": merchant_key})
#
#         # 数据断言
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         withhold_info = get_withhold_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "KN_TIMEOUT_CLOSE_ORDER", '代扣超时'
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_message"] == "KN_REQUEST_SUCCESS", '代扣超时'
#         assert_withhold_fail(self.db_test_payment, merchant_key, resp_withhold_autopay['content']['data']['channel_key'],
#                              resp_withhold_autopay['content']['data']['channel_name'],
#                              withhold_info[0]["withhold_card_uuid"], global_amount)
#
#     @pytest.mark.global_payment_thailand
#     @pytest.mark.global_taiguo_nocardpay
#     def test_nocard_ksher_ebank_timeout(self):
#         # 无卡支付：走ksher通道
#         update_channel_status_allusable(self.db_test_payment)
#         # 三要素数据进行海外global_payment_yinni加密处理，海外不需要传身份证
#         self.four_element = get_four_element_global()
#         self.mobile_encrypt = self.four_element["data"]["user_name_encrypt"]
#         self.user_name_encrypt = self.four_element["data"]["user_name_encrypt"]
#         self.email_encrypt = self.four_element["data"]["user_name_encrypt"]  # 用upi作为email
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay_no_carduuid(merchant_key, taiguo_sign_company_cymo2,
#                                                                     self.user_name_encrypt, self.mobile_encrypt,
#                                                                     self.email_encrypt, user_operator,
#                                                                     payment_type_ebank, "", "")
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"  # 依赖于通道代扣请求的返回
#         # 调用通道模拟代扣成功的接口
#         update_withhold_receipt_create_at(self.db_test_payment, merchant_key, month=-1)
#
#         # 手动执行callback
#         run_task_by_task_order_no(**{"orderNo": merchant_key})
#         run_task_by_task_order_no(**{"orderNo": merchant_key})
#
#         # 数据断言
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         withhold_info = get_withhold_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "KN_TIMEOUT_CLOSE_ORDER", '代扣超时'
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_message"] == "KN_REQUEST_SUCCESS", '代扣超时'
#         assert_withhold_fail(self.db_test_payment, merchant_key, resp_withhold_autopay['content']['data']['channel_key'],
#                              resp_withhold_autopay['content']['data']['channel_name'],
#                              withhold_info[0]["withhold_card_uuid"], global_amount)