# -*- coding: utf-8 -*-
import json

import pytest

from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config
from biztest.function.rbiz.rbiz_check_function import check_withhold_split_count_by_request_no, \
    check_withhold_result_without_split, check_account_recharge_and_repay, check_asset_tran_repay_one_period, \
    check_task_by_order_no_and_type, check_asset_tran_payoff, check_withhold_sign_company, \
    check_withhold_split_count_by_item_no_and_request_no, check_json_rs_data, check_withhold_by_serial_no, \
    check_withhold_data_by_sn, check_settle_payoff_capital_withhold_detail_vs_asset_tran, check_card_by_item_no, \
    check_card_by_card_no, check_individual_by_item_no
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    get_asset_info_by_item_no, get_withhold_by_item_no, wait_expect_task_appear, get_withhold_by_serial_no, \
    get_withhold_order_by_item_no, get_task_by_order_no_and_task_type
from biztest.interface.rbiz.rbiz_interface import mozhi_beiyin_callback, \
    combo_active_repay_without_no_loan, run_withholdAutoV1_by_api, monitor_check, paysvr_callback
from biztest.util.easymock.rbiz.mozhi_jinmeixin import RepayMozhiJinmeixinMock
from biztest.util.easymock.rbiz.paysvr import PaysvrMock
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.util.tools.tools import get_four_element
import common.global_const as gc


class TestRbizMozhiJinmeixin(BaseRepayTest):
    """
    mozhi_jinmeixin 还款

    """
    loan_channel = "mozhi_jinmeixin"
    grant_principal = 600000
    first_period_interest = 15541  # 第一期息费
    exp_sign_company = "tq,tqa,tqb"
    exp_sign_company_no_loan = "tq,tqa,tqb"

    @classmethod
    def setup_class(cls):
        monitor_check()
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        cls.paysvr_mock = PaysvrMock(rbiz_mock)
        cls.beiyin_mock = RepayMozhiJinmeixinMock(rbiz_mock)
        cls.task = Task("rbiz{0}".format(gc.ENV))
        cls.msg = Msg("rbiz{0}".format(gc.ENV))

    def setup_method(self):
        # 在每个脚本执行之前，初始化限制配置
        # mock代扣成功
        self.paysvr_mock.update_query_protocol_channels_bind_sms()
        self.paysvr_mock.update_auto_pay_withhold_process()
        self.paysvr_mock.update_withhold_query(2)
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element,
                                                                               asset_amount=6000)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzjmx
    def test_active_advance_repay(self):
        """
        提前还1期
        """
        # step 1 主动还款
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest)
        self.beiyin_mock.update_repay_result(int(asset_tran_amount["asset_tran_balance_amount"]), due_bill_no)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan, code=0)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 2 数据检查，
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        param_loan = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel,
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzjmx
    def test_active_normal_repay(self):
        """
        正常还款1期
        """
        # step 1 主动还款
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest)
        self.beiyin_mock.update_repay_result(int(asset_tran_amount["asset_tran_balance_amount"]), due_bill_no)

        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 2 数据检查，大单1单小单1单，都走我方代扣
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        param_loan = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel,
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzjmx
    def test_overdue_repay(self):
        """
        逾期还1期
        """
        # step 1 主动还款
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_capital_plan(due_bill_no)
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest,
                                           late_interest=150)

        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.beiyin_mock.update_repay_result(int(asset_tran_amount["asset_tran_balance_amount"]), due_bill_no)

        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 2 逾期数据检查，大单1单小单1单，都走我方代扣
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        param_loan = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel,
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzjmx
    def test_overdue_fail_not_switch_to_our(self):
        """
        逾期还1期 代扣失败后不切我方  仍走资方代扣
        """
        # step 1 主动还款
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_capital_plan(due_bill_no)
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest,
                                           late_interest=150)

        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.beiyin_mock.update_repay_result(int(asset_tran_amount["asset_tran_balance_amount"]), due_bill_no, "",
                                             'FAIL')
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        # step 4 数据检查
        order_no_no_loan = repay_resp["data"]["project_list"][1]["order_no"]
        order_no = repay_resp["data"]["project_list"][0]["order_no"]

        check_withhold_data_by_sn(order_no, withhold_status='fail',
                                  withhold_amount=int(asset_tran_amount["asset_tran_balance_amount"]),
                                  withhold_channel=self.loan_channel)
        check_withhold_data_by_sn(order_no_no_loan, withhold_status='cancel',
                                  withhold_amount=int(asset_tran_amount_no_loan["asset_tran_balance_amount"]))
        # 第2次代扣  1期
        # 发起主动代扣
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_capital_plan(due_bill_no)
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest,
                                           late_interest=150)
        repay_resp_two = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_no_two = repay_resp_two["data"]["project_list"][0]["order_no"]
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        check_withhold_data_by_sn(order_no_two, withhold_status='fail',
                                  withhold_amount=int(asset_tran_amount["asset_tran_balance_amount"]),
                                  withhold_channel=self.loan_channel)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzjmx
    def test_auto_normal_repay(self):
        # step 1 发起自动代扣
        self.change_asset_due_at(-1, 0)
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest)

        run_withholdAutoV1_by_api(self.item_no, self.loan_channel)
        wait_expect_task_appear(self.item_no, 'auto_withhold_execute')
        check_task_by_order_no_and_type(self.item_no, 'auto_withhold_execute', task_status='open')
        self.task.run_task(self.item_no, 'auto_withhold_execute')
        self.get_auto_withhold_execute_task_run(self.item_no)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        self.beiyin_mock.update_repay_result(int(asset_tran_amount["asset_tran_balance_amount"]), due_bill_no)
        self.run_all_task_after_repay_success()

        # step 2 数据检查
        withhold = get_withhold_by_item_no(self.item_no)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 1)
        param_loan = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel,
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzjmx
    def test_active_advance_settle_payoff(self):
        """
        提前结清走我方
        """
        self.change_asset_due_at(0, -10)
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_trail(self.grant_principal, 1000)
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, 1000)
        self.beiyin_mock.update_repay_result(self.grant_principal + 1000, due_bill_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        # step 2 数据检查
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        order_no_capital = resp_repay["data"]["project_list"][0]["order_no"]
        order_no_our = resp_repay["data"]["project_list"][1]["order_no"]
        # 拆单代扣
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, None)
        #  还1期的金额，withhold_detail里面的3个金额是一样的
        capital_withhold = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": self.grant_principal + 1000,
            "asset_tran_amount": 612000
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        check_settle_payoff_capital_withhold_detail_vs_asset_tran(order_no_capital, 1000)
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(
                asset_tran_amount["asset_tran_balance_amount"]) - self.grant_principal - 1000,
            "asset_tran_amount": 123324
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzjmx
    def test_active_normal_settle_payoff(self):
        """
        到期日提前结清
        """
        self.change_asset_due_at(-1, 0)
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_trail(self.grant_principal, 12000)  # 第一期利息12000
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest)
        self.beiyin_mock.update_repay_result(self.grant_principal + self.first_period_interest, due_bill_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        # step 2 数据检查
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        order_no_capital = resp_repay["data"]["project_list"][0]["order_no"]
        order_no_our = resp_repay["data"]["project_list"][1]["order_no"]
        # 拆单代扣
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, None)
        #  还1期的金额，withhold_detail里面的3个金额是一样的
        capital_withhold = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": self.grant_principal + self.first_period_interest,
            "asset_tran_amount": 623105
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(
                asset_tran_amount["asset_tran_balance_amount"]) - self.grant_principal - self.first_period_interest,
            "asset_tran_amount": 111324
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'], 1)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzjmx
    def test_active_overdue_one_day_settle_payoff(self):
        """
        逾期第1天提前结清
        """
        self.change_asset_due_at(-1, -1)
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_capital_plan(due_bill_no)
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest,
                                           late_interest=150)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount_one = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        self.beiyin_mock.update_repay_result(int(asset_tran_amount_one["asset_tran_balance_amount"]), due_bill_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        order_no_loan_one = resp_repay["data"]["project_list"][0]["order_no"]
        order_no_no_loan = resp_repay["data"]["project_list"][1]["order_no"]
        # 大单只扣了第1期，都给金美信扣
        check_withhold_data_by_sn(order_no_loan_one, withhold_status='success',
                                  withhold_amount=int(asset_tran_amount_one["asset_tran_balance_amount"]),
                                  withhold_channel=self.loan_channel)
        # 小单全扣了
        check_withhold_data_by_sn(order_no_no_loan, withhold_status='success',
                                  withhold_amount=int(asset_tran_amount_no_loan["asset_tran_balance_amount"]))
        # 第2次代扣  2-12期
        from_sec_principal = 555264
        sec_fees = 11105
        self.beiyin_mock.update_repay_list(due_bill_no, from_sec_principal, sec_fees, term=2, status='PRE_REPAY')
        self.beiyin_mock.update_repay_trail(from_sec_principal, 1000)  # 试算利息为1000
        self.beiyin_mock.update_repay_result(from_sec_principal + sec_fees, due_bill_no)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        # 发起主动代扣
        params_combo_active = {
            "card_num_encrypt": self.four_element['data']["bank_code_encrypt"],
            "card_user_id_encrypt": self.four_element['data']["id_number_encrypt"],
            "card_user_name_encrypt": self.four_element['data']["user_name_encrypt"],
            "card_user_phone_encrypt": self.four_element['data']["phone_number_encrypt"],
            "project_num_loan_channel": self.item_no,
            "project_num_loan_channel_priority": 1,
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = combo_active_repay_without_no_loan(**params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active}"
        check_json_rs_data(resp_combo_active['content'], code=0, message="交易处理中")
        self.run_all_task_after_repay_success()
        order_no_capital = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        order_no_our = resp_combo_active['content']["data"]["project_list"][1]["order_no"]
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, None)
        #  还1期的金额，withhold_detail里面的3个金额是一样的
        capital_withhold = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": from_sec_principal + sec_fees,
            "asset_tran_amount": 566369
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(
                asset_tran_amount["asset_tran_balance_amount"]) - from_sec_principal - sec_fees,
            "asset_tran_amount": 96678
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        # 检查充值还款
        withhold_capital = get_withhold_by_serial_no(order_no_capital)
        withhold_our = get_withhold_by_serial_no(order_no_our)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_capital[0]['withhold_channel_key'], 2)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_our[0]['withhold_channel_key'], 2)
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzjmx
    def test_auto_normal_retry(self):
        """
        自动代扣- 重试
        """

        card_1, tel1 = self.add_a_card()
        card_2, tel2 = self.add_a_card()

        # step 1 修改资产到期日
        self.change_asset_due_at(-1, -1)

        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest,
                                           late_interest=150)

        # step 2 发起自动代扣
        run_withholdAutoV1_by_api(self.item_no)
        self.task.wait_task_appear(self.item_no, 'auto_withhold_execute')
        self.task.run_task(self.item_no, 'auto_withhold_execute')
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        self.beiyin_mock.update_repay_result(int(asset_tran_amount["asset_tran_balance_amount"]), due_bill_no,
                                             pay_status="FAIL")
        self.get_auto_withhold_execute_task_run(self.item_no, 2)
        # 轮询card 1 TODO
        # task_withhold_retry_card = json.loads(
        #     get_task_by_order_no_and_task_type(self.item_no, 'withhold_retry_execute', 'open')[0]['task_request_data'])[
        #     'data'][
        #     'cardNo']
        # check_card_by_card_no(task_withhold_retry_card, card_acc_num_encrypt=card_1)

