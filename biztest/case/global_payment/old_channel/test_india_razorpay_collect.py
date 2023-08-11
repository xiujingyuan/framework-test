# # -*- coding: utf-8 -*-
# import json
# import time
#
# import pytest
#
# from biztest.config.payment.url_config import global_job_group_mapping_payment, \
#     global_razorpay_collect_inner_no, global_razorpay_collect_channel_key1, global_razorpay_collect_cardnum_encrypt, \
#     global_sign_company_yomoyo, global_razorpay_collect_channel_key2, global_razorpay_ebank_service_fee, \
#     global_razorpay_ebank_service_tax, global_razorpay_collect_payment_mode_upi, \
#     global_razorpay_collect_payment_mode_other, global_razorpay_collect_payment_option
# from biztest.function.global_payment.global_payment_db_operation import update_kv_mockrazorpay, \
#     undo_update_kv_mockrazorpay, \
#     update_withholdaccount_only_one_usableaccount, delete_razorpay_collect_withholdandreceiptandcard, \
#     get_one_usable_withhold_account_no, get_rbiz_collect_callbackurl, update_withholdaccount_allactive, \
#     get_withhold_account_by_account_no, get_task_collectWithholdChargeQuery, get_usable_card_uuid, \
#     update_channel_status_allusable, get_haveclosed_account_no, get_withhold_receipt_by_merchant_key, \
#     uppdate_withholdandreceipt_channel_key
# from biztest.interface.payment.payment_interface import get_timestamp, global_withhold_autoRegister, global_withhold_unRegister
# from biztest.util.asserts.assert_util import Assert
# from biztest.util.db.db_util import DataBase
# from biztest.util.easymock.global_payment.global_payment_razorpay import RazorpayMock
# from biztest.util.xxl_job.xxl_job import XxlJob
# from biztest.function.global_payment.global_payment_db_assert import run_task_collectWithholdChargeQuery, \
#     assert_razorpay_collect_withhold_withholdreceipt_sendmsg, assert_razorpay_collect_haverepaycard, \
#     assert_autoRegister_chaneck_withholdaccount, assert_razorpay_autoRegister_fail, \
#     assert_razorpay_autoRegister_success, assert_razorpay_collect_norepaycard
#
#
# # global_payment下razorpay通道：  线下还款开虚户 & 线下还款信息保存 & 虚户注销
# class TestIndiaRazorpayCollect:
#     """
#     global razorpay collect
#     author: fangchangfang
#     date: 2020
#     """
#     db_test_payment = None
#
#     @classmethod
#     def setup_class(self):
#         self.env_test = pytest.config.getoption("--env") if hasattr(pytest, "config") else 1
#         self.db_test_payment = DataBase("global_payment_test%s" % self.env_test)
#         # 修改KV中地址改为easymock
#         update_kv_mockrazorpay(self.db_test_payment)
#         # 初始化一些基础信息
#         self.ifsc = "mock_test_0001"
#         self.address_encrypt = "enc_06_2752832664892874752_745"  # 随意邮箱
#         self.user_name_encrypt = "enc_04_2752870379604680704_505"
#         self.mobile_encrypt = "enc_01_2752562028249358336_117"
#         self.email_encrypt = "enc_05_2752999188760895488_191"
#         # 从KV中拿到rbiz的线下还款回调地址
#         kv_callback_config = get_rbiz_collect_callbackurl(self.db_test_payment)
#         callback_config_info = json.loads(kv_callback_config[0]["keyvalue_value"])
#         self.global_rbiz_callbackurl = callback_config_info['rbiz_callback']['withhold']
#
#     @classmethod
#     def teardown_class(self):
#         # 还原环境
#         undo_update_kv_mockrazorpay(self.db_test_payment)
#         update_channel_status_allusable(self.db_test_payment)
#         DataBase.close_connects()
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.razorpay_collect
#     def test_razorpay_openvirtualaccount_fail_001(self):
#         # 线下还款开虚户：创建联系人直接失败-导致开户失败
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_customer_register_fail()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         merchant_key = "auto_test" + get_timestamp()
#         user_uuid = "auto_test" + get_timestamp()
#         individual_uuid = "auto_test" + get_timestamp()
#         account_no = "auto_test" + get_timestamp()  # 新开户的account_no唯一即可
#         sign_company = global_sign_company_yomoyo
#         # 发起开户
#         resp_withhold_autoRegister = global_withhold_autoRegister(merchant_key, sign_company, card_uuid, account_no, user_uuid, individual_uuid, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt)
#         # 断言，开户统一检查
#         assert_autoRegister_chaneck_withholdaccount(self.db_test_payment, account_no, card_uuid, user_uuid, individual_uuid,
#                                                     self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt, resp_withhold_autoRegister)
#         assert_razorpay_autoRegister_fail(self.db_test_payment, account_no, resp_withhold_autoRegister)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.razorpay_collect
#     def test_razorpay_openvirtualaccount_fail_002(self):
#         # 线下还款开虚户：创建联系人成功+开户失败-导致开户失败
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_customer_register_success()
#         global_payment_mock.update_razorpay_collect_account_register_fail()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         merchant_key = "auto_test" + get_timestamp()
#         user_uuid = "auto_test" + get_timestamp()
#         individual_uuid = "auto_test" + get_timestamp()
#         account_no = "auto_test" + get_timestamp()  # 新开户的account_no唯一即可
#         sign_company = global_sign_company_yomoyo
#         # 发起开户
#         resp_withhold_autoRegister = global_withhold_autoRegister(merchant_key, sign_company, card_uuid, account_no, user_uuid, individual_uuid, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt)
#         # 断言，开户统一检查
#         assert_autoRegister_chaneck_withholdaccount(self.db_test_payment, account_no, card_uuid, user_uuid, individual_uuid,
#                                                     self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt, resp_withhold_autoRegister)
#         assert_razorpay_autoRegister_fail(self.db_test_payment, account_no, resp_withhold_autoRegister)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.razorpay_collect
#     def test_razorpay_openvirtualaccount_success_new(self):
#         # 线下还款开虚户：新资产创建虚户成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_customer_register_success()
#         global_payment_mock.update_razorpay_collect_account_register_success()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         merchant_key = "auto_test" + get_timestamp()
#         user_uuid = "auto_test" + get_timestamp()
#         individual_uuid = "auto_test" + get_timestamp()
#         account_no = "auto_test" + get_timestamp()  # 新开户的account_no唯一即可
#         sign_company = global_sign_company_yomoyo
#         # 发起开户
#         resp_withhold_autoRegister = global_withhold_autoRegister(merchant_key, sign_company, card_uuid, account_no, user_uuid, individual_uuid, self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt)
#         # 断言，开户统一检查
#         assert_autoRegister_chaneck_withholdaccount(self.db_test_payment, account_no, card_uuid, user_uuid, individual_uuid,
#                                                     self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt, resp_withhold_autoRegister)
#         assert_razorpay_autoRegister_success(self.db_test_payment, account_no, resp_withhold_autoRegister)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.razorpay_collect
#     def test_razorpay_openvirtualaccount_success_old(self):
#         # 线下还款开虚户：已关闭的虚户再次创建虚户成功
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_customer_register_success()
#         global_payment_mock.update_razorpay_collect_account_register_success()
#         usable_card_uuid = get_usable_card_uuid(self.db_test_payment)
#         card_uuid = usable_card_uuid[0]['account_card_uuid']
#         haveclosed_account_no = get_haveclosed_account_no(self.db_test_payment)
#         account_no = haveclosed_account_no[0]['withhold_account_no']
#         # update_
#         merchant_key = "auto_test" + get_timestamp()
#         user_uuid = "auto_test" + get_timestamp()
#         individual_uuid = "auto_test" + get_timestamp()
#         sign_company = global_sign_company_yomoyo
#         # 发起开户
#         resp_withhold_autoRegister = global_withhold_autoRegister(merchant_key, sign_company, card_uuid, account_no,
#                                                                   user_uuid, individual_uuid, self.user_name_encrypt,
#                                                                   self.mobile_encrypt, self.email_encrypt)
#         # 断言，开户统一检查
#         assert_autoRegister_chaneck_withholdaccount(self.db_test_payment, account_no, card_uuid, user_uuid,
#                                                     individual_uuid,
#                                                     self.user_name_encrypt, self.mobile_encrypt, self.email_encrypt,
#                                                     resp_withhold_autoRegister)
#         assert_razorpay_autoRegister_success(self.db_test_payment, account_no, resp_withhold_autoRegister)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.razorpay_collect
#     def test_razorpay_closevirtualaccount_fail(self):
#         # 注销虚户失败
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_closeaccount_fail()
#         merchant_key = "auto_test" + get_timestamp()
#         # 保留一个active的虚户用来注销
#         update_withholdaccount_allactive(self.db_test_payment, global_razorpay_collect_inner_no)
#         update_withholdaccount_only_one_usableaccount(self.db_test_payment, global_razorpay_collect_inner_no)
#         withhold_account_info = get_one_usable_withhold_account_no(self.db_test_payment)
#         active_withhold_account_no = withhold_account_info[0]["withhold_account_no"]
#         # dsq发起注销
#         resp_withhold_unRegister = global_withhold_unRegister(merchant_key, active_withhold_account_no)
#         Assert.assert_equal(resp_withhold_unRegister['content']['code'], 1, '注销失败')
#         # 检查原虚户状态
#         withhold_account_info2 = get_withhold_account_by_account_no(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(withhold_account_info2[0]["withhold_account_status"], "active", "注销失败，不更新withhold_account状态")
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.razorpay_collect
#     def test_razorpay_closevirtualaccount_success_norepay(self):
#         # 注销虚户成功 + 未查询到还款信息
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_closeaccount_success()
#         merchant_key = "auto_test" + get_timestamp()
#         # 保留一个active的虚户用来注销
#         update_withholdaccount_allactive(self.db_test_payment, global_razorpay_collect_inner_no)
#         update_withholdaccount_only_one_usableaccount(self.db_test_payment, global_razorpay_collect_inner_no)
#         withhold_account_info = get_one_usable_withhold_account_no(self.db_test_payment)
#         active_withhold_account_no = withhold_account_info[0]["withhold_account_no"]
#         # 删除withhold和withhold_receipt、card表已有的还款信息
#         delete_razorpay_collect_withholdandreceiptandcard(self.db_test_payment, global_razorpay_collect_channel_key1,
#                                                           global_razorpay_collect_channel_key2,global_razorpay_collect_cardnum_encrypt)
#         # dsq发起注销
#         resp_withhold_unRegister = global_withhold_unRegister(merchant_key, active_withhold_account_no)
#         Assert.assert_equal(resp_withhold_unRegister['content']['code'], 0, '注销成功')
#         # 检查原虚户状态
#         withhold_account_info2 = get_withhold_account_by_account_no(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(withhold_account_info2[0]["withhold_account_status"], "closed", "注销成功，更新withhold_account状态")
#         # 虚户注销成功后会再查询一次还款信息
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_repaylist_norepay()
#         # 执行还款记录查询task
#         run_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         # 检查task是否关闭，未打款不会保存代扣记录
#         task_info = get_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(task_info[0]["task_status"], "close", "没有查询到还款信息也会关闭task")
#
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.razorpay_collect
#     def test_razorpay_savewithhold_norepay_001(self):
#         # 一直未打款 & 查询到虚户已关闭
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_repaylist_norepay()
#         global_payment_mock.update_razorpay_collect_accountstatus_closed()
#         # 初始化数据：1、只保留一个能查询到线下打款记录的虚户&2、虚户未过期
#         update_withholdaccount_allactive(self.db_test_payment, global_razorpay_collect_inner_no)
#         update_withholdaccount_only_one_usableaccount(self.db_test_payment, global_razorpay_collect_inner_no)
#         withhold_account_info = get_one_usable_withhold_account_no(self.db_test_payment)
#         active_withhold_account_no = withhold_account_info[0]["withhold_account_no"]
#         # 删除withhold和withhold_receipt、card表已有的还款信息
#         delete_razorpay_collect_withholdandreceiptandcard(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2,
#                                                           global_razorpay_collect_cardnum_encrypt)
#         # 调度job：线下还款虚户状态查询及支付查询处理
#         xxl_job = XxlJob(global_job_group_mapping_payment["global-payment-jobs-test{}".format(self.env_test)], "collectWithholdJob",
#                          password="123456", xxl_job_type="global_xxl_job_new")
#         xxl_job.trigger_job()
#         # 执行还款记录查询task
#         run_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         # 检查task是否关闭，未打款不会保存代扣记录
#         task_info = get_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(task_info[0]["task_status"], "close", "没有查询到还款信息也会关闭task")
#         # 检查原虚户状态
#         withhold_account_info2 = get_withhold_account_by_account_no(self.db_test_payment, active_withhold_account_no)
#         assert withhold_account_info2[0]["withhold_account_status"] == "closed", "虚户已过期，更新withhold_account状态"
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.razorpay_collect
#     def test_razorpay_savewithhold_norepay_002(self):
#         # 一直未打款 & 查询到虚户未关闭
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_repaylist_norepay()
#         global_payment_mock.update_razorpay_collect_accountstatus_active()
#         # 初始化数据：1、只保留一个能查询到线下打款记录的虚户&2、虚户未过期
#         update_withholdaccount_allactive(self.db_test_payment, global_razorpay_collect_inner_no)
#         update_withholdaccount_only_one_usableaccount(self.db_test_payment, global_razorpay_collect_inner_no)
#         withhold_account_info = get_one_usable_withhold_account_no(self.db_test_payment)
#         active_withhold_account_no = withhold_account_info[0]["withhold_account_no"]
#         # 删除withhold和withhold_receipt、card表已有的还款信息
#         delete_razorpay_collect_withholdandreceiptandcard(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2,
#                                                           global_razorpay_collect_cardnum_encrypt)
#         # 调度job：线下还款虚户状态查询及支付查询处理
#         xxl_job = XxlJob(global_job_group_mapping_payment["global-payment-jobs-test{}".format(self.env_test)], "collectWithholdJob",
#                          password="123456", xxl_job_type="global_xxl_job_new")
#         xxl_job.trigger_job()
#         # 执行还款记录查询task
#         run_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         # 检查task是否关闭，未打款不会保存代扣记录
#         task_info = get_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(task_info[0]["task_status"], "close", "没有查询到还款信息也会关闭task")
#         # 检查原虚户状态
#         withhold_account_info2 = get_withhold_account_by_account_no(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(withhold_account_info2[0]["withhold_account_status"], "active",
#                             "虚户未关闭，不更新withhold_account状态")
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay_collect
#     @pytest.mark.global_razorpay_collect_success
#     def test_razorpay_closevirtualaccount_success_haverepay(self):
#         # 注销虚户成功 + 再次查询到还款信息
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_closeaccount_success()
#         merchant_key = "auto_test" + get_timestamp()
#         # 保留一个active的虚户用来注销
#         update_withholdaccount_allactive(self.db_test_payment, global_razorpay_collect_inner_no)
#         update_withholdaccount_only_one_usableaccount(self.db_test_payment, global_razorpay_collect_inner_no)
#         withhold_account_info = get_one_usable_withhold_account_no(self.db_test_payment)
#         active_withhold_account_no = withhold_account_info[0]["withhold_account_no"]
#         # 删除withhold和withhold_receipt、card表已有的还款信息
#         delete_razorpay_collect_withholdandreceiptandcard(self.db_test_payment, global_razorpay_collect_channel_key1,
#                                                           global_razorpay_collect_channel_key2, global_razorpay_collect_cardnum_encrypt)
#         # dsq发起注销
#         resp_withhold_unRegister = global_withhold_unRegister(merchant_key, active_withhold_account_no)
#         Assert.assert_equal(resp_withhold_unRegister['content']['code'], 0, '注销成功')
#         # 检查原虚户状态
#         withhold_account_info2 = get_withhold_account_by_account_no(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(withhold_account_info2[0]["withhold_account_status"], "closed", "注销成功，更新withhold_account状态")
#         # 虚户注销成功后会再查询一次还款信息
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_repaylist_onesuccess()
#         global_payment_mock.update_razorpay_collect_repaydetail_success_channelkey1_havecard()
#         global_payment_mock.update_razorpay_collect_accountstatus_closed()
#         # 执行还款记录查询task
#         run_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         time.sleep(5)
#         # 打款明细中返回了还款卡，卡号保存检查
#         assert_razorpay_collect_haverepaycard(self.db_test_payment)
#         # 线下还款成功withhold、withhold_receipt和card表统一检查
#         assert_razorpay_collect_withhold_withholdreceipt_sendmsg(self.db_test_payment, global_razorpay_collect_channel_key1,
#                                                                  withhold_account_info[0]["withhold_account_no"], withhold_account_info[0]["withhold_account_card_uuid"],
#                                                                  withhold_account_info[0]["withhold_account_receiver_channel"], self.global_rbiz_callbackurl)
#         # 无法统一的断言，mock返回的场景决定
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, global_razorpay_collect_channel_key1)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_charge"], global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax, '通道流水号')
#         assert withhold_receipt_info[0]["withhold_receipt_payment_option"] == global_razorpay_collect_payment_option, 'option'
#         assert withhold_receipt_info[0]["withhold_receipt_payment_mode"] == global_razorpay_collect_payment_mode_upi, 'mode'
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay_collect
#     @pytest.mark.global_razorpay_collect_success
#     def test_razorpay_savewithhold_success_accountclosed_nocard(self):
#         # 打款成功一次无还款卡 & 查询到虚户未关闭
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_repaylist_onesuccess()
#         global_payment_mock.update_razorpay_collect_repaydetail_success_channelkey1_nocard()
#         global_payment_mock.update_razorpay_collect_accountstatus_active()
#         # 初始化数据：1、只保留一个能查询到线下打款记录的虚户
#         update_withholdaccount_allactive(self.db_test_payment, global_razorpay_collect_inner_no)
#         update_withholdaccount_only_one_usableaccount(self.db_test_payment, global_razorpay_collect_inner_no)
#         withhold_account_info = get_one_usable_withhold_account_no(self.db_test_payment)
#         active_withhold_account_no = withhold_account_info[0]["withhold_account_no"]
#         # 删除withhold和withhold_receipt、card表已有的还款信息
#         delete_razorpay_collect_withholdandreceiptandcard(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2,
#                                                           global_razorpay_collect_cardnum_encrypt)
#         # 调度job：线下还款虚户状态查询及支付查询处理
#         xxl_job = XxlJob(global_job_group_mapping_payment["global-payment-jobs-test{}".format(self.env_test)], "collectWithholdJob",
#                          password="123456", xxl_job_type="global_xxl_job_new")
#         xxl_job.trigger_job()
#         # 执行还款记录查询task
#         run_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         time.sleep(5)
#         # 打款明细中没有返回还款卡
#         assert_razorpay_collect_norepaycard(self.db_test_payment)
#         # 线下还款成功withhold、withhold_receipt和sendmsg表统一检查
#         assert_razorpay_collect_withhold_withholdreceipt_sendmsg(self.db_test_payment,
#                                                                  global_razorpay_collect_channel_key1,
#                                                                  withhold_account_info[0]["withhold_account_no"],
#                                                                  withhold_account_info[0]["withhold_account_card_uuid"],
#                                                                  withhold_account_info[0]["withhold_account_receiver_channel"],
#                                                                  self.global_rbiz_callbackurl)
#         # 检查原虚户状态
#         withhold_account_info2 = get_withhold_account_by_account_no(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(withhold_account_info2[0]["withhold_account_status"], "active", "虚户未过期")
#         # 无法统一的断言，mock返回的场景决定
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, global_razorpay_collect_channel_key1)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_charge"], global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax, '通道流水号')
#         assert withhold_receipt_info[0]["withhold_receipt_payment_option"] == global_razorpay_collect_payment_option, 'option'
#         assert withhold_receipt_info[0]["withhold_receipt_payment_mode"] == global_razorpay_collect_payment_mode_other, 'mode'
#         # 把数据保留在代扣表
#         uppdate_withholdandreceipt_channel_key(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay_collect
#     @pytest.mark.global_razorpay_collect_success
#     @pytest.mark.test_razorpay_savewithhold_success_accountactive
#     def test_razorpay_savewithhold_success_accountactive(self):
#         # 打款成功一次有还款卡 & 查询到虚户未关闭
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_repaylist_onesuccess()
#         global_payment_mock.update_razorpay_collect_repaydetail_success_channelkey1_havecard()
#         global_payment_mock.update_razorpay_collect_accountstatus_active()
#         # 删除withhold和withhold_receipt、card表已有的还款信息
#         delete_razorpay_collect_withholdandreceiptandcard(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2,
#                                                           global_razorpay_collect_cardnum_encrypt)
#         # 初始化数据：1、只保留一个能查询到线下打款记录的虚户&2、虚户已过期
#         update_withholdaccount_allactive(self.db_test_payment, global_razorpay_collect_inner_no)
#         update_withholdaccount_only_one_usableaccount(self.db_test_payment, global_razorpay_collect_inner_no)
#         withhold_account_info = get_one_usable_withhold_account_no(self.db_test_payment)
#         active_withhold_account_no = withhold_account_info[0]["withhold_account_no"]
#         # 调度job：线下还款虚户状态查询及支付查询处理
#         xxl_job = XxlJob(global_job_group_mapping_payment["global-payment-jobs-test{}".format(self.env_test)], "collectWithholdJob",
#                          password="123456", xxl_job_type="global_xxl_job_new")
#         xxl_job.trigger_job()
#         # 执行还款记录查询task
#         run_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         time.sleep(3)
#         # 打款明细中返回了还款卡，卡号保存检查
#         assert_razorpay_collect_haverepaycard(self.db_test_payment)
#         # 线下还款成功withhold、withhold_receipt和sendmsg表统一检查
#         assert_razorpay_collect_withhold_withholdreceipt_sendmsg(self.db_test_payment,
#                                                                  global_razorpay_collect_channel_key1,
#                                                                  withhold_account_info[0]["withhold_account_no"],
#                                                                  withhold_account_info[0]["withhold_account_card_uuid"],
#                                                                  withhold_account_info[0]["withhold_account_receiver_channel"],
#                                                                  self.global_rbiz_callbackurl)
#         # 检查原虚户状态
#         withhold_account_info2 = get_withhold_account_by_account_no(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(withhold_account_info2[0]["withhold_account_status"], "active",
#                             "虚户未关闭，不更新withhold_account状态")
#         # 无法统一的断言，mock返回的场景决定
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, global_razorpay_collect_channel_key1)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_charge"], global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax, '通道流水号')
#         assert withhold_receipt_info[0]["withhold_receipt_payment_option"] == global_razorpay_collect_payment_option, 'option'
#         assert withhold_receipt_info[0]["withhold_receipt_payment_mode"] == global_razorpay_collect_payment_mode_upi, 'mode'
#         # 保留数据在代扣表
#         uppdate_withholdandreceipt_channel_key(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2)
#         # 把数据保留在代扣表
#         uppdate_withholdandreceipt_channel_key(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2)
#
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay_collect
#     @pytest.mark.global_razorpay_collect_success
#     def test_razorpay_savewithhold_success_accountclosed_havecard(self):
#         # 打款成功一次有还款卡 & 查询到虚户已关闭
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_repaylist_onesuccess()
#         global_payment_mock.update_razorpay_collect_repaydetail_success_channelkey1_havecard()
#         global_payment_mock.update_razorpay_collect_accountstatus_closed()
#         # 初始化数据：1、只保留一个能查询到线下打款记录的虚户&2、虚户未过期
#         update_withholdaccount_allactive(self.db_test_payment, global_razorpay_collect_inner_no)
#         update_withholdaccount_only_one_usableaccount(self.db_test_payment, global_razorpay_collect_inner_no)
#         withhold_account_info = get_one_usable_withhold_account_no(self.db_test_payment)
#         active_withhold_account_no = withhold_account_info[0]["withhold_account_no"]
#         # 删除withhold和withhold_receipt、card表已有的还款信息
#         delete_razorpay_collect_withholdandreceiptandcard(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2,
#                                                           global_razorpay_collect_cardnum_encrypt)
#         # 调度job：线下还款虚户状态查询及支付查询处理
#         xxl_job = XxlJob(global_job_group_mapping_payment["global-payment-jobs-test{}".format(self.env_test)], "collectWithholdJob",
#                          password="123456", xxl_job_type="global_xxl_job_new")
#         xxl_job.trigger_job()
#         # 执行还款记录查询task
#         run_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         time.sleep(3)
#         # 打款明细中返回了还款卡，卡号保存检查
#         assert_razorpay_collect_haverepaycard(self.db_test_payment)
#         # 线下还款成功withhold、withhold_receipt和sendmsg表统一检查
#         assert_razorpay_collect_withhold_withholdreceipt_sendmsg(self.db_test_payment,
#                                                                  global_razorpay_collect_channel_key1,
#                                                                  withhold_account_info[0]["withhold_account_no"],
#                                                                  withhold_account_info[0]["withhold_account_card_uuid"],
#                                                                  withhold_account_info[0]["withhold_account_receiver_channel"],
#                                                                  self.global_rbiz_callbackurl)
#         # 检查原虚户状态
#         withhold_account_info2 = get_withhold_account_by_account_no(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(withhold_account_info2[0]["withhold_account_status"], "closed",
#                             "虚户已过期，更新withhold_account状态")
#         # 无法统一的断言，mock返回的场景决定
#         withhold_receipt_info = get_withhold_receipt_by_merchant_key(self.db_test_payment, global_razorpay_collect_channel_key1)
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_charge"], global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax, '通道流水号')
#         assert withhold_receipt_info[0]["withhold_receipt_payment_option"] == global_razorpay_collect_payment_option, 'option'
#         assert withhold_receipt_info[0]["withhold_receipt_payment_mode"] == global_razorpay_collect_payment_mode_upi, 'mode'
#         # 把数据保留在代扣表
#         uppdate_withholdandreceipt_channel_key(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay_collect
#     @pytest.mark.global_razorpay_collect_success
#     def test_razorpay_savewithhold_twosuccess_001(self):
#         # 打款成功两次：一次查询到
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_repaylist_twosuccess()
#         global_payment_mock.update_razorpay_collect_repaydetail_success_channelkey1_havecard()
#         global_payment_mock.update_razorpay_collect_repaydetail_success_channelkey2()
#         global_payment_mock.update_razorpay_collect_accountstatus_active()
#         # 初始化数据：1、只保留一个能查询到线下打款记录的虚户&2、虚户已过期
#         update_withholdaccount_allactive(self.db_test_payment, global_razorpay_collect_inner_no)
#         update_withholdaccount_only_one_usableaccount(self.db_test_payment, global_razorpay_collect_inner_no)
#         withhold_account_info = get_one_usable_withhold_account_no(self.db_test_payment)
#         active_withhold_account_no = withhold_account_info[0]["withhold_account_no"]
#         # 删除withhold和withhold_receipt、card表已有的还款信息
#         delete_razorpay_collect_withholdandreceiptandcard(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2,
#                                                           global_razorpay_collect_cardnum_encrypt)
#         # 调度job：线下还款虚户状态查询及支付查询处理
#         xxl_job = XxlJob(global_job_group_mapping_payment["global-payment-jobs-test{}".format(self.env_test)], "collectWithholdJob",
#                          password="123456", xxl_job_type="global_xxl_job_new")
#         xxl_job.trigger_job()
#         # 执行还款记录查询task
#         run_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         time.sleep(3)
#         # 打款明细中返回了还款卡，卡号保存检查
#         assert_razorpay_collect_haverepaycard(self.db_test_payment)
#         # 线下还款成功withhold、withhold_receipt和sendmsg表统一检查:global_razorpay_collect_channel_key1、global_razorpay_collect_channel_key2
#         assert_razorpay_collect_withhold_withholdreceipt_sendmsg(self.db_test_payment, global_razorpay_collect_channel_key1,
#                                                                  withhold_account_info[0]["withhold_account_no"],
#                                                                  withhold_account_info[0]["withhold_account_card_uuid"],
#                                                                  withhold_account_info[0]["withhold_account_receiver_channel"],
#                                                                  self.global_rbiz_callbackurl)
#         assert_razorpay_collect_withhold_withholdreceipt_sendmsg(self.db_test_payment, global_razorpay_collect_channel_key2,
#                                                                  withhold_account_info[0]["withhold_account_no"],
#                                                                  withhold_account_info[0]["withhold_account_card_uuid"],
#                                                                  withhold_account_info[0]["withhold_account_receiver_channel"],
#                                                                  self.global_rbiz_callbackurl)
#         # 检查原虚户状态
#         withhold_account_info2 = get_withhold_account_by_account_no(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(withhold_account_info2[0]["withhold_account_status"], "active", "虚户未关闭，不更新withhold_account状态")
#
#         # 本地已保存还款信息后再次调度job查询：没有查询到新的还款
#         xxl_job = XxlJob(global_job_group_mapping_payment["global-payment-jobs-test{}".format(self.env_test)], "collectWithholdJob",
#                          password="123456", xxl_job_type="global_xxl_job_new")
#         xxl_job.trigger_job()
#         run_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         # 检查task是否关闭，本次不会保存代扣记录
#         task_info = get_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(task_info[0]["task_status"], "close", "关闭task")
#         # 无法统一的断言，mock返回的场景决定
#         withhold_receipt_info1 = get_withhold_receipt_by_merchant_key(self.db_test_payment, global_razorpay_collect_channel_key1)
#         withhold_receipt_info2 = get_withhold_receipt_by_merchant_key(self.db_test_payment, global_razorpay_collect_channel_key2)
#         Assert.assert_equal(withhold_receipt_info1[0]["withhold_receipt_service_charge"], global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info1[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info2[0]["withhold_receipt_service_charge"], global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info2[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax, '通道流水号')
#         # 把数据保留在代扣表
#         uppdate_withholdandreceipt_channel_key(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2)
#
#     @pytest.mark.global_payment_india
#     @pytest.mark.global_razorpay_collect
#     @pytest.mark.global_razorpay_collect_success
#     @pytest.mark.test_razorpay_savewithhold_twosuccess_002
#     def test_razorpay_savewithhold_twosuccess_002(self):
#         # 打款成功两次：分多次查询到
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_accountstatus_active()
#         global_payment_mock.update_razorpay_collect_repaylist_onesuccess()
#         global_payment_mock.update_razorpay_collect_repaydetail_success_channelkey1_havecard()
#         # 初始化数据：1、只保留一个能查询到线下打款记录的虚户
#         update_withholdaccount_allactive(self.db_test_payment, global_razorpay_collect_inner_no)
#         update_withholdaccount_only_one_usableaccount(self.db_test_payment, global_razorpay_collect_inner_no)
#         withhold_account_info = get_one_usable_withhold_account_no(self.db_test_payment)
#         active_withhold_account_no = withhold_account_info[0]["withhold_account_no"]
#         # 删除withhold和withhold_receipt、card表已有的还款信息
#         delete_razorpay_collect_withholdandreceiptandcard(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2,
#                                                           global_razorpay_collect_cardnum_encrypt)
#         # 调度job：线下还款虚户状态查询及支付查询处理
#         xxl_job = XxlJob(global_job_group_mapping_payment["global-payment-jobs-test{}".format(self.env_test)], "collectWithholdJob",
#                          password="123456", xxl_job_type="global_xxl_job_new")
#         xxl_job.trigger_job()
#         # 执行还款记录查询task
#         run_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         time.sleep(3)
#         # 打款明细中返回了还款卡，卡号保存检查
#         assert_razorpay_collect_haverepaycard(self.db_test_payment)
#         # 线下还款成功withhold、withhold_receipt和sendmsg表统一检查:global_razorpay_collect_channel_key1
#         assert_razorpay_collect_withhold_withholdreceipt_sendmsg(self.db_test_payment, global_razorpay_collect_channel_key1,
#                                                                  withhold_account_info[0]["withhold_account_no"], withhold_account_info[0]["withhold_account_card_uuid"],
#                                                                  withhold_account_info[0]["withhold_account_receiver_channel"], self.global_rbiz_callbackurl)
#         # 第二次打款：再次调度job，查询到有新的还款 + 虚户过期
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_collect_repaylist_twosuccess()
#         global_payment_mock.update_razorpay_collect_repaydetail_success_channelkey2()
#         global_payment_mock.update_razorpay_collect_accountstatus_closed()
#         xxl_job = XxlJob(global_job_group_mapping_payment["global-payment-jobs-test{}".format(self.env_test)], "collectWithholdJob",
#                          password="123456", xxl_job_type="global_xxl_job_new")
#         xxl_job.trigger_job()
#         run_task_collectWithholdChargeQuery(self.db_test_payment, active_withhold_account_no)
#         time.sleep(3)
#         # 线下还款成功withhold、withhold_receipt和sendmsg表统一检查:global_razorpay_collect_channel_key2
#         assert_razorpay_collect_withhold_withholdreceipt_sendmsg(self.db_test_payment, global_razorpay_collect_channel_key2,
#                                                                  withhold_account_info[0]["withhold_account_no"], withhold_account_info[0]["withhold_account_card_uuid"],
#                                                                  withhold_account_info[0]["withhold_account_receiver_channel"], self.global_rbiz_callbackurl)
#         # 检查原虚户状态
#         withhold_account_info2 = get_withhold_account_by_account_no(self.db_test_payment, active_withhold_account_no)
#         Assert.assert_equal(withhold_account_info2[0]["withhold_account_status"], "closed", "虚户关闭")
#         # 无法统一的断言，mock返回的场景决定
#         withhold_receipt_info1 = get_withhold_receipt_by_merchant_key(self.db_test_payment, global_razorpay_collect_channel_key1)
#         withhold_receipt_info2 = get_withhold_receipt_by_merchant_key(self.db_test_payment, global_razorpay_collect_channel_key2)
#         Assert.assert_equal(withhold_receipt_info1[0]["withhold_receipt_service_charge"], global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info1[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info2[0]["withhold_receipt_service_charge"], global_razorpay_ebank_service_fee-global_razorpay_ebank_service_tax, '通道流水号')
#         Assert.assert_equal(withhold_receipt_info2[0]["withhold_receipt_service_tax"], global_razorpay_ebank_service_tax, '通道流水号')
#         assert withhold_receipt_info1[0]["withhold_receipt_payment_option"] == global_razorpay_collect_payment_option, 'option'
#         assert withhold_receipt_info1[0]["withhold_receipt_payment_mode"] == global_razorpay_collect_payment_mode_upi, 'mode'
#         assert withhold_receipt_info2[0]["withhold_receipt_payment_option"] == global_razorpay_collect_payment_option, 'option'
#         assert withhold_receipt_info2[0]["withhold_receipt_payment_mode"] == global_razorpay_collect_payment_mode_other, 'mode'
#         # 把数据保留在代扣表
#         uppdate_withholdandreceipt_channel_key(self.db_test_payment, global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2)
#
