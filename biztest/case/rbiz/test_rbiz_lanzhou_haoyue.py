# -*- coding: utf-8 -*-
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config, update_repay_lanzhou_config
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_check_function import *
from biztest.function.rbiz.rbiz_db_function import *
from biztest.util.asserts.assert_util import Assert
from biztest.util.easymock.rbiz.paysvr import *
from biztest.interface.rbiz.rbiz_interface import *
from biztest.util.easymock.rbiz.lanzhou_haoyue import RepayLanzhouMock
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.function.rbiz.assertion import *
import common.global_const as gc


class TestRbizLanzhou(BaseRepayTest):
    """
    lanzhou_haoyue 还款

    """
    loan_channel = "lanzhou_haoyue"
    exp_pay_channel = "cpcn_tq_quick"
    capital_withhold_amount = 52054

    @classmethod
    def setup_class(cls):
        monitor_check()
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        update_repay_lanzhou_config()
        cls.paysvr_mock = PaysvrMock(rbiz_mock)
        cls.lanzhou_mock = RepayLanzhouMock(rbiz_mock)
        cls.task = Task("rbiz{0}".format(gc.ENV))
        cls.msg = Msg("rbiz{0}".format(gc.ENV))

    def setup_method(self):
        # 在每个脚本执行之前，初始化限制配置
        update_repay_lanzhou_config()
        # mock代扣成功
        self.paysvr_mock.update_query_protocol_channels_bind_sms()
        self.paysvr_mock.update_auto_pay_withhold_process()
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element,
                                                                               asset_amount=6000)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_active_advance_granted_day_repay(self):
        """
        兰州提前还1期
        """
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()

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

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_active_advance_repay(self):
        """
        兰州提前还1期
        """

        # step 1 主动还款
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()

        # step 2 数据检查，大单1单小单1单，都走我方代扣
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

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_active_normal_repay(self):
        """
        兰州正常还款1期，本息拆1单走资方，费拆1单走我方
        """
        # step 1 主动还款
        self.lanzhou_mock.update_repay_apply()
        self.lanzhou_mock.update_repay_query()
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()

        # step 2 数据检查，大单2单 小单1单
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
            "withhold_sign_company": 'hy',
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

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_normal_fail_switch_paysvr_repay(self):
        """
        正常还款失败切我方
        """
        # mock代扣失败
        self.lanzhou_mock.update_repay_apply()
        self.lanzhou_mock.update_repay_query("9999", 5)

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
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        withhold = get_withhold_by_serial_no(order_no)
        check_data(withhold[0], withhold_channel=self.loan_channel)
        order_list = [project["order_no"] for project in resp_combo_active['content']["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 3)
        self.run_task_after_withhold_callback(order_list)

        # 再次发起主动代扣
        resp_combo_active_twice, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_twice['content'][
                   'code'] == 0, f"第2次主动合并代扣失败,req_body={req_body},resp_combo_active={resp_combo_active_twice}"
        order_no_no_loan_twice = resp_combo_active_twice["content"]["data"]["project_list"][0]["order_no"]
        order_no_twice = resp_combo_active_twice["content"]["data"]["project_list"][1]["order_no"]

        LogUtil.log_info(f"第2次代扣成功，返回体是 {resp_combo_active_twice}")
        LogUtil.log_info(f"检查数据库中的代扣金额")

        withhold = get_withhold_by_serial_no(order_no_twice)
        withhold_no_loan = get_withhold_by_serial_no(order_no_no_loan_twice)
        Assert.assert_equal(
            str(withhold[0]["withhold_amount"]), str(asset_tran_amount["asset_tran_balance_amount"]),
            f'{order_no_no_loan_twice}withhold_amount应为{asset_tran_amount["asset_tran_balance_amount"]}')
        Assert.assert_equal(
            str(withhold_no_loan[0]["withhold_amount"]), str(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            f'{order_no_no_loan_twice}withhold_amount应为{asset_tran_amount_no_loan["asset_tran_balance_amount"]}')
        self.run_all_task_after_repay_success()

        # step3 验证数据
        withhold = get_withhold_by_serial_no(order_no_twice)
        check_asset_tran_repay_one_period(self.item_no)
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
        # 检查 asset_tran
        check_asset_tran_repay_one_period(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_overdue_repay(self):
        """
        lanzhou逾期还
        """
        # step 1 主动还款
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # # self.run_all_msg_after_repay_success()

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

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_auto_normal_repay(self):
        # step 1 发起自动代扣
        self.change_asset_due_at(-1, 0)
        run_withholdAutoV1_by_api(self.item_no)
        wait_expect_task_appear(self.item_no, 'auto_withhold_execute')
        check_task_by_order_no_and_type(self.item_no, 'auto_withhold_execute', task_status='open')
        self.task.run_task(self.item_no, 'auto_withhold_execute')
        self.get_auto_withhold_execute_task_run(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_manual_overdue_repay(self):
        """
        该测试用例涉及了逾期手动代扣，资产逾期后，由paysvr代扣，收罚息
        :return:
        """
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

        # step 2 数据检查，大单2单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        order_no = withhold[0]["withhold_serial_no"]
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "asset_tran_amount": int(asset_tran_amount["asset_tran_balance_amount"])
        }
        check_withhold_by_serial_no(order_no, **our_withhold)

        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])

        check_asset_tran_repay_one_period(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_manual_normal_repay(self):
        """
        该测试用例涉及了到期日手动代扣，资产拆为2单，本息由资方扣，剩余费由我方扣
        :return:
        """
        self.lanzhou_mock.update_repay_apply()
        self.lanzhou_mock.update_repay_query()
        self.change_asset_due_at(-1, 0)
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

        # step 3 验证数据

        withhold = get_withhold_by_item_no(self.item_no)
        print(withhold)
        #  检查资方代扣表
        capital_withhold = {
            "withhold_sign_company": "hy",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": self.capital_withhold_amount,
            "asset_tran_amount": self.capital_withhold_amount
        }
        check_withhold_by_serial_no(withhold[0]["withhold_serial_no"], **capital_withhold)

        our_withhold_amt = int(asset_tran_amount["asset_tran_balance_amount"]) - self.capital_withhold_amount

        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amt,
            "asset_tran_amount": our_withhold_amt
        }
        check_withhold_by_serial_no(withhold[1]["withhold_serial_no"], **our_withhold)

        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])

        check_asset_tran_repay_one_period(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_active_advance_settle_payoff(self):
        """
        提前结清走我方
        """
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # # self.run_all_msg_after_repay_success()

        # step 2 数据检查
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
        check_asset_tran_payoff(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_active_normal_settle_payoff(self):
        """
        到期日提前结清 改为capital_rule的拆单方式之后，这个场景全部走我方代扣
        """
        # step 1 主动还款
        self.lanzhou_mock.update_repay_apply()
        self.lanzhou_mock.update_repay_query()
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # # self.run_all_msg_after_repay_success()
        # step 2 数据检查
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        # 检查大单代扣部分
        loan_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(asset_tran_amount["asset_tran_amount"])
        }
        check_withhold_result_without_split(self.item_no, **loan_withhold)
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
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)
        check_asset_tran_payoff(self.item_num_no_loan)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_active_combine_overdue_and_normal_settle_payoff(self):
        """
        最后一期到期日为今天,全部走我方代扣
        """
        # step 1 主动还款
        self.lanzhou_mock.update_repay_apply()
        self.lanzhou_mock.update_repay_query()
        self.change_asset_due_at(-12, 0)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount_p12 = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 12)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()

        # Step 2：开始检查数据
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        # 拆成4单 第1期逾期部分本息资方扣，第2-12期本+2期息资方扣，剩余费用我方扣，小单最后
        order_no_our_p111 = resp_repay["data"]["project_list"][0]["order_no"]
        order_no_capital = resp_repay["data"]["project_list"][1]["order_no"]
        order_no_our_p12 = resp_repay["data"]["project_list"][2]["order_no"]

        capital_withhold = {
            "withhold_sign_company": 'hy',
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": self.capital_withhold_amount,
            "asset_tran_amount": self.capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        # 检查我方代扣部分
        # 第1期息费
        our_withhold_amount_p12 = int(asset_tran_amount_p12["asset_tran_balance_amount"]) - self.capital_withhold_amount
        print("our_withhold_amount_p12 ", our_withhold_amount_p12)
        our_withhold_p1 = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount_p12,
            "asset_tran_amount": our_withhold_amount_p12
        }
        check_withhold_by_serial_no(order_no_our_p12, **our_withhold_p1)

        # 2-12期
        our_withhold_amount_p111 = int(asset_tran_amount["asset_tran_balance_amount"]) - int(
            asset_tran_amount_p12["asset_tran_balance_amount"])
        print("our_withhold_amount_p111: ", our_withhold_amount_p111)
        our_withhold_p111 = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount_p111,
            "asset_tran_amount": our_withhold_amount_p111
        }
        check_withhold_by_serial_no(order_no_our_p111, **our_withhold_p111)

        # 检查小单代扣部分
        no_loan_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_amount"])
        }
        check_withhold_result_without_split(self.item_num_no_loan, **no_loan_withhold)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'], 1)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'], 12)

        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_active_overdue_one_day_settle_payoff(self):
        """
        逾期第一天提前结清，大单拆成2单，逾期期次1单，剩余1单，都走我方。----开发确认过，如果质疑这种拆法，不算online bug
        """
        # step 1 主动还款
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # # self.run_all_msg_after_repay_success()

        # step 2 数据检查
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        order_no_overdue_part = withhold[0]["withhold_serial_no"]
        order_no_advance_part = withhold[1]["withhold_serial_no"]
        overdue_part_withhold_amount = int(
            get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)["asset_tran_amount"])
        advance_part_withhold_amount = int(
            asset_tran_amount["asset_tran_balance_amount"]) - overdue_part_withhold_amount
        # 代扣顺序：小单、 第一期逾期部分、 剩余部分
        check_withhold_data_by_sn(order_no_overdue_part, withhold_channel="baidu_tq3_quick")
        # 代扣拆单：拆成2单,request_no拆成3单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)
        check_withhold_sign_company(order_no_overdue_part, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_advance_part, 'tq,tqa,tqb')

        #  还1期的金额，withhold_detail里面的3个金额是一样的
        overdue_part_withhold = {"withhold_sign_company": 'tq,tqa,tqb',
                                 "withhold_channel": "baidu_tq3_quick",
                                 "withhold_status": "success",
                                 "withhold_amount": overdue_part_withhold_amount,
                                 "asset_tran_amount": overdue_part_withhold_amount}
        check_withhold_by_serial_no(order_no_overdue_part, **overdue_part_withhold)

        # 检查我方代扣部分
        advance_par_withhold = {"withhold_sign_company": "tq,tqa,tqb",
                                "withhold_channel": "baidu_tq3_quick",
                                "withhold_status": "success",
                                "withhold_amount": advance_part_withhold_amount,
                                "asset_tran_amount": advance_part_withhold_amount}
        check_withhold_by_serial_no(order_no_advance_part, **advance_par_withhold)
        # 检查小单代扣部分
        no_loan_withhold = {"withhold_sign_company": "tq,tqa,tqb",
                            "withhold_channel": "baidu_tq3_quick",
                            "withhold_status": "success",
                            "withhold_amount": int(
                                get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)[
                                    "asset_tran_amount"])}
        check_withhold_result_without_split(self.item_num_no_loan, **no_loan_withhold)

        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'], 2)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_active_normal_last_period(self):
        """
        最后一期到期日为今天
        """
        # Step 1：还款
        self.lanzhou_mock.update_repay_apply()
        self.lanzhou_mock.update_repay_query()
        self.change_asset_due_at(-12, 0)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        update_asset_tran_status_by_item_no_and_period(self.item_no)
        update_asset_tran_status_by_item_no_and_period(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()

        # Step 2：检查数据
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        order_no_capital = withhold[0]["withhold_serial_no"]
        order_no_our = withhold[1]["withhold_serial_no"]

        our_withhold_amount = int(asset_tran_amount["asset_tran_balance_amount"]) - self.capital_withhold_amount
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        #  还1期的金额，withhold_detail里面的3个金额是一样的
        capital_withhold = {"withhold_sign_company": "hy",
                            "withhold_channel": self.loan_channel,
                            "withhold_status": "success",
                            "withhold_amount": self.capital_withhold_amount,
                            "asset_tran_amount": self.capital_withhold_amount}
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
        # 检查asset_tran TODO

    @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_manual_overdue_one_day_settle_payoff(self):
        """
        手动代扣，第一期逾期+提前结清
        """
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
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
        assert resp_manual['content']['code'] == 0, f"manual接口代扣失败,req_body={req_body},resp_manual={resp_manual}"

        self.run_all_task_after_repay_success()
        # # self.run_all_msg_after_repay_success()

        # step 2 数据检查
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        order_no_overdue_part = withhold[0]["withhold_serial_no"]
        order_no_advance_part = withhold[1]["withhold_serial_no"]
        overdue_part_withhold_amount = int(
            get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)["asset_tran_amount"])
        advance_part_withhold_amount = int(
            asset_tran_amount["asset_tran_balance_amount"]) - overdue_part_withhold_amount
        # 代扣顺序：小单、 第一期逾期部分、 剩余部分
        check_withhold_data_by_sn(order_no_overdue_part, withhold_channel="baidu_tq3_quick")
        # 代扣拆单：拆成2单,request_no拆成3单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no,
                                                             withhold[0]["withhold_request_no"], 2)
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)
        check_withhold_sign_company(order_no_overdue_part, 'tq,tqa,tqb')
        check_withhold_sign_company(order_no_advance_part, 'tq,tqa,tqb')

        #  还1期的金额，withhold_detail里面的3个金额是一样的
        overdue_part_withhold = {"withhold_sign_company": 'tq,tqa,tqb',
                                 "withhold_channel": "baidu_tq3_quick",
                                 "withhold_status": "success",
                                 "withhold_amount": overdue_part_withhold_amount,
                                 "asset_tran_amount": overdue_part_withhold_amount}
        check_withhold_by_serial_no(order_no_overdue_part, **overdue_part_withhold)

        # 检查我方代扣部分
        advance_par_withhold = {"withhold_sign_company": "tq,tqa,tqb",
                                "withhold_channel": "baidu_tq3_quick",
                                "withhold_status": "success",
                                "withhold_amount": advance_part_withhold_amount,
                                "asset_tran_amount": advance_part_withhold_amount}
        check_withhold_by_serial_no(order_no_advance_part, **advance_par_withhold)
        # 检查小单代扣部分
        no_loan_withhold = {"withhold_sign_company": "tq,tqa,tqb",
                            "withhold_channel": "baidu_tq3_quick",
                            "withhold_status": "success",
                            "withhold_amount": int(
                                get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)[
                                    "asset_tran_amount"])}
        check_withhold_result_without_split(self.item_num_no_loan, **no_loan_withhold)

        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'], 2)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)

    @pytest.mark.lzhy
    def test_capital_sign_change_card_repay(self):
        """
        该测试用例涉及了还款签约和更改还款卡的流程，改卡则走到资方的协议支付流程。
        :return:
        """
        self.lanzhou_mock.update_pre_tied_card("9999")

        # 修改资产到期日
        self.change_asset_due_at(-1, 0)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        new_four_element = get_four_element()
        # 换卡发起主动代扣
        params_combo_active = {
            "card_num_encrypt": new_four_element['data']["bank_code_encrypt"],
            "card_user_id_encrypt": self.four_element['data']["id_number_encrypt"],
            "card_user_name_encrypt": self.four_element['data']["user_name_encrypt"],
            "card_user_phone_encrypt": new_four_element['data']["phone_number_encrypt"],
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"主动合并代扣失败,resp_combo_active={resp_combo_active},req_body={req_body}"

        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        verify_seq = bind_sms(order_no)
        params_combo_active.update(order_no=order_no, verify_seq=verify_seq, verify_code='123456')
        resp_combo_active_bind_card, req_body_bind_card = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_bind_card['content']['code'] == 0, \
            f"发起合并代扣绑卡失败,resp_combo_active_bind_card={resp_combo_active_bind_card}," \
            f"req_body_bind_card={req_body_bind_card}"

        self.run_all_task_after_repay_success()

        card_bind = {
            "card_bind_serial_no": order_no,
            "card_bind_channel": "baofoo_tq4_protocol",
            "card_bind_status": "success"
        }

        check_card_bind_info(new_four_element['data']["bank_code_encrypt"], **card_bind)
        # self.task.run_task(order_no, 'withholdCard')
        # 不会更新原有的card和individual
        check_card_by_item_no(self.item_no,
                              card_acc_name_encrypt=self.four_element['data']["user_name_encrypt"],
                              card_acc_num_encrypt=self.four_element['data']["bank_code_encrypt"],
                              card_acc_id_num_encrypt=self.four_element['data']["id_number_encrypt"],
                              card_acc_tel_encrypt=self.four_element['data']["phone_number_encrypt"])
        check_individual_by_item_no(self.item_no,
                                    individual_name_encrypt=self.four_element['data']["user_name_encrypt"],
                                    individual_id_num_encrypt=self.four_element['data']["id_number_encrypt"],
                                    individual_tel_encrypt=self.four_element['data']["phone_number_encrypt"])

        # 新增一条withhold_card from_app是banana
        check_withhold_card_by_card_num(new_four_element['data']["bank_code_encrypt"], withhold_card_from_app="banana")

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.lzhy
    def test_capital_sign_pre_sign_fail(self):
        """
        该测试用例涉及了还款签约和更改还款卡的流程，预签约失败后，直接走paysvr绑卡，代扣失败cancel报协议支付号为空。
        :return:
        """
        # 兰州mock代扣预签约失败
        self.lanzhou_mock.update_pre_tied_card("9000")
        # 修改资产到期日
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)

        new_four_element = get_four_element()
        # 换卡发起主动代扣
        params_combo_active = {
            "card_num_encrypt": new_four_element['data']["bank_code_encrypt"],
            "card_user_id_encrypt": new_four_element['data']["id_number_encrypt"],
            "card_user_name_encrypt": new_four_element['data']["user_name_encrypt"],
            "card_user_phone_encrypt": new_four_element['data']["phone_number_encrypt"],
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"主动合并代扣失败,resp_combo_active={resp_combo_active},req_body={req_body}"

        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        verify_seq = bind_sms(order_no)
        params_combo_active.update(order_no=order_no, verify_seq=verify_seq, verify_code='123456')
        resp_combo_active_bind_card, req_body_bind_card = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active_bind_card['content']['code'] == 0, \
            f"发起合并代扣绑卡失败,resp_combo_active_bind_card={resp_combo_active_bind_card}," \
            f"req_body_bind_card={req_body_bind_card}"

        order_no_capital = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        withhold = get_withhold_by_serial_no(order_no_capital)

        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)
        self.task.run_task(withhold[0]["withhold_serial_no"], "withhold_order_sync")

        card_bind = {
            "card_bind_serial_no": order_no,
            "card_bind_channel": "baofoo_tq4_protocol",
            "card_bind_status": "success"
        }

        check_card_bind_info(new_four_element['data']["bank_code_encrypt"], **card_bind)
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel,
                                  withhold_serial_no=order_no_capital,
                                  withhold_status="success", withhold_channel_message="自动化测试")
