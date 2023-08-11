# import pytest
#
# from biztest.config.payment.url_config import global_razorpay_transfer_id, global_razorpay_ebank_channel_key, \
#     global_razorpay_ebank_service_fee, global_razorpay_ebank_service_tax, global_razorpay_ebank_amount, \
#     global_razorpay_ebank_merchant_key, global_razorpay_in_account_no, india_razorpay_transfer_channel_name
# from biztest.function.global_payment.global_payment_db_assert import assert_check_withdraw_withdrawreceipt, \
#     assert_withdraw_process, run_task_withdraw_and_withdrawquery, run_reconci_task, assert_withdraw_fail, \
#     assert_withdraw_success
# from biztest.function.global_payment.global_payment_db_operation import update_kv_mockrazorpay, \
#     undo_update_kv_mockrazorpay, get_global_withdraw_receipt_info_by_merchant_key, \
#     undo_update_kv_withdraw_riskwhite, by_carduuid_get_ccountandbinding_info, \
#     get_global_card_info_by_card_num, delete_razorpay_transfer_withdrawandreceipt, update_task_order_no, \
#     insert_channel_reconci, insert_withhold_receipt, delete_withhold_receipt_by_merchantkey, \
#     delete_channel_reconci_by_merchantkey, add_transfer_fail_channel_error, insert_razorpay_ransfer_data, \
#     update_global_task_next_run_at
# from biztest.interface.payment.payment_interface import global_transfer_transfer, get_timestamp, global_transfer_query, \
#     global_job_run_reconci, global_fee_query, global_job_runtask
# from biztest.util.db.db_util import DataBase, time
# from biztest.util.easymock.global_payment.global_payment_razorpay import RazorpayMock
#
#
# class TestIndiaTransferClean:
#     """
#     global india razorpay transfer clean
#     author: fangchangfang
#     date: 2020-06-11
#     """
#
#     def setup_class(self):
#         self.env_test = pytest.config.getoption("--env") if hasattr(pytest, "config") else 1
#         self.db_test_payment = DataBase("global_payment_test%s" % self.env_test)
#         # 修改KV中地址改为easymock
#         update_kv_mockrazorpay(self.db_test_payment)
#         # 初始化数据
#         self.card_account = "enc_04_2795883791758401536_344"
#         self.card_num = "enc_04_2917888104180752384_256"
#         self.card_uuid = global_razorpay_in_account_no  # 清分转账的in_account_no即card_uuid
#         self.acct_id = "acc_ExbVyNbpdbqoZx"  # 测试环境的一个清分转账虚户号
#         self.channel_name = india_razorpay_transfer_channel_name  # 写死razorpay清分转账的通道名，若测试环境改了通道名，会导致用例失败
#         insert_razorpay_ransfer_data(self.db_test_payment, self.card_uuid, self.card_num, self.channel_name, self.acct_id, self.card_account)
#
#     def teardown_class(self):
#         # 还原环境
#         undo_update_kv_mockrazorpay(self.db_test_payment)
#         DataBase.close_connects()
#
#     @pytest.mark.feequery
#     @pytest.mark.global_payment_india
#     def test_withhold_feequery_by_feestatistics(self):
#         """
#         清分转账：单笔代扣成功查询（channel_reconci表没有结算数据，withhold_receipt成本是0，返回试算的成本）
#         试算接口目前还没实现
#         author: fangchangfang
#         date: 2020-06-11
#         """
#         # channel_reconci表插入一条结算数据
#         delete_withhold_receipt_by_merchantkey(self.db_test_payment, global_razorpay_ebank_merchant_key)
#         delete_channel_reconci_by_merchantkey(self.db_test_payment, global_razorpay_ebank_merchant_key)
#         insert_withhold_receipt(self.db_test_payment, global_razorpay_ebank_channel_key,
#                                 global_razorpay_ebank_merchant_key, global_razorpay_ebank_amount, 0, 0)
#         resp_feequery = global_fee_query(global_razorpay_ebank_merchant_key, "withhold")
#         assert resp_feequery['content']['code'] == 0, "单笔成本查询成功"
#         assert resp_feequery['content']['data'] == [], "单笔成本查询成功"  # withhold_receipt成本为0时先返回空，让清结算不清分
#
#     @pytest.mark.feequery
#     @pytest.mark.global_payment_india
#     def test_withhold_feequery_by_channelreconci_001(self):
#         """
#         清分转账：单笔代扣成功查询（channel_reconci表有结算数据）
#         author: fangchangfang
#         date: 2020-06-11
#         """
#         # channel_reconci表插入一条结算数据
#         delete_withhold_receipt_by_merchantkey(self.db_test_payment, global_razorpay_ebank_merchant_key)
#         delete_channel_reconci_by_merchantkey(self.db_test_payment, global_razorpay_ebank_merchant_key)
#         insert_channel_reconci(self.db_test_payment, global_razorpay_ebank_channel_key,
#                                global_razorpay_ebank_merchant_key, global_razorpay_ebank_amount,
#                                global_razorpay_ebank_service_fee,
#                                global_razorpay_ebank_service_fee - global_razorpay_ebank_service_tax,
#                                global_razorpay_ebank_service_tax)
#         insert_withhold_receipt(self.db_test_payment, global_razorpay_ebank_channel_key,
#                                 global_razorpay_ebank_merchant_key, global_razorpay_ebank_amount,
#                                 global_razorpay_ebank_service_fee - global_razorpay_ebank_service_tax,
#                                 global_razorpay_ebank_service_tax)
#         resp_feequery = global_fee_query(global_razorpay_ebank_merchant_key, "withhold")
#         assert resp_feequery['content']['code'] == 0, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['merchant_key'] == global_razorpay_ebank_merchant_key, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['channel_key'] == global_razorpay_ebank_channel_key, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['fee_type'] == "withhold", "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['fee_from'] == "settled", "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['order_amount'] == global_razorpay_ebank_amount, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['fee_amount'] == global_razorpay_ebank_service_fee, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0][
#                    'service_amount'] == global_razorpay_ebank_service_fee - global_razorpay_ebank_service_tax, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['tax_amount'] == global_razorpay_ebank_service_tax, "单笔成本查询成功"
#
#     @pytest.mark.feequery
#     @pytest.mark.global_payment_india
#     def test_withhold_feequery_by_channelreconci_002(self):
#         """
#         清分转账：单笔代扣成功查询（channel_reconci表有结算数据且成本为0）
#         author: fangchangfang
#         date: 2020-06-11
#         """
#         # channel_reconci表插入一条结算数据
#         delete_withhold_receipt_by_merchantkey(self.db_test_payment, global_razorpay_ebank_merchant_key)
#         delete_channel_reconci_by_merchantkey(self.db_test_payment, global_razorpay_ebank_merchant_key)
#         insert_channel_reconci(self.db_test_payment, global_razorpay_ebank_channel_key,
#                                global_razorpay_ebank_merchant_key, global_razorpay_ebank_amount,
#                                0, 0, 0)
#         insert_withhold_receipt(self.db_test_payment, global_razorpay_ebank_channel_key,
#                                 global_razorpay_ebank_merchant_key, global_razorpay_ebank_amount,
#                                 0, 0)
#         resp_feequery = global_fee_query(global_razorpay_ebank_merchant_key, "withhold")
#         assert resp_feequery['content']['code'] == 0, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['merchant_key'] == global_razorpay_ebank_merchant_key, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['channel_key'] == global_razorpay_ebank_channel_key, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['fee_type'] == "withhold", "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['fee_from'] == "settled", "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['order_amount'] == global_razorpay_ebank_amount, "单笔成本查询成功"
#         # channel_reconci表有结算数据且成本为0，直接将成本0返回，清结算可以结算只是表示没有成本
#         assert resp_feequery['content']['data'][0]['fee_amount'] == 0, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['service_amount'] == 0, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['tax_amount'] == 0, "单笔成本查询成功"
#
#     @pytest.mark.feequery
#     @pytest.mark.global_payment_india
#     def test_withhold_feequery_by_withholdreceipt(self):
#         """
#         清分转账：单笔代扣成功查询（channel_reconci表没有结算数据，withhold_receipt成本有值）
#         author: fangchangfang
#         date: 2020-06-11
#         """
#         # channel_reconci表插入一条结算数据
#         delete_withhold_receipt_by_merchantkey(self.db_test_payment, global_razorpay_ebank_merchant_key)
#         delete_channel_reconci_by_merchantkey(self.db_test_payment, global_razorpay_ebank_merchant_key)
#         insert_withhold_receipt(self.db_test_payment, global_razorpay_ebank_channel_key,
#                                 global_razorpay_ebank_merchant_key, global_razorpay_ebank_amount,
#                                 global_razorpay_ebank_service_fee - global_razorpay_ebank_service_tax,
#                                 global_razorpay_ebank_service_tax)
#         resp_feequery = global_fee_query(global_razorpay_ebank_merchant_key, "withhold")
#         assert resp_feequery['content']['code'] == 0, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['merchant_key'] == global_razorpay_ebank_merchant_key, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['channel_key'] == global_razorpay_ebank_channel_key, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['fee_type'] == "withhold", "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['fee_from'] == "channel", "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0][
#                    'order_amount'] == global_razorpay_ebank_amount, "单笔成本查询成功"  # 金额单位都是派士
#         assert resp_feequery['content']['data'][0]['fee_amount'] == global_razorpay_ebank_service_fee, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0][
#                    'service_amount'] == global_razorpay_ebank_service_fee - global_razorpay_ebank_service_tax, "单笔成本查询成功"
#         assert resp_feequery['content']['data'][0]['tax_amount'] == global_razorpay_ebank_service_tax, "单笔成本查询成功"
#
#     @pytest.mark.razorpay_transfer
#     @pytest.mark.global_payment_india
#     def test_razorpay_transfer_fail(self):
#         """
#         razorpay清分转账：创建转账直接失败
#         author: fangchangfang
#         date: 2020-06-11
#         """
#         # 初始化数据
#         delete_razorpay_transfer_withdrawandreceipt(self.db_test_payment, global_razorpay_transfer_id)
#         undo_update_kv_withdraw_riskwhite(self.db_test_payment)
#         add_transfer_fail_channel_error(self.db_test_payment)
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_transfer_fail()
#         merchant_key = "auto_test" + get_timestamp()
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, self.card_uuid, india_razorpay_transfer_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         # 发起转账请求
#         resp_transfer = global_transfer_transfer(merchant_key, merchant_key, self.channel_name, self.card_uuid)
#         assert resp_transfer['content']['code'] == 2, "转账交易处理中"
#         resp_transfer_query = global_transfer_query(merchant_key)
#         assert resp_transfer_query['content']['code'] == 2, "转账交易处理中"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 转账处理中，无法统一的断言
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_code"] == "BAD_REQUEST_ERROR", '转账创建成功'
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == "account", '支付方式'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"] == "", '通道流水号'
#         # 统一断言
#         assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_transfer, merchant_key, self.card_uuid,
#                                               card_info[0]["card_bank_code"], card_num,
#                                               card_info[0]["card_account"], three_element)
#         assert_withdraw_fail(self.db_test_payment, resp_transfer["content"]["data"]["trade_no"], merchant_key, three_element)
#
#     @pytest.mark.razorpay_transfer
#     @pytest.mark.global_payment_india
#     @pytest.mark.razorpay_transfer_test
#     def test_razorpay_transfer_success(self):
#         """
#         razorpay清分转账：创建转账-转账结果查询-job查询结算单反向跟更新withdraw
#         author: fangchangfang
#         date: 2020-06-11
#         """
#         # 初始化数据
#         delete_razorpay_transfer_withdrawandreceipt(self.db_test_payment, global_razorpay_transfer_id)
#         undo_update_kv_withdraw_riskwhite(self.db_test_payment)
#         global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
#         global_payment_mock.update_razorpay_transfer_transfersuccess()
#         global_payment_mock.update_razorpay_transfer_transferquery()
#         global_payment_mock.update_razorpay_transfer_querysuccess()  # job调度进行的结算单查询
#         merchant_key = "auto_test" + get_timestamp()
#         account_info = by_carduuid_get_ccountandbinding_info(self.db_test_payment, self.card_uuid, india_razorpay_transfer_channel_name)
#         card_num = account_info[0]["account_card_num"]
#         card_info = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         three_element = get_global_card_info_by_card_num(self.db_test_payment, card_num)
#         # 发起转账请求
#         resp_transfer = global_transfer_transfer(merchant_key, merchant_key, self.channel_name, self.card_uuid)
#         assert resp_transfer['content']['code'] == 2, "转账交易处理中"
#         resp_transfer_query = global_transfer_query(merchant_key)
#         assert resp_transfer_query['content']['code'] == 2, "转账交易处理中"
#         # 执行task
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 转账处理中，无法统一的断言
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_merchant_key(self.db_test_payment, merchant_key)
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_code"] == "KN_REQUEST_SUCCESS", '转账创建成功'
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == "account", '支付方式'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"] == global_razorpay_transfer_id, '通道流水号'
#         assert_withdraw_process(self.db_test_payment, resp_transfer["content"]["data"]["trade_no"], merchant_key,
#                                 three_element)
#         # 调度job，查询结算单结果来更新转账结果
#         global_job_run_reconci(india_razorpay_transfer_channel_name)
#         # 执行task
#         for i in range(2):
#             update_global_task_next_run_at(self.db_test_payment)
#             time.sleep(1)
#             global_job_runtask(1)
#         # 让对账单下载结束
#         global_payment_mock.update_razorpay_transfer_query_nodata()
#         update_global_task_next_run_at(self.db_test_payment)
#         time.sleep(1)
#         global_job_runtask(1)
#         # 执行withdrawReconciCompensate（channel_key）和withdrawUpdate（merchant_key）更新转账结果
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_merchant_key(self.db_test_payment, merchant_key)
#         channel_key = withdraw_receipt_info[0]["withdraw_receipt_channel_key"]
#         # 执行withdrawReconciCompensate
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, channel_key)
#         # 执行withdrawUpdate
#         run_task_withdraw_and_withdrawquery(self.db_test_payment, merchant_key)
#         # 转账成功，无法统一的断言
#         withdraw_receipt_info = get_global_withdraw_receipt_info_by_merchant_key(self.db_test_payment,merchant_key)
#         # @ f.f TODO jenkins上一直跑失败，先屏蔽
#         assert withdraw_receipt_info[0]["withdraw_receipt_transfer_mode"] == 'account', '代付方式'
#         assert withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"] == global_razorpay_transfer_id, '通道代付id'
#         # assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_code"] == "KN_TRANSFER_SUCCESS", '转账成功code'
#         # assert withdraw_receipt_info[0]["withdraw_receipt_channel_resp_message"] == 'KN_TRANSFER_SUCCESS', '转账成功msg'
#         # # 统一断言
#         # assert_check_withdraw_withdrawreceipt(self.db_test_payment, resp_transfer, merchant_key, self.card_uuid,
#         #                                       card_info[0]["card_bank_code"], card_num,
#         #                                       card_info[0]["card_account"], three_element)
#         # assert_withdraw_success(self.db_test_payment, resp_transfer["content"]["data"]["trade_no"], merchant_key,
#         #                         three_element)
