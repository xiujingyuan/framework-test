# -*- coding: utf-8 -*-
import pytest

from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.easymock.easymock_config import rbiz_mock, mock_project
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config
from biztest.function.rbiz.rbiz_check_function import check_asset_tran_repay_one_period, \
    check_withhold_result_without_split, check_withhold_split_count_by_item_no_and_request_no, \
    check_account_recharge_and_repay, check_withhold_sign_company, check_withhold_split_count_by_request_no, \
    check_asset_tran_payoff, check_json_rs_data, check_withhold_order_by_order_no
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    get_withhold_by_item_no, get_qinnong_reserve_amount
from biztest.interface.rbiz.rbiz_interface import refresh_late_fee, run_withholdAutoV1_by_api, fox_manual_withhold, \
    simple_active_repay, monitor_check
from biztest.util.easymock.rbiz.paysvr import PaysvrMock
from biztest.util.easymock.rbiz.qinnong import RepayQinnongMock

from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
import common.global_const as gc
from biztest.util.tools.tools import get_four_element


class TestRbizQinnong(BaseRepayTest):
    """
     秦农还款
    """
    loan_channel = "qinnong"
    principal_amount = 800000
    first_principal_amount = 64317
    trail_interest_amount = 5000

    @classmethod
    def setup_class(cls):
        monitor_check()
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        cls.paysvr_mock = PaysvrMock(rbiz_mock)
        cls.qinnong_mock = RepayQinnongMock(rbiz_mock)
        cls.task = Task("rbiz{0}".format(gc.ENV))
        cls.msg = Msg("rbiz{0}".format(gc.ENV))

    def setup_method(self):
        self.paysvr_mock.update_query_protocol_channels_bind_sms()
        self.paysvr_mock.update_auto_pay_withhold_process()
        self.paysvr_mock.update_withhold_query(2)
        self.qinnong_mock.update_repay_trail(self.principal_amount, self.trail_interest_amount)
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = \
            asset_import_and_loan_to_success(self.loan_channel, self.four_element)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.qinnong
    def test_active_advance_repay(self):
        """
        提前还1期
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)

        # step 3 执行task和msg
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
        check_withhold_sign_company(order_no_no_loan, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no, 'tq,tqa,tqb')
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

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.qinnong
    def test_active_normal_repay(self):
        """
        正常还1期
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)

        # step 3 执行task和msg
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
        check_withhold_sign_company(order_no_no_loan, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no, 'tq,tqa,tqb')
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

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.qinnong
    def test_active_overdue_repay(self):
        """
        逾期还1期
        """
        # step 1 修改资产到期日 刷罚息
        self.change_asset_due_at(-1, -1)
        refresh_late_fee(self.item_no)
        refresh_late_fee(self.item_num_no_loan)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)

        # step 3 执行task和msg
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
        check_withhold_sign_company(order_no_no_loan, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no, 'tq,tqa,tqb')
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

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.qinnong
    def test_active_advance_settle_payoff(self):
        """
        第1期到期日之内提前结清
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(0, -10)
        fee_amount = get_qinnong_reserve_amount(self.item_no, 0, 1)
        # step 2 发起主动代扣
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        params_combo_active = {
            "project_num_loan_channel_amount": int(self.principal_amount + self.trail_interest_amount + fee_amount),
            "project_num_no_loan_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)
        repay_resp = resp_combo_active['content']

        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 4 数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        order_no_no_loan = repay_resp["data"]["project_list"][0]["order_no"]
        order_no = repay_resp["data"]["project_list"][1]["order_no"]
        order_no_prov = withhold[0]["withhold_serial_no"]

        check_withhold_split_count_by_request_no(withhold[1]["withhold_request_no"], 2)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[1]["withhold_request_no"], 1)
        check_withhold_order_by_order_no(order_no_prov, "capital_decrease")
        check_withhold_sign_company(order_no_no_loan, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no, 'tq,tqa,tqb')

        # param_loan = {
        #     "withhold_amount": int(self.principal_amount + self.trail_interest_amount + fee_amount)
        # }
        # check_withhold_result_without_split(self.item_no, **param_loan)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_payoff(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.qinnong
    def test_active_normal_settle_payoff(self):
        """
        第1期到期日提前结清, 资方扣当期息+12期本，我方扣剩下
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, 0)
        self.trail_interest_amount = 5200
        self.qinnong_mock.update_repay_trail(self.principal_amount, self.trail_interest_amount)
        fee_amount = get_qinnong_reserve_amount(self.item_no, 0, 1)
        # step 2 发起主动代扣
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        params_combo_active = {
            "project_num_loan_channel_amount": int(self.principal_amount + self.trail_interest_amount + fee_amount),
            "project_num_no_loan_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)
        repay_resp = resp_combo_active['content']

        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 4 数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        order_no_no_loan = repay_resp["data"]["project_list"][0]["order_no"]
        order_no = repay_resp["data"]["project_list"][1]["order_no"]
        order_no_prov = withhold[0]["withhold_serial_no"]

        check_withhold_split_count_by_request_no(withhold[1]["withhold_request_no"], 2)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[1]["withhold_request_no"], 1)
        check_withhold_order_by_order_no(order_no_prov, "capital_decrease")
        check_withhold_sign_company(order_no_no_loan, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no, 'tq,tqa,tqb')

        # param_loan = {
        #     "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"])
        # }
        # check_withhold_result_without_split(self.item_no, **param_loan)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_payoff(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.qinnong
    def test_active_overdue_one_day_settle_payoff(self):
        """
        第1期逾期1天提前结清
        """
        # step 1 修改资产到期日 刷罚息
        self.change_asset_due_at(-1, -1)
        refresh_late_fee(self.item_no)
        refresh_late_fee(self.item_num_no_loan)
        # step 2 发起主动代扣
        self.left_principal_amount = self.principal_amount - self.first_principal_amount
        self.trail_interest_amount = 4700
        self.qinnong_mock.update_repay_trail(self.left_principal_amount, self.trail_interest_amount)
        fee_amount = get_qinnong_reserve_amount(self.item_no, 1, 2)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        params_combo_active = {
            "project_num_loan_channel_amount": int(self.left_principal_amount + self.trail_interest_amount +
                                                   fee_amount + int(asset_tran_amount["asset_tran_balance_amount"])),
            "project_num_no_loan_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=0)
        repay_resp = resp_combo_active['content']

        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 4 数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        order_no_no_loan = repay_resp["data"]["project_list"][0]["order_no"]
        order_no = repay_resp["data"]["project_list"][1]["order_no"]
        order_no_prov = withhold[0]["withhold_serial_no"]

        check_withhold_split_count_by_request_no(withhold[1]["withhold_request_no"], 2)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[1]["withhold_request_no"], 1)
        check_withhold_order_by_order_no(order_no_prov, "capital_decrease")
        check_withhold_sign_company(order_no_no_loan, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no, 'tq,tqa,tqb')

        # param_loan = {
        #     "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"])
        # }
        # check_withhold_result_without_split(self.item_no, **param_loan)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_payoff(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.qinnong
    def test_auto_normal_repay(self):
        """
        自动代扣-正常还1期
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, 0)

        # step 2 发起自动代扣
        run_withholdAutoV1_by_api(self.item_no)
        wait_expect_task_appear(self.item_no, 'auto_withhold_execute')
        self.task.run_task(self.item_no, 'auto_withhold_execute')
        self.task.run_task(self.item_num_no_loan, 'auto_withhold_execute')
        self.get_auto_withhold_execute_task_run(self.item_no)
        self.get_auto_withhold_execute_task_run(self.item_num_no_loan)
        self.run_all_task_after_repay_success()

        # step 4 数据检查，大单2单 小单1单
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        order_no_no_loan = withhold_no_loan[0]["withhold_serial_no"]
        order_no = withhold[0]["withhold_serial_no"]
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 1)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 1)
        check_withhold_sign_company(order_no_no_loan, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no, 'tq,tqa,tqb')
        param_loan = {
            "withhold_amount": int(asset_tran_amount["asset_tran_amount"])
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_amount"])
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.qinnong
    def test_fox_overdue_repay(self):
        """
        该测试用例涉及了逾期手动代扣，资产逾期后，由paysvr代扣，收罚息
        :return:
        """
        # step 1 修改资产到期日 刷罚息
        self.change_asset_due_at(-1, -1)
        refresh_late_fee(self.item_no)
        refresh_late_fee(self.item_num_no_loan)

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

        withhold = get_withhold_by_item_no(self.item_no)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_serial_no"], count=3)

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
