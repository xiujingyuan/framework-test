import pytest

from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.easymock.easymock_config import global_rbiz_mock
from biztest.config.global_rbiz.global_rbiz_kv_config import update_phl_rbiz_paysvr_config, update_rbiz_config
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto
from biztest.function.global_rbiz.rbiz_global_db_function import get_asset_tran_balance_amount_by_item_no, \
    get_asset_tran
from biztest.interface.rbiz.rbiz_global_interface import trade_withhold, asset_void_withhold, paysvr_callback, \
    fox_withhold, run_FoxAdvancePushJob_by_api, run_refreshLateFeeV1_by_api
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.payment_global import PaymentGlobalMock
from biztest.util.task.task import TaskGlobalRepay
from biztest.util.tools.tools import get_four_element_global, get_date


class TestRbizPhlUPeso(BaseGlobalRepayTest):
    """
       u_peso repay
    """
    from_system = "phi011"
    loan_channel = "copper_stone"
    source_type = "postservice54%_rate1‰_late7%"
    principal_amount = 500000

    @classmethod
    def setup_class(cls):
        update_rbiz_config(auto_tolerance=True, special_service_name="phl_special_service")
        update_phl_rbiz_paysvr_config()
        cls.task = TaskGlobalRepay()
        cls.mock = PaymentGlobalMock(global_rbiz_mock)

    @classmethod
    def teardown_class(cls):
        update_phl_rbiz_paysvr_config()
        update_rbiz_config(auto_tolerance=True, special_service_name="phl_special_service")

    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass

        request.addfinalizer(teardown)
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, "phl", self.from_system,
                                                     self.source_type, self.four_element, 4)
        self.wh_number = "PAY" + self.item_no
        self.expire_time = get_date(day=7)

    @pytest.mark.global_rbiz_philippines11
    @pytest.mark.global_rbiz_philippines_u_peso
    def test_active_advance_repay(self, setup):
        self.update_asset_due_at(-1, period=1, refresh=True)
        # run_FoxAdvancePushJob_by_api()
        # trade_withhold(self.item_no, "asset_delay", 67500 + 3500 * 4 + 8750 * 9, payment_type="paycode",
        #                payment_option="wallet", period_list=[1, 2, 3, 4], delay_days=7, four_element=self.four_element)
        # self.repay_trade({"item_no": self.item_no, "amount": 67500 + 3500 * 4 + 8750 * 9, "status": 2})
        # self.update_asset_due_at(-8, period=1, refresh=True)
        #
        # project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.loan_active_repay_apply(0, period_list=[1], payment_type="paycode", payment_option="wallet")
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        for i in range(1, 100, 1):
            self.update_asset_due_at(-i, period=2, refresh=True)

        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [1, 2, 3, 4])
        self.repay_trade({"item_no": self.item_no, "amount": 0, "status": 2})

        self.update_asset_due_at(-10, period=2, refresh=True)
        trade_withhold(self.item_no, "asset_delay", 67500 + 3500 * 3 + 60000, payment_type="paycode", payment_option="wallet",
                       period_list=[2, 3, 4], delay_days=7, four_element=self.four_element)
        self.mock.mock_fox_delay_entry(get_asset_tran(asset_tran_asset_item_no=self.item_no), [2, 3, 4])
        self.repay_trade({"item_no": self.item_no, "amount": 0, "status": 2})

        self.update_asset_due_at(-1, refresh=True)
        run_refreshLateFeeV1_by_api(self.item_no)
        self.task.run_task(self.item_no, "RefreshLateInterest")

        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        resp_combo_active = self.loan_active_repay_apply(project_num_loan_channel_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        self.update_asset_due_at(-2, refresh=True)
        run_refreshLateFeeV1_by_api(self.item_no)
        self.task.run_task(self.item_no, "RefreshLateInterest")
        self.update_asset_due_at(-3, refresh=True)
        run_refreshLateFeeV1_by_api(self.item_no)
        self.task.run_task(self.item_no, "RefreshLateInterest")
        paysvr_callback(order_no, 393000, 2, finished_at=get_date(day=-1))
