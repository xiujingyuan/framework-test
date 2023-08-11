# from biztest.function.biz.biz_db_function import set_capital_loan_condition
# from biztest.interface.gbiz.gbiz_interface import *
# from biztest.util.task.task import Task
# from biztest.util.msg.msg import Msg
# from biztest.util.easymock.tongrongmiyang import TongrongmiyangMock
# from biztest.util.easymock.deposit import DepositMock
# from biztest.function.gbiz.gbiz_check_function import *
# from biztest.config.gbiz.gbiz_kv_config import *
# import pytest
#
# env = get_sysconfig("--env")
#
#
# class TestJining(object):
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
#     @pytest.mark.test10
#     def test_deposit_1(self, case):
#         """
#         开户失败，超过最大次数后，资产做废
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         msg = Msg("gbiz%s" % env)
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 3000)
#         task.run_task(item_no, "AssetImport", excepts={"code": 0})
#         msg.run_msg_by_order_no(item_no)
#         task.run_task(item_no, "AssetImportVerify")
#         deposit.update_balance_enough()
#         task.run_task(item_no, "ApplyCanLoan")
#
#         deposit.update_member_query_no_member()
#         deposit.update_memeber_register_success()
#         task.run_task(item_no, "LoanPreApply")
#
#         deposit.update_member_query_fail()
#         task.run_task(item_no, "LoanPreApply")
#         task.run_task(item_no, "LoanPreApply")
#         task.run_task(item_no, "LoanPreApply")
#         update_task_by_item_no_task_type(item_no, "ChangeCapital", task_status="open")
#         task.run_task(item_no, "ChangeCapital")
#         update_task_by_item_no_task_type(item_no, "AssetVoid", task_status="open")
#         task.run_task(item_no, "AssetVoid", 2)
#         msg.run_msg_by_order_no(item_no)
#         check_asset_void_data(item_no)
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_2(self, case):
#         """
#         JiningWithdrawNew 额度不足时延迟执行
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 3000)
#         task.run_task(item_no, "AssetImport", excepts={"code": 0})
#         task.run_task(item_no, "AssetImportVerify")
#
#         deposit.update_balance_enough()
#         task.run_task(item_no, "ApplyCanLoan")
#
#         deposit.update_member_query_success()
#         deposit.update_memeber_register_success()
#         task.run_task(item_no, "LoanPreApply")
#
#         tongrong.update_apply_success()
#         task.run_task(item_no, "LoanApplyNew")
#         deposit.update_balance_not_enough()
#         task.run_task(item_no, "JiningWithdrawNew")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawNew")
#         Assert.assert_match(task_info['task_memo'], r"资产\[.*\],查询到\[.*\]可用余额\[.*元\],已小于预警值\[.*\],延迟代付", 'msg匹配')
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdraw")
#         Assert.assert_equal(task_info, None, "task不应该有")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_3(self, case):
#         """
#         JiningWithdrawNew 12小时内存在代付失败记录，task创建后，状态为终止
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 3000)
#         task.run_task(item_no, "AssetImport", excepts={"code": 0})
#         task.run_task(item_no, "AssetImportVerify")
#
#         deposit.update_balance_enough()
#         task.run_task(item_no, "ApplyCanLoan")
#
#         deposit.update_member_query_success()
#         deposit.update_memeber_register_success()
#         task.run_task(item_no, "LoanPreApply")
#
#         tongrong.update_apply_success()
#         task.run_task(item_no, "LoanApplyNew")
#
#         insert_withdraw(item_no, four_element)
#         task.run_task(item_no, "JiningWithdrawNew")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_4(self, case):
#         """
#         JiningWithdraw 查到交易处理中or成功or失败，直接创建JiningWithdrawQury
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 3000)
#         task.run_task(item_no, "AssetImport", excepts={"code": 0})
#         task.run_task(item_no, "AssetImportVerify")
#
#         deposit.update_balance_enough()
#         task.run_task(item_no, "ApplyCanLoan")
#
#         deposit.update_member_query_success()
#         deposit.update_memeber_register_success()
#         task.run_task(item_no, "LoanPreApply")
#
#         tongrong.update_apply_success()
#         task.run_task(item_no, "LoanApplyNew")
#         task.run_task(item_no, "JiningWithdrawNew")
#
#         deposit.update_trade_query_not_exist()
#         deposit.update_trade_loan_fail()
#         task.run_task(item_no, "JiningWithdraw")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdraw")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],merchant_key[%s_JN1],济宁存管代付放款返回code[1],"
#                                                     r"message[四要素验证不通过]" % (item_no, item_no), "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "open", "task状态不正确")
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info, None, "task不应该有")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_5(self, case):
#         """
#         JiningWithdraw 查到交易处理中or成功or失败，直接创建JiningWithdrawQury
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 3000)
#         task.run_task(item_no, "AssetImport", excepts={"code": 0})
#         task.run_task(item_no, "AssetImportVerify")
#
#         deposit.update_balance_enough()
#         task.run_task(item_no, "ApplyCanLoan")
#
#         deposit.update_member_query_success()
#         deposit.update_memeber_register_success()
#         task.run_task(item_no, "LoanPreApply")
#
#         tongrong.update_apply_success()
#         task.run_task(item_no, "LoanApplyNew")
#         task.run_task(item_no, "JiningWithdrawNew")
#
#         deposit.update_trade_query_process()
#         deposit.update_trade_loan_fail()
#         task.run_task(item_no, "JiningWithdraw")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdraw")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],已代付成功或者处理中,直接创建代付查询任务" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_status"], "open", "task状态不正确")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_6(self, case):
#         """
#         JiningWithdraw 放款申请返回疑似风险交易，任务关闭，创建JiningWithdrawNew，状态为终止
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 3000)
#         task.run_task(item_no, "AssetImport", excepts={"code": 0})
#         task.run_task(item_no, "AssetImportVerify")
#
#         deposit.update_balance_enough()
#         task.run_task(item_no, "ApplyCanLoan")
#
#         deposit.update_member_query_success()
#         deposit.update_memeber_register_success()
#         task.run_task(item_no, "LoanPreApply")
#
#         tongrong.update_apply_success()
#         task.run_task(item_no, "LoanApplyNew")
#         task.run_task(item_no, "JiningWithdrawNew")
#
#         deposit.update_trade_query_not_exist()
#         deposit.update_trade_loan_risk_trade()
#         task.run_task(item_no, "JiningWithdraw")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdraw")
#         Assert.assert_equal(task_info["task_memo"], r"济宁存管资产[%s],由于：疑似风险交易,已重新创建中断代付任务,"
#                                                     r"需人工处理,code:[1]" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawNew")
#         Assert.assert_equal(task_info["task_status"], "terminated", "task状态不正确")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_7(self, case):
#         """
#         JiningWithdrawQuery code=1or2or其他，重试
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 3000)
#         task.run_task(item_no, "AssetImport", excepts={"code": 0})
#         task.run_task(item_no, "AssetImportVerify")
#
#         deposit.update_balance_enough()
#         task.run_task(item_no, "ApplyCanLoan")
#
#         deposit.update_member_query_success()
#         deposit.update_memeber_register_success()
#         task.run_task(item_no, "LoanPreApply")
#
#         tongrong.update_apply_success()
#         task.run_task(item_no, "LoanApplyNew")
#         task.run_task(item_no, "JiningWithdrawNew")
#
#         deposit.update_trade_query_not_exist()
#         deposit.update_trade_loan_success()
#         task.run_task(item_no, "JiningWithdraw")
#
#         deposit.update_trade_query_error_code()
#         task.run_task(item_no, "JiningWithdrawQuery")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_match(task_info["task_memo"], r"资产\[%s\],merchant_key\[%s_JN1\],济宁存管代付放款查询返回code\[(1|2)\],"
#                                                     r"message\[交易中\]" % (item_no, item_no), "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "open", "task状态不正确")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_8(self, case):
#         """
#         JiningWithdrawQuery code=0&status=2，四要素不一致，重试
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 3000)
#         task.run_task(item_no, "AssetImport", excepts={"code": 0})
#         task.run_task(item_no, "AssetImportVerify")
#
#         deposit.update_balance_enough()
#         task.run_task(item_no, "ApplyCanLoan")
#
#         deposit.update_member_query_success()
#         deposit.update_memeber_register_success()
#         task.run_task(item_no, "LoanPreApply")
#
#         tongrong.update_apply_success()
#         task.run_task(item_no, "LoanApplyNew")
#         task.run_task(item_no, "JiningWithdrawNew")
#
#         deposit.update_trade_query_not_exist()
#         deposit.update_trade_loan_success()
#         task.run_task(item_no, "JiningWithdraw")
#
#         four_element2 = get_four_element()
#         deposit.update_trade_query_success(item_no,
#                                            asset_info['data']['asset']['amount'],
#                                            four_element2['data']['bank_code_encrypt'],
#                                            four_element['data']['id_number_encrypt'])
#         task.run_task(item_no, "JiningWithdrawQuery")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_match(task_info["task_memo"], r"济宁存管资产\[%s\],返回mem_acct_no\[.*\]与我方"
#                                                     r"account_card_number_encrypt\[.*\]不匹配" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "open", "task状态不正确")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_9(self, case):
#         """
#         JiningWithdrawQuery code=0&status=3，msg在withdraw_terminate_messges中，创建JiningWithdrawNew状态未终止
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 3000)
#         task.run_task(item_no, "AssetImport", excepts={"code": 0})
#         task.run_task(item_no, "AssetImportVerify")
#
#         deposit.update_balance_enough()
#         task.run_task(item_no, "ApplyCanLoan")
#
#         deposit.update_member_query_success()
#         deposit.update_memeber_register_success()
#         task.run_task(item_no, "LoanPreApply")
#
#         tongrong.update_apply_success()
#         task.run_task(item_no, "LoanApplyNew")
#         task.run_task(item_no, "JiningWithdrawNew")
#
#         deposit.update_trade_query_not_exist()
#         deposit.update_trade_loan_success()
#         task.run_task(item_no, "JiningWithdraw")
#
#         deposit.update_trade_query_failed_terminate(four_element)
#         task.run_task(item_no, "JiningWithdrawQuery")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[疑似风险交易],已创建手工代付任务,"
#                                                     r"需人工确认memo处理下次代付" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawNew")
#         Assert.assert_equal(task_info["task_status"], "terminated", "task状态不正确")
#
#
#     @pytest.mark.gbiz_jining
#     @pytest.mark.test11
#     def test_deposit_10(self, case):
#         """
#         JiningWithdrawQuery msg在delay_withdraw_messges中，创建JiningWithdrawNew，延迟执行
#         :param case:
#         :return:
#         """
#         task = Task("gbiz%s" % env)
#         tongrong = TongrongmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
#         deposit = DepositMock('carltonliu', 'lx19891115', '5dddb8bdd1784d36471d5f78')
#         four_element = get_four_element()
#         item_no, asset_info = asset_import("tongrongmiyang", four_element, 6, 3000)
#         task.run_task(item_no, "AssetImport", excepts={"code": 0})
#         task.run_task(item_no, "AssetImportVerify")
#
#         deposit.update_balance_enough()
#         task.run_task(item_no, "ApplyCanLoan")
#
#         deposit.update_member_query_success()
#         deposit.update_memeber_register_success()
#         task.run_task(item_no, "LoanPreApply")
#
#         tongrong.update_apply_success()
#         task.run_task(item_no, "LoanApplyNew")
#         task.run_task(item_no, "JiningWithdrawNew")
#
#         deposit.update_trade_query_not_exist()
#         deposit.update_trade_loan_success()
#         task.run_task(item_no, "JiningWithdraw")
#
#         deposit.update_trade_query_failed_delay(four_element)
#         task.run_task(item_no, "JiningWithdrawQuery")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawQuery")
#         Assert.assert_equal(task_info["task_memo"], r"资产[%s],代付状态返回status:[3],memo:[账户可提现余额不足],"
#                                                     r"延迟2小时创建下次代付" % item_no, "memo不正确")
#         Assert.assert_equal(task_info["task_status"], "close", "task状态不正确")
#
#         task_info = get_task_by_item_no_and_task_type(item_no, "JiningWithdrawNew")
#         Assert.assert_equal(task_info["task_status"], "open", "task状态不正确")
#
#
# if __name__ == "__main__":
#     pytest.main(["-s", "/Users/fenlai/code/framework-test/biztest/case/gbiz/jining.py", "--env=9" "--junt"])
