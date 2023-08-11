from biztest.interface.gbiz_global.gbiz_global_interface import update_receive_card
from biztest.config.global_gbiz.global_gbiz_kv_config import update_gbiz_capital_channel, update_gbiz_payment_config
from biztest.function.global_gbiz.gbiz_global_db_function import update_all_channel_amount, \
    update_confirm_data_by_item_no
from biztest.case.global_gbiz.global_base_test_capital import BaseTestCapital
import pytest
from biztest.function.global_gbiz.gbiz_global_check_function import *


@pytest.mark.global_gbiz_update_card
@pytest.mark.global_gbiz_thailand
class TestUptateCard(BaseTestCapital):
    def init(self):
        super(TestUptateCard, self).init()
        update_all_channel_amount()
        update_gbiz_payment_config(self.paymentmock.url)

    @pytest.fixture()
    def case(self):
        self.init()

    @pytest.mark.global_gbiz_thailand2
    def test_update_card_o2o(self, case):
        """
        线上->线上换卡后，放款成功
        """
        item_no, asset_info = self.asset_import_data()
        channel = asset_info["data"]["asset"]["loan_channel"]
        update_gbiz_capital_channel(channel)

        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})

        check_confirm_data(item_no, channel, 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        update_receive_card(asset_info, time_out=False, withdraw_type="online")
        check_confirm_data(item_no, channel, 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
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

    def test_goldlion_update_card_bc_time_out(self, case):
        """
        换卡超时（bc超时）
        """
        item_no, asset_info = self.asset_import_data()
        channel = asset_info["data"]["asset"]["loan_channel"]
        update_gbiz_capital_channel(channel)

        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        check_confirm_data(item_no, channel, 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        # bc超时
        update_receive_card(asset_info, time_out=True, withdraw_type="online")
        check_confirm_data(item_no, channel, 3, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_global_wait_assetvoid_data(item_no, 10, "换卡超时")

    def test_goldlion_update_card_gbiz_time_out(self, case):
        """
        换卡超时（gbiz超时）
        """
        item_no, asset_info = self.asset_import_data()
        channel = asset_info["data"]["asset"]["loan_channel"]
        update_gbiz_capital_channel(channel)

        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        check_confirm_data(item_no, channel, 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        # gbiz超时
        update_confirm_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 0})
        check_confirm_data(item_no, channel, 3, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_global_wait_assetvoid_data(item_no, 10005, "换卡超时")

    def test_goldlion_update_card_fail(self, case):
        """
        换卡后，放款失败（卡原因）
        """
        item_no, asset_info = self.asset_import_data()
        channel = asset_info["data"]["asset"]["loan_channel"]
        update_gbiz_capital_channel(channel)

        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        check_confirm_data(item_no, channel, 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        update_receive_card(asset_info, time_out=False, withdraw_type="online")
        check_confirm_data(item_no, channel, 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
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
        item_no, asset_info = self.asset_import_data()
        channel = asset_info["data"]["asset"]["loan_channel"]
        update_gbiz_capital_channel(channel)

        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        check_confirm_data(item_no, channel, 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        update_receive_card(asset_info, time_out=False, withdraw_type="online")
        check_confirm_data(item_no, channel, 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
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
    #     item_no, asset_info = self.asset_import_data()
    #     channel = asset_info["data"]["asset"]["loan_channel"]
    #     update_gbiz_capital_channel(channel, allow_update_card="false")
    #
    #     self.before_update_card_process(item_no)
    #     self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
    #     check_wait_change_capital_data(item_no, 1, "\\[KN_INVALID_ACCOUNT\\]Invalid account, please check it")
