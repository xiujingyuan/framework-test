# -*- coding: utf-8 -*-
import datetime

import pytest
import datetime

from biztest.case.rbiz.base_repay_test import BaseRepayTest

from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config
from biztest.function.biz.biz_check_function import check_capital_push_request_log
from biztest.function.rbiz.rbiz_check_function import check_withhold_request_log, check_withhold_result_without_split, \
    check_account_recharge_and_repay, check_asset_tran_repay_one_period, check_withhold_split_count_by_request_no, \
    check_withhold_split_count_by_item_no_and_request_no, check_asset_tran_payoff, check_withhold_by_serial_no, \
    check_settle_payoff_capital_withhold_detail_vs_asset_tran
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    get_withhold_by_item_no
from biztest.interface.rbiz.rbiz_interface import monitor_check
from biztest.util.easymock.rbiz.zhongke_hegang import RepayZhongkeHegangMock
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.util.tools.tools import get_four_element
import common.global_const as gc


class TestRbizZhongkeHegang(BaseRepayTest):
    """
    zhongke_hegang 还款

    """
    loan_channel = "zhongke_hegang"
    exp_sign_company_no_loan = "tq,tqa,tqb"
    grant_principal = 800000
    one_interest = 4467
    one_fee = 11259

    @classmethod
    def setup_class(cls):
        monitor_check()
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        cls.zkhg_mock = RepayZhongkeHegangMock(rbiz_mock)
        cls.task = Task("rbiz%s" % gc.ENV)
        cls.msg = Msg("rbiz%s" % gc.ENV)

    def setup_method(self):
        # 大小单进件
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element)
        print("set up method")

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.zkhg
    def test_active_advance_repay(self):
        """
        提前还1期 不允许
        """
        # step 1 主动还款 提前还款
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan, code=1)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.zkhg
    def test_active_normal_repay(self):
        """
        正常还1期，
        中科鹤岗是36%走资方代扣，但是是paysvr帮忙代扣
        """
        # step 1 主动还款 到期日
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
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
            "withhold_sign_company": "zhongrong"
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

        # 处理推送部分
        self.zkhg_mock.mock_hegang_repay_query_1000()
        self.zkhg_mock.mock_hegang_repay_apply()
        # self.wait_and_run_central_task(self.item_no, "UserRepay")
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "ZhongkeHegangCapitalPush",
                                       excepts={"code": 2, "message": "自动化测试repayApply"})
        # 检查推送请求的参数
        check_capital_push_request_log(self.item_no, self.loan_channel, "ZhongkeHegangCapitalPush")
        # 查询结果
        self.zkhg_mock.mock_hegang_repay_query()
        self.wait_and_run_central_task(self.item_no, "ZhongkeHegangCapitalPush")

        # check 数据 todo

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.zkhg
    def test_active_advance_settle_payoff(self):
        """
        在第一期内提前结清
        """
        self.change_asset_due_at(0, -10)
        self.zkhg_mock.mock_hegang_repay_trail()
        self.zkhg_mock.mock_hegang_repay_trail_query()
        self.zkhg_mock.mock_hegang_repay_query(int_amt=10, prin_amt=8000)
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
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

        #  拆成2单，资方扣本8000元+息10元，我方扣剩余费用
        capital_withhold = {
            "withhold_sign_company": "zhongrong",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": self.grant_principal + 1000 + self.one_fee,
            "asset_tran_amount": self.grant_principal + self.one_interest + self.one_fee
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        our_withhold = {
            "withhold_sign_company": self.exp_sign_company_no_loan,
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(
                asset_tran_amount["asset_tran_balance_amount"]) - self.grant_principal - 1000 - self.one_fee,
            "asset_tran_amount": int(
                asset_tran_amount["asset_tran_balance_amount"]) - self.grant_principal - self.one_fee
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

        # 处理推送部分
        self.zkhg_mock.mock_hegang_repay_query_1000()
        self.zkhg_mock.mock_hegang_repay_apply()
        # self.wait_and_run_central_task(self.item_no, "UserRepay")
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "ZhongkeHegangCapitalPush", excepts=None)
        self.wait_and_run_central_task(self.item_no, "ZhongkeHegangCapitalPush", excepts=None)
        # 检查推送请求的参数
        check_capital_push_request_log(self.item_no, self.loan_channel + "_advance_payoff", "ZhongkeHegangCapitalPush")
        # 查询结果
        self.zkhg_mock.mock_hegang_repay_query(int_amt=10, prin_amt=8000)
        self.wait_and_run_central_task(self.item_no, "ZhongkeHegangCapitalPush")

        # check 数据 todo
