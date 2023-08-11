# -*- coding: utf-8 -*-
from biztest.util.tools.tools import *
import pytest

from biztest.case.rbiz.base_repay_test import BaseRepayTest

from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config
from biztest.function.biz.biz_check_function import check_capital_push_request_log, check_capital_notify, check_data
from biztest.function.biz.biz_db_function import get_capital_notify_req_data_param_by_item_no, \
    get_capital_notify_req_data_by_item_no
from biztest.function.rbiz.rbiz_check_function import check_withhold_request_log, check_withhold_result_without_split, \
    check_account_recharge_and_repay, check_asset_tran_repay_one_period, check_withhold_split_count_by_request_no, \
    check_withhold_split_count_by_item_no_and_request_no, check_asset_tran_payoff, check_withhold_by_serial_no, \
    check_settle_payoff_capital_withhold_detail_vs_asset_tran, check_capital_withhold_detail_vs_asset_tran, \
    check_withhold_data_by_sn, check_withhold_sign_company
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    get_withhold_by_item_no
from biztest.interface.rbiz.rbiz_interface import monitor_check
from biztest.util.easymock.rbiz.yilian_dingfeng import RepayYilianDingfengMock
from biztest.util.easymock.rbiz.zhongke_hegang import RepayZhongkeHegangMock
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.util.tools.tools import get_four_element
import common.global_const as gc


class TestRbizYilianDingfeng(BaseRepayTest):
    """
    yilian_dingfeng 还款

    """
    loan_channel = "yilian_dingfeng"
    exp_sign_company_no_loan = "tq,tqa,tqb"
    grant_principal = 400000
    one_interest = 2833
    one_fee = 2926

    @classmethod
    def setup_class(cls):
        monitor_check()
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        cls.yldf_mock = RepayYilianDingfengMock(rbiz_mock)
        cls.task = Task("rbiz%s" % gc.ENV)
        cls.msg = Msg("rbiz%s" % gc.ENV)

    def setup_method(self):
        # 大小单进件
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element,
                                                                               asset_amount=4000)
        print("set up method")

    @pytest.mark.rbiz_auto_test
    @pytest.mark.yldf
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
    @pytest.mark.yldf
    def test_active_normal_repay(self):
        """
        正常还1期，
        资方扣1单，我方扣1单，小单1单
        """
        # step 1 主动还款 到期日
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()

        # step 2 数据检查，检查推给资金方的日志
        check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel, "execute_combine_withhold",
                                   withhold[0]['withhold_serial_no'], 5)

        # step 3 数据检查，大单1单 小单1单
        # 资方代扣金额 = 第1期本金 利息 技术服务费
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        order_no_capital = withhold[0]['withhold_serial_no']
        order_no_our = withhold[1]['withhold_serial_no']
        capital_withhold_amount = 37814
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - capital_withhold_amount
        # 代扣顺序： 资方先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[0]["withhold_request_no"], 2)
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        capital_withhold = {
            "withhold_sign_company": "dingfeng",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        capital_withhold_type = ['repayprincipal', 'repayinterest', 'technical_service']
        check_capital_withhold_detail_vs_asset_tran(order_no_capital, capital_withhold_type)
        # 检查我方代扣部分
        our_withhold = {
            "withhold_sign_company": self.exp_sign_company_no_loan,
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_withhold_amount
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)

        # 小单代扣数据检查
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_repay_one_period(self.item_no)

        # 处理推送部分
        # "trancode": "QLZS000000108",
        # "transerno": "KN10001202205121645034694e9e8dae",
        self.yldf_mock.mock_yilian_dingfeng_normal_repay_notice(self.item_no, "KN10001" + self.item_no)
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "YilianDingfengCapitalPush")
        # # 检查推送请求的参数
        capital_notify_param = get_capital_notify_req_data_param_by_item_no(self.item_no)
        print("capital_notify_param: ", capital_notify_param)
        time.sleep(5)
        check_capital_push_request_log(self.item_no, self.loan_channel, "YilianDingfengCapitalPush",
                                       capital_notify_info=capital_notify_param)
        # check 数据 todo

    @pytest.mark.rbiz_auto_test
    @pytest.mark.yldf
    def test_active_advance_settle_payoff(self):
        """
        在第一期内提前结清
        """
        self.change_asset_due_at(0, -10)
        due_bill_no = "DN" + self.item_no
        self.yldf_mock.mock_yilian_dingfeng_repay_trial(due_bill_no, prin_amt=4000)
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()

        # # step 2 数据检查，检查推给资金方的日志
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
            "withhold_sign_company": "dingfeng",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": self.grant_principal + 1000 + self.one_fee,
            "asset_tran_amount": self.grant_principal + self.one_interest + self.one_fee
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
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


        # 推送时有增加利息，capital_transaction有贴息
        self.yldf_mock.mock_yilian_dingfeng_repay_trial(due_bill_no, prin_amt=4000, int_amt=11.5)
        self.yldf_mock.mock_yilian_dingfeng_settle_repay_notice(self.item_no, "KN10001" + self.item_no)
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "YilianDingfengCapitalPush")
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
                   indeedservicefee='29.26', indeedtotal='4040.76')
        time.sleep(5)
        check_capital_push_request_log(self.item_no, self.loan_channel + "_advance_payoff", "YilianDingfengCapitalPush",
                                       capital_notify_info=capital_notify_param)
