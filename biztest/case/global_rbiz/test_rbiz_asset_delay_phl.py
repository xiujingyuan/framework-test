import pytest

from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.global_rbiz.global_rbiz_kv_config import update_rbiz_config
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto
from biztest.function.global_rbiz.rbiz_global_check_function import check_asset_data, check_asset_delay_data
from biztest.function.global_rbiz.rbiz_global_db_function import get_asset_tran_balance_amount_by_item_no, \
    get_asset_tran, earease_amount, get_withhold
from biztest.interface.rbiz.rbiz_global_interface import trade_withhold
from biztest.util.asserts.assert_util import Assert
from biztest.util.db.db_util import DataBase
from biztest.util.tools.tools import get_four_element_global, get_date

"""
展期：先还展期(够的情况)，再还资产，再还共债，再放到虚户

"""


@pytest.mark.global_rbiz_thailand
@pytest.mark.asset_delay_phl
class TestRbizAssetDelayPhl(BaseGlobalRepayTest):
    source_type = "service20_rate1%_late1%"
    @pytest.fixture(scope="function")
    def setup_4(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        super(TestRbizAssetDelayPhl, self).init()
        update_rbiz_config(special_service_name="phl_special_service")
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element, 4)

    def test_asset_delay_fail_amount_less(self, setup_4):
        # 打款金额 < （bc返回展期金额 - 增量罚息）- 抹零
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.loan_active_repay_apply(project_num_loan_channel_amount, payment_type="paycode", payment_option="wallet")
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})

        delay_apply_amount = 25000 * 0.2 + 3500 * 3 + 125 * 1
        self.update_asset_due_at(-1, period=2, refresh=True)
        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="paycode",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-2, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount + 125

        trade_merchant_key = self.repay_trade(
            {"item_no": self.item_no, "amount": bc_delay_amount - earease_amount(bc_delay_amount - 125) - 125 - 1,
             "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_fee_amount=39749, repaid_late_amount=250, repaid_amount=168499,
                         fee_amount=100000, late_amount=250, balance_amount=445751)
        check_asset_delay_data(trade_merchant_key, apply_amount=15625, pay_amount=14999, pay_status="success",
                               delay_status="fail")

    def test_asset_delay_success_amount_equal(self, setup_4):
        # 打款金额 = （bc返回展期金额 - 增量罚息）- 抹零
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.loan_active_repay_apply(project_num_loan_channel_amount, payment_type="paycode", payment_option="wallet")
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})

        delay_apply_amount = 25000 * 0.2 + 3500 * 3 + 125 * 1
        self.update_asset_due_at(-1, period=2, refresh=True)
        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="paycode",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-2, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount + 125

        trade_merchant_key = self.repay_trade(
            {"item_no": self.item_no, "amount": bc_delay_amount - earease_amount(bc_delay_amount - 125) - 125,
             "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25000, repaid_late_amount=250, repaid_amount=164250,
                         fee_amount=100000, late_amount=250, balance_amount=450000)
        check_asset_delay_data(trade_merchant_key, apply_amount=15625, pay_amount=15000, pay_status="success",
                               delay_status="success")

    def test_asset_delay_success_amount_more(self, setup_4):
        # 打款金额 > bc返回展期金额，多余还资产
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.loan_active_repay_apply(project_num_loan_channel_amount, payment_type="paycode", payment_option="wallet")
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})

        delay_apply_amount = 25000 * 0.2 + 3500 * 3 + 125 * 1
        self.update_asset_due_at(-1, period=2, refresh=True)
        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="paycode",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-2, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount + 125

        trade_merchant_key = self.repay_trade(
            {"item_no": self.item_no, "amount": bc_delay_amount + 1,
             "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25001, repaid_late_amount=250, repaid_amount=164251,
                         fee_amount=100000, late_amount=250, balance_amount=449999)
        check_asset_delay_data(trade_merchant_key, apply_amount=15625, pay_amount=15751, pay_status="success",
                               delay_status="success")

    def test_asset_delay_second_success_amount_equal(self, setup_4):
        # 打款金额 = （bc返回展期金额 - 增量罚息）- 抹零
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.loan_active_repay_apply(project_num_loan_channel_amount, payment_type="paycode", payment_option="wallet")
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})

        delay_apply_amount = 25000 * 0.2 + 3500 * 3 + 125 * 1
        self.update_asset_due_at(-1, period=2, refresh=True)
        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="paycode",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-2, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount + 125

        self.repay_trade(
            {"item_no": self.item_no, "amount": bc_delay_amount - earease_amount(bc_delay_amount - 125) - 125,
             "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25000, repaid_late_amount=250, repaid_amount=164250,
                         fee_amount=100000, late_amount=250, balance_amount=450000)

        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="paycode",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-10, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount
        trade_merchant_key = self.repay_trade(
            {"item_no": self.item_no, "amount": bc_delay_amount - earease_amount(bc_delay_amount - 125) - 125,
             "status": 2, "finish_at": get_date(day=-1)})

        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25000, repaid_late_amount=375, repaid_amount=164375,
                         fee_amount=100000, late_amount=375, balance_amount=450000)
        check_asset_delay_data(trade_merchant_key, apply_amount=15625, pay_amount=15000, pay_status="success",
                               delay_status="success")

    def test_asset_delay_second_success_amount_more(self, setup_4):
        # 打款金额 > bc返回展期金额，多余还资产
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.loan_active_repay_apply(project_num_loan_channel_amount, payment_type="paycode", payment_option="wallet")
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})

        delay_apply_amount = 25000 * 0.2 + 3500 * 3 + 125 * 1
        self.update_asset_due_at(-1, period=2, refresh=True)
        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="paycode",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-2, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount + 125

        self.repay_trade(
            {"item_no": self.item_no, "amount": bc_delay_amount + 1,
             "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25001, repaid_late_amount=250, repaid_amount=164251,
                         fee_amount=100000, late_amount=250, balance_amount=449999)

        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="paycode",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-10, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount
        trade_merchant_key = self.repay_trade(
            {"item_no": self.item_no, "amount": bc_delay_amount + 1,
             "status": 2, "finish_at": get_date(day=-1)})

        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25002, repaid_late_amount=375, repaid_amount=164377,
                         fee_amount=100000, late_amount=375, balance_amount=449998)
        check_asset_delay_data(trade_merchant_key, apply_amount=15625, pay_amount=15626, pay_status="success",
                               delay_status="success")

    def test_collect_asset_delay_fail_amount_less(self, setup_4):
        # 打款金额 < （bc返回展期金额 - 增量罚息）- 抹零
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.loan_active_repay_apply(project_num_loan_channel_amount, payment_type="paycode", payment_option="wallet")
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})

        delay_apply_amount = 25000 * 0.2 + 3500 * 3 + 125 * 1
        self.update_asset_due_at(-1, period=2, refresh=True)
        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="collect",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-2, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount + 125

        trade_merchant_key = self.repay_collect(
            {"item_no": self.item_no, "amount": bc_delay_amount - earease_amount(bc_delay_amount - 125) - 125 - 1,
             "repay_type": "delay", "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_fee_amount=39749, repaid_late_amount=250, repaid_amount=168499,
                         fee_amount=100000, late_amount=250, balance_amount=445751)
        withhold = get_withhold(withhold_serial_no=trade_merchant_key)[0]
        Assert.assert_match_json(
            self.task.get_task(task_order_no=withhold["withhold_channel_key"],
                               task_type="offline_withhold_process")[0]["task_response_data"],
            {"code": 0, "message": "未匹配到可以用的代扣记录进行共债资产还款"})

    def test_collect_asset_delay_success_amount_equal(self, setup_4):
        # 打款金额 = （bc返回展期金额 - 增量罚息）- 抹零
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.loan_active_repay_apply(project_num_loan_channel_amount, payment_type="paycode", payment_option="wallet")
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})

        delay_apply_amount = 25000 * 0.2 + 3500 * 3 + 125 * 1
        self.update_asset_due_at(-1, period=2, refresh=True)
        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="collect",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-2, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount + 125

        trade_merchant_key = self.repay_collect(
            {"item_no": self.item_no, "amount": bc_delay_amount - earease_amount(bc_delay_amount - 125) - 125,
             "repay_type": "delay", "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25000, repaid_late_amount=250, repaid_amount=164250,
                         fee_amount=100000, late_amount=250, balance_amount=450000)
        check_asset_delay_data(trade_merchant_key, apply_amount=15625, pay_amount=15000, pay_status="success",
                               delay_status="success")

    def test_collect_asset_delay_success_amount_more(self, setup_4):
        # 打款金额 > bc返回展期金额 - 抹零 - 增量罚息
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.loan_active_repay_apply(project_num_loan_channel_amount, payment_type="paycode", payment_option="wallet")
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})

        delay_apply_amount = 25000 * 0.2 + 3500 * 3 + 125 * 1
        self.update_asset_due_at(-1, period=2, refresh=True)
        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="collect",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-2, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount + 125

        trade_merchant_key = self.repay_collect(
            {"item_no": self.item_no, "amount": bc_delay_amount + 1,
             "repay_type": "delay", "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25001, repaid_late_amount=250, repaid_amount=164251,
                         fee_amount=100000, late_amount=250, balance_amount=449999)
        check_asset_delay_data(trade_merchant_key, apply_amount=15625, pay_amount=15751, pay_status="success",
                               delay_status="success")

    def test_collect_asset_delay_second_fail_amount_less(self, setup_4):
        # 打款金额 = （bc返回展期金额 - 增量罚息）- 抹零
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.loan_active_repay_apply(project_num_loan_channel_amount, payment_type="paycode", payment_option="wallet")
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})

        delay_apply_amount = 25000 * 0.2 + 3500 * 3 + 125 * 1
        self.update_asset_due_at(-1, period=2, refresh=True)
        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="collect",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-2, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount + 125

        self.repay_collect(
            {"item_no": self.item_no, "amount": bc_delay_amount - earease_amount(bc_delay_amount - 125) - 125,
             "repay_type": "delay", "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25000, repaid_late_amount=250, repaid_amount=164250,
                         fee_amount=100000, late_amount=250, balance_amount=450000)

        self.update_asset_due_at(-10, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount
        trade_merchant_key = self.repay_collect(
            {"item_no": self.item_no, "amount": bc_delay_amount - earease_amount(bc_delay_amount - 125) - 125 - 1,
             "repay_type": "delay", "status": 2, "finish_at": get_date(day=-1)})
        withhold = get_withhold(withhold_serial_no=trade_merchant_key)[0]
        Assert.assert_match_json(
            self.task.get_task(task_order_no=withhold["withhold_channel_key"],
                               task_type="offline_withhold_process")[0]["task_response_data"],
            {"code": 0, "message": "未匹配到可以用的代扣记录进行共债资产还款"})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=39874, repaid_late_amount=375, repaid_amount=179249,
                         fee_amount=100000, late_amount=375, balance_amount=435126)

    def test_collect_asset_delay_second_success_amount_equal(self, setup_4):
        # 打款金额 = （bc返回展期金额 - 增量罚息）- 抹零
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.loan_active_repay_apply(project_num_loan_channel_amount, payment_type="paycode", payment_option="wallet")
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})

        delay_apply_amount = 25000 * 0.2 + 3500 * 3 + 125 * 1
        self.update_asset_due_at(-1, period=2, refresh=True)
        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="collect",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-2, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount + 125

        self.repay_collect(
            {"item_no": self.item_no, "amount": bc_delay_amount - earease_amount(bc_delay_amount - 125) - 125,
             "repay_type": "delay", "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25000, repaid_late_amount=250, repaid_amount=164250,
                         fee_amount=100000, late_amount=250, balance_amount=450000)

        self.update_asset_due_at(-10, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount
        trade_merchant_key = self.repay_collect(
            {"item_no": self.item_no, "amount": bc_delay_amount - earease_amount(bc_delay_amount - 125) - 125,
             "repay_type": "delay", "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25000, repaid_late_amount=375, repaid_amount=164375,
                         fee_amount=100000, late_amount=375, balance_amount=450000)
        check_asset_delay_data(trade_merchant_key, apply_amount=15625, pay_amount=15000, pay_status="success",
                               delay_status="success")

    def test_collect_asset_delay_second_success_amount_more(self, setup_4):
        # 打款金额 > bc返回展期金额，多余还资产
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.loan_active_repay_apply(project_num_loan_channel_amount, payment_type="paycode", payment_option="wallet")
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})

        delay_apply_amount = 25000 * 0.2 + 3500 * 3 + 125 * 1
        self.update_asset_due_at(-1, period=2, refresh=True)
        trade_withhold(self.item_no, "asset_delay", delay_apply_amount, payment_type="collect",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.update_asset_due_at(-2, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount + 125

        self.repay_collect(
            {"item_no": self.item_no, "amount": bc_delay_amount + 1,
             "repay_type": "delay", "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25001, repaid_late_amount=250, repaid_amount=164251,
                         fee_amount=100000, late_amount=250, balance_amount=449999)

        self.update_asset_due_at(-10, period=2, refresh=True)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4], 0.2)
        bc_delay_amount = delay_apply_amount
        trade_merchant_key = self.repay_collect(
            {"item_no": self.item_no, "amount": bc_delay_amount + 1,
             "repay_type": "delay", "status": 2, "finish_at": get_date(day=-1)})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=14000,
                         repaid_fee_amount=25002, repaid_late_amount=375, repaid_amount=164377,
                         fee_amount=100000, late_amount=375, balance_amount=449998)
        check_asset_delay_data(trade_merchant_key, apply_amount=15625, pay_amount=15626, pay_status="success",
                               delay_status="success")
