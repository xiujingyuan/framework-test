# # -*- coding: utf-8 -*-
#
# import pytest
#
# from biztest.config.payment.url_config import global_sign_company_yomoyo, system_operator, global_cashfree_subscribe_url, \
#     global_autoSubscribe_withhold_successcode, global_autoSubscribe_withhold_message, \
#     global_autoSubscribe_withhold_failcode, global_amount
# from biztest.function.global_payment.global_payment_db_assert import assert_verify_check_card_account_binding_bindingrequest, \
#     assert_verify_fail, autobind_result_success_query, assert_verify_success, \
#     assert_cardSubscribe_check_cardandaccount_auth_mode, autoSubscribe_result_fail_query, \
#     autoSubscribe_result_success_query, assert_verify_process, autoSubscribe_result_process_query, \
#     run_task_bindingQuery, assert_withhold_success, assert_check_withhold_withholdreceipt, \
#     run_task_withholdReceipt_withholdcharge_and_chargequery, assert_check_cashfree_subscribe_channelrequestlog, \
#     assert_withhold_fail, assert_withhold_process, assert_accountverify_check_cardandaccount_auth_mode
# from biztest.function.global_payment.global_payment_db_operation import \
#     update_global_channel_verify_only_cashfree, \
#     undo_update_global_channel_verify_only_cashfree, get_usable_card_uuid, \
#     update_kv_mockcashfree, \
#     undo_update_kv_mockcashfree, get_usable_subscribe_carduuid, by_card_carduuid_get_account, \
#     get_withhold_receipt_by_merchant_key
# from biztest.function.payment.common import get_english_name, get_mobile, get_bank_account
# from biztest.interface.payment.payment_interface import global_encrypt, get_timestamp, global_withhold_autoSubscribe, \
#     global_withhold_autopay, global_autobind
# from biztest.util.asserts.assert_util import Assert
# from biztest.util.db.db_util import DataBase
# from biztest.util.easymock.global_payment.global_payment_cashfree import CashfreeMock
#
#
# # global_payment下cashfree通道： 1、订阅路由card+自动代扣
# class TestIndiaCashfreeSubscribe:
#     """
#     global cashfree subscribe
#     author: fangchangfang
#     date: 2020
#     """
#
#     @classmethod
#     def setup_class(self):
#         self.env_test = pytest.config.getoption("--env") if hasattr(pytest, "config") else 1
#         self.db_test_payment = DataBase("global_payment_test%s" % self.env_test)
#         # 修改KV中绑卡&代付&代扣地址改为easymock
#         update_kv_mockcashfree(self.db_test_payment)
#         # 初始化一些基础信息
#         self.ifsc = "mock_test_0001"
#         self.email_encrypt = "enc_05_2752999188760895488_191"  # 随意邮箱
#         self.address_encrypt = "enc_06_2752832664892874752_745"  # 随意邮箱
#         self.sign_company_yomoyo = global_sign_company_yomoyo
#         self.system_operator = system_operator
#         self.system_payment_type = "subscribe"  # ebank、sdk、subscribe，订阅可以更新为 subscribe
#
#     def teardown_class(self):
#         # 还原环境
#         undo_update_kv_mockcashfree(self.db_test_payment)
#         undo_update_global_channel_verify_only_cashfree(self.db_test_payment)
#         DataBase.close_connects()
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_autobind_success_cashfree_account(self):
#         # 单独先调用bank_account绑卡，更新一个最新的card_uuid
#         update_global_channel_verify_only_cashfree(self.db_test_payment)
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
#         # 更新easymock为绑卡成功
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_bind_success_cashfree("mock" + " " + get_english_name())  # 名字前面加上mock是因为对名字有检验，必须有一部分一样
#         upi_encrypt = None
#         # 发起绑卡
#         resp_autobind = global_autobind(self.merchant_key, global_sign_company_yomoyo, self.bank_account_encrypt, upi_encrypt,
#                                         self.ifsc, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt, self.address_encrypt)
#         # cashfree是同步绑卡，会立即返回绑卡结果给dsq，不能作为统一断言
#         assert resp_autobind["content"]["code"] == 0, "绑卡验证成功"
#         # dsq绑卡结果查询接口
#         autobind_result_success_query(self.merchant_key)
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.bank_account_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_accountverify_check_cardandaccount_auth_mode(self.db_test_payment, self.bank_account_encrypt)
#         assert_verify_success(self.db_test_payment, self.bank_account_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_card_fail_001(self):
#         # cashfree订阅是异步的：1、创建订阅直接失败了
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_fail_cashfree()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.card_num_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         # 发起绑卡
#         resp_autobind = global_withhold_autoSubscribe(self.merchant_key, card_uuid, self.card_num_encrypt,
#                                                       self.user_name_encrypt, self.mobile_encrypt,
#                                                       self.email_encrypt, self.address_encrypt, self.ifsc)
#         # cashfree订阅是异步的，需要用户介入
#         assert resp_autobind["content"]["code"] == 1, "订阅失败"
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autoSubscribe_result_fail_query(self.merchant_key)
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.card_num_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_cardSubscribe_check_cardandaccount_auth_mode(self.db_test_payment, self.card_num_encrypt)
#         assert_verify_fail(self.db_test_payment, self.card_num_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_card_fail_002(self):
#         # 订阅失败：查询到订阅失败
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_success_cashfree()
#         global_payment_mock.update_autoSubscribe_resultquery_fail_cashfree_001()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.card_num_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         # 发起绑卡
#         resp_autobind = global_withhold_autoSubscribe(self.merchant_key, card_uuid, self.card_num_encrypt,
#                                                       self.user_name_encrypt, self.mobile_encrypt,
#                                                       self.email_encrypt, self.address_encrypt, self.ifsc)
#         run_task_bindingQuery(self.db_test_payment, self.card_num_encrypt)  # 执行task-bindingQuery
#         # cashfree订阅是异步的，需要用户介入
#         assert resp_autobind["content"]["code"] == 2, "订阅中"
#         assert resp_autobind["content"]["data"]["redirect_url"] == global_cashfree_subscribe_url, "订阅链接"
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autoSubscribe_result_fail_query(self.merchant_key)
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.card_num_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_cardSubscribe_check_cardandaccount_auth_mode(self.db_test_payment, self.card_num_encrypt)
#         assert_verify_fail(self.db_test_payment, self.card_num_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_card_fail_003(self):
#         # 订阅失败：查询到订阅失败
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_success_cashfree()
#         global_payment_mock.update_autoSubscribe_resultquery_fail_cashfree_002()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.card_num_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         # 发起绑卡
#         resp_autobind = global_withhold_autoSubscribe(self.merchant_key, card_uuid, self.card_num_encrypt,
#                                                       self.user_name_encrypt, self.mobile_encrypt,
#                                                       self.email_encrypt, self.address_encrypt, self.ifsc)
#         run_task_bindingQuery(self.db_test_payment, self.card_num_encrypt)  # 执行task-bindingQuery
#         # cashfree订阅是异步的，需要用户介入
#         assert resp_autobind["content"]["code"] == 2, "订阅中"
#         assert resp_autobind["content"]["data"]["redirect_url"] == global_cashfree_subscribe_url, "订阅链接"
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autoSubscribe_result_fail_query(self.merchant_key)
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.card_num_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_cardSubscribe_check_cardandaccount_auth_mode(self.db_test_payment, self.card_num_encrypt)
#         assert_verify_fail(self.db_test_payment, self.card_num_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_card_fail_004(self):
#         # 订阅失败：执行task查询返回订阅中，调用订阅结果查询/withhold/subscribeResult返回订阅失败
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_success_cashfree()
#         global_payment_mock.update_autoSubscribe_resultquery_process_cashfree()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.card_num_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         # 发起绑卡
#         resp_autobind = global_withhold_autoSubscribe(self.merchant_key, card_uuid, self.card_num_encrypt,
#                                                       self.user_name_encrypt, self.mobile_encrypt,
#                                                       self.email_encrypt, self.address_encrypt, self.ifsc)
#         run_task_bindingQuery(self.db_test_payment, self.card_num_encrypt)  # 执行task-bindingQuery
#         # cashfree订阅是异步的，需要用户介入
#         assert resp_autobind["content"]["code"] == 2, "订阅中"
#         assert resp_autobind["content"]["data"]["redirect_url"] == global_cashfree_subscribe_url, "订阅链接"
#         # 更新为订阅失败
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_resultquery_fail_cashfree_001()
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autoSubscribe_result_fail_query(self.merchant_key)
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.card_num_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_cardSubscribe_check_cardandaccount_auth_mode(self.db_test_payment, self.card_num_encrypt)
#         assert_verify_fail(self.db_test_payment, self.card_num_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_card_process(self):
#         # 订阅中
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_success_cashfree()
#         global_payment_mock.update_autoSubscribe_resultquery_process_cashfree()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.card_num_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         # 发起绑卡
#         resp_autobind = global_withhold_autoSubscribe(self.merchant_key, card_uuid, self.card_num_encrypt,
#                                                       self.user_name_encrypt, self.mobile_encrypt,
#                                                       self.email_encrypt, self.address_encrypt, self.ifsc)
#         run_task_bindingQuery(self.db_test_payment, self.card_num_encrypt)  # 执行task-bindingQuery
#         # cashfree订阅是异步的，需要用户介入
#         assert resp_autobind["content"]["code"] == 2, "订阅中"
#         assert resp_autobind["content"]["data"]["redirect_url"] == global_cashfree_subscribe_url, "订阅链接"
#         run_task_bindingQuery(self.db_test_payment, self.card_num_encrypt)  # 执行task-bindingQuery
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autoSubscribe_result_process_query(self.merchant_key)
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.card_num_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_cardSubscribe_check_cardandaccount_auth_mode(self.db_test_payment, self.card_num_encrypt)
#         assert_verify_process(self.db_test_payment, self.card_num_encrypt)
#
#     # def test_cashfree_autoSubscribe_card_cancel(self):
#     #     # 用户一直未操作链接，超时后调用取消接口，取消订阅，即订阅失败，mock有bug暂不能跑
#     #     global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#     #     global_payment_mock.update_autoSubscribe_success_cashfree()
#     #     global_payment_mock.update_autoSubscribe_resultquery_expire_cashfree()
#     #     # 取消接口这里mock不到，请教下宝哥为什么？？？
#     #     global_payment_mock.update_autoSubscribe_cancel_sucess_cashfree()
#     #     # 三要素数据进行海外加密处理，海外不需要传身份证
#     #      params_no_encrypt = {
#     #         "plain1": get_mobile(),
#     #         "plain2": get_bank_account(),
#     #         "plain3": get_english_name()
#     #     }
#     #     resp_encrypt = global_encrypt(**params_no_encrypt)
#     #     self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#     #     self.card_num_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#     #     self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#     #     self.merchant_key = get_timestamp()
#     #     usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#     #     card_uuid = usable_card_uuid[0]['account_card_uuid']
#     #     # 发起绑卡
#     #     resp_autobind = global_withhold_autoSubscribe(self.merchant_key, card_uuid, self.card_num_encrypt,
#     #                                                   self.user_name_encrypt, self.mobile_encrypt,
#     #                                                   self.email_encrypt, self.address_encrypt, self.ifsc)
#     #     # cashfree订阅是异步的，需要用户介入
#     #     assert resp_autobind["content"]["code"] == 2, "订阅中"
#     #     run_task_bindingQuery(self.db_test_payment, self.card_num_encrypt) # 执行task-bindingQuery
#     #     # 数据库断言，字段统一检查
#     #     assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.card_num_encrypt,
#     #                                                             resp_autobind, self.user_name_encrypt,
#     #                                                             self.mobile_encrypt, self.ifsc, self.email_encrypt,
#     #                                                             self.address_encrypt)
#     #     assert_cardSubscribe_check_cardandaccount_auth_mode(self.db_test_payment, self.card_num_encrypt)
#     #     assert_verify_fail(self.db_test_payment, self.card_num_encrypt)
#     #     # dsq订阅结果查询接口
#     #     autoSubscribe_result_fail_query(self.merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_card_success_001(self):
#         # 查询到订阅绑卡成功
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_success_cashfree()
#         global_payment_mock.update_autoSubscribe_resultquery_success_cashfree()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.card_num_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         # 发起绑卡
#         resp_autobind = global_withhold_autoSubscribe(self.merchant_key, card_uuid, self.card_num_encrypt,
#                                                       self.user_name_encrypt, self.mobile_encrypt,
#                                                       self.email_encrypt, self.address_encrypt, self.ifsc)
#         # cashfree订阅是异步的，需要用户介入
#         assert resp_autobind["content"]["code"] == 2, "订阅中"
#         assert resp_autobind["content"]["data"]["redirect_url"] == global_cashfree_subscribe_url, "订阅链接"
#         run_task_bindingQuery(self.db_test_payment, self.card_num_encrypt)  # 执行task-bindingQuery
#
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autoSubscribe_result_success_query(self.merchant_key)
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.card_num_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_cardSubscribe_check_cardandaccount_auth_mode(self.db_test_payment, self.card_num_encrypt)
#         assert_verify_success(self.db_test_payment, self.card_num_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_card_success_002(self):
#         # 订阅成功：执行task查询返回订阅中，调用订阅结果查询/withhold/subscribeResult返回订阅成功
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_success_cashfree()
#         global_payment_mock.update_autoSubscribe_resultquery_process_cashfree()
#         # 三要素数据进行海外加密处理，海外不需要传身份证
#         params_no_encrypt = {
#             "plain1": get_mobile(),
#             "plain2": get_bank_account(),
#             "plain3": get_english_name()
#         }
#         resp_encrypt = global_encrypt(**params_no_encrypt)
#         self.mobile_encrypt = resp_encrypt["content"]["data"][0]["hash"]
#         self.card_num_encrypt = resp_encrypt["content"]["data"][1]["hash"]
#         self.user_name_encrypt = resp_encrypt["content"]["data"][2]["hash"]
#         self.merchant_key = get_timestamp()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         # 发起绑卡
#         resp_autobind = global_withhold_autoSubscribe(self.merchant_key, card_uuid, self.card_num_encrypt,
#                                                       self.user_name_encrypt, self.mobile_encrypt,
#                                                       self.email_encrypt, self.address_encrypt, self.ifsc)
#         # cashfree订阅是异步的，需要用户介入
#         assert resp_autobind["content"]["code"] == 2, "订阅中"
#         assert resp_autobind["content"]["data"]["redirect_url"] == global_cashfree_subscribe_url, "订阅链接"
#         run_task_bindingQuery(self.db_test_payment, self.card_num_encrypt)  # 执行task-bindingQuery
#         # 更新为订阅成功
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_resultquery_success_cashfree()
#         # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
#         autoSubscribe_result_success_query(self.merchant_key)
#         # 数据库断言，字段统一检查
#         assert_verify_check_card_account_binding_bindingrequest(self.db_test_payment, self.card_num_encrypt,
#                                                                 resp_autobind, self.user_name_encrypt,
#                                                                 self.mobile_encrypt, self.ifsc, self.email_encrypt,
#                                                                 self.address_encrypt)
#         assert_cardSubscribe_check_cardandaccount_auth_mode(self.db_test_payment, self.card_num_encrypt)
#         assert_verify_success(self.db_test_payment, self.card_num_encrypt)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_withhold_fail(self):
#         # 自动代扣-订阅代test_cashfree_autoSubscribe_card_fail_002扣直接失败
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_withhold_fail_cashfree()
#         usable_card_uuid = get_usable_subscribe_carduuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_card_carduuid_get_account(self.db_test_payment, card_uuid)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起自动代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, self.sign_company_yomoyo, card_uuid, self.system_operator, self.system_payment_type)
#         # 自动代扣异步处理的，请求成功一定是返回code=2处理中
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，cashfree的mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_code"], global_autoSubscribe_withhold_failcode, '代扣失败')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"], global_autoSubscribe_withhold_message, '代扣失败')
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_fail(self.db_test_payment, merchant_key, withhold_receipt_info[0]["withhold_receipt_channel_key"],
#                                resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，代扣相关表统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key, card_num, resp_withhold_autopay)
#         assert_check_cashfree_subscribe_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_withhold_queryfail_001(self):
#         # 自动代扣-订阅代扣请求异常，后查询到代扣失败
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_withhold_error_cashfree()
#         global_payment_mock.update_autoSubscribe_withhold_query_fail_cashfree()
#         usable_card_uuid = get_usable_subscribe_carduuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_card_carduuid_get_account(self.db_test_payment, card_uuid)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起自动代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, self.sign_company_yomoyo, card_uuid, self.system_operator, self.system_payment_type)
#         # 自动代扣异步处理的，请求成功一定是返回code=2处理中
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，cashfree的mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_code"], global_autoSubscribe_withhold_failcode, '代扣失败')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"], global_autoSubscribe_withhold_message, '代扣失败')
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_fail(self.db_test_payment, merchant_key, withhold_receipt_info[0]["withhold_receipt_channel_key"],
#                                resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，代扣相关表统一检查 ，   由于自动代扣卡号不固定，需要重新写统一的断言
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_cashfree_subscribe_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_withhold_queryfail_002(self):
#         # 自动代扣-订阅代扣请求处理中，后查询到代扣失败
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_withhold_process_cashfree()
#         global_payment_mock.update_autoSubscribe_withhold_query_fail_cashfree()
#         usable_card_uuid = get_usable_subscribe_carduuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_card_carduuid_get_account(self.db_test_payment, card_uuid)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起自动代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, self.sign_company_yomoyo, card_uuid, self.system_operator, self.system_payment_type)
#         # 自动代扣异步处理的，请求成功一定是返回code=2处理中
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，cashfree的mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_code"], global_autoSubscribe_withhold_failcode, '代扣失败')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"], global_autoSubscribe_withhold_message, '代扣失败')
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_fail(self.db_test_payment, merchant_key, withhold_receipt_info[0]["withhold_receipt_channel_key"],
#                                resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，代扣相关表统一检查 ，   由于自动代扣卡号不固定，需要重新写统一的断言
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_cashfree_subscribe_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_withhold_process_001(self):
#         # 自动代扣-订阅代扣查询返回处理中
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_withhold_process_cashfree()
#         global_payment_mock.update_autoSubscribe_withhold_query_process_cashfree()
#         usable_card_uuid = get_usable_subscribe_carduuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_card_carduuid_get_account(self.db_test_payment, card_uuid)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起自动代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, self.sign_company_yomoyo, card_uuid, self.system_operator, self.system_payment_type)
#         # 自动代扣异步处理的，请求成功一定是返回code=2处理中
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_process(self.db_test_payment, merchant_key)
#         # 断言，代扣相关表统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key, card_num, resp_withhold_autopay)
#         assert_check_cashfree_subscribe_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_withhold_process_002(self):
#         # 自动代扣-订阅代扣查询返回异常：代扣处理中
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_withhold_process_cashfree()
#         global_payment_mock.update_autoSubscribe_withhold_query_error_cashfree()
#         usable_card_uuid = get_usable_subscribe_carduuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_card_carduuid_get_account(self.db_test_payment, card_uuid)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起自动代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, self.sign_company_yomoyo, card_uuid, self.system_operator, self.system_payment_type)
#         # 自动代扣异步处理的，请求成功一定是返回code=2处理中
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_process(self.db_test_payment, merchant_key)
#         # 断言，代扣相关表统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key, card_num, resp_withhold_autopay)
#         assert_check_cashfree_subscribe_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_withhold_success(self):
#         # 自动代扣-订阅代扣直接成功
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_withhold_success_cashfree()
#         usable_card_uuid = get_usable_subscribe_carduuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_card_carduuid_get_account(self.db_test_payment, card_uuid)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起自动代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, self.sign_company_yomoyo, card_uuid, self.system_operator, self.system_payment_type)
#         # 自动代扣异步处理的，请求成功一定是返回code=2处理中
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，cashfree的mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_code"], global_autoSubscribe_withhold_successcode, '代扣成功')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"], global_autoSubscribe_withhold_message, '代扣成功')
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key, withhold_receipt_info[0]["withhold_receipt_channel_key"],
#                                resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，代扣相关表统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_cashfree_subscribe_channelrequestlog(self.db_test_payment, merchant_key)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.cashfree_subscribe
#     def test_cashfree_autoSubscribe_withhold_querysuccess(self):
#         # 自动代扣-订阅代扣查询到代扣成功
#         global_payment_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_autoSubscribe_withhold_process_cashfree()
#         global_payment_mock.update_autoSubscribe_withhold_query_success_cashfree()
#         usable_card_uuid = get_usable_subscribe_carduuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         account_info = by_card_carduuid_get_account(self.db_test_payment, card_uuid)
#         card_num = account_info[0]["account_card_num"]
#         merchant_key = get_timestamp()
#         # 发起自动代扣
#         resp_withhold_autopay = global_withhold_autopay(merchant_key, self.sign_company_yomoyo, card_uuid, self.system_operator, self.system_payment_type)
#         # 自动代扣异步处理的，请求成功一定是返回code=2处理中
#         assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"
#         # 手动执行task
#         run_task_withholdReceipt_withholdcharge_and_chargequery(self.db_test_payment, merchant_key)
#         # 无法统一的断言，cashfree的mock返回的场景决定code和message
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, merchant_key)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_code"], global_autoSubscribe_withhold_successcode, '代扣成功')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"], global_autoSubscribe_withhold_message, '代扣成功')
#         # 代扣成功状态检查 + rbiz代扣结果查询
#         assert_withhold_success(self.db_test_payment, merchant_key, withhold_receipt_info[0]["withhold_receipt_channel_key"],
#                                resp_withhold_autopay['content']['data']['channel_name'], card_uuid, global_amount)
#         # 断言，代扣相关表统一检查
#         assert_check_withhold_withholdreceipt(self.db_test_payment, card_uuid, merchant_key,
#                                               card_num, resp_withhold_autopay)
#         assert_check_cashfree_subscribe_channelrequestlog(self.db_test_payment, merchant_key)
#
# # cashfree订阅路由取消mock不了处理
# # 根据card_uuid拿到的card_num不一定准确，想想