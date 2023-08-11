#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.function.global_gbiz.gbiz_global_db_function import get_asset_import_data_by_item_no
from biztest.util.easymock.payment_global import PaymentGlobalMock
from biztest.util.msgsender.msgsender import Msgsender
from biztest.util.task.task import TaskGlobal
from biztest.config.global_gbiz.global_gbiz_kv_config import *
from biztest.function.global_gbiz.gbiz_global_common_function import init_capital_plan
from biztest.interface.gbiz_global.gbiz_global_interface import asset_import, payment_callback, asset_cancel, \
    grant_at_update
from biztest.util.db.db_util import DataBase
from biztest.util.tools.tools import get_four_element_global
from biztest.config.easymock.easymock_config import global_gbiz_mock
from biztest.function.global_gbiz.gbiz_global_check_function import *


class BaseTestCapital(object):
    def init(self):
        self.task = TaskGlobal()
        self.msgsender = Msgsender("gbiz")
        self.mock = PaymentGlobalMock(global_gbiz_mock)
        self.paymentmock = PaymentGlobalMock(global_gbiz_mock)
        update_gbiz_payment_config(self.paymentmock.url)

    def asset_import_data(self):
        case_list = []
        city = gc.COUNTRY
        init_capital_plan(city)
        for channel_data in global_gbiz_common_config.capital_plan[city]:
            case_list.append(channel_data)
        if city == 'thailand':
            element = get_four_element_global(id_num_begin='110')
        else:
            element = get_four_element_global()
        channel_name = case_list[0].get('channel')
        update_gbiz_capital_channel(channel_name)
        from_system = case_list[0].get('from_system')
        from_app = case_list[0].get('from_app')
        source_type = case_list[0].get('source_type')
        withdraw_type = case_list[0].get('withdraw_type')
        rlue_code = case_list[0].get('rule_code')
        fees = case_list[0].get('fees')
        late_num = case_list[0].get('late_num')
        item_no, asset_info = asset_import(channel_name, 1, 7, "day", 500000, from_system, from_app, source_type,
                                           element, withdraw_type, rlue_code=rlue_code, fees=fees, late_num=late_num)
        return item_no, asset_info

    @classmethod
    def teardown_method(cls):
        update_gbiz_payment_config()
        DataBase.close_connects()

    def loan_to_success(self, item_no, finish_at=None):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})

        self.paymentmock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        self.paymentmock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})

        self.paymentmock.update_withdraw_query_status(asset_info, "success", "success", finish_at=finish_at)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalDataNotify", excepts={"code": 0})
        self.task.run_task(item_no, "GrantSuccessNotify", excepts={"code": 0})
        self.msgsender.run_msg_by_order_no(item_no)

    def loan_to_success_offline(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})

        self.paymentmock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        self.paymentmock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})

        self.paymentmock.update_phl_offline_withdraw_query_status(asset_info, "process", "process")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        payment_callback(asset_info, 2)
        # 只要付款码和上次是一样的，就可以顺利走下去
        self.paymentmock.update_withdraw_query_status(asset_info, "success", "success")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalDataNotify", excepts={"code": 0})
        self.task.run_task(item_no, "GrantSuccessNotify", excepts={"code": 0})
        self.msgsender.run_msg_by_order_no(item_no)

    def noloan_to_success(self, item_no_noloan):
        self.task.run_task(item_no_noloan, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no_noloan, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no_noloan, "RefreshNoLoan", excepts={"code": 0})
        self.msgsender.run_msg_by_order_no(item_no_noloan)

    def loan_to_fail(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})

        self.paymentmock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        self.paymentmock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})

        self.paymentmock.update_withdraw_query_status(asset_info, "fail", "fail", False, "KN_INVALID_ACCOUNT")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.msgsender.run_msg_by_order_no(item_no)

    def before_update_card_process(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        self.paymentmock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.paymentmock.update_withdraw_query_status(asset_info, "fail", "fail", platform_code="KN_INVALID_ACCOUNT",
                                                      platform_message="Invalid account, please check it")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})

    def process_to_withdraw(self, item_no):
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.mock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})

    def loan_cancel_01(self, item_no):
        """0/1/5状态直接取消,"""
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        resp = asset_cancel(item_no)
        Assert.assert_equal(0, resp['code'], "接口异常")
        Assert.assert_equal("取消成功", resp['message'], "接口异常")
        check_asset_event_exist(item_no, "USER_CANCEL_EVENT_TYPE")
        check_asset_loan_record(item_no, asset_loan_record_status=5, asset_loan_record_memo="用户取消")
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        check_global_wait_assetvoid_data(item_no, 16, "用户取消")

    def loan_cancel_02(self, item_no):
        """3状态取消，后续任务不允许取消"""
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 发起取消
        resp = asset_cancel(item_no)
        Assert.assert_equal(0, resp['code'], "接口异常")
        Assert.assert_equal("资产取消拦截中，请稍后查看", resp['message'], "接口异常")
        check_asset_event_exist(item_no, "USER_CANCEL_EVENT_TYPE")
        # LoanApplyQuery不可取消，继续放款流程
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_asset_loan_record(item_no, asset_loan_record_status=3)

    def loan_cancel_03(self, item_no):
        """3状态取消，被后续任务拦截，取消成功"""
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 发起取消
        resp = asset_cancel(item_no)
        Assert.assert_equal(0, resp['code'], "接口异常")
        Assert.assert_equal("资产取消拦截中，请稍后查看", resp['message'], "接口异常")
        check_asset_event_exist(item_no, "USER_CANCEL_EVENT_TYPE")
        # LoanApplyQuery可取消，拦截执行，取消成功
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_asset_loan_record(item_no, asset_loan_record_status=5, asset_loan_record_memo="用户取消")
        check_global_wait_assetvoid_data(item_no, 16, "用户取消")

    def grant_at_update(self, asset_info, new_grant_at):
        grant_at_update(asset_info, new_grant_at)
        item_no = asset_info['data']['asset']['item_no']
        self.task.run_task_by_order_no(item_no)
        self.task.run_task_by_order_no(item_no)
        self.task.run_task_by_order_no(item_no)
        self.msgsender.run_msg_by_order_no(item_no)
