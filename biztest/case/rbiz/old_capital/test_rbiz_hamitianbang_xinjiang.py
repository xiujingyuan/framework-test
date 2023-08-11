# -*- coding: utf-8 -*-
import pytest
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.easymock.easymock_config import mock_project
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config, \
    update_repay_hamitianbang_xinjiang_config
from biztest.function.rbiz.rbiz_check_function import check_withhold_split_count_by_request_no, \
    check_withhold_result_without_split, check_account_recharge_and_repay, check_asset_tran_repay_one_period, \
    check_withhold_split_count_by_item_no_and_request_no, check_withhold_sign_company, check_asset_tran_payoff, \
    check_withhold_by_serial_no, check_withhold_order_by_order_no, \
    check_capital_withhold_detail_vs_asset_tran, check_settle_payoff_capital_withhold_detail_vs_asset_tran, \
    check_withhold_data_by_sn
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_withhold_by_item_no, \
    get_asset_tran_balance_amount_by_item_no_and_period, \
    get_withhold_order_by_item_no, get_withhold_by_serial_no, get_asset_tran_balance_amount_by_item_no_and_type, \
    wait_expect_task_appear, update_asset_tran_status_by_item_no_and_period
from biztest.interface.rbiz.rbiz_interface import paysvr_callback, simple_active_repay, fox_manual_withhold, \
    run_withholdAutoV1_by_api, monitor_check
from biztest.util.easymock.rbiz.paysvr import PaysvrMock, rbiz_mock
from biztest.util.log.log_util import LogUtil
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.util.tools.tools import get_four_element
import common.global_const as gc


class TestRbizHamitianshanTianbang(BaseRepayTest):
    """
     hamitianbang_xinjiang还款

    """
    loan_channel = "hamitianbang_xinjiang"
    capital_withhold_amount = 70333

    @classmethod
    def setup_class(cls):
        monitor_check()
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        update_repay_hamitianbang_xinjiang_config(mock_project['rbiz_auto_test']['id'])
        cls.paysvr_mock = PaysvrMock(rbiz_mock)
        cls.task = Task("rbiz%s" % gc.ENV)
        cls.msg = Msg("rbiz%s" % gc.ENV)

    def setup_method(self):
        # 在每个脚本执行之前，初始化限制配置
        # mock代扣成功
        self.paysvr_mock.update_query_protocol_channels_bind_sms()
        self.paysvr_mock.update_auto_pay_withhold_process()
        self.paysvr_mock.update_withhold_query(2)
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
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

        # step 4 数据检查，大单2单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_our = repay_resp["data"]["project_list"][1]["order_no"]
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - self.capital_withhold_amount
        # 代扣顺序： 资方先扣
        check_withhold_order_by_order_no(order_no_capital, self.loan_channel)
        # 代扣拆单：大单拆成2单，一个request拆成3单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)

        #  还1期的金额，资方代扣本息2个类型
        capital_withhold = {
            "withhold_sign_company": 'hm',
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": self.capital_withhold_amount,
            "asset_tran_amount": self.capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        capital_withhold_type = ['repayprincipal', 'repayinterest']
        check_capital_withhold_detail_vs_asset_tran(order_no_capital, capital_withhold_type)
        # 检查我方代扣部分
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_withhold_amount
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
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
    @pytest.mark.hami_xj
    def test_active_advance_repay_fail_still_capital(self):
        """
        提前还1期 走资方失败 仍走资方 不切我方
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(0, -10)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        # step 2 发起主动代扣 走资方失败
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, 3)
        self.task.run_task(self.item_no, "withhold_callback_process")
        withhold = get_withhold_by_serial_no(order_no)
        check_withhold_order_by_order_no(order_no, self.loan_channel)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)

        # step 3 发起主动代扣第二次 提前还款不切我方
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_twice['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active_twice}"
        order_no_capital_twice = resp_combo_active_twice["content"]["data"]["project_list"][0]["order_no"]
        order_no_twice = resp_combo_active_twice["content"]["data"]["project_list"][1]["order_no"]
        order_no_no_loan_twice = resp_combo_active_twice["content"]["data"]["project_list"][2]["order_no"]

        check_withhold_sign_company(order_no_capital_twice, 'hm')
        check_withhold_sign_company(order_no_no_loan_twice, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_twice, 'tq,tqa,tqb')

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
    def test_active_normal_capital_repay(self):
        """
        正常还1期
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 4 数据检查，大单2单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_our = repay_resp["data"]["project_list"][1]["order_no"]
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - self.capital_withhold_amount
        # 代扣顺序： 资方先扣
        check_withhold_order_by_order_no(order_no_capital, self.loan_channel)
        # 代扣拆单：大单拆成2单，一个request拆成3单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)

        #  还1期的金额，资方代扣本息2个类型
        capital_withhold = {
            "withhold_sign_company": 'hm',
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": self.capital_withhold_amount,
            "asset_tran_amount": self.capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        capital_withhold_type = ['repayprincipal', 'repayinterest']
        check_capital_withhold_detail_vs_asset_tran(order_no_capital, capital_withhold_type)
        # 检查我方代扣部分
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_withhold_amount
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
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
    @pytest.mark.hami_xj
    def test_active_normal_repay_fail_switch_to_paysvr(self):
        """
        正常还1期 走资方失败 切我方
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, 0)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        # step 2 发起主动代扣 走资方失败
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, 3)
        self.task.run_task(self.item_no, "withhold_callback_process")
        withhold = get_withhold_by_serial_no(order_no)
        check_withhold_order_by_order_no(order_no, self.loan_channel)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)

        # step 3 发起主动代扣第二次 走我方代扣
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_twice['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active_twice}"
        order_no_no_loan_twice = resp_combo_active_twice["content"]["data"]["project_list"][0]["order_no"]
        order_no_twice = resp_combo_active_twice["content"]["data"]["project_list"][1]["order_no"]
        check_withhold_sign_company(order_no_no_loan_twice, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_twice, 'tq,tqa,tqb')
        self.run_all_task_after_repay_success()

        # step4 验证数据
        withhold = get_withhold_by_serial_no(order_no_twice)
        withhold_no_loan = get_withhold_by_serial_no(order_no_no_loan_twice)

        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 1)
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
    @pytest.mark.hami_xj
    def test_active_overdue_capital_repay(self):
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
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 4 数据检查，大单2单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_our = repay_resp["data"]["project_list"][1]["order_no"]
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - self.capital_withhold_amount
        # 代扣顺序： 资方先扣
        check_withhold_order_by_order_no(order_no_capital, self.loan_channel)
        # 代扣拆单：大单拆成2单，一个request拆成3单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)

        #  还1期的金额，资方代扣本息2个类型
        capital_withhold = {
            "withhold_sign_company": 'hm',
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": self.capital_withhold_amount,
            "asset_tran_amount": self.capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        capital_withhold_type = ['repayprincipal', 'repayinterest']
        check_capital_withhold_detail_vs_asset_tran(order_no_capital, capital_withhold_type)
        # 检查我方代扣部分
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_withhold_amount
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
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
    @pytest.mark.hami_xj
    def test_active_overdue_repay(self):
        """
        逾期还1期 逾期4天
        """

        # step 1 修改资产到期日 刷罚息
        self.change_asset_due_at(-1, -4)
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

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
    def test_active_overdue_one_day_repay_fail_switch_to_paysvr(self):
        """
        逾期宽限期内还1期 走资方失败 切我方
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        # step 2 发起主动代扣 走资方失败
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, 3)
        self.task.run_task(self.item_no, "withhold_callback_process")
        withhold = get_withhold_by_serial_no(order_no)
        check_withhold_order_by_order_no(order_no, self.loan_channel)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)

        # step 3 发起主动代扣第二次 走我方代扣
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_twice['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active_twice}"
        order_no_no_loan_twice = resp_combo_active_twice["content"]["data"]["project_list"][0]["order_no"]
        order_no_twice = resp_combo_active_twice["content"]["data"]["project_list"][1]["order_no"]
        check_withhold_sign_company(order_no_no_loan_twice, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_twice, 'tq,tqa,tqb')
        self.run_all_task_after_repay_success()

        # step4 验证数据
        withhold = get_withhold_by_serial_no(order_no_twice)
        withhold_no_loan = get_withhold_by_serial_no(order_no_no_loan_twice)

        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 1)
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
    @pytest.mark.hami_xj
    def test_active_advance_settle_payoff(self):
        """
        第1期到期日之内提前结清, 资方扣当期息+12期本，我方扣剩下
        """

        # step 1 修改资产到期日
        self.change_asset_due_at(0, -10)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)

        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)

        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 4 数据检查，大单2单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_our = repay_resp["data"]["project_list"][1]["order_no"]
        amount_all_principal = int(
            get_asset_tran_balance_amount_by_item_no_and_type(self.item_no, 'repayprincipal')['asset_tran_amount'])
        amount_one_interest = int(
            get_asset_tran_balance_amount_by_item_no_and_type(self.item_no, 'repayinterest', 1)['asset_tran_amount'])
        capital_withhold_amount = amount_all_principal + amount_one_interest  # 所有本金+当期利息
        our_withhold_amount = int(asset_tran_amount["asset_tran_amount"]) - capital_withhold_amount
        # 代扣顺序： 资方先扣
        check_withhold_order_by_order_no(order_no_capital, self.loan_channel)
        # 代扣拆单：大单拆成2单，一个request拆成3单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)

        #  还1期的金额，资方代扣本息2个类型
        capital_withhold = {
            "withhold_sign_company": 'hm',
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        check_settle_payoff_capital_withhold_detail_vs_asset_tran(order_no_capital)
        # 检查我方代扣部分
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_withhold_amount
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)

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
        check_asset_tran_payoff(self.item_no)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
    def test_active_advance_settle_payoff_fail_still_capital(self):
        """
        到期日之前提前结清 走资方失败 仍走资方 不切我方
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(0, -10)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)

        # step 2 发起主动代扣 走资方失败
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, 3)
        self.task.run_task(self.item_no, "withhold_callback_process")
        withhold = get_withhold_by_serial_no(order_no)
        check_withhold_order_by_order_no(order_no, self.loan_channel)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)

        # step 3 发起主动代扣第二次 提前还款不切我方
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_twice['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active_twice}"
        order_no_capital_twice = resp_combo_active_twice["content"]["data"]["project_list"][0]["order_no"]
        order_no_twice = resp_combo_active_twice["content"]["data"]["project_list"][1]["order_no"]
        order_no_no_loan_twice = resp_combo_active_twice["content"]["data"]["project_list"][2]["order_no"]

        check_withhold_sign_company(order_no_capital_twice, 'hm')
        check_withhold_sign_company(order_no_no_loan_twice, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_twice, 'tq,tqa,tqb')

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
    def test_active_normal_settle_payoff(self):
        """
        第1期到期日提前结清, 资方扣当期息+12期本，我方扣剩下
        """

        # step 1 修改资产到期日
        self.change_asset_due_at(-1, 0)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)

        # step 2 发起主动代扣
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 1, f"到期日提前结清不允许,req_body={req_body},resp_combo_active={resp_combo_active}"

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
    def test_active_overdue_one_day_settle_payoff(self):
        """
        逾期第1天提前结清
        """
        self.change_asset_due_at(-1, -1)

        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)

        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in repay_resp["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)

        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 4 数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        # 拆成4单 第1期逾期部分本息资方扣，第2-12期本+2期息资方扣，剩余费用我方扣，小单最后
        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_capital_two = repay_resp["data"]["project_list"][1]["order_no"]
        order_no_our = repay_resp["data"]["project_list"][2]["order_no"]
        order_no_no_loan = repay_resp["data"]["project_list"][3]["order_no"]

        capital_withhold_one = 70333
        capital_withhold_two = 742470
        our_withhold_amount = int(
            asset_tran_amount["asset_tran_amount"]) - capital_withhold_one - capital_withhold_two

        # 代扣拆单：大单拆成3单,合并代扣拆成4单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 3)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 4)
        check_withhold_sign_company(order_no_capital, 'hm')
        check_withhold_sign_company(order_no_capital_two, 'hm')
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        capital_withhold = {
            "withhold_sign_company": "hm",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_one,
            "asset_tran_amount": capital_withhold_one
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        # 检查我方代扣部分 --- 第1期逾期部分
        capital_withhold_withhold_two = {
            "withhold_sign_company": "hm",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_two,
            "asset_tran_amount": capital_withhold_two
        }
        check_withhold_by_serial_no(order_no_capital_two, **capital_withhold_withhold_two)
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
        check_withhold_by_serial_no(order_no_no_loan, **no_loan_withhold)

        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'], 2)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[2]['withhold_channel_key'], 1)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)
        check_asset_tran_payoff(self.item_num_no_loan)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
    def test_active_overdue_four_day_settle_payoff(self):
        """
        逾期第4天提前结清
        """
        self.change_asset_due_at(-1, -4)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)

        # step 2 发起主动代扣
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)

        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        # step 4 数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        # 拆成4单 第1期逾期部分先扣，第2-12期本+2期息资方扣，剩余费用我方扣，小单最后
        order_no_our = resp_repay["data"]["project_list"][0]["order_no"]
        order_no_capital = resp_repay["data"]["project_list"][1]["order_no"]
        order_no_our_two = resp_repay["data"]["project_list"][2]["order_no"]
        order_no_no_loan = resp_repay["data"]["project_list"][3]["order_no"]
        capital_withhold_amount = 742470  # 第2-12期本+2期息资方扣
        our_withhold_amount = int(
            get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)["asset_tran_amount"])
        our_withhold_amount_twice = int(
            asset_tran_amount["asset_tran_amount"]) - our_withhold_amount - capital_withhold_amount

        # 代扣拆单：大单拆成3单,合并代扣拆成4单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 3)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 4)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, 'hm')
        LogUtil.log_info("开始检检查资方扣的部分 第2期开始的...")
        capital_withhold = {
            "withhold_sign_company": "hm",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        # 检查我方代扣部分 --- 第1期逾期部分
        LogUtil.log_info("开始检查我方代扣部分 --- 第1期逾期部分...")
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_withhold_amount
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        LogUtil.log_info("开始检查我方代扣部分 --- 第2期-第12期...")
        our_withhold_two = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount_twice,
            "asset_tran_amount": our_withhold_amount_twice
        }
        check_withhold_by_serial_no(order_no_our_two, **our_withhold_two)

        # 检查小单代扣部分
        no_loan_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "asset_tran_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        check_withhold_by_serial_no(order_no_no_loan, **no_loan_withhold)

        # 检查充值还款
        LogUtil.log_info("开始检查充值还款 --- 第1期逾期部分是在第1单，还第1期所有费用...")
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        LogUtil.log_info("开始检查充值还款 --- 第2期本息部分是在第3单，资方扣，还第2期本金和利息...")
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'], 2)
        LogUtil.log_info("开始检查充值还款 --- 第2期剩余部分和后续期次本金是在第3单，我方扣，还第2-12期本金和第2期利息...")
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[2]['withhold_channel_key'], 2)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)
        check_asset_tran_payoff(self.item_num_no_loan)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
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
        self.get_auto_withhold_execute_task_run(self.item_no)
        self.run_all_task_after_repay_success()

        # step 4 数据检查，大单2单 小单1单
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        withhold = get_withhold_by_item_no(self.item_no)

        order_no_capital = withhold[0]["withhold_serial_no"]
        order_no_our = withhold[1]["withhold_serial_no"]
        our_withhold_amount = int(asset_tran_amount["asset_tran_amount"]) - self.capital_withhold_amount
        # 代扣顺序： 资方先扣
        check_withhold_order_by_order_no(order_no_capital, self.loan_channel)
        # 代扣拆单：大单拆成2单，一个request拆成3单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 1)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 1)

        #  还1期的金额，资方代扣本息2个类型
        capital_withhold = {
            "withhold_sign_company": 'hm',
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": self.capital_withhold_amount,
            "asset_tran_amount": self.capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        capital_withhold_type = ['repayprincipal', 'repayinterest']
        check_capital_withhold_detail_vs_asset_tran(order_no_capital, capital_withhold_type)
        # 检查我方代扣部分
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_withhold_amount
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)

        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])

        check_asset_tran_repay_one_period(self.item_no)


    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
    def test_active_overdue_one_day_repay_only_fee(self):
        """
        逾期3天内还1期 本息走资方还款成功  费走我方还失败 单独还fee
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        # step 2 发起主动代扣 走资方失败
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        order_no_our = resp_combo_active["content"]["data"]["project_list"][1]["order_no"]
        order_no_noloan = resp_combo_active["content"]["data"]["project_list"][2]["order_no"]
        paysvr_callback(order_no_our, 3)
        self.task.run_task(self.item_no, "withhold_callback_process")

        withhold = get_withhold_by_serial_no(order_no)
        check_withhold_order_by_order_no(order_no, self.loan_channel)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)
        paysvr_callback(order_no, 2)
        paysvr_callback(order_no_our, 3)
        paysvr_callback(order_no_noloan, 3)
        self.task.run_task_by_order_no_count(self.item_no, count=3)
        self.task.run_task_by_order_no_count(self.item_num_no_loan, count=3)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_serial_no"], count=3)

        # step 3 发起主动代扣 只还fee
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content']['code'] == 0, \
            f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
    def test_active_overdue_one_day_repay_fee_and_current_one_period(self):
        """
        逾期3天内还1期 本息走资方还款成功  费走我方还失败 单独还fee+新的一期
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, -1)

        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        # step 2 发起主动代扣 走资方失败
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        order_no_our = resp_combo_active["content"]["data"]["project_list"][1]["order_no"]
        order_no_noloan = resp_combo_active["content"]["data"]["project_list"][2]["order_no"]
        paysvr_callback(order_no_our, 3)
        self.task.run_task(self.item_no, "withhold_callback_process")
        withhold = get_withhold_by_serial_no(order_no)
        check_withhold_order_by_order_no(order_no, self.loan_channel)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)
        paysvr_callback(order_no, 2)
        paysvr_callback(order_no_our, 3)
        paysvr_callback(order_no_noloan, 3)
        self.task.run_task_by_order_no_count(self.item_no, count=3)
        self.task.run_task_by_order_no_count(self.item_num_no_loan, count=3)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_serial_no"], count=3)

        # step 3 发起主动代扣 只还fee
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_current = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 2)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        params_combo_active = {
            "project_num_loan_channel_amount": int(asset_tran_amount["asset_tran_balance_amount"]) + int(
                asset_tran_amount_current["asset_tran_balance_amount"]),
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
    def test_active_overdue_one_day_repay_fee_and_early_settlement(self):
        """
        逾期3天内还1期 本息走资方还款成功  费走我方还失败  提前结清
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        # step 2 发起主动代扣 走资方失败
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        order_no_our = resp_combo_active["content"]["data"]["project_list"][1]["order_no"]
        order_no_noloan = resp_combo_active["content"]["data"]["project_list"][2]["order_no"]
        withhold = get_withhold_by_serial_no(order_no)
        check_withhold_order_by_order_no(order_no, self.loan_channel)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)
        paysvr_callback(order_no, 2)
        paysvr_callback(order_no_our, 3)
        paysvr_callback(order_no_noloan, 3)
        self.task.run_task_by_order_no_count(self.item_no, count=3)
        self.task.run_task_by_order_no_count(self.item_num_no_loan, count=3)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_serial_no"], count=3)

        # step 3 发起主动代扣 只还fee
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"

        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        order_no_our = resp_combo_active["content"]["data"]["project_list"][1]["order_no"]
        order_no_noloan = resp_combo_active["content"]["data"]["project_list"][2]["order_no"]
        paysvr_callback(order_no, 2)
        paysvr_callback(order_no_our, 2)
        paysvr_callback(order_no_noloan, 2)
        self.task.run_task_by_order_no_count(self.item_no, count=3)
        self.task.run_task_by_order_no_count(self.item_num_no_loan, count=3)
        self.task.run_task_by_order_no_count(order_no, count=3)
        self.task.run_task_by_order_no_count(order_no_our, count=3)
        self.task.run_task_by_order_no_count(order_no_noloan, count=3)

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
    def test_active_overdue_one_day_repay_fee_and_current_two_period(self):
        """
        逾期3天内还1期 本息走资方还款成功  费走我方还失败 单独还fee+新的2期 不允许还
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, -1)

        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        # step 2 发起主动代扣 走资方失败
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        order_no_our = resp_combo_active["content"]["data"]["project_list"][1]["order_no"]
        order_no_noloan = resp_combo_active["content"]["data"]["project_list"][2]["order_no"]
        withhold = get_withhold_by_serial_no(order_no)
        check_withhold_order_by_order_no(order_no, self.loan_channel)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)
        paysvr_callback(order_no, 2)
        paysvr_callback(order_no_our, 3)
        paysvr_callback(order_no_noloan, 3)
        self.task.run_task_by_order_no_count(self.item_no, count=3)
        self.task.run_task_by_order_no_count(self.item_num_no_loan, count=3)
        self.run_all_task_after_repay_success()

        # step 3 发起主动代扣 只还fee
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_current = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 2)
        asset_tran_amount_next = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 3)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        loan_channel_amount = int(asset_tran_amount["asset_tran_balance_amount"]) + int(
            asset_tran_amount_current["asset_tran_balance_amount"]) + int(
            asset_tran_amount_next["asset_tran_balance_amount"])

        params_combo_active = {
            "project_num_loan_channel_amount": loan_channel_amount,
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 1, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"

    # #@pytest.mark.rbiz_auto_test
    # @pytest.mark.hami_xj
    def test_active_normal_repay_fee_and_current_one_period(self):
        """
        正常还1期 本息走资方还款成功  费走我方还失败 单独还fee+新的一期 不允许
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, 0)

        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        # step 2 发起主动代扣 走资方失败
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        order_no_our = resp_combo_active["content"]["data"]["project_list"][1]["order_no"]
        order_no_noloan = resp_combo_active["content"]["data"]["project_list"][2]["order_no"]
        withhold = get_withhold_by_serial_no(order_no)
        check_withhold_order_by_order_no(order_no, self.loan_channel)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)
        paysvr_callback(order_no, 2)
        paysvr_callback(order_no_our, 3)
        paysvr_callback(order_no_noloan, 3)
        self.task.run_task_by_order_no_count(self.item_no, count=3)
        self.task.run_task_by_order_no_count(self.item_num_no_loan, count=3)
        self.run_all_task_after_repay_success()

        # step 3 发起主动代扣 只还fee
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_current = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 2)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        params_combo_active = {
            "project_num_loan_channel_amount": int(asset_tran_amount["asset_tran_balance_amount"]) + int(
                asset_tran_amount_current["asset_tran_balance_amount"]),
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"

    #@pytest.mark.rbiz_auto_test
    @pytest.mark.hami_xj
    def test_active_normal_last_period(self):
        """
        最后一期到期日为今天
        """
        # Step 1：还款
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

        capital_withhold_amount = 70333
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - capital_withhold_amount
        # 代扣顺序： 资方先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, "hm")
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        #  还1期的金额，withhold_detail里面的3个金额是一样的
        capital_withhold = {"withhold_sign_company": "hm",
                            "withhold_channel": self.loan_channel,
                            "withhold_status": "success",
                            "withhold_amount": capital_withhold_amount,
                            "asset_tran_amount": capital_withhold_amount}
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)

        # 检查我方代扣部分
        our_withhold = {"withhold_sign_company": "tq,tqa,tqb",
                        "withhold_channel": "baidu_tq3_quick",
                        "withhold_status": "success",
                        "withhold_amount": our_withhold_amount,
                        "asset_tran_amount": our_withhold_amount
                        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        # 检查小单代扣部分
        no_loan_withhold = {"withhold_sign_company": "tq,tqa,tqb",
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
