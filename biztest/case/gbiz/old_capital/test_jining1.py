# from biztest.interface.gbiz.gbiz_interface import *
# from biztest.util.task.task import Task
# from biztest.util.easymock.tongrongmiyang import TongrongmiyangMock
# from biztest.util.easymock.deposit import DepositMock
# from biztest.function.gbiz.gbiz_check_function import *
# from biztest.config.gbiz.gbiz_kv_config import *
# import pytest
#
# env = get_sysconfig("--env")
#
#
# def process_to_loan_success(task, deposit, tongrong, item_no):
#     """
#     公共函数，task运行到进件成功
#     """
#     task.run_task(item_no, "AssetImport", excepts={"code": 0})
#     task.run_task(item_no, "AssetImportVerify")
#     deposit.update_balance_enough()
#     task.run_task(item_no, "ApplyCanLoan")
#     deposit.update_member_query_success()
#     deposit.update_memeber_register_success()
#     task.run_task(item_no, "LoanPreApply")
#     tongrong.update_apply_success()
#     task.run_task(item_no, "LoanApplyNew")
#
#
# def process_to_grant_success(task, deposit, tongrong, item_no, four_element, asset_info):
#     """
#     公共函数，task运行到放款成功
#     """
#     process_to_loan_success(task, deposit, tongrong, item_no)
#
#     task.run_task(item_no, "JiningWithdrawNew")
#     deposit.update_trade_query_not_exist()
#     deposit.update_trade_loan_success()
#     task.run_task(item_no, "JiningWithdraw")
#
#     deposit.update_trade_query_success(item_no,
#                                        asset_info['data']['asset']['amount'],
#                                        four_element['data']['bank_code_encrypt'],
#                                        four_element['data']['id_number_encrypt'])
#     task.run_task(item_no, "JiningWithdrawQuery")
#     task.run_task(item_no, "LoanApplyQuery")
#
#
# def trade_query_failed_and_retry(task, deposit, item_no, asset_info, new_element, four_element):
#     task.run_task(item_no, "JiningWithdrawNew")
#
#     deposit.update_trade_query_not_exist()
#     deposit.update_trade_loan_success()
#     task.run_task(item_no, "JiningWithdraw")
#
#     deposit.update_trade_query_failed_retry(item_no,
#                                             asset_info['data']['asset']['amount'],
#                                             new_element['data']['bank_code_encrypt'],
#                                             four_element['data']['id_number_encrypt'])
#     task.run_task(item_no, "JiningWithdrawQuery")
#
#
# def trade_query_failed_other_msg(task, deposit, item_no, asset_info, new_element, four_element):
#     task.run_task(item_no, "JiningWithdrawNew")
#
#     deposit.update_trade_query_not_exist()
#     deposit.update_trade_loan_success()
#     task.run_task(item_no, "JiningWithdraw")
#
#     deposit.update_trade_query_failed_other_msg(item_no,
#                                                 asset_info['data']['asset']['amount'],
#                                                 new_element['data']['bank_code_encrypt'],
#                                                 four_element['data']['id_number_encrypt'])
#     task.run_task(item_no, "JiningWithdrawQuery")
#
#
# class TestJining1(object):
#
#     @classmethod
#     def setup_class(cls):
#         update_gbiz_silence_channel_list(["tongrongmiyang"])
#
#     @pytest.fixture()
#     def case(self):
#         update_tongrongmiyang_paydayloan("5d43957a09acc30020bb1c69")
#         update_gbiz_jining_stb_config("5dddb8bdd1784d36471d5f78")
#         pass
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.t121212
#     def test_deposit_121212(self, case):
#         """
#         JiningWithdrawQuery msg在withdraw_failed_messges中，换卡次数不超限，通知换卡，换卡后放款成功
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_loan_success(task, deposit, tongrong, item_no)
#
#         task.run_task(item_no, "JiningWithdrawNew")
#         deposit.update_trade_query_not_exist()
#         deposit.update_trade_loan_success()
#         task.run_task(item_no, "JiningWithdraw")
#
#         deposit.update_trade_query_failed_final(item_no,
#                                                 asset_info['data']['asset']['amount'],
#                                                 four_element['data']['bank_code_encrypt'],
#                                                 four_element['data']['id_number_encrypt'])
#         task.run_task(item_no, "JiningWithdrawQuery")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[当前卡交易失败，等待换卡],"
#                                                     r"当前卡代付最终失败,已通知用户换卡" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         check_change_card_data(item_no, 2, 1)
#
#         new_element = get_four_element()
#         update_receive_card(asset_info, new_element, four_element)
#         task.run_task(item_no, "UpdateCardVerify")
#         task.run_task(item_no, "UpdateCard")
#         task.run_task(item_no, "JiningWithdrawNew")
#
#         deposit.update_trade_query_not_exist()
#         deposit.update_trade_loan_success()
#         task.run_task(item_no, "JiningWithdraw")
#
#         deposit.update_trade_query_success(item_no,
#                                            asset_info['data']['asset']['amount'],
#                                            new_element['data']['bank_code_encrypt'],
#                                            four_element['data']['id_number_encrypt'])
#         task.run_task(item_no, "JiningWithdrawQuery")
#         task.run_task(item_no, "LoanApplyQuery")
#         task.run_task(item_no, "CapitalRepayPlanGenerate")
#
#         check_asset_success_data(item_no)
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test12
#     def test_deposit_12(self, case):
#         """
#         JiningWithdrawQuery msg在withdraw_failed_messges中，换卡次数超限，放款失败
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_loan_success(task, deposit, tongrong, item_no)
#
#         task.run_task(item_no, "JiningWithdrawNew")
#         deposit.update_trade_query_not_exist()
#         deposit.update_trade_loan_success()
#         task.run_task(item_no, "JiningWithdraw")
#
#         deposit.update_trade_query_failed_final(item_no,
#                                                 asset_info['data']['asset']['amount'],
#                                                 four_element['data']['bank_code_encrypt'],
#                                                 four_element['data']['id_number_encrypt'])
#         task.run_task(item_no, "JiningWithdrawQuery")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[当前卡交易失败，等待换卡],"
#                                                     r"当前卡代付最终失败,已通知用户换卡" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         check_change_card_data(item_no, 2, 1)
#
#         new_element = get_four_element()
#         update_receive_card(asset_info, new_element, four_element)
#         task.run_task(item_no, "UpdateCardVerify")
#         task.run_task(item_no, "UpdateCard")
#         task.run_task(item_no, "JiningWithdrawNew")
#         check_change_card_data(item_no, 0, 1)
#
#         deposit.update_trade_query_not_exist()
#         deposit.update_trade_loan_success()
#         task.run_task(item_no, "JiningWithdraw")
#
#         deposit.update_trade_query_failed_final(item_no,
#                                                 asset_info['data']['asset']['amount'],
#                                                 new_element['data']['bank_code_encrypt'],
#                                                 four_element['data']['id_number_encrypt'])
#         task.run_task(item_no, "JiningWithdrawQuery")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[此笔资产交易最终失败],"
#                                                     r"代付最终失败,且换卡次数[1]已经等于配置最大换卡次数[1]，不能再换" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         check_change_card_data(item_no, 3, 1)
#
#         task.run_task(item_no, "LoanApplyQuery")
#         update_task_by_item_no_task_type(item_no, "ChangeCapital", task_status="open")
#         task.run_task(item_no, "ChangeCapital")
#         update_task_by_item_no_task_type(item_no, "AssetVoid", task_status="open")
#         task.run_task(item_no, "AssetVoid", 2)
#         check_asset_void_data(item_no)
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_13(self, case):
#         """
#         JiningWithdrawQuery msg在withdraw_retry_messges中，未超过重试次数，重试
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_loan_success(task, deposit, tongrong, item_no)
#
#         trade_query_failed_and_retry(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[对手行状态异常，不能发起此交易。],"
#                                                     r"当前卡已经失败[0]次,最大重试次数[2],已创建新的代付任务,[240]分钟后执行" % item_no, "memo不正确")
#
#         trade_query_failed_and_retry(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[对手行状态异常，不能发起此交易。],"
#                                                     r"当前卡已经失败[1]次,最大重试次数[2],已创建新的代付任务,[240]分钟后执行" % item_no, "memo不正确")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_14(self, case):
#         """
#         JiningWithdrawQuery msg在withdraw_retry_messges中，超过失败最大重试次数，未超换卡次数，通知换卡
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_loan_success(task, deposit, tongrong, item_no)
#
#         trade_query_failed_and_retry(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[对手行状态异常，不能发起此交易。],"
#                                                     r"当前卡已经失败[%s]次,最大重试次数[2],已创建新的代付任务,[240]分钟后执行" %
#                             (item_no, 0), "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         trade_query_failed_and_retry(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[对手行状态异常，不能发起此交易。],"
#                                                     r"当前卡已经失败[%s]次,最大重试次数[2],已创建新的代付任务,[240]分钟后执行" %
#                             (item_no, 1), "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         trade_query_failed_and_retry(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[当前卡交易失败，等待换卡],"
#                                                     r"当前卡代付最终失败,已通知用户换卡" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         check_change_card_data(item_no, 2, 1)
#
#         new_element = get_four_element()
#         update_receive_card(asset_info, new_element, four_element)
#         task.run_task(item_no, "UpdateCardVerify")
#         task.run_task(item_no, "UpdateCard")
#         task.run_task(item_no, "JiningWithdrawNew")
#         check_change_card_data(item_no, 0, 1)
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_15(self, case):
#         """
#         JiningWithdrawQuery msg在withdraw_retry_messges中，超过失败最大重试次数，超换卡次数，放款失败
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_loan_success(task, deposit, tongrong, item_no)
#
#         trade_query_failed_and_retry(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[对手行状态异常，不能发起此交易。],"
#                                                     r"当前卡已经失败[%s]次,最大重试次数[2],已创建新的代付任务,[240]分钟后执行" %
#                             (item_no, 0), "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         trade_query_failed_and_retry(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[对手行状态异常，不能发起此交易。],"
#                                                     r"当前卡已经失败[%s]次,最大重试次数[2],已创建新的代付任务,[240]分钟后执行" %
#                             (item_no, 1), "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         trade_query_failed_and_retry(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[当前卡交易失败，等待换卡],"
#                                                     r"当前卡代付最终失败,已通知用户换卡" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         new_element = get_four_element()
#         update_receive_card(asset_info, new_element, four_element)
#         task.run_task(item_no, "UpdateCardVerify")
#         task.run_task(item_no, "UpdateCard")
#         task.run_task(item_no, "JiningWithdrawNew")
#         check_change_card_data(item_no, 0, 1)
#
#         trade_query_failed_and_retry(task, deposit, item_no, asset_info, new_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[对手行状态异常，不能发起此交易。],"
#                                                     r"当前卡已经失败[%s]次,最大重试次数[2],已创建新的代付任务,[240]分钟后执行" %
#                             (item_no, 0), "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         trade_query_failed_and_retry(task, deposit, item_no, asset_info, new_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[对手行状态异常，不能发起此交易。],"
#                                                     r"当前卡已经失败[%s]次,最大重试次数[2],已创建新的代付任务,[240]分钟后执行" %
#                             (item_no, 1), "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         trade_query_failed_and_retry(task, deposit, item_no, asset_info, new_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:"
#                                                     r"[此笔资产交易最终失败],代付最终失败,且换卡次数[1]已经等于配置最大换卡次数[1]，"
#                                                     r"不能再换" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         task.run_task(item_no, "LoanApplyQuery")
#         update_task_by_item_no_task_type(item_no, "ChangeCapital", task_status="open")
#         task.run_task(item_no, "ChangeCapital")
#         update_task_by_item_no_task_type(item_no, "AssetVoid", task_status="open")
#         task.run_task(item_no, "AssetVoid", 2)
#         check_asset_void_data(item_no)
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_16(self, case):
#         """
#         JiningWithdrawQuery msg不在配置中，未超过失败次数，创建JiningWithdrawNew状态未终止
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_loan_success(task, deposit, tongrong, item_no)
#
#         trade_query_failed_other_msg(task, deposit, item_no, asset_info, four_element, four_element)
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[test1234],已创建手工代付任务,"
#                                                     r"需人工确认memo处理下次代付" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawNew")
#         Assert.assert_equal(task_info["task_status"], "terminated", "task状态不正确")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_17(self, case):
#         """
#         JiningWithdrawQuery msg不在配置中，超过失败最大重试次数，未超过换卡次数，通知换卡
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_loan_success(task, deposit, tongrong, item_no)
#
#         trade_query_failed_other_msg(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[test1234],已创建手工代付任务,"
#                                                     r"需人工确认memo处理下次代付" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawNew")
#         Assert.assert_equal(task_info["task_status"], "terminated", "task状态不正确")
#         update_last_task_by_item_no_task_type(item_no, "JiningWithdrawNew", task_status="open")
#
#         trade_query_failed_other_msg(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[test1234],已创建手工代付任务,"
#                                                     r"需人工确认memo处理下次代付" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawNew")
#         Assert.assert_equal(task_info["task_status"], "terminated", "task状态不正确")
#         update_last_task_by_item_no_task_type(item_no, "JiningWithdrawNew", task_status="open")
#
#         trade_query_failed_other_msg(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[当前卡交易失败，等待换卡],"
#                                                     r"当前卡代付最终失败,已通知用户换卡" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         check_change_card_data(item_no, 2, 1)
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_18(self, case):
#         """
#         JiningWithdrawQuery msg不在配置中，超过失败最大重试次数，超过换卡次数，放款失败
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_loan_success(task, deposit, tongrong, item_no)
#
#         trade_query_failed_other_msg(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[test1234],已创建手工代付任务,"
#                                                     r"需人工确认memo处理下次代付" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawNew")
#         Assert.assert_equal(task_info["task_status"], "terminated", "task状态不正确")
#         update_last_task_by_item_no_task_type(item_no, "JiningWithdrawNew", task_status="open")
#
#         trade_query_failed_other_msg(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[test1234],已创建手工代付任务,"
#                                                     r"需人工确认memo处理下次代付" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawNew")
#         Assert.assert_equal(task_info["task_status"], "terminated", "task状态不正确")
#         update_last_task_by_item_no_task_type(item_no, "JiningWithdrawNew", task_status="open")
#
#         trade_query_failed_other_msg(task, deposit, item_no, asset_info, four_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[当前卡交易失败，等待换卡],"
#                                                     r"当前卡代付最终失败,已通知用户换卡" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         check_change_card_data(item_no, 2, 1)
#
#         new_element = get_four_element()
#         update_receive_card(asset_info, new_element, four_element)
#         task.run_task(item_no, "UpdateCardVerify")
#         task.run_task(item_no, "UpdateCard")
#         task.run_task(item_no, "JiningWithdrawNew")
#         check_change_card_data(item_no, 0, 1)
#
#         trade_query_failed_other_msg(task, deposit, item_no, asset_info, new_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[test1234],已创建手工代付任务,"
#                                                     r"需人工确认memo处理下次代付" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawNew")
#         Assert.assert_equal(task_info["task_status"], "terminated", "task状态不正确")
#         update_last_task_by_item_no_task_type(item_no, "JiningWithdrawNew", task_status="open")
#
#         trade_query_failed_other_msg(task, deposit, item_no, asset_info, new_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[test1234],已创建手工代付任务,"
#                                                     r"需人工确认memo处理下次代付" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawNew")
#         Assert.assert_equal(task_info["task_status"], "terminated", "task状态不正确")
#         update_last_task_by_item_no_task_type(item_no, "JiningWithdrawNew", task_status="open")
#
#         trade_query_failed_other_msg(task, deposit, item_no, asset_info, new_element, four_element)
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[此笔资产交易最终失败],代付最终失败,"
#                                                     r"且换卡次数[1]已经等于配置最大换卡次数[1]，不能再换" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         check_change_card_data(item_no, 3, 1)
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test13
#     def test_deposit_19(self, case):
#         """
#         JiningTransfer code!=0 重试
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_grant_success(task, deposit, tongrong, item_no, four_element, asset_info)
#
#         deposit.update_transfer_failed()
#         task.run_task(item_no, "JiningTransfer")
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningTransfer")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],转账任务未成功" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "open", "task状态不正确")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_20(self, case):
#         """
#         JiningTransfer code=0 生成JiningTransferQuery
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_grant_success(task, deposit, tongrong, item_no, four_element, asset_info)
#
#         deposit.update_transfer_success()
#         task.run_task(item_no, "JiningTransfer")
#         deposit.update_transfer_query_success()
#         task.run_task(item_no, "JiningTransferQuery")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningTransfer")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningTransferQuery")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_21(self, case):
#         """
#         JiningTransferQuery code=0&status=1 or 6 重试
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_grant_success(task, deposit, tongrong, item_no, four_element, asset_info)
#
#         deposit.update_transfer_success()
#         task.run_task(item_no, "JiningTransfer")
#         deposit.update_transfer_query_failed_retry()
#         task.run_task(item_no, "JiningTransferQuery")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningTransferQuery")
#         Assert.assert_match(task_info["task_memo"], r"资产\[%s\]济宁转账查询接口返回状态\[1\]不为成功.*" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "open", "task状态不正确")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_22(self, case):
#         """
#         JiningTransferQuery code=0&status=3 创建新的JiningTransfer
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_grant_success(task, deposit, tongrong, item_no, four_element, asset_info)
#
#         deposit.update_transfer_success()
#         task.run_task(item_no, "JiningTransfer")
#         deposit.update_transfer_query_failed()
#         task.run_task(item_no, "JiningTransferQuery")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningTransferQuery")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningTransfer", 1)
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningTransfer")
#         Assert.assert_equal(task_info["task_status"], "open", "task状态不正确")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.deposit23
#     def test_deposit_23(self, case):
#         """
#         济宁放款成功，全部接口正常
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 2500)
#         process_to_grant_success(task, deposit, tongrong, item_no, four_element, asset_info)
#
#         deposit.update_transfer_success()
#         task.run_task(item_no, "JiningTransfer")
#         deposit.update_transfer_query_success()
#         task.run_task(item_no, "JiningTransferQuery")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningTransfer")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningTransferQuery")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#
# if __name__ == "__main__":
#     pytest.main(["-s", "/Users/fenlai/code/framework-test/biztest/case/gbiz/jining.py", "--env=9" "--junt"])
