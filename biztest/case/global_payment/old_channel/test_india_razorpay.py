# # -*- coding: utf-8 -*-
#
# import pytest
#
# from biztest.config.payment.url_config import global_sign_company_yomoyo, \
#     global_withdraw_failed_message, global_NAME_NOT_MATCH, \
#     global_razorpay_ebank_fail_message, global_razorpay_ebank_payment_mode, global_razorpay_ebank_channel_key, \
#     global_order_not_exists, global_razorpay_withdraw_balance, \
#     global_cashfree_total_amount_lubi, global_cashfree_available_amount_lubi, global_order_binding_fail, \
#     global_razorpay_withdraw_inner_key, global_razorpay_withdraw_mode, global_razorpay_withdraw_fail_rejected, \
#     global_razorpay_withdraw_fail_cancelled, global_razorpay_withdraw_fail_reversed, \
#     global_razorpay_withdraw_success_processed, global_razorpay_withdraw_contact_id, \
#     global_razorpay_withdraw_fund_account_id, user_operator, payment_type_ebank, \
#     global_amount, global_razorpay_ebank_service_tax, global_razorpay_ebank_service_fee, india_bind_channel_name, \
#     global_razorpay_ebank_payment_option, global_razorpay_ebank_payment_option_card, \
#     global_razorpay_ebank_payment_mode_card, global_razorpay_ebank_success_message, \
#     global_razorpay_collect_channel_option_upi, global_razorpay_collect_payment_mode_upi
# from biztest.function.global_payment.global_payment_db_operation import get_global_card_info_by_card_account, \
#     get_global_binding_info_by_card_num, get_global_binding_request_info_by_card_num, \
#     get_global_withdraw_receipt_info_by_trade_no, get_withhold_receipt_by_merchant_key, \
#     get_usable_card_uuid, get_global_card_info_by_card_num, \
#     update_global_channel_ebank_only_razorpay, update_kv_mockrazorpay, undo_update_kv_mockrazorpay, \
#     update_global_channel_verify_only_razorpay, \
#     update_channel_status_allusable, undo_update_global_channel_withdraw_only_razorpay, \
#     update_global_channel_withdraw_only_razorpay, update_kv_withdraw_riskwhite, undo_update_kv_withdraw_riskwhite, \
#     delete_binding, get_usable_razorpay_withdraw_carduuid, update_kv_mockcashfree, \
#     undo_update_kv_mockcashfree, update_kv_verify_unchecked_name, update_kv_verify_checked_name, \
#     update_withhold_receipt_inner_key_null, by_carduuid_get_ccountandbinding_info, update_kv_razorpay_verify_false, \
#     update_kv_razorpay_verify_true
# from biztest.interface.payment.payment_interface import get_timestamp, global_Withdraw_balance, global_encrypt, \
#     global_withhold_autopay, global_autobind
# from biztest.util.asserts.assert_util import Assert
# from biztest.util.db.db_util import DataBase
# from biztest.function.payment.common import get_english_name, get_mobile, get_bank_account
# from biztest.util.easymock.global_payment.global_payment_cashfree import CashfreeMock
# from biztest.util.easymock.global_payment.global_payment_razorpay import RazorpayMock
# from biztest.interface.payment.payment_interface import time
# from biztest.function.global_payment.global_payment_db_assert import \
#     autobind_result_success_query, assert_verify_success, \
#     assert_verify_fail, autobind_result_fail_query, autobind_result_process_query, assert_verify_process, \
#     assert_check_withhold_withholdreceipt, assert_withhold_success, assert_withhold_fail, \
#     assert_withhold_process, assert_check_razorpay_channelrequestlog, \
#     assert_verify_check_card_account_binding_bindingrequest, \
#     assert_accountverify_check_cardandaccount_auth_mode, run_task_bindingQuery, \
#     withdraw_autoWithdraw, run_task_withdraw_and_withdrawquery, \
#     assert_check_withdraw_withdrawreceipt, assert_withdraw_fail, assert_check_razorpay_withdraw_channelrequestlog, \
#     assert_withdraw_process, assert_withdraw_success, run_task_withholdReceipt_withholdcharge_and_chargequery, \
#     assert_check_autopay_resp_data
#
#
# # global_payment下razorpay通道： account绑卡 & ebank代扣
# class TestIndiaRazorpay:
#     """
#     global razorpay
#     author: fangchangfang
#     date: 2020
#     """
#
#     @classmethod
#     def setup_class(self):
#         self.env_test = pytest.config.getoption("--env") if hasattr(pytest, "config") else 1
#         self.db_test_payment = DataBase("global_payment_test%s" % self.env_test)
#         # 修改KV中地址改为easymock
#         update_kv_mockrazorpay(self.db_test_payment)
#         update_kv_mockcashfree(self.db_test_payment)
#         # 放款次数更新到很大
#         undo_update_kv_withdraw_riskwhite(self.db_test_payment)
#         # 让绑卡&代扣路由到razorpay，把其他通道置为不可用
#         update_channel_status_allusable(self.db_test_payment)
#         update_global_channel_verify_only_razorpay(self.db_test_payment)
#         update_global_channel_ebank_only_razorpay(self.db_test_payment)
#         update_global_channel_withdraw_only_razorpay(self.db_test_payment)
#         # 初始化一些基础信息
#         self.ifsc = "mock_test_0001"
#         self.address_encrypt = "enc_06_2752832664892874752_745"  # 随意邮箱
#         self.user_name_encrypt = "enc_04_2752870379604680704_505"
#         self.mobile_encrypt = "enc_01_2752562028249358336_117"
#         self.email_encrypt = "enc_05_2752999188760895488_191"
#
#     def teardown_class(self):
#         # 还原环境
#         undo_update_kv_mockcashfree(self.db_test_payment)
#         undo_update_kv_mockrazorpay(self.db_test_payment)
#         update_channel_status_allusable(self.db_test_payment)
#         undo_update_kv_withdraw_riskwhite(self.db_test_payment)
#         update_kv_razorpay_verify_false(self.db_test_payment,"razorpay_yomoyo_verify")
#         DataBase.close_connects()
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     def test_autobind_process_razorpay_account(self):
#         # 在第三步打款验证返回处理中以及在第四步打款验证查询也返回处理中
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_bind_process_razorpay_steps3()
#         global_payment_mock.update_bind_query_process_razorpay_steps4()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": "mock" + " " + get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq，razorpy绑卡可能是异步的
#         assert resp_autobind["content"]["code"] == 2, "绑卡验证处理中"  # update_bind_process_razorpay_steps3由这一步mock决定
#         run_task_bindingQuery(self.db_test_payment, self.bank_account_encrypt)  # 手动执行task-bindingQuery
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autobind_result_process_query(self.merchant_key)
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.bank_account_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_accountverify_check_cardandaccount_auth_mode(self.db_test_payment, self.bank_account_encrypt)
#         assert_verify_process(self.db_test_payment, self.bank_account_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     def test_autobind_fail_razorpay_account_001(self):
#         # razorpay绑卡是异步的，razorpay第1步创建联系人直接绑卡失败
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_fail_razorpay_steps1()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": "mock" + " " + get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq的参数断言，以及绑卡成功后检查binding_request和binding表
#         assert resp_autobind["content"]["code"] == 1, "绑卡验证处理中"  # update_bind_fail_razorpay_steps1由这一步mock决定
#         run_task_bindingQuery(self.db_test_payment, self.bank_account_encrypt)  # 手动执行task-bindingQuery
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
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     def test_autobind_fail_razorpay_account_002(self):
#         # razorpay第2步创建资金账户直接绑卡失败
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_fail_razorpay_steps2()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": "mock" + " " + get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq的参数断言，以及绑卡成功后检查binding_request和binding表
#         assert resp_autobind["content"]["code"] == 1, "绑卡失败"  # update_bind_fail_razorpay_steps2由这一步mock决定
#         run_task_bindingQuery(self.db_test_payment, self.bank_account_encrypt)  # 手动执行task-bindingQuery
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
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     def test_autobind_fail_razorpay_account_003(self):
#         # razorpay第3步打款验证直接绑卡失败
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_bind_fail001_razorpay_steps3()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": "mock" + " " + get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq的参数断言，以及绑卡成功后检查binding_request和binding表
#         assert resp_autobind["content"]["code"] == 1, "绑卡直接失败-打款验证失败"  # update_bind_fail001_razorpay_steps3由这一步mock决定
#         # 打款验证直接失败不会生成绑卡查询task-bindingQuery
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
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     def test_autobind_fail_razorpay_account_004(self):
#         # razorpay第3步打款验证处理中 且 在第4步查询到绑卡失败
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_bind_process_razorpay_steps3()
#         global_payment_mock.update_bind_query_fail001_razorpay_steps4()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": "mock" + " " + get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq的参数断言，以及绑卡成功后检查binding_request和binding表
#         assert resp_autobind["content"]["code"] == 2, "绑卡验证处理中"  # update_bind_process_razorpay_steps3由这一步mock决定
#         run_task_bindingQuery(self.db_test_payment, self.bank_account_encrypt)  # 手动执行task-bindingQuery
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
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     def test_autobind_fail_razorpay_account_005(self):
#         # razorpay绑卡打款验证第3步返回接口处理中，在第4步结果查询到绑卡成功但是名字不一样，最终绑卡失败
#         update_kv_razorpay_verify_true(self.db_test_payment,"razorpay_yomoyo_verify")
#         update_kv_mockrazorpay(self.db_test_payment)
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_bind_process_razorpay_steps3()
#         global_payment_mock.update_bind_fail_razorpay_steps4()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": "mock" + " " + get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq的参数断言，以及绑卡成功后检查binding_request和binding表
#         assert resp_autobind["content"]["code"] == 2, "绑卡验证处理中"  # update_bind_process_razorpay_steps3由这一步mock决定
#         run_task_bindingQuery(self.db_test_payment, self.bank_account_encrypt)  # 手动执行task-bindingQuery
#         card_info = get_global_card_info_by_card_account(self.db_test_payment, self.bank_account_encrypt)
#         binding_request_info = get_global_binding_request_info_by_card_num(self.db_test_payment,
#                                                                            card_info[0]["card_num"])
#         # 无法统一的断言，由mock决定
#         assert binding_request_info[0]["binding_request_channel_code"] == global_NAME_NOT_MATCH  # 只有在绑卡返回名字不一样才会记录为KN_ACCOUNT_NAME_NOT_MATCH
#         assert binding_request_info[0]["binding_request_channel_message"] == "the similarity is less than 0.8"
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
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     def test_autobind_fail_razorpay_account_006(self):
#         # razorpay绑卡打款验证第3步查询到绑卡成功但是名字不一样，最终绑卡失败
#         update_kv_razorpay_verify_true(self.db_test_payment,"razorpay_yomoyo_verify")
#         update_kv_mockrazorpay(self.db_test_payment)
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_bind_success_razorpay_steps3("mock" + " " + get_english_name())  # 不加mock
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()  # 不加mock
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq的参数断言，以及绑卡成功后检查binding_request和binding表
#         assert resp_autobind["content"]["code"] == 1, "绑卡验证处理中"
#         run_task_bindingQuery(self.db_test_payment, self.bank_account_encrypt)  # 手动执行task-bindingQuery
#         card_info = get_global_card_info_by_card_account(self.db_test_payment, self.bank_account_encrypt)
#         binding_request_info = get_global_binding_request_info_by_card_num(self.db_test_payment, card_info[0]["card_num"])
#         # 无法统一的断言，由mock决定
#         assert binding_request_info[0]["binding_request_channel_code"] == global_NAME_NOT_MATCH  # 只有在绑卡返回名字不一样才会记录为KN_ACCOUNT_NAME_NOT_MATCH
#         assert binding_request_info[0]["binding_request_channel_message"] == "the similarity is less than 0.8"
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
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     def test_autobind_fail_razorpay_account_007(self):
#         # 在第三步打款验证返回处理中以及在第四步打款验证查询也返回处理中，但在绑卡结果查询/card/bindResult返回绑卡失败
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_bind_process_razorpay_steps3()
#         global_payment_mock.update_bind_query_process_razorpay_steps4()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": "mock" + " " + get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq的参数断言，以及绑卡成功后检查binding_request和binding表
#         assert resp_autobind["content"]["code"] == 2, "绑卡验证处理中"  # update_bind_process_razorpay_steps3由这一步mock决定
#         run_task_bindingQuery(self.db_test_payment, self.bank_account_encrypt)  # 手动执行task-bindingQuery
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_fail_razorpay_steps4()
#         autobind_result_fail_query(self.merchant_key)
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.bank_account_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_accountverify_check_cardandaccount_auth_mode(self.db_test_payment, self.bank_account_encrypt)
#         assert_verify_fail(self.db_test_payment, self.bank_account_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     @pytest.mark.global_razorpay_autobind_success
#     def test_autobind_success_razorpay_account_001(self):
#         # 在第三步打款验证返回处理中以及在第四步打款验证查询也返回处理中，但在绑卡结果查询/card/bindResult返回绑卡成功：返回的姓名和请求姓名一致
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_bind_process_razorpay_steps3()
#         global_payment_mock.update_bind_query_process_razorpay_steps4()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": "mock" + " " + get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq，razorpy绑卡可能是异步的
#         assert resp_autobind["content"]["code"] == 2, "绑卡验证处理中"  # update_bind_process_razorpay_steps3由这一步mock决定
#         run_task_bindingQuery(self.db_test_payment, self.bank_account_encrypt)  # 手动执行task-bindingQuery
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps4("mock" + " " + get_english_name())
#         autobind_result_success_query(self.merchant_key)        # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.bank_account_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_accountverify_check_cardandaccount_auth_mode(self.db_test_payment, self.bank_account_encrypt)
#         assert_verify_success(self.db_test_payment, self.bank_account_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     @pytest.mark.global_razorpay_autobind_success
#     def test_autobind_success_razorpay_account_002(self):
#         # razorpay绑卡打款验证第3步直接返回绑卡成功：返回的姓名和请求姓名一致
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": "mock" + " " + get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # razorpay绑卡打款验证第3步直接返回绑卡成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_bind_success_razorpay_steps3(
#             "mock" + " " + get_english_name())  # 名字前面加上mock是因为对名字有检验，绑卡成功必须有一部分一样
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq的参数断言，以及绑卡成功后检查binding_request和binding表
#         assert resp_autobind["content"]["code"] == 0, "绑卡验证处理中"  # update_bind_success_razorpay_steps3由这一步mock决定
#         run_task_bindingQuery(self.db_test_payment, self.bank_account_encrypt)  # 手动执行task-bindingQuery
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autobind_result_success_query(self.merchant_key)
#         # 数据库断言
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.bank_account_encrypt,
#                                                                 resp_autobind,
#                                                                 self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_accountverify_check_cardandaccount_auth_mode(self.db_test_payment, self.bank_account_encrypt)
#         assert_verify_success(self.db_test_payment, self.bank_account_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     @pytest.mark.global_razorpay_autobind_success
#     def test_autobind_success_razorpay_account_003(self):
#         # razorpay绑卡打款验证第3步返回接口处理中，在第4步结果查询到绑卡成功：返回的姓名和请求姓名一致
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": "mock" + " " + get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # razorpay绑卡打款验证第3步返回接口处理中，在第4步结果查询到绑卡成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_bind_process_razorpay_steps3()
#         global_payment_mock.update_bind_success_razorpay_steps4(
#             "mock" + " " + get_english_name())  # 名字前面加上mock是因为对名字有检验，绑卡成功必须有一部分一样
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq的参数断言，以及绑卡成功后检查binding_request和binding表
#         assert resp_autobind["content"]["code"] == 2, "绑卡验证处理中"  # update_bind_process_razorpay_steps3由这一步mock决定
#         run_task_bindingQuery(self.db_test_payment, self.bank_account_encrypt)  # 手动执行task-bindingQuery
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autobind_result_success_query(self.merchant_key)
#         card_info = get_global_card_info_by_card_account(self.db_test_payment, self.bank_account_encrypt)
#         binding_request_info = get_global_binding_request_info_by_card_num(self.db_test_payment, card_info[0]["card_num"])
#         assert binding_request_info[0]["binding_request_channel_code"] == "active"
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.bank_account_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_accountverify_check_cardandaccount_auth_mode(self.db_test_payment, self.bank_account_encrypt)
#         assert_verify_success(self.db_test_payment, self.bank_account_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     @pytest.mark.global_razorpay_autobind_success
#     def test_autobind_success_razorpay_account_004(self):
#         # razorpay绑卡打款验证第3步直接返回绑卡成功：KV配置不校验姓名且返回的姓名和请求姓名不一致
#         update_kv_razorpay_verify_false(self.db_test_payment, "razorpay_yomoyo_verify")
#         update_kv_mockrazorpay(self.db_test_payment)
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()  # 名字前面不加mock，请求的名字会和返回的不一样
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # razorpay绑卡打款验证第3步直接返回绑卡成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_bind_success_razorpay_steps3(get_english_name())  # 名字前面不加mock
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq的参数断言，以及绑卡成功后检查binding_request和binding表
#         assert resp_autobind["content"]["code"] == 0, "绑卡验证成功"  # update_bind_success_razorpay_steps3由这一步mock决定
#         card_info = get_global_card_info_by_card_account(self.db_test_payment, self.bank_account_encrypt)
#         binding_request_info = get_global_binding_request_info_by_card_num(self.db_test_payment, card_info[0]["card_num"])
#         assert binding_request_info[0]["binding_request_channel_code"] == global_NAME_NOT_MATCH  # 只有在绑卡返回名字不一样才会记录为KN_ACCOUNT_NAME_NOT_MATCH
#         assert binding_request_info[0]["binding_request_channel_message"] == "the similarity is less than 0.8"
#         run_task_bindingQuery(self.db_test_payment, self.bank_account_encrypt)  # 手动执行task-bindingQuery
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autobind_result_success_query(self.merchant_key)
#         # 数据库断言
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.bank_account_encrypt,
#                                                                 resp_autobind,
#                                                                 self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_accountverify_check_cardandaccount_auth_mode(self.db_test_payment, self.bank_account_encrypt)
#         assert_verify_success(self.db_test_payment, self.bank_account_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_autobind
#     @pytest.mark.global_razorpay_autobind_success
#     def test_autobind_success_razorpay_account_005(self):
#         # razorpay绑卡打款验证第3步返回接口处理中，在第4步结果查询到绑卡成功：返回的姓名和请求姓名不一致
#         update_kv_razorpay_verify_false(self.db_test_payment, "razorpay_yomoyo_verify")
#         update_kv_mockrazorpay(self.db_test_payment)
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()  # 名字前面不加mock，请求的名字会和返回的不一样
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.bank_account_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         upi_encrypt = None
#         # razorpay绑卡打款验证第3步直接返回绑卡成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_bind_process_razorpay_steps3()
#         global_payment_mock.update_bind_success_razorpay_steps4(get_english_name())  # 名字前面不加mock
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt,
#                                         upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                         self.address_encrypt)
#         # 【断言】 绑卡验证成功返回给dsq的参数断言，以及绑卡成功后检查binding_request和binding表
#         assert resp_autobind["content"]["code"] == 2, "绑卡验证处理中"  # update_bind_process_razorpay_steps3由这一步mock决定
#         run_task_bindingQuery(self.db_test_payment, self.bank_account_encrypt)  # 手动执行task-bindingQuery
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autobind_result_success_query(self.merchant_key)
#         card_info = get_global_card_info_by_card_account(self.db_test_payment, self.bank_account_encrypt)
#         binding_request_info = get_global_binding_request_info_by_card_num(self.db_test_payment, card_info[0]["card_num"])
#         assert binding_request_info[0]["binding_request_channel_code"] == global_NAME_NOT_MATCH  # 只有在绑卡返回名字不一样才会记录为KN_ACCOUNT_NAME_NOT_MATCH
#         assert binding_request_info[0]["binding_request_channel_message"] == "the similarity is less than 0.8"
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.bank_account_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_accountverify_check_cardandaccount_auth_mode(self.db_test_payment, self.bank_account_encrypt)
#         assert_verify_success(self.db_test_payment, self.bank_account_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_ebank
#     def test_razorpay_ebank_process_001(self):
#         # 更新easymock代扣查询返回代扣处理中，不会调用支付明细接口
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_process()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank是网关支付，请求成功一定是返回code=2处理中且会返回支付链接
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 代扣处理中状态检查 + rbiz代扣结果查询
#         assert_withhold_process(self.db_test_payment, merchant_key)
#         # 断言，代扣表统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_ebank
#     def test_razorpay_ebank_process_002(self):
#         # 结果查询返回交易不存在，但是withhold_receipt_channel_inner_key又不为空，不会置为代扣失败，还是处理中
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_fail_not_exist()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank是网关支付，请求成功一定是返回code=2处理中且会返回支付链接
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 代扣处理中状态检查 + rbiz代扣结果查询
#         assert_withhold_process(self.db_test_payment, merchant_key)
#         # 断言，代扣表统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_ebank
#     def test_razorpay_ebank_fail_001(self):
#         # 用户一直未操作链接，直到过期关单，会调用支付明细接口但查询不到可以更新的数据
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_fail_001()
#         # global_payment_mock.update_razorpay_ebank_query_fail_detail_001()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank网关支付，请求成功一定是返回code=2处理中
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(2)
#         # 无法统一的断言，razorpay的mock返回的场景决定mode和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_code"], "KN_TIMEOUT_CLOSE_ORDER",
#                             '超时关单')
#         # 代扣失败状态检查 + rbiz代扣结果查询
#         assert_withhold_fail(self.db_test_payment, merchant_key,
#                              resp_withhold_autopay['content']['data']['channel_key'],
#                              resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.test_razorpay_ebank
#     def test_razorpay_ebank_fail_002(self):
#         # 用户操作过链接但是支付失败了，后超时关单（PS：razorpay代扣失败只有超时关单的场景），会调用支付明细接口更新失败原因
#         # option、mode为card
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_fail_002()
#         # global_payment_mock.update_razorpay_ebank_query_fail_detail_002()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank网关支付，请求成功一定是返回code=2处理中
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(2)
#         # 无法统一的断言，razorpay的mock返回的场景决定mode和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_code"], "KN_TIMEOUT_CLOSE_ORDER",
#                             '超时关单')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"], global_razorpay_ebank_fail_message, '超时关单失败原因')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_option"], global_razorpay_ebank_payment_option_card, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_mode"], global_razorpay_ebank_payment_mode_card, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_inner_key"], global_razorpay_ebank_channel_key, '通道流水号')
#         # 代扣失败状态检查 + rbiz代扣结果查询
#         assert_withhold_fail(self.db_test_payment, merchant_key,
#                              resp_withhold_autopay['content']['data']['channel_key'],
#                              resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.test_razorpay_ebank
#     def test_razorpay_ebank_fail_003(self):
#         # 用户操作过链接但是支付失败了，后超时关单（PS：razorpay代扣失败只有超时关单的场景），会调用支付明细接口更新失败原因
#         # option、mode为netbanking且用户支付过多次均失败，失败原因取最后一条
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_fail_003()
#         # global_payment_mock.update_razorpay_ebank_query_fail_detail_002()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank网关支付，请求成功一定是返回code=2处理中
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，razorpay的mock返回的场景决定mode和message
#         time.sleep(1)
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_code"], "KN_TIMEOUT_CLOSE_ORDER", '超时关单')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"], global_razorpay_ebank_fail_message, '超时关单失败原因')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_option"], global_razorpay_ebank_payment_option, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_mode"], global_razorpay_ebank_payment_mode, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_inner_key"], global_razorpay_ebank_channel_key, '通道流水号')
#         # 代扣失败状态检查 + rbiz代扣结果查询
#         assert_withhold_fail(self.db_test_payment, merchant_key,
#                              resp_withhold_autopay['content']['data']['channel_key'],
#                              resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_ebank
#     def test_razorpay_ebank_fail_not_exists(self):
#         # 代扣失败：交易不存在，不会调用支付明细接口
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_fail_not_exist()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank网关支付
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 更新inner_key为空，才会置为交易不存在
#         update_withhold_receipt_inner_key_null(self.db_test_payment, merchant_key)
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(2)
#         # 无法统一的断言，razorpay的mock返回的场景决定mode和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_code"], global_order_not_exists,
#                             '交易不存在')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_inner_key"], "",
#                             '通道流水号')  # razorpay交易不存在时不能有withhold_receipt_channel_inner_key
#         # 代扣失败状态检查 + rbiz代扣结果查询
#         assert_withhold_fail(self.db_test_payment, merchant_key,
#                              resp_withhold_autopay['content']['data']['channel_key'],
#                              resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_ebank
#     @pytest.mark.global_razorpay_ebank_success
#     def test_razorpay_ebank_success_001(self):
#         # 查询返回代扣成功，option、mode为card
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_success_002()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank是网关支付，请求成功一定是返回code=2处理中
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 无法统一的断言，mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "paid", '代扣成功'
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_message"] == global_razorpay_ebank_success_message, '超时关单失败原因'
#         assert withhold_receipt_info[0]["withhold_receipt_payment_option"] == global_razorpay_ebank_payment_option_card, '支付方式'
#         assert withhold_receipt_info[0]["withhold_receipt_payment_mode"] ==  global_razorpay_ebank_payment_mode_card, '支付方式'
#         assert withhold_receipt_info[0]["withhold_receipt_channel_inner_key"] ==  global_razorpay_ebank_channel_key, '通道流水号'
#         assert withhold_receipt_info[0]["withhold_receipt_service_charge"] ==  global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号'
#         assert withhold_receipt_info[0]["withhold_receipt_service_tax"] ==  global_razorpay_ebank_service_tax, '通道流水号'
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key,
#                                 resp_withhold_autopay['content']['data']['channel_key'],
#                                 resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_ebank
#     @pytest.mark.global_razorpay_ebank_success
#     def test_razorpay_ebank_success_002(self):
#         # 查询返回代扣成功，option、mode为netbanking
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_success_new()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank是网关支付，请求成功一定是返回code=2处理中
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 无法统一的断言，mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "paid", '代扣成功'
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"], global_razorpay_ebank_success_message, '超时关单失败原因')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_option"],
#                             global_razorpay_ebank_payment_option, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_mode"],
#                             global_razorpay_ebank_payment_mode, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_inner_key"],
#                             global_razorpay_ebank_channel_key, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_charge"], global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax, '通道流水号')
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key,
#                                 resp_withhold_autopay['content']['data']['channel_key'],
#                                 resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_ebank
#     @pytest.mark.global_razorpay_ebank_success
#     def test_razorpay_ebank_success_003(self):
#         # 查询返回代扣成功，option、mode为card
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_success_003()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank是网关支付，请求成功一定是返回code=2处理中
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 无法统一的断言，mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "paid", '代扣成功'
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_message"] == global_razorpay_ebank_success_message, '超时关单失败原因'
#         assert withhold_receipt_info[0]["withhold_receipt_payment_option"] == global_razorpay_collect_channel_option_upi, '支付方式'
#         assert withhold_receipt_info[0]["withhold_receipt_payment_mode"] == '', '支付方式'
#         assert withhold_receipt_info[0]["withhold_receipt_channel_inner_key"] == global_razorpay_ebank_channel_key, '通道流水号'
#         assert withhold_receipt_info[0]["withhold_receipt_service_charge"] == global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号'
#         assert withhold_receipt_info[0]["withhold_receipt_service_tax"] == global_razorpay_ebank_service_tax, '通道流水号'
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key,
#                                 resp_withhold_autopay['content']['data']['channel_key'],
#                                 resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#
#     # 以下为razorpay代付余额查询与代付
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_balance
#     def test_razorpay_balance_fail(self):
#         # 更新easymock余额查询为失败,cashfree和razorpay均查询失败
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_cashfree_withdraw_balance_fail()
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_withdraw_balance_fail()
#         # 发起余额查询请求
#         resp_withdraw_balance = global_Withdraw_balance(global_sign_company_yomoyo)
#         # 断言
#         assert resp_withdraw_balance['content']['code'] == 1, "代付余额查询失败"
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_balance
#     def test_razorpay_withdraw_balance_success(self):
#         # cashfree查询失败，只有razorpay查询成功
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_cashfree_withdraw_balance_fail()
#         # 更新easymock余额查询为成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         # 发起余额查询请求
#         resp_withdraw_balance = global_Withdraw_balance(global_sign_company_yomoyo)
#         # 断言
#         assert resp_withdraw_balance['content']['code'] == 0, "余额查询成功"
#         # 通道返回的availableBalance作为data.available返回,razorpay只返回可用余额available
#         assert resp_withdraw_balance['content']['data']['total'] == global_razorpay_withdraw_balance, "可用余额和通道返回一致"
#         assert resp_withdraw_balance['content']['data']['available'] == global_razorpay_withdraw_balance, "可用余额和通道返回一致"
#         assert resp_withdraw_balance['content']['data']['data'][0][
#                    'total'] == global_razorpay_withdraw_balance, "可用余额和通道返回一致"
#         assert resp_withdraw_balance['content']['data']['data'][0][
#                    'available'] == global_razorpay_withdraw_balance, "可用余额和通道返回一致"
#         assert resp_withdraw_balance['content']['data']['data'][0][
#                    'channel_name'] == "razorpay_yomoyo_withdraw", "可用余额和通道返回一致"
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_balance
#     def test_razorpayandcashfree_withdraw_balance_success(self):
#         undo_update_global_channel_withdraw_only_razorpay(self.db_test_payment)
#         # cashfree和razorpay余额都查询成功
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_cashfree_withdraw_balance_success()
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         # 发起余额查询请求
#         resp_withdraw_balance = global_Withdraw_balance(global_sign_company_yomoyo)
#         # 断言
#         assert resp_withdraw_balance['content']['code'] == 0, "余额查询成功"
#         # 主体下多个通道余额：现在写死的测试环境cashfree_yomoyo_withdraw在razorpay_yomoyo_withdraw前面返回
#         assert resp_withdraw_balance['content']['data']['total'] ==  int(global_cashfree_total_amount_lubi * 100) + int(global_razorpay_withdraw_balance), "可用余额和通道返回一致"
#         assert resp_withdraw_balance['content']['data']['available'] == int(global_cashfree_available_amount_lubi * 100) + int(global_razorpay_withdraw_balance), "可用余额和通道返回一致"
#         assert resp_withdraw_balance['content']['data']['data'][0]['total'] == int(global_cashfree_total_amount_lubi * 100), "可用余额和通道返回一致"
#         assert resp_withdraw_balance['content']['data']['data'][0]['available'] == int(global_cashfree_available_amount_lubi * 100), "可用余额和通道返回一致"
#         assert resp_withdraw_balance['content']['data']['data'][0][
#                    'channel_name'] == "cashfree_yomoyo1_withdraw", "可用余额和通道返回一致"  # 这个会因为测试环境修改而跑不通
#         assert resp_withdraw_balance['content']['data']['data'][1][
#                    'total'] == global_razorpay_withdraw_balance, "可用余额和通道返回一致"
#         assert resp_withdraw_balance['content']['data']['data'][1][
#                    'available'] == global_razorpay_withdraw_balance, "可用余额和通道返回一致"
#         assert resp_withdraw_balance['content']['data']['data'][1][
#                    'channel_name'] == "razorpay_yomoyo_withdraw", "可用余额和通道返回一致"  # 这个会因为测试环境修改而跑不通
#         # 还原：后面流程要用
#         update_global_channel_withdraw_only_razorpay(self.db_test_payment)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     def test_razorpay_withdraw_balance_queryfail(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         # 1.查询余额失败，直接放款失败
#         global_payment_mock.update_razorpay_withdraw_balance_fail()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 1, "代付直接失败"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，因为message依赖于mock的返回
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == '', '代付方式'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"] == '', '通道代付id'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_code"] == "KN_INVALID_CHANNEL", '代付code'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_message"] == '', '代付msg'
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_withdraw_fail(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     def test_razorpay_withdraw_openaccount_fail_step1(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         # 1.开户失败：创建联系人失败，直接放款失败
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_bind_fail_razorpay_steps1()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 更新binding为未开户，直接删除绑卡信息
#         delete_binding(self.db_test_payment, card_num)
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 1, "代付直接失败"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，因为message依赖于mock的返回
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == '', '代付方式'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"] == '', '通道代付id'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_code"] == global_order_binding_fail, '代付code'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_message"] == '', '代付msg'
#         # 代付多了一步开户绑卡
#         binding_info = get_global_binding_info_by_card_num(self.db_test_payment, card_num)
#         assert binding_info[0]["binding_status"] == 2, "开户失败"
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_withdraw_fail(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     def test_razorpay_withdraw_openaccount_fail_step2(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         # 1.开户失败：创建联系人成功+创建资金账号失败，直接放款失败
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_fail_razorpay_steps2()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 更新binding为未开户，直接删除绑卡信息
#         delete_binding(self.db_test_payment, card_num)
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 1, "代付直接失败"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，因为message依赖于mock的返回
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == '', '代付方式'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"] == '', '通道代付id'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_code"] == global_order_binding_fail, '代付code'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_message"] == '', '代付msg'
#         # 代付多了一步开户绑卡
#         binding_info = get_global_binding_info_by_card_num(self.db_test_payment, card_num)
#         assert binding_info[0]["binding_status"] == 2, "开户失败"
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_withdraw_fail(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     def test_razorpay_withdraw_query_process_001(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         # 1.开户成功：创建联系人成功+创建资金账户成功，2.放款结果查询更新为处理中
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_razorpay_withdraw_success()
#         global_payment_mock.update_razorpay_withdraw_query_process_001()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 2, "代付交易处理中"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，因为message依赖于mock的返回
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_inner_key"] == global_razorpay_withdraw_inner_key, '通道代付id'
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_check_razorpay_withdraw_channelrequestlog(self.db_test_payment, params_withdraw_receipt_trade_no)
#         assert_withdraw_process(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     def test_razorpay_withdraw_query_process_002(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         # 1.开户成功：创建联系人成功+创建资金账户成功，2.放款结果查询更新为处理中
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_razorpay_withdraw_success()
#         global_payment_mock.update_razorpay_withdraw_query_process_002()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 2, "代付交易处理中"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，因为message依赖于mock的返回
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_inner_key"] == global_razorpay_withdraw_inner_key, '通道代付id'
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_check_razorpay_withdraw_channelrequestlog(self.db_test_payment, params_withdraw_receipt_trade_no)
#         assert_withdraw_process(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     def test_razorpay_withdraw_query_process_003(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         # 1.开户成功：创建联系人成功+创建资金账户成功，2.放款结果查询更新为处理中
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_razorpay_withdraw_success()
#         global_payment_mock.update_razorpay_withdraw_query_process_003()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 2, "代付交易处理中"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，因为message依赖于mock的返回
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_inner_key"] == global_razorpay_withdraw_inner_key, '通道代付id'
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_check_razorpay_withdraw_channelrequestlog(self.db_test_payment, params_withdraw_receipt_trade_no)
#         assert_withdraw_process(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     def test_razorpay_withdraw_query_fail_001(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         # 1.开户成功：创建联系人成功+创建资金账户成功，2.放款结果查询更新为处理中
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_razorpay_withdraw_success()
#         global_payment_mock.update_razorpay_withdraw_query_fail_001()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 2, "代付交易处理中"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，因为message依赖于mock的返回
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == global_razorpay_withdraw_mode, '代付方式'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_inner_key"] == global_razorpay_withdraw_inner_key, '通道代付id'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_resp_code"] == global_razorpay_withdraw_fail_rejected, '代付code'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_resp_message"] == global_withdraw_failed_message, '代付msg'
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_check_razorpay_withdraw_channelrequestlog(self.db_test_payment, params_withdraw_receipt_trade_no)
#         assert_withdraw_fail(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     def test_razorpay_withdraw_query_fail_002(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         # 1.开户成功：创建联系人成功+创建资金账户成功，2.放款结果查询更新为处理中
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_razorpay_withdraw_success()
#         global_payment_mock.update_razorpay_withdraw_query_fail_002()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 2, "代付交易处理中"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，因为message依赖于mock的返回
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == global_razorpay_withdraw_mode, '代付方式'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_inner_key"] == global_razorpay_withdraw_inner_key, '通道代付id'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_resp_code"] == global_razorpay_withdraw_fail_cancelled, '代付code'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_resp_message"] == global_withdraw_failed_message, '代付msg'
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_check_razorpay_withdraw_channelrequestlog(self.db_test_payment, params_withdraw_receipt_trade_no)
#         assert_withdraw_fail(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     def test_razorpay_withdraw_query_fail_003(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         # 1.开户成功：创建联系人成功+创建资金账户成功，2.放款结果查询更新为处理中
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_razorpay_withdraw_success()
#         global_payment_mock.update_razorpay_withdraw_query_fail_003()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 2, "代付交易处理中"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，因为message依赖于mock的返回
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == global_razorpay_withdraw_mode, '代付方式'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_inner_key"] == global_razorpay_withdraw_inner_key, '通道代付id'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_resp_code"] == global_razorpay_withdraw_fail_reversed, '代付code'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_resp_message"] == global_withdraw_failed_message, '代付msg'
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_check_razorpay_withdraw_channelrequestlog(self.db_test_payment, params_withdraw_receipt_trade_no)
#         assert_withdraw_fail(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     def test_razorpay_withdraw_query_fail_not_exists(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         # 1.开户成功：创建联系人成功+创建资金账户成功，2.放款请求返回异常没有id  3.放款结果查询更新为交易不存在
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_razorpay_withdraw_error()
#         global_payment_mock.update_razorpay_withdraw_query_not_exists()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 2, "代付交易处理中"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，因为message依赖于mock的返回
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == '', '代付方式'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"] == '', '通道代付id'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_code"] == global_order_not_exists, '代付code'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_resp_message"] == global_withdraw_failed_message, '代付msg'
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_check_razorpay_withdraw_channelrequestlog(self.db_test_payment, params_withdraw_receipt_trade_no)
#         assert_withdraw_fail(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     @pytest.mark.global_razorpay_withdraw_success
#     def test_razorpay_withdraw_query_success_001(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         # 1.之前有已开户成功的数据 2.放款结果查询更新为成功   这里需要改查询uuid的
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_razorpay_withdraw_success()
#         global_payment_mock.update_razorpay_withdraw_query_success()
#         usable_card_uuid = get_usable_razorpay_withdraw_carduuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 2, "代付交易处理中"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == global_razorpay_withdraw_mode, '代付方式'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_inner_key"] == global_razorpay_withdraw_inner_key, '通道代付id'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_resp_code"] == global_razorpay_withdraw_success_processed, '代付code'
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_check_razorpay_withdraw_channelrequestlog(self.db_test_payment, params_withdraw_receipt_trade_no)
#         assert_withdraw_success(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     @pytest.mark.global_razorpay_withdraw_success
#     def test_razorpay_withdraw_query_success_002(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         # 1.开户成功：创建联系人成功+创建资金账户成功，2.放款结果查询更新为成功
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_bind_success_razorpay_steps1()
#         global_payment_mock.update_bind_success_razorpay_steps2()
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         global_payment_mock.update_razorpay_withdraw_success()
#         global_payment_mock.update_razorpay_withdraw_query_success()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 更新binding为未开户，直接删除绑卡信息
#         delete_binding(self.db_test_payment, card_num)
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 2, "代付交易处理中"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == global_razorpay_withdraw_mode, '代付方式'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_inner_key"] == global_razorpay_withdraw_inner_key, '通道代付id'
#         assert withdraw_receipt_info[0][
#                    "withdraw_receipt_channel_resp_code"] == global_razorpay_withdraw_success_processed, '代付code'
#         # 代付多了一步开户绑卡
#         binding_info = get_global_binding_info_by_card_num(self.db_test_payment, card_num)
#         binding_protocol_info = json.loads(binding_info[0]["binding_protocol_info"])
#         assert binding_info[0]["binding_status"] == 1, "开户成功"
#         assert binding_protocol_info["contact_id"] == global_razorpay_withdraw_contact_id, "联系人开户信息保存"
#         assert binding_protocol_info["fund_account_id"] == global_razorpay_withdraw_fund_account_id, "资金账户开户信息保存"
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_check_razorpay_withdraw_channelrequestlog(self.db_test_payment, params_withdraw_receipt_trade_no)
#         assert_withdraw_success(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay
#     @pytest.mark.global_razorpay_withdraw
#     def test_razorpay_withdraw_fail_risk(self):
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_withdraw_balance_success()
#         # 更新KV为12h只能放款成功0笔
#         update_kv_withdraw_riskwhite(self.db_test_payment)
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         card_account = card_info[0]["card_account"]
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         merchant_key = get_timestamp()
#         # 发起代付请求
#         resp_autowithdraw = withdraw_autoWithdraw(card_uuid, merchant_key)
#         # 海外项目放款请求成功表示放款中，返回给gbiz的code=2处理中
#         assert resp_autowithdraw['content']['code'] == 1, "代付直接失败"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，因为message依赖于mock的返回
#         params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#             "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(self.db_test_payment,
#                                                                              params_withdraw_receipt_trade_no)
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == '', '代付方式'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"] == '', '通道代付id'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_code"] == "KN_RISK_CONTROL", '代付code'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_message"] == '', '代付msg'
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_autowithdraw, merchant_key, card_uuid,
#                                               card_info[0]["card_bank_code"], card_num, card_account, three_element)
#         assert_withdraw_fail(self.db_test_payment, params_withdraw_receipt_trade_no, merchant_key, three_element)
#         # 还原
#         undo_update_kv_withdraw_riskwhite(self.db_test_payment)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay_ebank
#     def test_razorpay_ebank_authorized_capture_success_001(self):
#         # 1.第一次查询支付结果通道返回状态为authorized且未超时，2.调用订单捕获capture接口成功，3.再次查询通道返回支付成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_authorized()
#         global_payment_mock.update_razorpay_ebank_capture_success()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank是网关支付，请求成功一定是返回code=2处理中
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 订单捕获后订单状态应为处理中
#         assert_withhold_process(self.db_test_payment, merchant_key)
#         # mock返回支付成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_query_success_new()
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 无法统一的断言，mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "paid", '代扣成功'
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"], global_razorpay_ebank_success_message, '超时关单失败原因')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_option"],
#                             global_razorpay_ebank_payment_option, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_mode"],
#                             global_razorpay_ebank_payment_mode, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_inner_key"],
#                             global_razorpay_ebank_channel_key, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_charge"], global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax, '通道流水号')
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key,
#                                 resp_withhold_autopay['content']['data']['channel_key'],
#                                 resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay_ebank
#     def test_razorpay_ebank_authorized_capture_success_002(self):
#         # 1.第一次查询支付结果通道返回状态为authorized且已超时，2.调用订单捕获capture接口成功，3.再次查询通道返回支付成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_authorized_timeout()
#         global_payment_mock.update_razorpay_ebank_capture_success()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank是网关支付，请求成功一定是返回code=2处理中
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 订单捕获后订单状态应为处理中
#         assert_withhold_process(self.db_test_payment, merchant_key)
#         # mock返回支付成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_query_success_new()
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 无法统一的断言，mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "paid", '代扣成功'
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"], global_razorpay_ebank_success_message, '超时关单失败原因')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_option"],
#                             global_razorpay_ebank_payment_option, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_mode"],
#                             global_razorpay_ebank_payment_mode, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_inner_key"],
#                             global_razorpay_ebank_channel_key, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_charge"], global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax, '通道流水号')
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key,
#                                 resp_withhold_autopay['content']['data']['channel_key'],
#                                 resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay_ebank
#     def test_razorpay_ebank_authorized_capture_success_003(self):
#         # 1.第一次查询支付结果通道返回状态为authorized且未超时，2.调用订单捕获capture接口异常，3.再次查询通道返回支付成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_authorized()
#         global_payment_mock.update_razorpay_ebank_capture_fail()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank是网关支付，请求成功一定是返回code=2处理中
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 订单捕获后订单状态应为处理中
#         assert_withhold_process(self.db_test_payment, merchant_key)
#         # mock返回支付成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_query_success_new()
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 无法统一的断言，mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "paid", '代扣成功'
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"],
#                             global_razorpay_ebank_success_message, '超时关单失败原因')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_option"],
#                             global_razorpay_ebank_payment_option, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_mode"],
#                             global_razorpay_ebank_payment_mode, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_inner_key"],
#                             global_razorpay_ebank_channel_key, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_charge"],
#                             global_razorpay_ebank_service_fee - global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax,
#                             '通道流水号')
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key,
#                                 resp_withhold_autopay['content']['data']['channel_key'],
#                                 resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay_ebank
#     def test_razorpay_ebank_authorized_capture_success_004(self):
#         # 1.第一次查询支付结果返回authorized状态的有两个，会发企业微信提醒：订单[RBIZ409094510985179750]有多个已认证支付，可能会重复扣款，请核查
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_success()
#         global_payment_mock.update_razorpay_ebank_query_two_authorized()
#         global_payment_mock.update_razorpay_ebank_capture_success()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, card_uuid, india_bind_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, global_sign_company_yomoyo, card_uuid,
#                                                         user_operator, payment_type_ebank)
#         # ebank是网关支付，请求成功一定是返回code=2处理中
#         assert_check_autopay_resp_data(resp_withhold_autopay, "ebank")
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 订单捕获后订单状态应为处理中
#         assert_withhold_process(self.db_test_payment, merchant_key)
#         # mock返回支付成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_ebank_query_success_new()
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         time.sleep(1)
#         # 无法统一的断言，mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withhold_receipt_info[0]["withhold_receipt_channel_resp_code"] == "paid", '代扣成功'
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"],
#                             global_razorpay_ebank_success_message, '超时关单失败原因')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_option"],
#                             global_razorpay_ebank_payment_option, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_mode"],
#                             global_razorpay_ebank_payment_mode, '支付方式')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_inner_key"],
#                             global_razorpay_ebank_channel_key, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_charge"],
#                             global_razorpay_ebank_service_fee - global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax,
#                             '通道流水号')
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key,
#                                 resp_withhold_autopay['content']['data']['channel_key'],
#                                 resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，razorpay代扣统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_razorpay_channelrequestlog(self.db_test_payment, merchant_key)
