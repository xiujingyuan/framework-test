# -*- coding: utf-8 -*-

from biztest.util.tools.tools import *
import pytest

from biztest.case.rbiz.base_repay_test import BaseRepayTest

from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.function.biz.biz_check_function import check_capital_push_request_log, check_data, check_capital_notify
from biztest.function.biz.biz_db_function import get_capital_notify_req_data_param_by_item_no, \
    get_capital_notify_req_data_by_item_no, update_capital_notify_plan_at_by_item_no
from biztest.function.rbiz.rbiz_check_function import check_withhold_request_log, check_withhold_result_without_split, \
    check_account_recharge_and_repay, check_asset_tran_repay_one_period, check_withhold_split_count_by_request_no, \
    check_withhold_split_count_by_item_no_and_request_no, check_asset_tran_payoff, check_withhold_by_serial_no, \
    check_settle_payoff_capital_withhold_detail_vs_asset_tran, check_capital_withhold_detail_vs_asset_tran, \
    check_withhold_data_by_sn, check_withhold_sign_company, check_card_bind_info, check_card_by_item_no, \
    check_withhold_card_by_card_num, check_individual_by_item_no
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    get_withhold_by_item_no, get_withhold_by_serial_no, update_card_bind_update_at_by_card_number, \
    get_asset_tran_by_item_no_and_type_and_period
from biztest.interface.rbiz.rbiz_interface import monitor_check, bind_sms, simple_active_repay, paysvr_callback
from biztest.util.easymock.rbiz.lanzhou_haoyue_qinjia import RepayLanzhouHaoyueQinjiaMock
from biztest.util.easymock.rbiz.zhongke_hegang import RepayZhongkeHegangMock
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.util.tools.tools import get_four_element, get_date_before_today
import common.global_const as gc


class TestRbizLanzhouHaoyueQinjia(BaseRepayTest):
    """
    lanzhou_haoyue_qinjia 还款

    """
    loan_channel = "lanzhou_haoyue_qinjia"
    our_sign_company = "tq,tqa,tqb"
    grant_principal = 400000

    @classmethod
    def setup_class(cls):
        monitor_check()
        cls.lzhyqj_mock = RepayLanzhouHaoyueQinjiaMock(rbiz_mock)
        cls.task = Task("rbiz%s" % gc.ENV)
        cls.msg = Msg("rbiz%s" % gc.ENV)

    def setup_method(self):
        # 大小单进件
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element,
                                                                               item_no="QJ" + get_item_no(),
                                                                               asset_amount=4000)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhyqj
    def test_active_advance_repay(self):
        """
        提前还1期 不允许
        """
        # step 1 主动还款 提前还款
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan, code=1)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhyqj
    def test_active_normal_repay(self):
        """
        正常还1期，
        资方扣1单，我方扣1单，小单1单
        """
        # step 1 主动还款 到期日
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        self.run_all_task_after_repay_success()

        # step 2 DB数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        # 资方代扣金额 = 第1期全额
        capital_withhold_amount = int(asset_tran_amount["asset_tran_amount"])
        # 代扣顺序： 资方先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[0]["withhold_request_no"], 1)
        capital_withhold = {
            "withhold_sign_company": "qjhy",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        capital_withhold_type = ['repayprincipal', 'repayinterest', 'consult', 'guarantee', 'reserve']
        check_capital_withhold_detail_vs_asset_tran(order_no_capital, capital_withhold_type)
        # 小单代扣数据检查
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_repay_one_period(self.item_no)

        # step 3 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel, "execute_combine_withhold",
                                   withhold[0]['withhold_serial_no'], 3)

        # 处理推送部分
        self.lzhyqj_mock.mock_lanzhou_haoyue_qinjia_normal_repay_notice(self.item_no, "KN10001" + self.item_no)
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "LanzhouHaoyueQinjiaCapitalPush")
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        # # 检查推送请求的参数
        check_capital_notify(self.item_no, withhold[0]["withhold_serial_no"], capital_notify_type="normal",
                             capital_notify_status='success')
        # # 检查推送请求的参数
        capital_notify_param = get_capital_notify_req_data_param_by_item_no(self.item_no)
        print("capital_notify_param: ", capital_notify_param)
        check_capital_push_request_log(self.item_no, self.loan_channel, "LanzhouHaoyueQinjiaCapitalPush",
                                       capital_notify_info=capital_notify_param)

        # 检查推送给资方的数据是否正确
        # step 1 检查capital_notify表中的取值
        # step 2 检查es日志是否按照capital_notify中repayNotifyReqDto的数据来推的
        check_data(capital_notify_param, deducttype='1', loanno="DN" + self.item_no)
        check_data(capital_notify_param["detaillist"][0], indeedcapital='322.48', indeedinterest='24.00',
                   indeedservicefee='31.74', indeedtotal='378.22')

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhyqj
    def test_lanzhou_haoyue_qinjia_active_advance_settle_payoff(self):
        """
        在第一期内提前结清
        """
        self.change_asset_due_at(0, -10)
        due_bill_no = "DN" + self.item_no
        self.lzhyqj_mock.mock_lanzhou_haoyue_qinjia_repay_trial(due_bill_no, prin_amt=4000)
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)

        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_our = repay_resp["data"]["project_list"][1]["order_no"]
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()

        # # step 2 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel + "_advance_payoff",
                                   "execute_combine_withhold",
                                   withhold[0]['withhold_serial_no'], 5)

        # step 3 数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        # 资方代扣金额 = 全额本金+第1期占用利息+第1期费
        # 我方代扣金额 = 第1期剩余利息 +2-12期息费
        one_interest = get_asset_tran_by_item_no_and_type_and_period(self.item_no, "repayinterest", 1)[0][
            'asset_tran_amount']
        capital_withhold_amount = 404174
        capital_tran_amount = 404174 + one_interest - 1000
        our_withhold_amount = int(asset_tran_amount["asset_tran_amount"]) - capital_withhold_amount
        our_tran_amount = int(asset_tran_amount["asset_tran_amount"]) - capital_withhold_amount + 1000
        # 代扣顺序： 资方先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[0]["withhold_request_no"], 2)

        #  拆成2单，资方扣本8000元+息10元，我方扣剩余费用
        capital_withhold = {
            "withhold_sign_company": 'qjhy',
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_tran_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_tran_amount
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
        # 推送时有增加利息，capital_transaction有贴息
        self.lzhyqj_mock.mock_lanzhou_haoyue_qinjia_repay_trial(due_bill_no, prin_amt=4000, int_amt=11.5)
        self.lzhyqj_mock.mock_lanzhou_haoyue_qinjia_settle_repay_notice(self.item_no, "KN10001" + self.item_no)
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        update_capital_notify_plan_at_by_item_no(self.item_no)
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "LanzhouHaoyueQinjiaCapitalPush")
        # 检查推送请求的参数
        capital_notify_param = get_capital_notify_req_data_param_by_item_no(self.item_no)
        print("capital_notify_param: ", capital_notify_param)

        # check 数据
        check_capital_notify(self.item_no, withhold[0]["withhold_serial_no"], capital_notify_type="early_settlement")
        # 检查推送给资方的数据是否正确
        # step 1 检查capital_notify表中的取值
        # step 2 检查es日志是否按照capital_notify中repayNotifyReqDto的数据来推的
        check_data(capital_notify_param, deducttype='1', loanno=due_bill_no)
        check_data(capital_notify_param["detaillist"][0], indeedcapital='4000.00', indeedinterest='11.50',
                   indeedservicefee='31.74', indeedtotal='4043.24')

        check_capital_push_request_log(self.item_no, self.loan_channel + "_advance_payoff",
                                       "LanzhouHaoyueQinjiaCapitalPush",
                                       capital_notify_info=capital_notify_param)

    @pytest.mark.lzhyqj
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
        # # 处理推送部分 1-11期，推送11次
        # for i in range(0, 11):
        #     self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        #     self.run_capital_push_by_api()
        #     self.wait_and_run_central_task(self.item_no, "JinmeixinDaqinCapitalPush")

        # step 2 发起主动代扣第二次，只有大单要扣了
        due_bill_no = "DN" + self.item_no
        self.lzhyqj_mock.mock_lanzhou_haoyue_qinjia_repay_trial(due_bill_no, prin_amt=344.36, int_amt=2.12)
        asset_tran_amount_p12 = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 12)
        params_combo_active = {
            "project_num_loan_channel_amount": int(asset_tran_amount_p12["asset_tran_balance_amount"]),
            "project_num_no_loan": None
        }
        resp_two, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_two['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_two}"
        order_no_one = resp_one["data"]["project_list"][1]["order_no"]  # 1-11期 大单
        order_no_p12_capital = resp_two["content"]["data"]["project_list"][0]["order_no"]  # 12期 大单



        self.run_all_task_after_repay_success()

        # 检查大单的代扣
        # 第1单 资方扣 12期本+100利息+费
        param_loan_one = {
            "withhold_amount": int(asset_tran_amount["asset_tran_amount"]),
            "asset_tran_amount": int(asset_tran_amount["asset_tran_amount"]),
            "withhold_channel": "baidu_tq3_quick"
        }
        check_withhold_by_serial_no(order_no_one, **param_loan_one)
        # 第2单资方扣第12期整期费用
        param_loan_p12_capital = {
            "withhold_amount": int(asset_tran_amount_p12["asset_tran_balance_amount"]),
            "asset_tran_amount": int(asset_tran_amount_p12["asset_tran_balance_amount"]),
            "withhold_channel": self.loan_channel,
            "withhold_sign_company": 'qjhy'
        }
        check_withhold_by_serial_no(order_no_p12_capital, **param_loan_p12_capital)

        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "withhold_sign_company": self.our_sign_company,
            "withhold_channel": "baidu_tq3_quick"
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        withhold_one = get_withhold_by_serial_no(order_no_one)
        withhold_two = get_withhold_by_serial_no(order_no_p12_capital)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_one[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_two[0]['withhold_channel_key'], start_period=12)
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)
