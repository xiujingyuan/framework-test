from biztest.interface.gbiz_global.gbiz_global_interface import asset_import, update_receive_card, payment_callback
from biztest.config.global_gbiz.global_gbiz_kv_config import update_pak_gbiz_payment_config, \
    update_gbiz_capital_channel
from biztest.function.global_gbiz.gbiz_global_db_function import update_router_capital_plan_amount_all_to_zero, \
    update_all_channel_amount, update_confirm_data_by_item_no
from biztest.case.global_gbiz.global_base_test_capital import BaseTestCapital
import pytest
from biztest.util.tools.tools import get_four_element_global
from biztest.function.global_gbiz.gbiz_global_check_function import *


@pytest.mark.global_gbiz_pakistan
class TestCountryPakistan(BaseTestCapital):
    def init(self):
        super(TestCountryPakistan, self).init()
        update_all_channel_amount()
        update_pak_gbiz_payment_config(self.paymentmock.url)

    @pytest.fixture()
    def case(self):
        self.init()

    params = ["channel", "source_type", "count", "day", "withdraw_type", "late_num", "fees"]
    values = [
        ("goldlion", "pl01", 1, 7, 'online', "late2%", {"fin_service": 33.00}),
        ("goldlion", "pl01", 1, 7, 'offline', "late2%", {"fin_service": 33.00}),
    ]
    @pytest.mark.parametrize(params, values)
    def test_pakistan_loan_success(self, case, channel, source_type, count, day, withdraw_type, late_num, fees):
        update_gbiz_capital_channel(channel)
        # 后置收费的资产没有小单
        element = get_four_element_global()
        item_no, asset_info = asset_import(channel, count, day, "day", 500000, "pak", "pak001", source_type, element,
                                           withdraw_type, fees={"fin_service": 33.00}, late_num="late2%")
        self.loan_to_success(item_no)
        # 放款数据检查
        asset = get_asset_info_by_item_no(item_no)
        asset_info['data']['asset']['cmdb_product_number'] = asset[0]["asset_cmdb_product_number"]
        check_asset_data(asset_info)

    def test_goldlion_update_card_o2o(self, case):
        """
        线上->线上换卡后，放款成功
        """
        update_gbiz_capital_channel("goldlion")
        element = get_four_element_global()
        item_no, asset_info = asset_import("goldlion", 1, 7, "day", 500000, "pak", "pak001", "pl01", element,
                                           "online", fees={"fin_service": 33.00}, late_num="late2%")
        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        self.msgsender.run_msg_by_order_no(item_no)
        check_confirm_data(item_no, "goldlion", 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        update_receive_card(asset_info, time_out=False, withdraw_type="online")
        check_confirm_data(item_no, "goldlion", 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_asset_event_exist(item_no, "UPDATE_CARD")
        # 换卡后放款成功
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        self.paymentmock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.paymentmock.update_withdraw_query_status(asset_info, "success", "success")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalDataNotify", excepts={"code": 0})
        self.task.run_task(item_no, "GrantSuccessNotify", excepts={"code": 0})
        self.msgsender.run_msg_by_order_no(item_no)

    def test_goldlion_update_card_bc_time_out(self, case):
        """
        换卡超时（bc超时）
        """
        update_gbiz_capital_channel("goldlion")
        element = get_four_element_global()
        item_no, asset_info = asset_import("goldlion", 1, 7, "day", 500000, "pak", "pak001", "pl01", element,
                                           "online", fees={"fin_service": 33.00}, late_num="late2%")
        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        self.msgsender.run_msg_by_order_no(item_no)
        check_confirm_data(item_no, "goldlion", 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        # bc超时
        update_receive_card(asset_info, time_out=True, withdraw_type="online")
        check_confirm_data(item_no, "goldlion", 3, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_global_wait_assetvoid_data(item_no, 10, "换卡超时")

    params = ["channel", "source_type", "count", "day", "withdraw_type"]
    values = [("goldlion", "postservice33%_rate0%_late2%", 1, 7, 'online')
              ]

    def test_goldlion_update_card_gbiz_time_out(self, case):
        """
        换卡超时（gbiz超时）
        """
        update_gbiz_capital_channel("goldlion", over_time_seconds=0)
        element = get_four_element_global()
        item_no, asset_info = asset_import("goldlion", 1, 7, "day", 500000, "pak", "pak001", "pl01", element,
                                           "online", fees={"fin_service": 33.00}, late_num="late2%")
        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        self.msgsender.run_msg_by_order_no(item_no)
        check_confirm_data(item_no, "goldlion", 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        # gbiz超时
        update_confirm_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 0})
        check_confirm_data(item_no, "goldlion", 3, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_global_wait_assetvoid_data(item_no, 10005, "换卡超时")

    def test_goldlion_update_card_fail(self, case):
        """
        换卡后，放款失败（卡原因）
        """
        update_gbiz_capital_channel("goldlion")
        element = get_four_element_global()
        item_no, asset_info = asset_import("goldlion", 1, 7, "day", 500000, "pak", "pak001", "pl01", element,
                                           "online", fees={"fin_service": 33.00}, late_num="late2%")
        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        self.msgsender.run_msg_by_order_no(item_no)
        check_confirm_data(item_no, "goldlion", 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        update_receive_card(asset_info, time_out=False, withdraw_type="online")
        check_confirm_data(item_no, "goldlion", 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_asset_event_exist(item_no, "UPDATE_CARD")
        # 由于卡原因再次代付失败
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        self.paymentmock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.paymentmock.update_withdraw_query_status(asset_info, "fail", "fail", platform_code="KN_INVALID_ACCOUNT",
                                                      platform_message="Invalid account, please check it")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "\\[KN_INVALID_ACCOUNT\\]Invalid account, please check it")

    def test_goldlion_update_card_fail_2(self, case):
        """
        换卡后，放款失败（非卡原因）
        """
        update_gbiz_capital_channel("goldlion")
        element = get_four_element_global()
        item_no, asset_info = asset_import("goldlion", 1, 7, "day", 500000, "pak", "pak001", "pl01", element,
                                           "online", fees={"fin_service": 33.00}, late_num="late2%")
        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        self.msgsender.run_msg_by_order_no(item_no)
        check_confirm_data(item_no, "goldlion", 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        update_receive_card(asset_info, time_out=False, withdraw_type="online")
        check_confirm_data(item_no, "goldlion", 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_asset_event_exist(item_no, "UPDATE_CARD")
        # 由于其他原因再次代付失败
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.paymentmock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.paymentmock.update_withdraw_query_status(asset_info, "fail", "fail", retry=True)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        self.paymentmock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.paymentmock.update_withdraw_query_status(asset_info, "fail", "fail", retry=True)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(
            item_no, 1, "\\[rejected\\]Payout failed. Reinitiate transfer after 30 min.")

    # def test_goldlion_update_card_switch_off(self, case):
    #     """
    #     换卡开关关闭，走切资方逻辑
    #     """
    #     update_gbiz_capital_channel("goldlion")
    #     element = get_four_element_global()
    #     item_no, asset_info = asset_import("goldlion", 1, 7, "day", 500000, "pak", "pak001", "pl01", element,
    #                                        "online", fees={"fin_service": 33.00}, late_num="late2%")
    #     self.before_update_card_process(item_no)
    #     self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
    #     check_wait_change_capital_data(item_no, 1, "\\[KN_INVALID_ACCOUNT\\]Invalid account, please check it")
