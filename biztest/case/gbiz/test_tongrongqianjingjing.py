from biztest.function.biz.biz_db_function import wait_biz_asset_appear
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.tongrongqianjingjing import TongrongqianjingjingMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.util.easymock.deposit import DepositMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_db_function import update_confirm_data_by_item_no, update_router_capital_plan_amount, \
    insert_asset_confirm, update_all_channel_amount
from biztest.util.tools.tools import get_four_element
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.gbiz.gbiz_tongrongqianjingjing_config import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest


class TestTongrongqianjingjing(BaseTestCapital):
    def init(self):
        super(TestTongrongqianjingjing, self).init()
        self.channel = "tongrongqianjingjing"
        self.capital_mock = TongrongqianjingjingMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        self.deposit_mock = DepositMock(gbiz_mock)
        update_gbiz_capital_tongrongqianjingjing()
        update_gbiz_capital_tongrongqianjingjing_const()
        update_gbiz_payment_config(self.payment_mock.url)
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):

        self.init()

    def register(self, item_no, four_element):
        self.payment_register(self.payment_mock, self.channel, four_element, item_no)

    def loan_to_success(self, item_no):
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_bk2001(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_bk2002(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_bk2003()
        self.capital_mock.update_bk3001()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_bk3003(item_no)
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.payment_mock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + 'w', "success", "success")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.capital_mock.update_bk4001()
        self.task.run_task(item_no, "LoanGrantStatusPush")
        self.msg.run_msg_by_order_no(item_no)
        wait_biz_asset_appear(item_no)
        # 下载借款合同，资方返回协议URL有有效性
        self.capital_mock.update_bk3004(item_no)
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})

    def trans_to_success(self, item_no):
        self.task.run_task(item_no, "BondTransfer", excepts={"code": 0})
        self.payment_mock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "PaymentTransferNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + 't', "success", "success")
        self.task.run_task(item_no, "PaymentTransferQuery", excepts={"code": 0})
        self.task.run_task(item_no, "BondTransferQuery", excepts={"code": 0})
        # 下载债转协议及债转通知书，资方返回协议URL有有效性
        # self.capital_mock.update_bk3005()
        # self.task.run_task(item_no, "BondContractDown", excepts={"code": 0})
        # self.capital_mock.update_bk3005()
        # self.task.run_task(item_no, "ElectronicReceiptDown", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_tongrongqianjingjing
    @pytest.mark.gbiz_tongrongqianjingjing_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12),
                                 # ("香蕉", "irr36_quanyi", 6),
                                 # ("草莓", "irr36_quanyi", 12),
                             ])
    def test_tongrongqianjingjing_success(self, case, app, source_type, period):
        """
         通融钱京京放款成功
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 4000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        self.trans_to_success(item_no)
        check_asset_tran_data(item_no)
        # check_request_log_by_channel(item_no, self.channel)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tongrongqianjingjing
    @pytest.mark.parametrize("count", [12])
    def test_tongrongqianjingjing_applynew_fail(self, case, count):
        """
         通融钱京京订单失败，切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 5000)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_bk2001(item_no, code="00000", applyStatus="3")
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_bk2002_noorder()
        check_wait_change_capital_data(item_no, 10000, "00000_true_成功_3_B")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tongrongqianjingjing
    @pytest.mark.parametrize("count", [12])
    def test_tongrongqianjingjing_applyquery_fail(self, case, count):
        """
         通融钱京京订单失败，切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_bk2001(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_bk2002(item_no, applyStatus="3")
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10000, "00000_true_成功_3_A")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tongrongqianjingjing
    @pytest.mark.parametrize("count", [12])
    def test_tongrongqianjingjing_withdraw_fail(self, case, count):
        """
         通融钱京京代付失败，切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_bk2001(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_bk2002(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_bk2003()
        self.capital_mock.update_bk3001()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_bk3003(item_no)
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.payment_mock.update_withdraw_balance_enough(0)
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 1})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "\\[1000\\].*代付账户余额为0")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tongrongqianjingjing
    @pytest.mark.parametrize("count", [12])
    def test_tongrongqianjingjing_canloan_fail(self, case, count):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        # canloan失败准备工作
        today = time.strftime("%Y-%m-%d", time.localtime())
        update_router_capital_plan_amount(0, today, self.channel)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        time.sleep(2)
        # canloan执行之后恢复
        update_router_capital_plan_amount(3333333333, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "tongrongqianjingjing->校验资金量失败;")

    def before_update_card_process(self):
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, 12, 8000)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_bk2001(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_bk2002(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_bk2003()
        self.capital_mock.update_bk3001()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_bk3003(item_no)
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.payment_mock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "w", "fail", "fail", platform_code="KN_INVALID_ACCOUNT", platform_message="无效账户")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        return item_no, asset_info, four_element

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tongrongqianjingjing
    def test_tongrongqianjingjing_update_card(self, case):
        """
        换卡后，放款成功
        """
        item_no, asset_info, old_element = self.before_update_card_process()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "等待换卡"})
        check_asset_loan_record(item_no, asset_loan_record_status=4)
        # 换卡
        self.msg.run_msg(item_no, "UpdateCardNotify", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        new_element = get_four_element()
        update_receive_card(asset_info, new_element, old_element)
        check_confirm_data(item_no, self.channel, 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_asset_event_exist(item_no, self.channel, "UPDATE_CARD_EVENT_TYPE")
        check_asset_loan_record(item_no, asset_loan_record_status=3)
        self.msg.run_msg(item_no, "UpdateCardSyncNotify", excepts={"code": 0})
        # 换卡后放款成功
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "w", "success", "success")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.capital_mock.update_bk4001()
        self.task.run_task(item_no, "LoanGrantStatusPush")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tongrongqianjingjing
    def test_tongrongqianjingjing_update_card_then_fail(self, case):
        """
        换卡后，放款失败（卡原因）
        """
        item_no, asset_info, old_element = self.before_update_card_process()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "等待换卡"})
        # 换卡
        self.msg.run_msg(item_no, "UpdateCardNotify", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        new_element = get_four_element()
        update_receive_card(asset_info, new_element, old_element)
        check_confirm_data(item_no, self.channel, 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_asset_event_exist(item_no, self.channel, "UPDATE_CARD_EVENT_TYPE")
        self.msg.run_msg(item_no, "UpdateCardSyncNotify", excepts={"code": 0})
        # 由于卡原因再次代付失败
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "w", "fail", "fail", platform_code="KN_INVALID_ACCOUNT", platform_message="无效账户")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "\\[KN_INVALID_ACCOUNT\\]无效账户")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tongrongqianjingjing
    def test_tongrongqianjingjing_update_card_then_fail_2(self, case):
        """
        换卡后，放款失败（非卡原因）
        """
        item_no, asset_info, old_element = self.before_update_card_process()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "等待换卡"})
        # 换卡
        self.msg.run_msg(item_no, "UpdateCardNotify", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        new_element = get_four_element()
        update_receive_card(asset_info, new_element, old_element)
        check_confirm_data(item_no, self.channel, 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_asset_event_exist(item_no, self.channel, "UPDATE_CARD_EVENT_TYPE")
        self.msg.run_msg(item_no, "UpdateCardSyncNotify", excepts={"code": 0})
        # 由于其他原因再次代付失败
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "w", "fail", "fail", retry=True)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "w", "fail", "fail", retry=True)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "\\[G00022\\]超过最大失败次数{\\[FAILED\\]放款失败}")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tongrongqianjingjing
    def test_tongrongqianjingjing_fail_already_update_card(self, case):
        """
        已换过一次卡，不再换卡，走切资方逻辑
        """
        item_no, asset_info, old_element = self.before_update_card_process()
        # 模拟haohan换卡记录
        insert_asset_confirm(item_no, "haohanqianjingjing", "WITHDRAW_FINAL_FAIL_UPDATE_CARD", 0)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "\\[KN_INVALID_ACCOUNT\\]无效账户")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tongrongqianjingjing
    def test_tongrongqianjingjing_update_card_gbiz_time_out(self, case):
        """
        换卡超时（gbiz超时）
        """
        item_no, asset_info, old_element = self.before_update_card_process()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "等待换卡"})
        self.msg.run_msg(item_no, "UpdateCardNotify", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        # gbiz超时
        update_confirm_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 3, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_wait_assetvoid_data(item_no, 10005, "确认类型\\[WITHDRAW_FINAL_FAIL_UPDATE_CARD\\]已超时")


if __name__ == "__main__":
    pytest.main(["-s", "/Users/fenlai/code/framework-test/biztest/case/gbiz/jining.py", "--env=9" "--junt"])
