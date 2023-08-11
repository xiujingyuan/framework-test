# -*- coding: utf-8 -*-
import pytest
import datetime

from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.easymock.easymock_config import rbiz_mock
from biztest.function.rbiz.rbiz_check_function import check_withhold_split_count_by_request_no, \
    check_withhold_result_without_split, check_account_recharge_and_repay, check_asset_tran_repay_one_period, \
    check_task_by_order_no_and_type, check_asset_tran_payoff, check_withhold_sign_company, \
    check_withhold_split_count_by_item_no_and_request_no, check_json_rs_data, check_withhold_by_serial_no, \
    check_withhold_data_by_sn
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    get_asset_info_by_item_no, get_withhold_by_item_no, wait_expect_task_appear
from biztest.interface.rbiz.rbiz_interface import mozhi_withhold_apply, mozhi_withhold_query, mozhi_beiyin_callback, \
    combo_active_repay_without_no_loan, run_withholdAutoV1_by_api, monitor_check, paysvr_callback
from biztest.util.easymock.rbiz.mozhi_beiyin_zhongyi import RepayBeiyinMock
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.util.tools.tools import get_four_element
import common.global_const as gc


class TestRbizBeiyin(BaseRepayTest):
    """
    mozhi_beiyin_zhongyi 还款

    """
    loan_channel = "mozhi_beiyin_zhongyi"
    grant_principal = 800000
    if datetime.datetime.today().month in (1, 3, 5, 7, 8, 10, 12):
        first_period_interest = 16940  # 第一期息费 大月份
        first_interest = 7233
    else:
        first_period_interest = 16707  # 第一期息费 小月份
        first_interest = 7000
    exp_sign_company = "tq,tqa,tqb"
    exp_sign_company_no_loan = "tq,tqa,tqb"

    @classmethod
    def setup_class(cls):
        monitor_check()
        cls.task = Task("rbiz{0}".format(gc.ENV))
        cls.msg = Msg("rbiz{0}".format(gc.ENV))
        cls.beiyin_mock = RepayBeiyinMock(rbiz_mock)

    def setup_method(self):
        # 在每个脚本执行之前，初始化限制配置
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzbyzy
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
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan, code=1)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzbyzy
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

        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 2 数据检查，大单1单小单1单，都走我方代扣
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        param_loan = {
            "withhold_sign_company": None,
            "withhold_channel": "mozhi_beiyin_zhongyi_BEIYIN",
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
    @pytest.mark.mzbyzy
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
        self.beiyin_mock.update_repay_result(int(asset_tran_amount["asset_tran_balance_amount"]), due_bill_no,
                                             "BAOFU_KUAINIU")

        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 2 逾期数据检查，大单1单小单1单，都走我方代扣
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        param_loan = {
            "withhold_sign_company": None,
            "withhold_channel": "mozhi_beiyin_zhongyi_BAOFU_KUAINIU",
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
    @pytest.mark.mzbyzy
    def test_overdue_fail_switch_to_our(self):
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
        self.beiyin_mock.update_repay_result(int(asset_tran_amount["asset_tran_balance_amount"]), due_bill_no,
                                             "KUAINIU_PAY", 'REPAYING')
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        withhold = get_withhold_by_item_no(self.item_no)
        resp_apply = mozhi_withhold_apply(due_bill_no, int(asset_tran_amount["asset_tran_balance_amount"]),
                                          self.four_element['data']['bank_code_encrypt'])
        check_json_rs_data(resp_apply['content'], code=0)
        resp_query = mozhi_withhold_query(due_bill_no)
        check_json_rs_data(resp_query['content'], code=1, message='还款结果查询失败，代扣信息未查询到')
        self.run_all_task_after_repay_success()
        resp_query_2 = mozhi_withhold_query(due_bill_no)
        check_json_rs_data(resp_query_2['content'], code=0, message='成功')
        check_json_rs_data(resp_query_2['content']['data'], repayStatus='SUCCESS')
        order_list = [project["order_no"] for project in repay_resp["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        # step 4 数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        order_no_no_loan = repay_resp["data"]["project_list"][0]["order_no"]
        order_no = repay_resp["data"]["project_list"][1]["order_no"]
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 1)
        check_withhold_sign_company(order_no_no_loan, self.exp_sign_company_no_loan)
        check_withhold_sign_company(order_no, self.exp_sign_company)
        param_loan = {
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "withhold_sign_company": self.exp_sign_company
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "withhold_sign_company": self.exp_sign_company_no_loan
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzbyzy
    def test_auto_normal_repay(self):
        # step 1 发起自动代扣
        self.change_asset_due_at(-1, 0)
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest)

        run_withholdAutoV1_by_api(self.item_no)
        wait_expect_task_appear(self.item_no, 'auto_withhold_execute')
        check_task_by_order_no_and_type(self.item_no, 'auto_withhold_execute', task_status='open')
        self.task.run_task(self.item_no, 'auto_withhold_execute')
        self.get_auto_withhold_execute_task_run(self.item_no)
        withhold = get_withhold_by_item_no(self.item_no)
        mozhi_beiyin_callback(withhold[0]['withhold_serial_no'], due_bill_no, withhold[0]['withhold_amount'], 'FAIL')
        mozhi_beiyin_callback(withhold[0]['withhold_serial_no'], due_bill_no, withhold[0]['withhold_amount'])

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzbyzy
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
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
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
        #  还1期的金额，资方扣1-12期本金+1000利息，剩余我方扣=1-12期息费-1000利息
        capital_withhold = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel + "_BEIYIN",
            "withhold_status": "success",
            "withhold_amount": self.grant_principal + 1000,
            "asset_tran_amount": self.grant_principal + self.first_interest
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        # check_settle_payoff_capital_withhold_detail_vs_asset_tran(order_no_capital, 1000)
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(
                asset_tran_amount["asset_tran_balance_amount"]) - self.grant_principal - 1000,
            "asset_tran_amount": int(
                asset_tran_amount["asset_tran_balance_amount"]) - self.grant_principal
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
    @pytest.mark.mzbyzy
    def test_active_normal_settle_payoff(self):
        """
        到期日提前结清
        """
        self.change_asset_due_at(-1, 0)
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_trail(self.grant_principal, self.first_interest)  # 第1期利息
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest)
        self.beiyin_mock.update_repay_result(self.grant_principal + self.first_period_interest, due_bill_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
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
            "withhold_channel": self.loan_channel + "_BEIYIN",
            "withhold_status": "success",
            "withhold_amount": self.grant_principal + self.first_period_interest,
            "asset_tran_amount": self.grant_principal + self.first_period_interest
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        # check_settle_payoff_capital_withhold_detail_vs_asset_tran(order_no_capital, 7233)
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(
                asset_tran_amount["asset_tran_balance_amount"]) - self.grant_principal - self.first_period_interest,
            "asset_tran_amount": int(
                asset_tran_amount["asset_tran_balance_amount"]) - self.grant_principal - self.first_period_interest
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'], 2)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.mzbyzy
    def test_active_overdue_one_day_settle_payoff(self):
        """
        逾期第1天提前结清，代偿日之前，
        1. 第1期逾期先砍单扣
        2. 第2次代扣，第2-12期提前结清，北银的试算结果>墨智的还款计划时，直接返回交易失败
        """
        self.change_asset_due_at(-1, -1)
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_capital_plan(due_bill_no)
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest,
                                           late_interest=150)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        self.beiyin_mock.update_repay_result(int(asset_tran_amount["asset_tran_balance_amount"]), due_bill_no,
                                             "BAOFU_KUAINIU")
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_all_task_after_repay_success()
        order_no_capital = resp_repay["data"]["project_list"][0]["order_no"]
        order_no_our = resp_repay["data"]["project_list"][1]["order_no"]

        check_withhold_data_by_sn(order_no_capital, withhold_status='success',
                                  withhold_amount=int(asset_tran_amount["asset_tran_balance_amount"]),
                                  withhold_channel=self.loan_channel + "_BAOFU_KUAINIU")
        check_withhold_data_by_sn(order_no_our, withhold_status='success',
                                  withhold_amount=int(asset_tran_amount_no_loan["asset_tran_balance_amount"]))
        # 第2次代扣  2-12期
        self.beiyin_mock.update_repay_list(due_bill_no, 736481, 16366, term=2, status='PRE_REPAY')
        # self.beiyin_mock.update_repay_trail(736481, 1000)
        self.beiyin_mock.update_repay_trail(self.grant_principal, 1000)
        self.beiyin_mock.update_repay_result(753411, due_bill_no)
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
                   'code'] == 1, f"主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active}"
        check_json_rs_data(resp_combo_active['content'],
                           code=1, message="交易失败")
