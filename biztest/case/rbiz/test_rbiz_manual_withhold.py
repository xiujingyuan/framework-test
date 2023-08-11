# -*- coding: utf-8 -*-

from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_check_function import *
from biztest.function.rbiz.rbiz_db_function import *
from biztest.util.easymock.rbiz.paysvr import *
from biztest.interface.rbiz.rbiz_interface import *
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.function.rbiz.assertion import *
import common.global_const as gc


class TestRbizManualWithhold(BaseRepayTest):
    """
    手动代扣
    接口文档：https://git.kuainiujinke.com/cd_biz/biz-repay/wikis/%E4%BB%A3%E6%89%A3%E7%9B%B8%E5%85%B3%E6%8E%A5%E5%8F%A3#fox%E4%BB%A3%E6%89%A3%E6%8E%A5%E5%8F%A3
    """

    loan_channel = "tongrongqianjingjing"
    exp_sign_company = "tq,tqa,tqb"
    exp_sign_company_no_loan = "tq,tqa,tqb"
    pricipal_amount = 800000

    @classmethod
    def setup_class(cls):
        monitor_check()
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        cls.paysvr_mock = PaysvrMock(rbiz_mock)
        cls.task = Task("rbiz{0}".format(gc.ENV))
        cls.msg = Msg("rbiz{0}".format(gc.ENV))

    def setup_method(self):
        # mock代扣成功
        self.paysvr_mock.update_query_protocol_channels_bind_sms()
        self.paysvr_mock.update_auto_pay_withhold_process()
        self.paysvr_mock.update_withhold_query(2)
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = \
            asset_import_and_loan_to_success(self.loan_channel, self.four_element)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.rbiz_interface
    def test_manual_overdue_one_period_only_loan_asset(self):
        """
        逾期手动扣整期
        """
        # # 修改大小单还款时间
        self.change_asset_due_at(-1, -1)
        # 刷新罚息
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

        withhold = get_withhold_by_item_no(self.item_no)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_serial_no"], count=3)

        # step 3 逾期数据检查，大单1单
        withhold = get_withhold_by_item_no(self.item_no)
        # 只检查大单代扣情况
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 1)
        param_loan = {
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "withhold_sign_company": "qjj"
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.rbiz_interface
    def test_manual_overdue_one_period_two_asset(self):
        """
        :return:
        """
        # 修改大小单还款时间
        self.change_asset_due_at(-1, -1)

        # 刷新罚息
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

        # 发起manual代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
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

        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)
        self.task.run_task_by_order_no_count(withhold_no_loan[0]["withhold_request_no"], count=3)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_serial_no"], count=3)
        self.task.run_task_by_order_no_count(withhold_no_loan[0]["withhold_serial_no"], count=3)
        self.task.run_task_by_order_no_count(self.item_no, count=3)
        self.task.run_task_by_order_no_count(self.item_num_no_loan, count=3)

        # step 3 逾期数据检查，大单1单
        withhold = get_withhold_by_item_no(self.item_no)
        # 检查大单代扣情况
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 2)
        param_loan = {
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "withhold_sign_company": "qjj"
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_num_no_loan)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.rbiz_interface
    def test_fox_overdue_repay(self):
        """
        该测试用例涉及了逾期手动代扣，资产逾期后，由paysvr代扣，收罚息
        :return:
        """
        # 修改大小单还款时间
        self.change_asset_due_at(-1, -1)

        # 刷新罚息
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

        withhold = get_withhold_by_item_no(self.item_no)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_request_no"], count=3)
        self.task.run_task_by_order_no_count(withhold[0]["withhold_serial_no"], count=3)

        # step 3 逾期数据检查，大单1单
        withhold = get_withhold_by_item_no(self.item_no)
        # 只检查大单代扣情况
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 1)
        param_loan = {
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "withhold_sign_company": "qjj"
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.rbiz_interface
    def test_four_factor_withhold(self):
        """
        该测试用例涉及了四要素代扣
        :return:
        """
        params_four_factor = {
            "card_num_encrypt": self.four_element['data']["bank_code_encrypt"],
            "card_user_phone_encrypt": self.four_element['data']["phone_number_encrypt"],
            "card_user_id_encrypt": self.four_element['data']["id_number_encrypt"],
            "card_user_name_encrypt": self.four_element['data']["user_name_encrypt"],
            "amount": 10000

        }
        four_factor_withhold(**params_four_factor)

    # @pytest.mark.rbiz_auto_test
    # @pytest.mark.rbiz_interface
    def test_trade_withhold(self):
        """
        该测试用例涉及了订单代扣
        :return:
        """
        resp = trade_withhold("Trade" + get_random_num(), "test_trade_type", "KN", 50000)
        merchant_key = resp['content']['data']['order_no']
        paysvr_trade_callback(merchant_key, 3, channel_name="baofoo_tq4_protocol")
        paysvr_trade_callback(merchant_key, 2, channel_name="baofoo_tq4_protocol")

    @pytest.mark.rbiz_auto_test
    @pytest.mark.rbiz_interface
    def test_asset_tran_decrease_late_fee(self):
        """
        该测试用例涉及了减免罚息
        :return:
        """
        # 修改大小单还款时间
        self.change_asset_due_at(-1, -1)
        # 刷新罚息
        self.refresh_late_fee(self.item_no)
        asset_tran_decrease_late_fee(self.item_no, 1, 1)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.rbiz_interface
    def test_asset_provision_settle(self):
        """
        该测试用例涉及了拨备结清
        :return:
        """
        # 修改大小单还款时间
        self.change_asset_due_at(-1, -1)
        asset_provision_settle(self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.rbiz_interface
    def test_account_balance_clear(self):
        """
        该测试用例涉及了 逆操作以及余额清空
        :return:
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # step 3 执行task和msg
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()
        # # self.run_all_msg_after_repay_success()
        self.check_response_after_apply_success(repay_resp, withhold, withhold_no_loan)
        withhold = get_withhold_by_item_no(self.item_no)
        asset_repay_reverse(self.item_no, withhold[0]['withhold_channel_key'])
        account_balance_clear(self.item_no, self.four_element['data']["id_number_encrypt"])
        fix_status_asset_change_mq_sync(self.item_no)

    # @pytest.mark.rbiz_auto_test
    # @pytest.mark.rbiz_interface
    def test_active_coupon_repay(self):
        """
        提前还1期
        """
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element, sub_order_type="runqian")
        # step 1 修改资产到期日
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        params_combo_active = {
            "project_num_loan_channel_amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "project_num_no_loan_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]),
            "coupon_num": "coupon" + get_random_num(),
            "coupon_amount": 1000
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'])
        repay_resp = resp_combo_active['content']
        # step 3 执行task和msg
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()
        # # self.run_all_msg_after_repay_success()
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
        check_withhold_sign_company(order_no, "qjj")
        param_loan = {
            "withhold_amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "withhold_sign_company": "qjj"
        }
        check_withhold_result_without_split(self.item_no, **param_loan)
        # 小单代扣和明细
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"]) - 1000,
            "coupon_amount": 1000,
            "withhold_sign_company": self.exp_sign_company_no_loan
        }
        # check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        check_asset_tran_repay_one_period(self.item_no)
