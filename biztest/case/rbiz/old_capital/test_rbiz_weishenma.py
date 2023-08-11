# -*- coding: utf-8 -*-
import pytest

from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config
from biztest.function.rbiz.rbiz_check_function import check_withhold_split_count_by_request_no, \
    check_withhold_order_by_order_no, check_withhold_split_count_by_item_no_and_request_no, \
    check_withhold_sign_company, \
    check_withhold_by_serial_no, check_capital_withhold_detail_vs_asset_tran, check_withhold_result_without_split, \
    check_account_recharge_and_repay, check_asset_tran_repay_one_period, check_json_rs_data, check_data, \
    check_settle_payoff_capital_withhold_detail_vs_asset_tran, check_asset_tran_payoff, check_withhold_data_by_sn, \
    check_card_bind_info, check_task_by_order_no_and_type
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    get_withhold_by_item_no, get_withhold_by_serial_no, \
    get_asset_tran_balance_amount_by_item_no_and_type, update_card_bind_update_at_by_card_number, \
    update_asset_tran_status_by_item_no_and_period, wait_expect_task_appear
from biztest.interface.rbiz.rbiz_interface import simple_active_repay, bind_sms, manual_withhold, fox_manual_withhold, \
    weishenma_daxinganling_callback, paysvr_callback, run_withholdAutoV1_by_api, monitor_check
from biztest.util.easymock.rbiz.paysvr import PaysvrMock
from biztest.util.easymock.rbiz.weishenma_daxinganling import RepayWeishenmaMock
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
import common.global_const as gc
from biztest.util.tools.tools import get_four_element


class TestRbizWeishenma(BaseRepayTest):
    """
    微神马 repay
    """

    loan_channel = "weishenma_daxinganling"
    principal_amount = 800000
    trail_interest_amount = 100
    first_period_amount = 69037

    @classmethod
    def setup_class(cls):
        monitor_check()
        # 更新kv
        update_repay_weishenma_config(mock_project['rbiz_auto_test']['id'])
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        cls.paysvr_mock = PaysvrMock(rbiz_mock)
        cls.wsmmock = RepayWeishenmaMock(rbiz_mock)
        cls.task = Task("rbiz{0}".format(gc.ENV))
        cls.msg = Msg("rbiz{0}".format(gc.ENV))

    def setup_method(self):
        self.paysvr_mock.update_query_protocol_channels_bind_sms()
        self.paysvr_mock.update_auto_pay_withhold_process()
        self.paysvr_mock.update_withhold_query(2)
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_active_advance_repay(self):
        """
        提前还1期，本息资方，费我方
        """
        # step 1 主动还款
        self.wsmmock.active_repay_apply_success(self.item_no, "1")
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        resp_combo_active = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_no_capital = resp_combo_active["data"]["project_list"][0]["order_no"]
        order_no_our = resp_combo_active["data"]["project_list"][1]["order_no"]
        capital_amount = self.first_period_amount
        self.wsmmock.update_active_repay_query("1", str(capital_amount))

        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        # step 3 验证数据
        withhold = get_withhold_by_item_no(self.item_no)
        # 拆成3单代扣
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)
        # 资方代扣金额 = 第1期本金+占用天数利息
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - capital_amount
        # 代扣顺序： 资方先扣
        check_withhold_order_by_order_no(order_no_capital, self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, None)
        #  检查资方代扣表   资方通道sign_company为空
        capital_withhold = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_amount,
            "asset_tran_amount": capital_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        # 检查资方代扣明细 还1期的金额，withhold_detail里面的3个金额是一样的
        check_capital_withhold_detail_vs_asset_tran(order_no_capital)
        # 检查我方代扣表
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
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
        # 检查 asset_tran 第1期结清
        check_asset_tran_repay_one_period(self.item_no)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_active_normal_repay(self):
        """
        微神马到期日主动还款
        """
        # step 1 还款
        self.wsmmock.active_repay_apply_success(self.item_no, "1")
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        capital_amount = self.first_period_amount
        self.wsmmock.update_active_repay_query("1", str(capital_amount))
        resp_combo_active = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_no_capital = resp_combo_active["data"]["project_list"][0]["order_no"]
        order_no_our = resp_combo_active["data"]["project_list"][1]["order_no"]
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        # step 2 验证数据
        withhold = get_withhold_by_item_no(self.item_no)
        # 拆成2单代扣
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)
        # 资方代扣金额 = 第1期本金+第1期整期利息
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - capital_amount
        # 代扣顺序： 资方先扣
        check_withhold_order_by_order_no(order_no_capital, self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, None)
        #  检查资方代扣表   资方通道sign_company为空
        capital_withhold = {"withhold_sign_company": None,
                            "withhold_channel": self.loan_channel,
                            "withhold_status": "success",
                            "withhold_amount": capital_amount,
                            "asset_tran_amount": capital_amount}
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        # 检查资方代扣明细 还1期的金额，withhold_detail里面的3个金额是一样的
        check_capital_withhold_detail_vs_asset_tran(order_no_capital)
        # 检查我方代扣表
        our_withhold = {"withhold_sign_company": "tq,tqa,tqb",
                        "withhold_channel": "baidu_tq3_quick",
                        "withhold_status": "success",
                        "withhold_amount": our_withhold_amount,
                        "asset_tran_amount": our_withhold_amount}
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
        # 检查 asset_tran 第1期结清
        check_asset_tran_repay_one_period(self.item_no)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_normal_fail_switch_paysvr_repay(self):
        """
        到期日走资方失败，切我方
        """
        self.wsmmock.active_repay_apply_success(self.item_no, "1")
        capital_amount = self.first_period_amount
        self.wsmmock.update_active_repay_query("2", capital_amount)

        # 修改资产到期日
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        # 发起主动代扣
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)
        order_no = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        withhold = get_withhold_by_serial_no(order_no)
        check_data(withhold[0], withhold_channel=self.loan_channel)
        order_list = [project["order_no"] for project in resp_combo_active['content']["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 3)
        self.run_task_after_withhold_callback(order_list)

        # 再次发起主动代扣
        self.wsmmock.update_active_repay_query("1", capital_amount)
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)
        order_no = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        order_no_no_loan = resp_combo_active['content']["data"]["project_list"][1]["order_no"]
        self.run_all_task_after_repay_success()
        # step 2 检查数据
        withhold = get_withhold_by_serial_no(order_no)
        withhold_no_loan = get_withhold_by_serial_no(order_no_no_loan)
        # 拆成2单代扣
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        # 大单代扣数据检查
        param_loan = {
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
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

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_active_overdue_repay(self):
        """
        逾期还款1期
        """
        # step 1 还款
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 2 逾期数据检查，大单1单小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        # 拆成2单代扣
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        param_loan = {
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

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_active_advance_settle_payoff(self):
        """
        提前结清
        """
        # 修改资产到期日
        self.wsmmock.early_settle_apply_success(self.item_no, 1)
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        # mock微神马代扣成功
        amount_interest = \
            get_asset_tran_balance_amount_by_item_no_and_type(self.item_no, "repayinterest", 1)[
                "asset_tran_balance_amount"]
        capital_withhold_amount = self.principal_amount + self.trail_interest_amount
        our_withhold_amount = int(int(asset_tran_amount["asset_tran_amount"]) - int(capital_withhold_amount))
        asset_amount = self.principal_amount + int(amount_interest)
        self.wsmmock.update_active_settle_trail(self.principal_amount, capital_withhold_amount)
        self.wsmmock.update_active_repay_query("1", str(capital_withhold_amount))

        resp_combo_active = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 3 验证数据
        order_no_capital = resp_combo_active["data"]["project_list"][0]["order_no"]
        order_no_our = resp_combo_active["data"]["project_list"][1]["order_no"]
        withhold = get_withhold_by_item_no(self.item_no)
        #  代扣顺序： 资方先扣
        check_data(withhold[0], withhold_channel=self.loan_channel)
        # 拆成2单代扣
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)
        # 资方代扣金额 = 第1期本金+占用天数利息
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, None)
        #  还1期的金额，withhold_detail里面的3个金额是一样的
        capital_withhold = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": asset_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        check_settle_payoff_capital_withhold_detail_vs_asset_tran(order_no_capital, self.trail_interest_amount)
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_withhold_amount + self.trail_interest_amount
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

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_active_normal_settle_payoff(self):
        """
        到期日提前结清 不允许
        """
        # step 1 还款
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_combo_active = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan, 1)
        check_json_rs_data(resp_combo_active, message=f"资产[{self.item_no}],到期日当天不允许结清")

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_capital_sign_repay(self):
        """
        该测试用例涉及了还款签约的流程
        :return:
        """
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        # mock微神马代扣成功
        self.wsmmock.update_active_repay_query("1", self.first_period_amount)
        self.wsmmock.active_repay_apply_success(self.item_no, "1")
        # 发起主动代扣
        params_combo_active = {

            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]

        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)

        order_no = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        verify_seq = bind_sms(order_no)
        params_combo_active.update(order_no=order_no, verify_seq=verify_seq, verify_code='123456')
        resp_combo_active_bind_card, req_body_bind_card = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active_bind_card['content'], code=0)
        order_no = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        check_withhold_data_by_sn(order_no, withhold_channel=self.loan_channel)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        card_bind = {
            "card_bind_serial_no": order_no,
            "card_bind_channel": "weishenma_daxinganling_sign",
            "card_bind_status": "success"
        }

        check_card_bind_info(self.four_element['data']["bank_code_encrypt"], **card_bind)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_capital_sign_two_times(self):
        """
        该测试用例涉及了在期限内还款2次，应签约2次，资方1次，我方1次
        :return:
        """
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        # 发起主动代扣
        params_combo_active = {

            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]

        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)

        # mock微神马代扣失败
        self.wsmmock.update_active_repay_query("2", self.first_period_amount)
        self.wsmmock.active_repay_apply_success(self.item_no, "1")
        self.paysvr_mock.update_withhold_bind_query_success()

        order_no = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        verify_seq = bind_sms(order_no)
        params_combo_active.update(order_no=order_no, verify_seq=verify_seq, verify_code='123456')
        resp_combo_active_bind_card, req_body_bind_card = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active_bind_card['content'], code=0)
        order_no = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        withhold = get_withhold_by_serial_no(order_no)
        check_data(withhold[0], withhold_channel=self.loan_channel)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)
        self.wsmmock.update_active_repay_query("1", self.first_period_amount)
        print("--------------------第二次发起代扣----------------------------")
        params_combo_active.update(order_no="", verify_seq="", verify_code='')
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)
        order_no = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        verify_seq = bind_sms(order_no)
        params_combo_active.update(order_no=order_no, verify_seq=verify_seq, verify_code='123456')
        resp_combo_active_bind_card, req_body_bind_card = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active_bind_card['content'], code=0)

        order_no = resp_combo_active_bind_card['content']["data"]["project_list"][0]["order_no"]
        self.run_all_task_after_repay_success()
        print("--------------------检查签约情况----------------------------")
        # 第二次走到paysvr签约了
        card_bind = {
            "card_bind_serial_no": order_no,
            "card_bind_channel": "baofoo_tq4_protocol",
            "card_bind_status": "success"
        }

        check_card_bind_info(self.four_element['data']["bank_code_encrypt"], **card_bind)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_capital_sign_bind_card_expiry_days(self):
        """
        该测试用例涉及了签约绑卡期限验证
        :return:
        """
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        # 发起主动代扣
        params_combo_active = {

            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]

        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)

        # 绑卡和代扣
        self.wsmmock.update_active_repay_query("2", self.first_period_amount)
        self.wsmmock.active_repay_apply_success(self.item_no, "1")

        order_no = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        verify_seq = bind_sms(order_no)
        params_combo_active.update(order_no=order_no, verify_seq=verify_seq, verify_code='123456')
        resp_combo_active_bind_card, req_body_bind_card = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active_bind_card['content'], code=0)
        withhold = get_withhold_by_item_no(self.item_no)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)
        # 修改card_bind_update_at为一个月前，配置中是7天过期，因此第二次代扣仍会调资方签约
        update_card_bind_update_at_by_card_number(self.four_element['data']["bank_code_encrypt"])
        self.wsmmock.update_active_repay_query("1", self.first_period_amount)
        # 第二次发起代扣
        params_combo_active.update(order_no="", verify_seq="", verify_code='')
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)
        order_no = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        verify_seq = bind_sms(order_no)
        params_combo_active.update(order_no=order_no, verify_seq=verify_seq, verify_code='123456')
        resp_combo_active_bind_card, req_body_bind_card = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active_bind_card['content'], code=0)

        order_no = resp_combo_active_bind_card['content']["data"]["project_list"][0]["order_no"]
        order_no_no_loan = resp_combo_active_bind_card['content']["data"]["project_list"][1]["order_no"]
        self.run_all_task_after_repay_success()

        # 第二次走到paysvr签约了
        card_bind = {
            "card_bind_serial_no": order_no,
            "card_bind_channel": "weishenma_daxinganling_sign",
            "card_bind_status": "success"
        }
        check_card_bind_info(self.four_element['data']["bank_code_encrypt"], **card_bind)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_manual_overdue_repay(self):
        """
        该测试用例涉及了逾期手动代扣，资产逾期后，由paysvr代扣，收罚息
        :return:
        """
        # 修改大小单还款时间
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)

        # 发起manual代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        params_manual = {
            "card_num_encrypt": self.four_element['data']["bank_code_encrypt"],
            "card_user_phone_encrypt": self.four_element['data']["phone_number_encrypt"],
            "card_user_id_encrypt": self.four_element['data']["id_number_encrypt"],
            "card_user_name_encrypt": self.four_element['data']["user_name_encrypt"],
            "project_num": self.item_no,
            "amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "period": ""

        }
        resp_manual, req_body = manual_withhold(**params_manual)
        assert resp_manual['content']['code'] == 0, f"manual接口代扣失败,req_body={req_body},resp_manual={resp_manual}"

        self.run_all_task_after_repay_success()

        # step 3 逾期数据检查，大单1单
        withhold = get_withhold_by_item_no(self.item_no)
        # 只检查大单代扣情况
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 1)
        param_loan = {
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_manual_normal_repay(self):
        """
        该测试用例涉及了到期日手动代扣，资产拆为2单，本息由资方扣，剩余费由我方扣
        :return:
        """
        self.change_asset_due_at(-1, 0)
        self.refresh_late_fee(self.item_no)

        # 发起manual代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        capital_amount = self.first_period_amount
        self.wsmmock.update_active_repay_query("1", str(capital_amount))
        self.wsmmock.active_repay_apply_success(self.item_no, "1")
        params_manual = {
            "card_num_encrypt": self.four_element['data']["bank_code_encrypt"],
            "card_user_phone_encrypt": self.four_element['data']["phone_number_encrypt"],
            "card_user_id_encrypt": self.four_element['data']["id_number_encrypt"],
            "card_user_name_encrypt": self.four_element['data']["user_name_encrypt"],
            "project_num": self.item_no,
            "amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "period": ""

        }
        resp_manual, req_body = manual_withhold(**params_manual)
        assert resp_manual['content']['code'] == 0, f"manual接口代扣失败,req_body={req_body},resp_manual={resp_manual}"

        withhold = get_withhold_by_item_no(self.item_no)
        self.run_all_task_after_repay_success()
        # step 3 验证数据
        # 拆成2单代扣
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        # 资方代扣金额 = 第1期本金+第1期整期利息
        withhold = get_withhold_by_item_no(self.item_no)
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - capital_amount
        # 代扣顺序： 资方先扣
        check_withhold_order_by_order_no(withhold[0]["withhold_serial_no"], self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(withhold[0]["withhold_serial_no"], None)
        check_withhold_sign_company(withhold[1]["withhold_serial_no"], 'tq,tqa,tqb')
        #  检查资方代扣表   资方通道sign_company为空
        capital_withhold = {"withhold_sign_company": None,
                            "withhold_channel": self.loan_channel,
                            "withhold_status": "success",
                            "withhold_amount": capital_amount,
                            "asset_tran_amount": capital_amount}
        check_withhold_by_serial_no(withhold[0]["withhold_serial_no"], **capital_withhold)
        # 检查资方代扣明细 还1期的金额，withhold_detail里面的3个金额是一样的
        check_capital_withhold_detail_vs_asset_tran(withhold[0]["withhold_serial_no"])
        # 检查我方代扣表
        our_withhold = {"withhold_sign_company": "tq,tqa,tqb",
                        "withhold_channel": "baidu_tq3_quick",
                        "withhold_status": "success",
                        "withhold_amount": our_withhold_amount,
                        "asset_tran_amount": our_withhold_amount}
        check_withhold_by_serial_no(withhold[1]["withhold_serial_no"], **our_withhold)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'])
        # 检查 asset_tran 第1期结清
        check_asset_tran_repay_one_period(self.item_no)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_active_overdue_one_day_settle_payoff(self):
        """
        逾期第1天提前结清，砍单，只扣第1期
        """
        # step 1 还款
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 2 验证数据
        # 第1期代扣成功
        withhold = get_withhold_by_item_no(self.item_no)
        asset_tran_amount_first_period = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no,
                                                                                             1)
        # 只检查大单代扣情况
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        param_loan = {
            "withhold_amount": int(asset_tran_amount_first_period["asset_tran_amount"])
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_fox_overdue_one_day_settle_payoff(self):
        """
        fox代扣 逾期1天+提前结清
        这是一个线上问题，逾期部分拆给了微神马
        """
        # step 1 还款
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)

        params_fox = {
            "customer_bank_card_encrypt": self.four_element['data']["bank_code_encrypt"],
            "customer_mobile_encrypt": self.four_element['data']["phone_number_encrypt"],
            "asset_item_no": self.item_no,
            "amount": asset_tran_amount['asset_tran_amount'],
            "asset_period": None

        }
        resp_fox_manual, req_body_fox_manual = fox_manual_withhold(**params_fox)
        assert resp_fox_manual['content']['code'] == 1, \
            f"manual代扣失败,resp_fox_manual={resp_fox_manual},req_body_fox_manual={req_body_fox_manual}"

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_fox_overdue_repay(self):
        """
        该测试用例涉及了逾期手动代扣，资产逾期后，由paysvr代扣，收罚息
        :return:
        """
        # step 1 还款
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)

        # 发起manual代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        params_fox = {
            "customer_bank_card_encrypt": self.four_element['data']["bank_code_encrypt"],
            "customer_mobile_encrypt": self.four_element['data']["phone_number_encrypt"],
            "asset_item_no": self.item_no,
            "amount": asset_tran_amount['asset_tran_amount'],
            "asset_period": 1

        }
        resp_fox_manual, req_body_fox_manual = fox_manual_withhold(**params_fox)
        assert resp_fox_manual['content']['code'] == 2, \
            f"manual代扣失败,resp_fox_manual={resp_fox_manual},req_body_fox_manual={req_body_fox_manual}"

        self.run_all_task_after_repay_success()

        # step 3 逾期数据检查，大单1单
        withhold = get_withhold_by_item_no(self.item_no)
        # 只检查大单代扣情况
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 1)
        param_loan = {
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_fox_normal_repay(self):
        """
        该测试用例涉及了到期日手动代扣，资产拆为2单，本息由资方扣，剩余费由我方扣
        :return:
        """
        # step 1 还款
        self.change_asset_due_at(-1, 0)
        # 发起manual代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        capital_amount = self.first_period_amount
        self.wsmmock.update_active_repay_query("1", str(capital_amount))
        self.wsmmock.active_repay_apply_success(self.item_no, "1")

        # 发起fox代扣
        params_fox = {
            "customer_bank_card_encrypt": self.four_element['data']["bank_code_encrypt"],
            "customer_mobile_encrypt": self.four_element['data']["phone_number_encrypt"],
            "asset_item_no": self.item_no,
            "amount": asset_tran_amount['asset_tran_amount'],
            "asset_period": 1

        }
        resp_fox_manual, req_body_fox_manual = fox_manual_withhold(**params_fox)
        assert resp_fox_manual['content']['code'] == 2, \
            f"manual代扣失败,resp_fox_manual={resp_fox_manual},req_body_fox_manual={req_body_fox_manual}"
        self.run_all_task_after_repay_success()
        withhold = get_withhold_by_item_no(self.item_no)
        # step 3 验证数据
        # 拆成2单代扣
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        # 资方代扣金额 = 第1期本金+第1期整期利息
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - capital_amount
        # 代扣顺序： 资方先扣
        check_withhold_order_by_order_no(withhold[0]["withhold_serial_no"], self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(withhold[0]["withhold_serial_no"], None)
        check_withhold_sign_company(withhold[1]["withhold_serial_no"], 'tq,tqa,tqb')
        #  检查资方代扣表   资方通道sign_company为空
        capital_withhold = {"withhold_sign_company": None,
                            "withhold_channel": self.loan_channel,
                            "withhold_status": "success",
                            "withhold_amount": capital_amount,
                            "asset_tran_amount": capital_amount}
        check_withhold_by_serial_no(withhold[0]["withhold_serial_no"], **capital_withhold)
        # 检查资方代扣明细 还1期的金额，withhold_detail里面的3个金额是一样的
        check_capital_withhold_detail_vs_asset_tran(withhold[0]["withhold_serial_no"])
        # 检查我方代扣表
        our_withhold = {"withhold_sign_company": "tq,tqa,tqb",
                        "withhold_channel": "baidu_tq3_quick",
                        "withhold_status": "success",
                        "withhold_amount": our_withhold_amount,
                        "asset_tran_amount": our_withhold_amount}
        check_withhold_by_serial_no(withhold[1]["withhold_serial_no"], **our_withhold)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'])
        # 检查 asset_tran 第1期结清
        check_asset_tran_repay_one_period(self.item_no)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_fox_normal_settle_payoff(self):
        """
        fox代扣。到期日提前结清，不允许
        """
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)

        # 发起fox代扣
        params_fox = {
            "customer_bank_card_encrypt": self.four_element['data']["bank_code_encrypt"],
            "customer_mobile_encrypt": self.four_element['data']["phone_number_encrypt"],
            "asset_item_no": self.item_no,
            "amount": asset_tran_amount['asset_tran_amount'],
            "asset_period": None

        }
        resp_fox_manual, req_body_fox_manual = fox_manual_withhold(**params_fox)

        assert resp_fox_manual['content']['code'] == 1, \
            f"manual接口代扣失败,req_body={req_body_fox_manual},resp_fox_manual={resp_fox_manual}"
        assert resp_fox_manual['content']['message'] == f"资产[{self.item_no}],到期日当天不允许结清", \
            f"手动代扣失败,req_body={req_body_fox_manual},resp_manual={resp_fox_manual}"

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_manual_normal_settle_payoff(self):
        """
        manual代扣，到期日提前结清，不允许
        """
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)

        params_manual = {
            "card_num_encrypt": self.four_element['data']["bank_code_encrypt"],
            "card_user_phone_encrypt": self.four_element['data']["phone_number_encrypt"],
            "card_user_id_encrypt": self.four_element['data']["id_number_encrypt"],
            "card_user_name_encrypt": self.four_element['data']["user_name_encrypt"],
            "project_num": self.item_no,
            "no_loan_no": self.item_num_no_loan,
            "no_loan_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "period": ""

        }
        resp_manual, req_body = manual_withhold(**params_manual)

        assert resp_manual['content']['code'] == 1, \
            f"manual接口代扣失败,req_body={req_body},resp_manual={resp_manual}"
        assert resp_manual['content']['message'] == f"资产[{self.item_no}],到期日当天不允许结清", \
            f"手动代扣失败,req_body={req_body},resp_manual={resp_manual}"

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_active_advance_repay_fail_still_capital(self):
        """
        提前还1期 走资方失败 仍走资方 不切我方
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(0, -10)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        # step 2 发起主动代扣 走资方失败
        capital_amount = self.first_period_amount
        self.wsmmock.update_active_repay_query("2", capital_amount)
        self.wsmmock.active_repay_apply_success(self.item_no, "1")
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)
        order_no = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        withhold_once = check_withhold_data_by_sn(order_no, withhold_channel=self.loan_channel)
        self.task.run_task(withhold_once[0]['withhold_request_no'], 'execute_combine_withhold')
        self.task.run_task(withhold_once[0]['withhold_request_no'], 'execute_combine_withhold')

        # step 3 发起主动代扣第二次 提前还款不切
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)
        order_no_capital_twice = resp_combo_active_twice['content']["data"]["project_list"][0]["order_no"]
        order_no_twice = resp_combo_active_twice['content']["data"]["project_list"][1]["order_no"]
        order_no_no_loan_twice = resp_combo_active_twice['content']["data"]["project_list"][2]["order_no"]
        withhold_twice = check_withhold_data_by_sn(order_no_capital_twice, withhold_channel=self.loan_channel)
        self.task.run_task(withhold_twice[0]['withhold_request_no'], 'execute_combine_withhold')
        self.task.run_task(withhold_twice[0]['withhold_request_no'], 'execute_combine_withhold')
        check_withhold_sign_company(order_no_capital_twice, None)
        check_withhold_sign_company(order_no_no_loan_twice, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_twice, 'tq,tqa,tqb')

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_active_advance_payoff_fail_still_capital(self):
        """
        提前结清 走资方失败 仍走资方 不切我方
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(0, -10)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        # step 2 发起主动代扣 走资方失败

        self.wsmmock.early_settle_apply_success(self.item_no, 1)
        capital_amount = self.principal_amount + self.trail_interest_amount
        self.wsmmock.update_active_settle_trail(self.principal_amount, capital_amount)
        self.wsmmock.update_active_repay_query("2", capital_amount)

        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)
        order_no = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        withhold = get_withhold_by_serial_no(order_no)
        check_withhold_order_by_order_no(order_no, self.loan_channel)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)

        # step 3 发起主动代扣第二次 提前还款不切我方
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)
        order_no_capital_twice = resp_combo_active_twice['content']["data"]["project_list"][0]["order_no"]
        order_no_twice = resp_combo_active_twice['content']["data"]["project_list"][1]["order_no"]
        order_no_no_loan_twice = resp_combo_active_twice['content']["data"]["project_list"][2]["order_no"]
        check_withhold_order_by_order_no(order_no_capital_twice, self.loan_channel)
        check_withhold_sign_company(order_no_capital_twice, None)
        check_withhold_sign_company(order_no_no_loan_twice, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_twice, 'tq,tqa,tqb')

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_active_normal_last_period_last_day(self):
        """
        最后一期到期日为今天
        """
        # Step 1：还款 最后一期的最后一天  为提前还款
        self.wsmmock.active_repay_apply_success(self.item_no, "12")
        capital_amount = self.first_period_amount
        self.wsmmock.update_active_repay_query("1", capital_amount)
        self.change_asset_due_at(-12, 0)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        update_asset_tran_status_by_item_no_and_period(self.item_no)
        update_asset_tran_status_by_item_no_and_period(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        # Step 2：检查数据
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        order_no_capital = withhold[0]["withhold_serial_no"]
        order_no_our = withhold[1]["withhold_serial_no"]

        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - capital_amount
        # 代扣顺序： 资方先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel, withhold_status='success',
                                  withhold_order=2)
        check_withhold_data_by_sn(order_no_our, withhold_status='success', withhold_order=4)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, None)
        #  还1期的金额，withhold_detail里面的3个金额是一样的
        capital_withhold = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_amount,
            "asset_tran_amount": capital_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)

        # 检查我方代扣部分
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_withhold_amount
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        # 检查小单代扣部分
        no_loan_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "asset_tran_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        check_withhold_by_serial_no(withhold_no_loan[0]["withhold_serial_no"], **no_loan_withhold)

        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'],
                                         12)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'],
                                         12)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'], 12)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_active_normal_last_period_advance_day(self):
        """
        最后一期到期日为昨天
        """
        # Step 1：还款 最后一期为提前结清
        self.change_asset_due_at(-12, 10)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        update_asset_tran_status_by_item_no_and_period(self.item_no)
        update_asset_tran_status_by_item_no_and_period(self.item_num_no_loan)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)

        # 各种代扣金额 试算利息1元
        self.wsmmock.early_settle_apply_success(self.item_no, 12)
        principal_amount = int(get_asset_tran_balance_amount_by_item_no_and_type(self.item_no, "repayprincipal", 12)[
                                   "asset_tran_balance_amount"])  # 最后一期本金
        capital_amount = principal_amount + self.trail_interest_amount  # 本+1元利息
        capital_asset_tran_amount = self.first_period_amount  # 本+全额利息
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - capital_amount
        our_asset_tran_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - principal_amount
        self.wsmmock.update_active_settle_trail(principal_amount, capital_amount)
        self.wsmmock.update_active_repay_query("1", capital_amount)

        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        # Step 2：检查数据
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        order_no_capital = withhold[0]["withhold_serial_no"]
        order_no_our = withhold[1]["withhold_serial_no"]

        # 代扣顺序： 资方先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel, withhold_status='success',
                                  withhold_order=2)
        check_withhold_data_by_sn(order_no_our, withhold_status='success', withhold_order=4)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, None)
        #  还1期的金额，withhold_detail里面的3个金额是一样的
        capital_withhold = {
            "withhold_sign_company": None,
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_amount,
            "asset_tran_amount": capital_asset_tran_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)

        # 检查我方代扣部分
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_asset_tran_amount
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        # 检查小单代扣部分
        no_loan_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "asset_tran_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        check_withhold_by_serial_no(withhold_no_loan[0]["withhold_serial_no"], **no_loan_withhold)

        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'],
                                         12)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'],
                                         12)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'], 12)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.weishenma
    def test_auto_normal_repay(self):
        # step 1 发起自动代扣
        self.change_asset_due_at(-1, 0)
        run_withholdAutoV1_by_api(self.item_no)
        wait_expect_task_appear(self.item_no, 'auto_withhold_execute')
        check_task_by_order_no_and_type(self.item_no, 'auto_withhold_execute', task_status='open')
        self.task.run_task(self.item_no, 'auto_withhold_execute')
        self.get_auto_withhold_execute_task_run(self.item_no)
        withhold = get_withhold_by_item_no(self.item_no)
        weishenma_daxinganling_callback(withhold[0]['withhold_serial_no'], self.item_no, withhold[0]['withhold_amount'],
                                        'error')
        paysvr_callback(withhold[1]['withhold_serial_no'], 3)
