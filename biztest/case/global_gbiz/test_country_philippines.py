from biztest.function.global_gbiz.gbiz_global_common_function import run_terminated_task
from biztest.interface.gbiz_global.gbiz_global_interface import asset_import, payment_callback, update_receive_card
from biztest.case.global_gbiz.global_base_test_capital import BaseTestCapital
from biztest.function.global_gbiz.gbiz_global_check_function import check_asset_data, check_wait_change_capital_data, \
    check_confirm_data, check_asset_event_exist, check_global_wait_assetvoid_data
import pytest
from biztest.function.global_gbiz.gbiz_global_db_function import get_asset_import_data_by_item_no, \
    update_all_channel_amount, update_confirm_data_by_item_no, insert_asset_confirm
from biztest.util.tools.tools import get_four_element_global
from biztest.config.global_gbiz.global_gbiz_kv_config import update_gbiz_capital_channel


@pytest.mark.global_gbiz_philippines
class TestCountryPhilippines(BaseTestCapital):
    def init(self):
        super(TestCountryPhilippines, self).init()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()
        self.element = get_four_element_global()

    params = ["channel", "source_type", "count", "day", "withdraw_type", "late_num", "fees"]
    values = [
        ("copper_stone", "pl01", 1, 7, "online", "late7%", {"fin_service": 54.00, "interest": 36.00}),
        ("copper_stone", "pl01", 1, 7, "online", "late12%", {"fin_service": 54.00, "interest": 36.00}),
        ("copper_stone", "pl01", 1, 7, "online", "late12%", {"fin_service": 54.00, "interest": 0}),
        ("glitter", "pl01", 1, 7, "online", "late7%", {"fin_service": 54.00, "interest": 36.00}),
        ("glitter", "pl01", 1, 7, "online", "late12%", {"fin_service": 54.00, "interest": 36.00}),
        ("glitter", "pl01", 1, 7, "online", "late12%", {"fin_service": 54.00, "interest": 0})
    ]

    @pytest.mark.global_gbiz_philippines
    @pytest.mark.parametrize(params, values)
    def test_philippines_loan_success(self, case, channel, source_type, count, day, withdraw_type, late_num, fees):
        update_gbiz_capital_channel(channel)
        item_no, asset_info = asset_import(channel, count, day, "day", 500000, "phl", "peony", source_type,
                                           self.element, withdraw_type, fees=fees, late_num=late_num)
        # 根据withdraw_type判断走线上还是线下
        if withdraw_type == "offline":
            self.loan_to_success_offline(item_no)
        else:
            self.loan_to_success(item_no)
        check_asset_data(asset_info)


    def test_copper_stone_offline_exception(self, case):
        update_gbiz_capital_channel('copper_stone')
        item_no, asset_info = asset_import("copper_stone", 1, 7, "day", 500000, "phl", "jasmine",
                                           "pl01", self.element, "offline",
                                           fees={"fin_service": 54.00, "interest": 36.00}, late_num='late12%')

        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})

        self.paymentmock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        self.paymentmock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})

        self.paymentmock.update_phl_offline_withdraw_query_status(asset_info, "process", "process")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        payment_callback(asset_info, 1)
        # 对于线下支付来说，若是返回的支付码与上一次获取到的不一致，则会报错重试
        self.paymentmock.update_phl_offline_withdraw_status_exception(asset_info, "process", "process")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 2})

    def test_copper_stone_online_exception(self, case):
        update_gbiz_capital_channel('copper_stone')
        item_no, asset_info = asset_import("copper_stone", 1, 7, "day", 500000, "phl", "jasmine",
                                           "pl01", self.element, "online",
                                           fees={"fin_service": 54.00, "interest": 36.00}, late_num='late12%')
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})

        self.paymentmock.update_withdraw_balance_not_enouth()
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        # 因为余额不足，会导致代付任务重试
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 2})

    def test_copper_stone_online_fail(self, case):
        update_gbiz_capital_channel('copper_stone')
        item_no, asset_info = asset_import("copper_stone", 1, 7, "day", 500000, "phl", "jasmine",
                                           "pl01", self.element, "online",
                                           fees={"fin_service": 54.00, "interest": 36.00}, late_num='late12%')
        self.loan_to_fail(item_no)
        check_wait_change_capital_data(item_no, 1, "\\[KN_INVALID_ACCOUNT\\]")
        # 更新
        run_terminated_task(item_no, "ChangeCapital", 1)


    def test_copper_stone_update_card_o2o(self, case):
        """
        线上->线上换卡后，放款成功
        """
        update_gbiz_capital_channel('copper_stone')
        item_no, asset_info = asset_import("copper_stone", 1, 7, "day", 500000, "phl", "jasmine",
                                           "pl01", self.element, "online",
                                           fees={"fin_service": 54.00, "interest": 36.00}, late_num='late12%')
        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        self.msgsender.run_msg_by_order_no(item_no)
        check_confirm_data(item_no, "copper_stone", 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        update_receive_card(asset_info, time_out=False, withdraw_type="online")
        check_confirm_data(item_no, "copper_stone", 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
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


    def test_copper_stone_update_card_o2f(self, case):
        """
        线上->线下换卡后，放款成功
        """
        update_gbiz_capital_channel('copper_stone')
        item_no, asset_info = asset_import("copper_stone", 1, 7, "day", 500000, "phl", "jasmine",
                                           "pl01", self.element, "online",
                                           fees={"fin_service": 54.00, "interest": 36.00}, late_num='late12%')
        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        self.msgsender.run_msg_by_order_no(item_no)
        check_confirm_data(item_no, "copper_stone", 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        update_receive_card(asset_info, time_out=False, withdraw_type="offline")
        check_confirm_data(item_no, "copper_stone", 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_asset_event_exist(item_no, "UPDATE_CARD")
        # 换卡后放款成功
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.paymentmock.update_withdraw_balance_enough()
        self.paymentmock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.paymentmock.update_phl_offline_withdraw_query_status(asset_info, "process", "process")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        self.msgsender.run_msg_by_order_no(item_no)
        payment_callback(asset_info, 2)
        self.paymentmock.update_withdraw_query_status(asset_info, "success", "success")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalDataNotify", excepts={"code": 0})
        self.task.run_task(item_no, "GrantSuccessNotify", excepts={"code": 0})
        self.msgsender.run_msg_by_order_no(item_no)

    def test_copper_stone_update_card_fail(self, case):
        """
        换卡后，放款失败（卡原因）
        """
        update_gbiz_capital_channel('copper_stone')
        item_no, asset_info = asset_import("copper_stone", 1, 7, "day", 500000, "phl", "jasmine",
                                           "pl01", self.element, "online",
                                           fees={"fin_service": 54.00, "interest": 36.00}, late_num='late12%')
        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        self.msgsender.run_msg_by_order_no(item_no)
        check_confirm_data(item_no, "copper_stone", 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        update_receive_card(asset_info, time_out=False, withdraw_type="online")
        check_confirm_data(item_no, "copper_stone", 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
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


    def test_copper_stone_update_card_fail_2(self, case):
        """
        换卡后，放款失败（非卡原因）
        """
        update_gbiz_capital_channel('copper_stone')
        item_no, asset_info = asset_import("copper_stone", 1, 7, "day", 500000, "phl", "jasmine",
                                           "pl01", self.element, "online",
                                           fees={"fin_service": 54.00, "interest": 36.00}, late_num='late12%')
        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        self.msgsender.run_msg_by_order_no(item_no)
        check_confirm_data(item_no, "copper_stone", 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        update_receive_card(asset_info, time_out=False, withdraw_type="online")
        check_confirm_data(item_no, "copper_stone", 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
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
            item_no, 1, "\\[G00022\\]超过最大失败次数{\\[rejected\\]Payout failed. Reinitiate transfer after 30 min.}")


    def test_copper_stone_fail_already_update_card(self, case):
        """
        已换过一次卡，不再换卡，走切资方逻辑
        """
        update_gbiz_capital_channel('copper_stone')
        item_no, asset_info = asset_import("copper_stone", 1, 7, "day", 500000, "phl", "jasmine",
                                           "pl01", self.element, "online",
                                           fees={"fin_service": 54.00, "interest": 36.00}, late_num='late12%')
        self.before_update_card_process(item_no)
        # 模拟u_peso换卡记录
        insert_asset_confirm(item_no, "glitter", "WITHDRAW_FINAL_FAIL_UPDATE_CARD", 0)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "\\[KN_INVALID_ACCOUNT\\]Invalid account, please check it")
    # @pytest.mark.global_gbiz_philippines1
    # def test_copper_stone_update_card_switch_off(self, case):
    #     """
    #     换卡开关关闭，走切资方逻辑
    #     """
    #     update_gbiz_capital_channel('copper_stone')
    #     item_no, asset_info = asset_import("copper_stone", 1, 7, "day", 500000, "phl", "jasmine",
    #                                        "postservice54%_rate1‰_late7%", self.element, "online")
    #     self.before_update_card_process(item_no)
    #     self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
    #     check_wait_change_capital_data(item_no, 1, "\\[KN_INVALID_ACCOUNT\\]Invalid account, please check it")

    def test_copper_stone_update_card_bc_time_out(self, case):
        """
        换卡超时（bc超时）
        """
        update_gbiz_capital_channel('copper_stone')
        item_no, asset_info = asset_import("copper_stone", 1, 7, "day", 500000, "phl", "jasmine",
                                           "pl01", self.element, "online",
                                           fees={"fin_service": 54.00, "interest": 36.00}, late_num='late12%')
        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        self.msgsender.run_msg_by_order_no(item_no)
        check_confirm_data(item_no, "copper_stone", 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        # bc超时
        update_receive_card(asset_info, time_out=True, withdraw_type="online")
        check_confirm_data(item_no, "copper_stone", 3, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_global_wait_assetvoid_data(item_no, 10, "换卡超时")

    def test_copper_stone_update_card_gbiz_time_out(self, case):
        """
        换卡超时（gbiz超时）
        """
        update_gbiz_capital_channel('copper_stone')
        item_no, asset_info = asset_import("copper_stone", 1, 7, "day", 500000, "phl", "jasmine",
                                           "pl01", self.element, "online",
                                           fees={"fin_service": 54.00, "interest": 36.00}, late_num='late12%')
        self.before_update_card_process(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
        self.msgsender.run_msg_by_order_no(item_no)
        check_confirm_data(item_no, "copper_stone", 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        # gbiz超时
        update_confirm_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 0})
        check_confirm_data(item_no, "copper_stone", 3, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_global_wait_assetvoid_data(item_no, 10005, "换卡超时")
