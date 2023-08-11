# -*- coding: utf-8 -*-
import datetime

import pytest

from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config
from biztest.function.rbiz.rbiz_check_function import check_account_recharge_and_repay, \
    check_asset_tran_repay_one_period, check_withhold_by_serial_no, check_capital_withhold_detail_vs_asset_tran, \
    check_withhold_sign_company, check_withhold_split_count_by_item_no_and_request_no, check_withhold_data_by_sn, \
    check_withhold_split_count_by_request_no, check_withhold_result_without_split, check_asset_tran_payoff, \
    check_settle_payoff_capital_withhold_detail_vs_asset_tran, check_withhold_order_by_order_no, check_json_rs_data
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    get_withhold_by_item_no, get_withhold_by_serial_no, wait_expect_task_appear
from biztest.interface.rbiz.rbiz_interface import paysvr_callback, simple_active_repay, run_withholdAutoV1_by_api, \
    combo_active_repay_without_no_loan, monitor_check
from biztest.util.easymock.rbiz.paysvr import PaysvrMock
from biztest.util.log.log_util import LogUtil
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
import common.global_const as gc
from biztest.util.tools.tools import get_four_element


class TestRbizShilongsiping(BaseRepayTest):
    """
    shilong_siping repay
    """
    loan_channel = "shilong_siping"
    amount_loan_channel = 8000

    @classmethod
    def setup_class(cls):
        monitor_check()
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        # 默认将代偿日设置到32号，这样会优先走资方代扣
        fail_times = {"auto": {"times": 1, "calByDay": False},
                      "active": {"times": 1, "calByDay": False},
                      "manual": {"times": 1, "calByDay": False}}

        cls.paysvr_mock = PaysvrMock(rbiz_mock)
        cls.task = Task("rbiz{0}".format(gc.ENV))
        cls.msg = Msg("rbiz{0}".format(gc.ENV))

    def setup_method(self):
        self.paysvr_mock.update_query_protocol_channels_bind_sms()
        self.paysvr_mock.update_auto_pay_withhold_process()
        self.paysvr_mock.update_withhold_query(2)
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element)

   # @pytest.mark.rbiz_auto_test
    @pytest.mark.siping
    def test_active_normal_repay(self):
        """
        shilongsiping提前还1期，本息拆1单，费拆1单
        """
        # 修改资产到期日
        self.change_asset_due_at(-1, 0)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_our = repay_resp["data"]["project_list"][1]["order_no"]

        # step 3 验证数据
        # 资方代扣金额 = 第1期本金+占用天数利息
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        capital_withhold_amount = 69776
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - capital_withhold_amount
        # 代扣顺序： 四平先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, 'hq')
        #  还1期的金额，withhold_detail里面的3个金额是一样的
        capital_withhold = {
            "withhold_sign_company": "hq",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        check_capital_withhold_detail_vs_asset_tran(order_no_capital)
        # 检查我方代扣部分
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
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
        # 检查 asset_tran
        check_asset_tran_repay_one_period(self.item_no)

   # @pytest.mark.rbiz_auto_test
    @pytest.mark.siping
    def test_normal_fail_switch_paysvr_repay(self):
        """
        shilongsiping正常还款失败切我方
        """
        # 修改资产到期日
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
        withhold = get_withhold_by_serial_no(order_no)
        paysvr_callback(resp_combo_active["content"]["data"]["project_list"][0]["order_no"], 3)
        self.task.run_task_by_order_no(self.item_no)
        check_withhold_data_by_sn(order_no, withhold_channel=self.loan_channel)
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

   # @pytest.mark.rbiz_auto_test
    @pytest.mark.siping
    def test_overdue_repay(self):
        """
        第一期逾期还当期
        """
        # step 1 主动还款
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 2 逾期数据检查，大单1单小单1单，都走我方代扣
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
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

   # @pytest.mark.rbiz_auto_test
    @pytest.mark.siping
    def test_active_advance_settle_payoff(self):
        """
        到提前结清，全额本金+第一期利息拆给资方，剩余我方扣, 代偿日
        """
        # step 1 准备数据
        self.change_asset_due_at(0, -10)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)

        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)

        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 4 数据检查，大单2单 小单1单
        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_our = repay_resp["data"]["project_list"][1]["order_no"]
        withhold = get_withhold_by_item_no(self.item_no)
        # TODO 应根据开发的算法来实时计算这个金额，不然每个月都要改一次
        capital_withhold_amount = 801889
        capital_withhold_asset_amount = 805667
        our_withhold_asset_amount = 164440
        our_withhold_amount = 162551
        capital_withhold_interest = capital_withhold_amount - self.amount_loan_channel * 100
        # 代扣顺序： 四平先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, 'hq')
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        #  还1期的金额，withhold_detail里面的3个金额是一样的
        capital_withhold = {"withhold_sign_company": "hq",
                            "withhold_channel": "shilong_siping",
                            "withhold_status": "success",
                            "withhold_amount": capital_withhold_amount,
                            "asset_tran_amount": capital_withhold_asset_amount}
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        check_settle_payoff_capital_withhold_detail_vs_asset_tran(order_no_capital,
                                                                  capital_withhold_interest)
        # 检查我方代扣部分
        our_withhold = {"withhold_sign_company": "tq,tqa,tqb",
                        "withhold_channel": "baidu_tq3_quick",
                        "withhold_status": "success",
                        "withhold_amount": our_withhold_amount,
                        "asset_tran_amount": our_withhold_asset_amount}
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)

   # @pytest.mark.rbiz_auto_test
    @pytest.mark.siping
    def test_active_normal_settle_payoff(self):
        """
        四平到期日提前结清，全额本金+第一期利息拆给资方，剩余我方扣，拆成2单
        """

        self.change_asset_due_at(-1, 0)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)

        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)

        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_our = repay_resp["data"]["project_list"][1]["order_no"]

        # Step 3：开始检查数据
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        capital_withhold_amount = 805667
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - capital_withhold_amount
        # 代扣顺序： 四平先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, 'hq')
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        #  还1期的金额，withhold_detail里面的3个金额是一样的
        capital_withhold = {
            "withhold_sign_company": "hq",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        # 资方代扣明细和asset_tran对比
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
        # 检查小单代扣部分
        no_loan_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_amount"])
        }
        check_withhold_result_without_split(self.item_num_no_loan, **no_loan_withhold)

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
    @pytest.mark.siping
    def test_active_overdue_one_day_settle_payoff(self):
        """
        逾期第1天提前结清，代偿日之前，
        1. 第1期逾期先砍单扣
        2. 第2次代扣，第2-12期提前结清，第2-12期本进+1天利息1单，剩余费用1单。
        """
        self.change_asset_due_at(-1, -1)

        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)

        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)

        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

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

        order_no_capital = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        order_no_our = resp_combo_active["content"]["data"]["project_list"][1]["order_no"]

        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 3 验证数据
        # 资方代扣金额 = 第1期本金+占用天数利息
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        # TODO 应根据开发的算法来实时计算这个金额，不然每个月都要改一次
        capital_withhold_amount = 736065
        capital_withhold_asset_amount = 741104
        our_withhold_asset_amount = 148179
        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - capital_withhold_amount
        # 代扣顺序： 四平先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        # 代扣拆单：拆成2单 第2次代扣 只剩大单的2-12期
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, 'hq')
        # 提前结清 检查资方扣的部分 第2期开始的
        capital_withhold = {"withhold_sign_company": "hq",
                            "withhold_channel": "shilong_siping",
                            "withhold_status": "success",
                            "withhold_amount": capital_withhold_amount,
                            "asset_tran_amount": capital_withhold_asset_amount}
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        # 检查我方代扣部分 --- 第1期逾期部分
        our_withhold = {"withhold_sign_company": "tq,tqa,tqb",
                        "withhold_channel": "baidu_tq3_quick",
                        "withhold_status": "success",
                        "withhold_amount": our_withhold_amount,
                        "asset_tran_amount": our_withhold_asset_amount}
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        # 检查小单代扣部分
        no_loan_withhold = {"withhold_sign_company": "tq,tqa,tqb",
                            "withhold_channel": "baidu_tq3_quick",
                            "withhold_status": "success",
                            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_amount"])}
        check_withhold_result_without_split(self.item_num_no_loan, **no_loan_withhold)

        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'], 2)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'], 1)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)
        check_asset_tran_payoff(self.item_num_no_loan)

   # @pytest.mark.rbiz_auto_test
    @pytest.mark.siping
    def test_active_normal_compensate_settle_payoff(self):
        """
        到提前结清，全额本金+第一期利息拆给资方，剩余我方扣, 代偿日为2号。拆成3单。
        >1日放款 第一期到期日提前结清
        https://www.tapd.cn/20584621/sparrow/tcase/view/1120584621001011210?url_cache_key=fb18ec212b49195ebee6c6fb15ee7701
        """
        # 昨天为代偿日，资方还款计划的到期日为2天前，用户到期日为昨天，这样保障每天跑出来的脚本利息是一样的。

        self.change_asset_due_at(-1, 0)  # 修改资产到期日

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)

        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)

        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # 拆成4单 第1期逾期部分先扣，第2期本息资方扣，剩余费用我方扣，小单最后
        order_no_our = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_capital = repay_resp["data"]["project_list"][1]["order_no"]
        order_no_our_two = repay_resp["data"]["project_list"][2]["order_no"]
        order_no_no_loan = repay_resp["data"]["project_list"][3]["order_no"]

        # step 3 验证数据  大单拆成3单，小单单独1单
        # 资方代扣金额 = 第1期本金+占用天数利息
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        # TODO 应根据开发的算法来实时计算这个金额，不然每个月都要改一次
        capital_withhold_amount = 736239
        capital_withhold_asset_amount = 741104
        our_withhold_amount = 80370
        our_withhold_asset_amount = 80370
        our_withhold_asset_amount_twice = 148179
        our_withhold_amount_twice = int(
            asset_tran_amount["asset_tran_balance_amount"]) - our_withhold_amount - capital_withhold_amount

        # 代扣拆单：大单拆成3单,合并代扣拆成4单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 3)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 4)
        check_withhold_sign_company(order_no_our, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_capital, 'hq')
        LogUtil.log_info("开始检检查资方扣的部分 第2期开始的...")
        capital_withhold = {"withhold_sign_company": "hq",
                            "withhold_channel": "shilong_siping",
                            "withhold_status": "success",
                            "withhold_amount": capital_withhold_amount,
                            "asset_tran_amount": capital_withhold_asset_amount}
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        # 检查我方代扣部分 --- 第1期逾期部分
        LogUtil.log_info("开始检查我方代扣部分 --- 第1期逾期部分...")
        our_withhold = {"withhold_sign_company": "tq,tqa,tqb",
                        "withhold_channel": "baidu_tq3_quick",
                        "withhold_status": "success",
                        "withhold_amount": our_withhold_amount,
                        "asset_tran_amount": our_withhold_asset_amount}
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        LogUtil.log_info("开始检查我方代扣部分 --- 第2期-第12期...")
        our_withhold_two = {"withhold_sign_company": "tq,tqa,tqb",
                            "withhold_channel": "baidu_tq3_quick",
                            "withhold_status": "success",
                            "withhold_amount": our_withhold_amount_twice,
                            "asset_tran_amount": our_withhold_asset_amount_twice}
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

   # @pytest.mark.rbiz_auto_test
    @pytest.mark.siping
    def test_active_settle_fail_switch_pay_payoff(self):
        """
        提前结清，走资方失败切我方
        """
        update_repay_shilong_siping_config(mock_project['rbiz_auto_test']['id'], "31")
        # 修改资产到期日
        self.change_asset_due_at(0, -22)

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
        withhold = get_withhold_by_serial_no(order_no)
        check_withhold_order_by_order_no(order_no, self.loan_channel)
        order_list = [project["order_no"] for project in resp_combo_active['content']["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 3)
        self.run_task_after_withhold_callback(order_list)

        # step 3 发起主动代扣第二次 走我方代扣
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_twice['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active_twice}"
        order_no_no_loan_twice = resp_combo_active_twice["content"]["data"]["project_list"][0]["order_no"]
        order_no_twice = resp_combo_active_twice["content"]["data"]["project_list"][1]["order_no"]
        check_withhold_sign_company(order_no_no_loan_twice, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_twice, 'tq,tqa,tqb')
        self.run_all_task_after_repay_success()

        # 切我方代扣后，大单1单，小单1单
        withhold = get_withhold_by_serial_no(order_no_twice)
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
                                         withhold[0]['withhold_channel_key'], 1)
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)

   # @pytest.mark.rbiz_auto_test
    @pytest.mark.siping
    def test_active_multi_repay_not_allowed(self):
        """
        四平提前还2期，不允许
        """
        # 修改资产到期日
        self.change_asset_due_at(-1, 0)

        asset_tran_amount_1 = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_2 = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 2)
        asset_tran_amount_no_loan_1 = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        asset_tran_amount_no_loan_2 = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 2)
        asset_tran_amount = int(asset_tran_amount_1["asset_tran_balance_amount"]) + int(
            asset_tran_amount_2["asset_tran_balance_amount"])
        asset_tran_amount_no_loan = int(asset_tran_amount_no_loan_1["asset_tran_balance_amount"]) + int(
            asset_tran_amount_no_loan_2["asset_tran_balance_amount"])
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount,
            "project_num_no_loan_amount": asset_tran_amount_no_loan
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=1)
        check_json_rs_data(resp_combo_active['content'], message=f"资产[{self.item_no}],正常单期不允许多期还款")

   # @pytest.mark.rbiz_auto_test
    @pytest.mark.siping
    def test_active_advance_repay_not_allowed(self):
        """
        提前还1期，本息拆1单，费拆1单
        """

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan, 1)
        check_json_rs_data(repay_resp, message=f"资产{self.item_no}还款类型不允许还款")

   # @pytest.mark.rbiz_auto_test
    @pytest.mark.siping
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
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()

        # step 4 数据检查，大单2单 小单1单
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        order_no_capital = withhold[0]["withhold_serial_no"]
        order_no_our = withhold[1]["withhold_serial_no"]
        capital_withhold_amount = 69776
        our_withhold_amount = int(asset_tran_amount["asset_tran_amount"]) - capital_withhold_amount
        # 代扣顺序： 资方先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        # 代扣拆单：大单拆成2单，一个request拆成3单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 1)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 1)

        #  还1期的金额，资方代扣本息2个类型
        capital_withhold = {
            "withhold_sign_company": 'hq',
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_withhold_amount
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
    @pytest.mark.siping
    def test_auto_normal_repay_fail_retry_switch_to_paysvr(self):
        """
        自动代扣-正常还1期 失败重试切paysvr代扣
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(-1, 0)

        # step 2 发起自动代扣
        run_withholdAutoV1_by_api(self.item_no)
        wait_expect_task_appear(self.item_no, 'auto_withhold_execute')
        self.task.run_task(self.item_no, 'auto_withhold_execute')
        self.get_auto_withhold_execute_task_run(self.item_no)
        withhold_list = get_withhold_by_item_no(self.item_no)
        for withhold in withhold_list:
            paysvr_callback(withhold["withhold_serial_no"], 3)
        self.task.run_task_by_order_no(self.item_no)
        self.task.run_task_by_order_no(self.item_num_no_loan)
        self.task.run_task(self.item_no, 'withhold_retry_execute')
        self.task.run_task(self.item_no, 'auto_withhold_execute')
        self.run_all_task_after_repay_success()

        # # step4 验证数据
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 1)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 1)
        check_withhold_sign_company(withhold[0]['withhold_serial_no'], 'tq,tqa,tqb')
        check_withhold_sign_company(withhold_no_loan[0]['withhold_serial_no'], 'tq,tqa,tqb')
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
