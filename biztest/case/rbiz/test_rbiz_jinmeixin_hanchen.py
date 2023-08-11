# -*- coding: utf-8 -*-
import time

from biztest.util.easymock.rbiz.jinmeixin_hanchen import RepayJinmeixinHanchenMock
from biztest.util.tools.tools import *

import pytest

from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config
from biztest.function.biz.biz_check_function import check_capital_push_request_log, check_data, check_capital_notify
from biztest.function.biz.biz_db_function import get_capital_notify_req_data_by_item_no
from biztest.function.rbiz.rbiz_check_function import check_withhold_request_log, check_withhold_result_without_split, \
    check_account_recharge_and_repay, check_asset_tran_repay_one_period, check_withhold_split_count_by_request_no, \
    check_withhold_split_count_by_item_no_and_request_no, check_asset_tran_payoff, check_withhold_by_serial_no
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    get_withhold_by_item_no, get_withhold_by_serial_no, get_withhold_data_by_request_no
from biztest.interface.rbiz.rbiz_interface import monitor_check, simple_active_repay
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.util.tools.tools import get_four_element
import common.global_const as gc


@pytest.mark.rbiz_jinmeixin_hanchen
class TestRbizJinmeixinHanchen(BaseRepayTest):
    """
    jinmeixin_hanchen 还款

    """
    loan_channel = "jinmeixin_hanchen"
    our_sign_company = "tq,tqa,tqb"
    grant_principal = 300000
    one_interest = 4833
    one_fee = 374
    last_period_total = 28368

    @classmethod
    def setup_class(cls):
        monitor_check()
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        cls.jmxhc_mock = RepayJinmeixinHanchenMock(rbiz_mock)
        cls.task = Task("rbiz%s" % gc.ENV)
        cls.msg = Msg("rbiz%s" % gc.ENV)

    def setup_method(self):
        # 大小单进件
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element,
                                                                               asset_amount=3000)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.jmxhc
    def test_active_advance_repay(self):
        """
        不允许提前还1期
        """
        # step 1 主动还款 提前还款
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan, code=1)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.jmxhc
    def test_active_normal_repay(self):
        """
        正常还1期 全额成功
        资方扣1单 小单1单
        """
        # step 1 主动还款 到期日
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no)

        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        withhold = get_withhold_by_item_no(self.item_no)
        # mock全额还款
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_success(self.item_no, withhold[0]['withhold_serial_no'],
                                                                   "C" + withhold[0]['withhold_serial_no'])
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()

        # step 2 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel, "execute_combine_withhold",
                                   withhold[0]['withhold_serial_no'], 3)

        # step 3 数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 1)

        param_loan = {
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "withhold_sign_company": self.our_sign_company
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

        # 处理推送部分
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")
        check_capital_push_request_log(self.item_no, self.loan_channel, "JinmeixinHanchenCapitalPush")

        # check 数据 todo

    @pytest.mark.rbiz_auto_test
    @pytest.mark.jmxhc
    def test_active_normal_part_repay(self):
        """
        正常还1期 部分成功
        资方扣第1期本息成功，fee失败
        在宽限期内资方扣fee
        """
        # step 1 主动还款 到期日
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no)

        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        resp_combo_active = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        withhold = get_withhold_by_item_no(self.item_no)
        # mock部分还款 本息

        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_success(self.item_no, withhold[0]['withhold_serial_no'],
                                                                   "C" + withhold[0]['withhold_serial_no'], fee_amt=0,
                                                                   repay_status="PART")
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()

        # step 2 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel + "_part_normal",
                                   "execute_combine_withhold",
                                   withhold[0]['withhold_serial_no'], 1)

        # step 3 发起主动代扣第二次 资方扣费
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no, prin_amt=0, int_amt=0)
        asset_tran_amount_two = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount_two["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_twice['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active_twice}"
        order_no_one = resp_combo_active["data"]["project_list"][0]["order_no"]
        order_no_two = resp_combo_active_twice["content"]["data"]["project_list"][0]["order_no"]
        order_no_no_loan_two = resp_combo_active_twice["content"]["data"]["project_list"][1]["order_no"]

        print("order_no_one", order_no_one)
        print("order_no_two", order_no_two)
        print("order_no_no_loan_two", order_no_no_loan_two)

        withhold = get_withhold_by_serial_no(order_no_two)
        # mock部分还款 fee

        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_success(self.item_no, withhold[0]['withhold_serial_no'],
                                                                   "C" + withhold[0]['withhold_serial_no'], prin_amt=0,
                                                                   int_amt=0, repay_status="PART")
        self.run_all_task_after_repay_success(withhold=withhold)

        # step 3 数据检查，大单3单 小单1单
        withhold = get_withhold_by_serial_no(order_no_two)
        withhold_no_loan = get_withhold_by_serial_no(order_no_no_loan_two)

        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 1)
        # 检查大单的代扣
        param_loan_one = {
            "withhold_amount": 27517,
            "asset_tran_amount": 27517,
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_by_serial_no(order_no_one, **param_loan_one)
        param_loan_two = {
            "withhold_amount": 374,
            "asset_tran_amount": 374,
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_by_serial_no(order_no_two, **param_loan_two)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "withhold_sign_company": self.our_sign_company
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

        # 处理推送部分
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")
        check_capital_push_request_log(self.item_no, self.loan_channel, "JinmeixinHanchenCapitalPush")

        # check 数据 todo

    @pytest.mark.rbiz_auto_test
    @pytest.mark.jmxhc
    def test_active_advance_settle_payoff(self):
        """
        在第一期内提前结清，全额成功，第1期全额利息走资方
        1. 提前结清收整期利息 资方扣=1-12期本金+第1期利息+第1期fee
        2. 我方扣=2-12期利息+fee
        """
        self.change_asset_due_at(0, -10)
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial_settle(self.item_no)
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        withhold = get_withhold_by_item_no(self.item_no)
        # mock全额还款 提前结清的还款结果查询，会返回12期的还款计划，没有总金额

        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_settle_success(self.item_no,
                                                                          withhold[0]['withhold_serial_no'],
                                                                          "C" + withhold[0]['withhold_serial_no'],
                                                                          int_amt=self.one_interest / 100)
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()

        # step 2 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel + "_advance_payoff",
                                   "execute_combine_withhold",
                                   withhold[0]['withhold_serial_no'], 5)

        # step 3 数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        order_no_capital = resp_repay["data"]["project_list"][0]["order_no"]
        order_no_our = resp_repay["data"]["project_list"][1]["order_no"]
        # 拆单代扣
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[0]["withhold_request_no"], 2)

        #  拆成2单，资方扣本3000元+息+fee，我方扣剩余费用
        capital_withhold = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": self.grant_principal + self.one_interest + self.one_fee,
            "asset_tran_amount": self.grant_principal + self.one_interest + self.one_fee
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        our_withhold = {
            "withhold_sign_company": self.our_sign_company,
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(
                asset_tran_amount[
                    "asset_tran_balance_amount"]) - self.grant_principal - self.one_interest - self.one_fee,
            "asset_tran_amount": int(
                asset_tran_amount[
                    "asset_tran_balance_amount"]) - self.grant_principal - self.one_interest - self.one_fee
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'], start_period=2)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)

        # 处理推送部分 资方代扣 默认推送成功 不调资方接口
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")
        check_capital_push_request_log(self.item_no, self.loan_channel, "JinmeixinHanchenCapitalPush")

    @pytest.mark.rbiz_auto_test
    @pytest.mark.jmxhc
    def test_active_advance_settle_part_payoff(self):
        """
        在第一期内提前结清，提前结清收第一期整期，后面期次都只收本金，
        1. 全部本金+第一期息还成功，费还失败。
        2. 修改资产为到期日还款，然后还fee  fee走资方
        """
        self.change_asset_due_at(0, -10)
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial_settle(self.item_no)
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_combo_active = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        withhold = get_withhold_by_item_no(self.item_no)
        # mock全额还款 提前结清的还款结果查询，会返回12期的还款计划，没有总金额

        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_settle_success(self.item_no,
                                                                          withhold[0]['withhold_serial_no'],
                                                                          "C" + withhold[0]['withhold_serial_no'],
                                                                          fee_amt=0, repay_status='PART')
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()

        # step 2 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel + "_advance_part_payoff",
                                   "execute_combine_withhold",
                                   withhold[0]['withhold_serial_no'], 1)

        self.change_asset_due_at(-1, 0)
        # step 3 发起主动代扣第二次 提前结清 资方扣费
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no, prin_amt=0, int_amt=0, repay_type="PRE")
        asset_tran_amount_two = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        params_combo_active = {
            "project_num_loan_channel_amount": int(asset_tran_amount_two["asset_tran_balance_amount"]),
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_twice['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active_twice}"
        order_no_one = resp_combo_active["data"]["project_list"][0]["order_no"]
        order_no_two = resp_combo_active_twice["content"]["data"]["project_list"][0]["order_no"]
        order_no_three = resp_combo_active_twice["content"]["data"]["project_list"][1]["order_no"]
        order_no_no_loan_two = resp_combo_active_twice["content"]["data"]["project_list"][2]["order_no"]

        withhold = get_withhold_by_serial_no(order_no_two)
        # mock部分还款 fee

        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_success(self.item_no, withhold[0]['withhold_serial_no'],
                                                                   "C" + withhold[0]['withhold_serial_no'], prin_amt=0,
                                                                   int_amt=0, repay_status="PART")

        withhold = get_withhold_data_by_request_no(withhold[0]['withhold_request_no'])
        withhold, withhold_noloan = self.run_all_task_after_repay_success(withhold=withhold)


        # step 3 数据检查，大单2单 小单1单
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)

        print("order_no_one", order_no_one)
        print("order_no_two", order_no_two)
        print("order_no_three", order_no_three)
        print("order_no_no_loan_two", order_no_no_loan_two)
        # 检查大单的代扣
        # 第1单 资方扣 12期本+第一期利息
        param_loan_one = {
            "withhold_amount": self.grant_principal + self.one_interest,
            "asset_tran_amount": self.grant_principal + self.one_interest,
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_by_serial_no(order_no_one, **param_loan_one)
        # 第2单资方扣第1期费
        param_loan_two = {
            "withhold_amount": self.one_fee,
            "asset_tran_amount": self.one_fee,
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_by_serial_no(order_no_two, **param_loan_two)

        # 第3单我方扣
        our_withhold_amount = int(asset_tran_amount["asset_tran_amount"]) - (
                self.grant_principal + self.one_interest + self.one_fee)
        param_loan_three = {
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_withhold_amount,
            "withhold_sign_company": self.our_sign_company
        }

        check_withhold_by_serial_no(order_no_three, **param_loan_three)

        withhold_no_loan = get_withhold_by_serial_no(order_no_no_loan_two)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "withhold_sign_company": self.our_sign_company,
            "withhold_channel": "baidu_tq3_quick"
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        withhold_one = get_withhold_by_serial_no(order_no_one)
        withhold_two = get_withhold_by_serial_no(order_no_two)
        withhold_three = get_withhold_by_serial_no(order_no_three)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_one[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_two[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_three[0]['withhold_channel_key'], start_period=2)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)

        # 处理推送部分
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")
        check_capital_push_request_log(self.item_no, self.loan_channel, "JinmeixinHanchenCapitalPush")

    @pytest.mark.rbiz_auto_test
    @pytest.mark.jmxhc
    def test_active_normal_last_period(self):
        """
        最后一期到期日为今天
        1、提前结清 1-11期 全部逾期，砍单先还。分11次推送给资方，类型为overdue
        2、12期本息费都走资方扣，全额成功。这个场景capital_transaction第12期是刷为early_settlement
        """
        # Step 1：提前结清 1-11期
        self.change_asset_due_at(-12, 0)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, before_tran_period=11)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_one = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # 处理推送部分 1-11期，推送11次
        for i in range(0, 11):
            self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
            self.run_capital_push_by_api()
            self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")

        # step 2 发起主动代扣第二次，只有大单要扣了
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no, prin_amt=274.55, int_amt=4.79, fee_amt=4.34,
                                                           term_no=12)
        asset_tran_amount_two = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        params_combo_active = {
            "project_num_loan_channel_amount": int(asset_tran_amount_two["asset_tran_balance_amount"]),
            "project_num_no_loan": None
        }
        resp_two, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_two['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_two}"
        order_no_one = resp_one["data"]["project_list"][1]["order_no"]  # 1-11期 大单
        order_no_two = resp_two["content"]["data"]["project_list"][0]["order_no"]  # 12期 大单

        withhold = get_withhold_by_serial_no(order_no_two)
        # mock全额还款

        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_success(self.item_no, withhold[0]['withhold_serial_no'],
                                                                   "C" + withhold[0]['withhold_serial_no'],
                                                                   prin_amt=274.55, int_amt=4.79, fee_amt=4.34,
                                                                   term_no=12)
        self.run_all_task_after_repay_success(withhold)

        # step 2 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel + "_last_period",
                                   "execute_combine_withhold",
                                   withhold[0]['withhold_serial_no'], 1)

        # 检查大单的代扣
        # 第1单 资方扣 12期本+第一期利息
        param_loan_one = {
            "withhold_amount": int(asset_tran_amount["asset_tran_amount"]),
            "asset_tran_amount": int(asset_tran_amount["asset_tran_amount"]),
            "withhold_channel": "baidu_tq3_quick"
        }
        check_withhold_by_serial_no(order_no_one, **param_loan_one)
        # 第2单资方扣第12期整期费用
        param_loan_two = {
            "withhold_amount": self.last_period_total,
            "asset_tran_amount": self.last_period_total,
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_by_serial_no(order_no_two, **param_loan_two)

        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "withhold_sign_company": self.our_sign_company,
            "withhold_channel": "baidu_tq3_quick"
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        withhold_one = get_withhold_by_serial_no(order_no_one)
        withhold_two = get_withhold_by_serial_no(order_no_two)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_one[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_two[0]['withhold_channel_key'], start_period=12)
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.jmxhc
    def test_active_advance_last_period(self):
        """
        最后一期提前结清
        1、提前结清 1-11期 全部逾期，砍单先还。分11次推送给资方，类型为overdue
        2、12期本息费都走资方扣，全额成功。  这个场景capital_transaction第12期是刷为early_settlement
        """
        # Step 1：提前结清 1-11期
        self.change_asset_due_at(-11, -10)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, before_tran_period=11)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_one = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # 处理推送部分 1-11期，推送11次
        for i in range(0, 11):
            self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
            self.run_capital_push_by_api()
            self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")

        # step 2 发起主动代扣第二次，只有大单要扣了
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no, prin_amt=274.55, int_amt=4.79, fee_amt=4.34,
                                                           term_no=12)
        asset_tran_amount_two = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        params_combo_active = {
            "project_num_loan_channel_amount": int(asset_tran_amount_two["asset_tran_balance_amount"]),
            "project_num_no_loan": None
        }
        resp_two, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_two['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_two}"
        order_no_one = resp_one["data"]["project_list"][1]["order_no"]  # 1-11期 大单
        order_no_two = resp_two["content"]["data"]["project_list"][0]["order_no"]  # 12期 大单

        withhold = get_withhold_by_serial_no(order_no_two)
        # mock全额还款
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_success(self.item_no, withhold[0]['withhold_serial_no'],
                                                                   "C" + withhold[0]['withhold_serial_no'],
                                                                   prin_amt=274.55, int_amt=4.79, fee_amt=4.34,
                                                                   term_no=12)
        self.run_all_task_after_repay_success()

        # step 2 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel + "_pre_last_period",
                                   "execute_combine_withhold",
                                   withhold[0]['withhold_serial_no'], 1)

        # 检查大单的代扣
        # 第1单 资方扣 12期本+第一期利息
        param_loan_one = {
            "withhold_amount": int(asset_tran_amount["asset_tran_amount"]),
            "asset_tran_amount": int(asset_tran_amount["asset_tran_amount"]),
            "withhold_channel": "baidu_tq3_quick"
        }
        check_withhold_by_serial_no(order_no_one, **param_loan_one)
        # 第2单资方扣第12期整期费用
        param_loan_two = {
            "withhold_amount": self.last_period_total,
            "asset_tran_amount": self.last_period_total,
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_by_serial_no(order_no_two, **param_loan_two)

        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "withhold_sign_company": self.our_sign_company,
            "withhold_channel": "baidu_tq3_quick"
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        withhold_one = get_withhold_by_serial_no(order_no_one)
        withhold_two = get_withhold_by_serial_no(order_no_two)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_one[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_two[0]['withhold_channel_key'], start_period=12)
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")

    @pytest.mark.rbiz_auto_test
    @pytest.mark.jmxhc
    def test_active_overdue_capital_last_period(self):
        """
        最后一期到期日在宽限期内
        1、提前结清 1-11期 全部逾期，砍单先还。分11次推送给资方，类型为overdue
        2、12期本息费都走资方扣，全额成功。  这个场景capital_transaction第12期是刷为early_settlement
        """
        # Step 1：提前结清 1-11期

        self.change_asset_due_at(-12, -2)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, before_tran_period=11)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_one = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # 处理推送部分 1-11期，推送11次
        for i in range(0, 11):
            self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
            self.run_capital_push_by_api()
            self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")

        # step 2 发起主动代扣第二次，只有大单要扣了
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no, prin_amt=274.55, int_amt=4.79, fee_amt=4.34,
                                                           term_no=12)
        asset_tran_amount_two = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        params_combo_active = {
            "project_num_loan_channel_amount": int(asset_tran_amount_two["asset_tran_balance_amount"]),
            "project_num_no_loan": None
        }
        resp_two, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_two['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_two}"
        order_no_one = resp_one["data"]["project_list"][1]["order_no"]  # 1-11期 大单
        order_no_two = resp_two["content"]["data"]["project_list"][0]["order_no"]  # 12期 大单
        order_no_three = resp_two["content"]["data"]["project_list"][1]["order_no"]  # 12期 罚息

        withhold_order_no_two = get_withhold_by_serial_no(order_no_two)
        # mock全额还款
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_success(self.item_no, withhold_order_no_two[0]['withhold_serial_no'],
                                                                   "C" + withhold_order_no_two[0]['withhold_serial_no'],
                                                                   prin_amt=274.55, int_amt=4.79, fee_amt=4.34,
                                                                   term_no=12)
        self.run_all_task_after_repay_success(withhold_order_no_two)

        withhold_order_no_three = get_withhold_by_serial_no(order_no_three)
        self.run_all_task_after_repay_success(withhold_order_no_three)

        # step 2 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold_order_no_two[0]['withhold_request_no'], self.loan_channel + "_last_period",
                                   "execute_combine_withhold",
                                   withhold_order_no_two[0]['withhold_serial_no'], 3)

        # 检查大单的代扣
        # 第1单 资方扣 12期本+第一期利息
        param_loan_one = {
            "withhold_amount": int(asset_tran_amount["asset_tran_amount"]),
            "asset_tran_amount": int(asset_tran_amount["asset_tran_amount"]),
            "withhold_channel": "baidu_tq3_quick"
        }
        check_withhold_by_serial_no(order_no_one, **param_loan_one)
        # 第2单资方扣第12期整期费用
        param_loan_two = {
            "withhold_amount": self.last_period_total,
            "asset_tran_amount": self.last_period_total,
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_by_serial_no(order_no_two, **param_loan_two)

        # 第2单我方扣第1期罚息
        param_loan_three = {
            "withhold_amount": 22,
            "asset_tran_amount": 22,
            "withhold_channel": "baidu_tq3_quick"
        }
        check_withhold_by_serial_no(order_no_three, **param_loan_three)

        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "withhold_sign_company": self.our_sign_company,
            "withhold_channel": "baidu_tq3_quick"
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        withhold_one = get_withhold_by_serial_no(order_no_one)
        withhold_two = get_withhold_by_serial_no(order_no_two)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_one[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_two[0]['withhold_channel_key'], start_period=12)
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")

    @pytest.mark.rbiz_auto_test
    @pytest.mark.jmxhc
    def test_active_overdue_normal(self):
        """
        宽限期还款，走资方代扣，全额还款成功
        """
        # step 1 主动还款 逾期2天
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no)
        self.change_asset_due_at(-1, -2)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        withhold = get_withhold_by_item_no(self.item_no)
        # mock全额还款
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_success(self.item_no, withhold[0]['withhold_serial_no'],
                                                                   "C" + withhold[0]['withhold_serial_no'])
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()
        order_no_one = resp_repay["data"]["project_list"][0]["order_no"]  # 1期本息费
        order_no_two = resp_repay["data"]["project_list"][1]["order_no"]  # 1期罚息

        # step 2 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel, "execute_combine_withhold",
                                   withhold[0]['withhold_serial_no'], 5)

        # step 3 数据检查，大单2单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)

        # 检查大单的代扣
        # 第1单 资方扣 1期本息费
        param_loan_one = {
            "withhold_amount": 27891,
            "asset_tran_amount": 27891,
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_by_serial_no(order_no_one, **param_loan_one)
        # 第2单我方扣第1期罚息
        param_loan_two = {
            "withhold_amount": 18,
            "asset_tran_amount": 18,
            "withhold_channel": "baidu_tq3_quick"
        }
        check_withhold_by_serial_no(order_no_two, **param_loan_two)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "withhold_sign_company": self.our_sign_company
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

        # 处理推送部分
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")
        check_capital_push_request_log(self.item_no, self.loan_channel, "JinmeixinHanchenCapitalPush")

    @pytest.mark.rbiz_auto_test
    @pytest.mark.jmxhc
    def test_active_overdue_compensate(self):
        """
        宽限期外还款
        推送代偿消息给dcs
        """
        # step 1 主动还款 逾期2天
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no)
        self.change_asset_due_at(-1, -3)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()

        # 处理推送部分
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.run_generate_compensate_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")
        capital_notify_info = get_capital_notify_req_data_by_item_no(self.item_no)
        check_capital_push_request_log(self.item_no, self.loan_channel + "_notify_capital",
                                       "JinmeixinHanchenCapitalPush",
                                       capital_notify_info=capital_notify_info["repayNotifyReqDto"])
        self.wait_and_run_central_task(self.loan_channel, "CapitalCompensateBatch")
        self.wait_and_run_central_task(self.item_no, "CapitalCompensateProcess")
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")

    @pytest.mark.rbiz_auto_test
    @pytest.mark.jmxhc
    def test_active_part_repay_fee_overdue(self):
        """
        正常还款
        1、第1期本息：正常还款  部分成功走资方
        2、第1期费：  逾期还款 走我方
        3、第2期全额： 到期日还款  全额  走资方

        """
        # step 1 主动还款 到期日
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no)
        resp_combo_active = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        withhold = get_withhold_by_item_no(self.item_no)
        # mock部分还款 本息
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_success(self.item_no, withhold[0]['withhold_serial_no'],
                                                                   "C" + withhold[0]['withhold_serial_no'], fee_amt=0,
                                                                   repay_status="PART")
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()

        # step 2 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel + "_part_normal",
                                   "execute_combine_withhold",
                                   withhold[0]['withhold_serial_no'], 1)

        # 处理推送部分 不推资方
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")
        check_capital_push_request_log(self.item_no, self.loan_channel, "JinmeixinHanchenCapitalPush")
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")

        # step 3 发起主动代扣第二次 费逾期了  我方扣费
        self.change_asset_due_at(-1, -4)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        asset_tran_amount_two = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount_two["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_twice['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active_twice}"
        order_no_one = resp_combo_active["data"]["project_list"][0]["order_no"]
        order_no_no_loan_two = resp_combo_active_twice["content"]["data"]["project_list"][0]["order_no"]
        order_no_two = resp_combo_active_twice["content"]["data"]["project_list"][1]["order_no"]

        print("order_no_one", order_no_one)
        print("order_no_two", order_no_two)
        print("order_no_no_loan_two", order_no_no_loan_two)
        withhold = get_withhold_by_serial_no(order_no_two)
        self.run_all_task_after_repay_success(withhold=withhold)

        # step 3 数据检查，大单3单 小单1单
        withhold = get_withhold_by_serial_no(order_no_two)
        withhold_no_loan = get_withhold_by_serial_no(order_no_no_loan_two)

        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 1)
        # 检查大单的代扣
        param_loan_one = {
            "withhold_amount": 27517,
            "asset_tran_amount": 27517,
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_by_serial_no(order_no_one, **param_loan_one)
        param_loan_two = {
            "withhold_amount": 374,
            "asset_tran_amount": 374,
            "withhold_sign_company": self.our_sign_company
        }
        check_withhold_by_serial_no(order_no_two, **param_loan_two)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "withhold_sign_company": self.our_sign_company
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

        # 处理推送部分 fee推资方
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")
        check_capital_push_request_log(self.item_no, self.loan_channel, "JinmeixinHanchenCapitalPush")
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        time.sleep(5)  # ES日志需等待5s
        check_capital_notify(self.item_no, withhold[0]["withhold_serial_no"], capital_notify_type="overdue")
        capital_notify_info = get_capital_notify_req_data_by_item_no(self.item_no, withhold[0]["withhold_serial_no"])
        # 检查推送给资方的数据是否正确
        # step 1 检查capital_notify表中的取值
        # step 2 检查es日志是否按照capital_notify中repayNotifyReqDto的数据来推的
        check_data(capital_notify_info["repayNotifyReqDto"], repayStatus='SUCCESS', repayAmt=3.74)
        check_capital_push_request_log(self.item_no, self.loan_channel + "_notify_capital",
                                       "JinmeixinHanchenCapitalPush",
                                       0, capital_notify_info["repayNotifyReqDto"])

        # step 4 发起主动代扣第3次 第二期  资方扣 本金=23403 利息=4016  fee=424
        self.change_asset_due_at(-2, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount_p2 = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 2)
        asset_tran_amount_no_loan_p2 = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 2)
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no, prin_amt=230.81, int_amt=48.53, fee_amt=4.34,
                                                           term_no=2)
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount_p2["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan_p2["asset_tran_balance_amount"]
        }
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_twice['content'][
                   'code'] == 0, f"第3次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active_twice}"
        order_no_p2 = resp_combo_active_twice["content"]["data"]["project_list"][0]["order_no"]

        withhold = get_withhold_by_serial_no(order_no_p2)
        # mock部分还款 fee
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_success(self.item_no, withhold[0]['withhold_serial_no'],
                                                                   "C" + withhold[0]['withhold_serial_no'],
                                                                   prin_amt=230.81, int_amt=48.53, fee_amt=4.34,
                                                                   repay_status="SUCCESS",
                                                                   term_no=2)
        self.run_all_task_after_repay_success(withhold=withhold)

        param_loan_p2 = {
            "withhold_amount": 28368,
            "asset_tran_amount": 28368,
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_by_serial_no(order_no_p2, **param_loan_p2)
        # 处理推送部分 资方代扣不推资方
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")
        check_capital_push_request_log(self.item_no, self.loan_channel, "JinmeixinHanchenCapitalPush")
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")

    @pytest.mark.rbiz_auto_test
    @pytest.mark.jmxhc
    def test_active_advance_settle_fee_overdue_part_payoff(self):
        """
        在第一期内提前结清，提前结清收第一期整期，后面期次都只收本金，
        1. 全部本金+第一期息还成功，费还失败。
        2. 1期fee 逾期
        3. 还第2期利息和费

        金美信大秦，不允许提前还款 -update by shasha 2022-10-22
        """
        self.change_asset_due_at(0, -10)
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial_settle(self.item_no)
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_combo_active = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        withhold = get_withhold_by_item_no(self.item_no)
        # mock全额还款 提前结清的还款结果查询，会返回12期的还款计划，没有总金额

        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_settle_success(self.item_no,
                                                                          withhold[0]['withhold_serial_no'],
                                                                          "C" + withhold[0]['withhold_serial_no'],
                                                                          fee_amt=0, repay_status='PART')
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()

        # step 2 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel + "_advance_part_payoff",
                                   "execute_combine_withhold",
                                   withhold[0]['withhold_serial_no'], 1)
        # 处理推送部分 不推资方
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush")
        check_capital_push_request_log(self.item_no, self.loan_channel, "JinmeixinHanchenCapitalPush")
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")

        # step 3 发起主动代扣第二次 费逾期了  我方扣费
        self.change_asset_due_at(-1, -3)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        asset_tran_amount_two = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount_two["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_twice['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active_twice}"
        order_no_one = resp_combo_active["data"]["project_list"][0]["order_no"]
        order_no_no_loan_two = resp_combo_active_twice["content"]["data"]["project_list"][0]["order_no"]
        order_no_two = resp_combo_active_twice["content"]["data"]["project_list"][1]["order_no"]

        print("order_no_one", order_no_one)
        print("order_no_two", order_no_two)
        print("order_no_no_loan_two", order_no_no_loan_two)
        withhold = get_withhold_by_serial_no(order_no_two)
        self.run_all_task_after_repay_success(withhold=withhold)

        # 检查大单的代扣
        # 第1单 资方扣 12期本+第一期利息
        param_loan_one = {
            "withhold_amount": self.grant_principal + self.one_interest,
            "asset_tran_amount": self.grant_principal + self.one_interest,
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_by_serial_no(order_no_one, **param_loan_one)
        # 第2单 第1期费逾期了 我方扣
        param_loan_two = {
            "withhold_amount": self.one_fee,
            "asset_tran_amount": self.one_fee,
            "withhold_sign_company": self.our_sign_company
        }
        check_withhold_by_serial_no(order_no_two, **param_loan_two)

        # 处理推送部分 fee推资方
        self.run_generate_compensate_by_api()
        self.wait_and_run_central_task(self.loan_channel, "CapitalCompensateBatch")
        self.wait_and_run_central_task(self.item_no, "CapitalCompensateProcess")
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")

        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no, prin_amt=0, int_amt=0, fee_amt=4.24)
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush", excepts={
            "code": 0,
            "message": "推送成功",
            "data": {
                "notifyFg": "Y"
            }
        })
        # self.wait_and_run_central_task(self.item_no, "JinmeixinHanchenCapitalPush", excepts={
        #     "code": 2,
        #     "message": f"[{order_no_two}_early_settlement_1_1]待数据刷为代偿后，再执行推送"
        # })
        check_capital_push_request_log(self.item_no, self.loan_channel, "JinmeixinHanchenCapitalPush")
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        time.sleep(5)  # ES日志需等待5s
        check_capital_notify(self.item_no, withhold[0]["withhold_serial_no"], capital_notify_type="early_settlement")
        capital_notify_info = get_capital_notify_req_data_by_item_no(self.item_no, withhold[0]["withhold_serial_no"])
        # 检查推送给资方的数据是否正确
        # step 1 检查capital_notify表中的取值
        # step 2 检查es日志是否按照capital_notify中repayNotifyReqDto的数据来推的
        check_data(capital_notify_info["repayNotifyReqDto"], repayStatus='PART', repayAmt=4.24)
        check_capital_push_request_log(self.item_no, self.loan_channel + "_notify_capital",
                                       "JinmeixinHanchenCapitalPush",
                                       0, capital_notify_info["repayNotifyReqDto"])

        # step 4 发起主动代扣第3次 资方扣2fee=424  我方扣 2利息
        self.change_asset_due_at(-2, -0)
        asset_tran_amount_p2 = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_trial(self.item_no, prin_amt=0, int_amt=0, fee_amt=4.34, term_no=2)

        resp_p2 = self.repay_only_one_project_success(asset_tran_amount_p2["asset_tran_balance_amount"], self.item_no)
        assert resp_p2['code'] == 0, f"第3次主动合并代扣失败,resp_combo_active={resp_p2}"
        order_no_p2 = resp_p2["data"]["project_list"][0]["order_no"]

        withhold = get_withhold_by_serial_no(order_no_p2)
        # mock部分还款 fee

        self.jmxhc_mock.mock_jinmeixin_hanchen_repay_query_success(self.item_no, withhold[0]['withhold_serial_no'],
                                                                   "C" + withhold[0]['withhold_serial_no'],
                                                                   prin_amt=0, int_amt=0, fee_amt=4.34,
                                                                   repay_status="SUCCESS",
                                                                   term_no=2)
        self.run_all_task_after_repay_success(withhold=withhold)
        check_data(json.loads(withhold[0]["withhold_extend_info"]), jinmeixinDaqinRepayType='PRE')

        param_loan_p2 = {
            "withhold_amount": 434,
            "asset_tran_amount": 434,
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": None
        }
        check_withhold_by_serial_no(order_no_p2, **param_loan_p2)
