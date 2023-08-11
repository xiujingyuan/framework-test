# -*- coding: utf-8 -*-
import json

import pytest

from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_check_function import check_withhold_split_count_by_request_no, \
    check_withhold_result_without_split, check_account_recharge_and_repay, check_asset_tran_repay_one_period, \
    check_withhold_split_count_by_item_no_and_request_no, check_withhold_sign_company, check_asset_tran_payoff, \
    check_task_by_order_no_and_type, check_card_by_item_no, check_individual_by_item_no, \
    check_card_by_card_no
from biztest.function.rbiz.rbiz_db_function import get_withhold_by_item_no, \
    get_asset_tran_balance_amount_by_item_no_and_period, get_task_by_order_no_and_task_type, \
    get_withhold_order_by_item_no
from biztest.interface.rbiz.rbiz_interface import fox_manual_withhold, paysvr_callback, run_withholdAutoV1_by_api, \
    monitor_check
from biztest.util.easymock.rbiz.paysvr import PaysvrMock, rbiz_mock, mock_project
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.util.tools.tools import get_four_element
import common.global_const as gc


class TestRbizTongrongqianjingjing(BaseRepayTest):
    """
    tongrongqianjingjing repay
    """
    loan_channel = "tongrongqianjingjing"
    exp_sign_company = "qjj"
    exp_sign_company_no_loan = "tq,tqa,tqb"

    @classmethod
    def setup_class(cls):
        monitor_check()
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        cls.paysvr_mock = PaysvrMock(rbiz_mock)
        cls.task = Task("rbiz{0}".format(gc.ENV))
        cls.msg = Msg("rbiz{0}".format(gc.ENV))

    def setup_method(self):
        monitor_check()
        # 在每个脚本执行之前，初始化限制配置
        # mock代扣成功
        self.paysvr_mock.update_query_protocol_channels_bind_sms()
        self.paysvr_mock.update_auto_pay_withhold_process()
        self.paysvr_mock.update_withhold_query(2)
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.tongrongqianjingjing
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
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        self.check_response_after_apply_success(repay_resp, withhold, withhold_no_loan)

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

    @pytest.mark.rbiz_auto_test
    @pytest.mark.tongrongqianjingjing
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
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        self.check_response_after_apply_success(repay_resp, withhold, withhold_no_loan)

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

    @pytest.mark.rbiz_auto_test
    @pytest.mark.tongrongqianjingjing
    def test_active_overdue_repay(self):
        """
        逾期还1期
        """
        # step 1 修改资产到期日 刷罚息
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # step 3 执行task和msg
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        self.check_response_after_apply_success(repay_resp, withhold, withhold_no_loan)

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

    @pytest.mark.rbiz_auto_test
    @pytest.mark.tongrongqianjingjing
    def test_active_advance_settle_payoff(self):
        """
        第1期到期日之内提前结清
        """

        # step 1 修改资产到期日
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # step 3 执行task和msg
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        self.check_response_after_apply_success(repay_resp, withhold, withhold_no_loan)

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
        check_asset_tran_payoff(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.tongrongqianjingjing
    def test_active_normal_settle_payoff(self):
        """
        第1期到期日提前结清, 资方扣当期息+12期本，我方扣剩下
        """

        # step 1 修改资产到期日
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # step 3 执行task和msg
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        self.check_response_after_apply_success(repay_resp, withhold, withhold_no_loan)

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
        check_asset_tran_payoff(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.tongrongqianjingjing
    def test_active_overdue_one_day_settle_payoff(self):
        """
        第1期逾期1天提前结清
        """
        # step 1 修改资产到期日 刷罚息
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # step 3 执行task和msg
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()
        self.check_response_after_apply_success(repay_resp, withhold, withhold_no_loan)

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
        check_asset_tran_payoff(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.tongrongqianjingjing
    def test_auto_normal_repay(self):
        """
        自动代扣-正常还1期
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, 0)

        # step 2 发起自动代扣
        run_withholdAutoV1_by_api(self.item_no)
        self.task.wait_task_appear(self.item_no, 'auto_withhold_execute')
        check_task_by_order_no_and_type(self.item_no, 'auto_withhold_execute', task_status='open')
        self.task.run_task(self.item_no, 'auto_withhold_execute')
        self.get_auto_withhold_execute_task_run(self.item_no)
        self.run_all_task_after_repay_success()

        # step 3 执行task和msg
        self.run_all_task_after_repay_success()

        # step 4 数据检查，大单1单 小单1单
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        withhold = get_withhold_by_item_no(self.item_no)

        order_no = withhold[0]["withhold_serial_no"]
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 1)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 1)
        check_withhold_sign_company(order_no, self.exp_sign_company)
        param_loan = {
            "withhold_amount": int(asset_tran_amount["asset_tran_amount"]),
            "withhold_sign_company": self.exp_sign_company
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.tongrongqianjingjing
    def test_fox_overdue_repay(self):
        """
        该测试用例涉及了逾期手动代扣，资产逾期后，由paysvr代扣，收罚息
        :return:
        """
        # step 1 修改资产到期日 刷罚息
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

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
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "withhold_sign_company": self.exp_sign_company
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.tongrongqianjingjing
    def test_auto_normal_retry(self):
        """
        自动代扣- 用新增的代扣卡来轮询
        """
        card_1, tel1 = self.add_a_card()
        card_2, tel2 = self.add_a_card()
        print("self.four_element  ", self.four_element)

        # step 1 修改资产到期日
        self.change_asset_due_at(-1, 0)

        # step 2 发起自动代扣
        run_withholdAutoV1_by_api(self.item_no)
        self.task.wait_task_appear(self.item_no, 'auto_withhold_execute')
        self.task.run_task(self.item_no, 'auto_withhold_execute')
        self.get_auto_withhold_execute_task_run(self.item_no)
        order_no = get_withhold_order_by_item_no(self.item_no)[0]["withhold_order_serial_no"]
        paysvr_callback(order_no, 3, channel_message="余额不足")
        self.task.run_task(self.item_no, "withhold_callback_process")
        # 轮询card 1
        task_withhold_retry_card = json.loads(
            get_task_by_order_no_and_task_type(self.item_no, 'withhold_retry_execute', 'open')[0]['task_request_data'])[
            'data'][
            'cardNo']
        check_card_by_card_no(task_withhold_retry_card, card_acc_num_encrypt=card_1)
        self.task.run_task(self.item_no, 'withhold_retry_execute')
        self.task.run_task(self.item_no, 'auto_withhold_execute')
        self.get_auto_withhold_execute_task_run(self.item_no)
        order_no = get_withhold_order_by_item_no(self.item_no)[0]["withhold_order_serial_no"]
        paysvr_callback(order_no, 3, channel_message="余额不足")
        self.task.run_task(self.item_no, "withhold_callback_process")
        # 轮询card 2
        task_withhold_retry_card_2 = json.loads(
            get_task_by_order_no_and_task_type(self.item_no, 'withhold_retry_execute', 'open')[0]['task_request_data'])[
            'data'][
            'cardNo']
        check_card_by_card_no(task_withhold_retry_card_2, card_acc_num_encrypt=card_2)
        self.task.run_task(self.item_no, 'withhold_retry_execute')
        self.task.run_task(self.item_no, 'auto_withhold_execute')
        self.get_auto_withhold_execute_task_run(self.item_no)
        order_no = get_withhold_order_by_item_no(self.item_no)[0]["withhold_order_serial_no"]
        paysvr_callback(order_no, 3, channel_message="余额不足")
        self.task.run_task(self.item_no, "withhold_callback_process")

        # 不会更新原有的card和individual
        check_card_by_item_no(self.item_no, card_acc_num_encrypt=self.four_element['data']["bank_code_encrypt"],
                              card_acc_id_num_encrypt=self.four_element['data']["id_number_encrypt"],
                              card_acc_tel_encrypt=self.four_element['data']["phone_number_encrypt"])
        check_individual_by_item_no(self.item_no,
                                    individual_name_encrypt=self.four_element['data']["user_name_encrypt"],
                                    individual_id_num_encrypt=self.four_element['data']["id_number_encrypt"],
                                    individual_tel_encrypt=self.four_element['data']["phone_number_encrypt"])
