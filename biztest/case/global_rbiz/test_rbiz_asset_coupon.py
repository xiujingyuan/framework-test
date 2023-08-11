import pytest

from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto
from biztest.function.global_rbiz.rbiz_global_check_function import check_asset_data, check_withhold_success_data
from biztest.util.db.db_util import DataBase
from biztest.util.tools.tools import get_four_element_global, get_random_str

"""
优惠卷

优惠卷申请
线上还款，优惠卷使用
线下还款，优惠卷使用


bc先申请代扣，传入优惠卷，fox代扣完成后使用优惠卷
"""


@pytest.mark.global_rbiz_thailand
@pytest.mark.asset_coupon
class TestRbizAssetCoupon(BaseGlobalRepayTest):
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
        super(TestRbizAssetCoupon, self).init()
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element, 4)

    def test_asset_coupon_normal_repay_all_period_amount_less(self, setup_4):
        coupon_num = "coupon_" + get_random_str(10)
        self.loan_active_repay_apply(0, period_list=[1], coupon_amount=1000, coupon_num=coupon_num)
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_fee_amount=25000, repaid_amount=153500,
                         fee_amount=100000, balance_amount=460500, asset_status="repay")

        self.update_asset_due_at(-1, period=2, refresh=True)
        self.loan_active_repay_apply(0, period_list=[2, 3, 4], coupon_amount=1000, coupon_num=coupon_num)
        self.repay_normal({"item_no": self.item_no, "amount": 460500 - 625 - 1000 - 1, "status": 2})

        check_asset_data(self.item_no, repaid_principal_amount=498249, repaid_interest_amount=14000,
                         repaid_fee_amount=100000, repaid_late_amount=125, late_amount=125, repaid_amount=612374,
                         fee_amount=100000, balance_amount=1751, asset_status="repay")

    def test_asset_coupon_normal_repay_all_period_amount_equal(self, setup_4):
        coupon_num = "coupon_" + get_random_str(10)
        self.loan_active_repay_apply(0, period_list=[1], coupon_amount=1000, coupon_num=coupon_num)
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_fee_amount=25000, repaid_amount=153500,
                         fee_amount=100000, balance_amount=460500, asset_status="repay")

        self.update_asset_due_at(-1, period=2, refresh=True)
        self.loan_active_repay_apply(0, period_list=[2, 3, 4], coupon_amount=1000, coupon_num=coupon_num)
        self.repay_normal({"item_no": self.item_no, "amount": 460500 - 625 - 1000, "status": 2})
        self.run_all_task_by_serial_no("COUPON_" + coupon_num)
        check_asset_data(self.item_no, repaid_principal_amount=499250, repaid_interest_amount=14000,
                         repaid_fee_amount=100000, repaid_late_amount=125, late_amount=125, repaid_amount=613375,
                         fee_amount=100000, balance_amount=750, asset_status="repay")

    def test_asset_coupon_normal_repay_all_period_amount_more(self, setup_4):
        coupon_num = "coupon_" + get_random_str(10)
        self.loan_active_repay_apply(0, period_list=[1], coupon_amount=1000, coupon_num=coupon_num)
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_fee_amount=25000, repaid_amount=153500,
                         fee_amount=100000, balance_amount=460500, asset_status="repay")

        self.update_asset_due_at(-1, period=2, refresh=True)
        self.loan_active_repay_apply(0, period_list=[2, 3, 4], coupon_amount=1000, coupon_num=coupon_num)
        self.repay_normal({"item_no": self.item_no, "amount": 460500 - 625 - 1000 + 1, "status": 2})
        self.run_all_task_by_serial_no("COUPON_" + coupon_num)
        check_asset_data(self.item_no, repaid_principal_amount=499251, repaid_interest_amount=14000,
                         repaid_fee_amount=100000, repaid_late_amount=125, late_amount=125, repaid_amount=613376,
                         fee_amount=100000, balance_amount=749, asset_status="repay")

    def test_asset_coupon_normal_repay_remain_amount_equal_coupon(self, setup_4):
        self.repay_collect({"item_no": self.item_no, "repay_type": "asset", "amount": 612000, "status": 2})

        check_asset_data(self.item_no, repaid_principal_amount=498000, repaid_interest_amount=14000,
                         repaid_fee_amount=100000, fee_amount=100000, repaid_amount=612000,
                         balance_amount=2000, asset_status="repay")

        coupon_num = "coupon_" + get_random_str(10)
        resp = self.loan_active_repay_apply(0, period_list=[4], coupon_amount=2000, coupon_num=coupon_num)
        self.run_all_task_by_serial_no("COUPON_" + coupon_num)

        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=14000,
                         repaid_fee_amount=100000, fee_amount=100000, repaid_amount=614000, asset_status="payoff")
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "sign_company": "amberstar1",
            "withhold_channel": "coupon",
            "withhold_amount": 2000,
            "repay_type": "advance",
            "withhold_sub_status": "normal",
            "payment_type": "paycode",
            "withhold_third_serial_no": resp["content"]["data"]["project_list"][0]["order_no"]
        }
        check_withhold_success_data("COUPON_" + coupon_num, **withhold)

    def test_asset_coupon_normal_repay_remain_amount_less_coupon(self, setup_4):
        self.repay_collect({"item_no": self.item_no, "repay_type": "asset", "amount": 612001, "status": 2})

        check_asset_data(self.item_no, repaid_principal_amount=498001, repaid_interest_amount=14000,
                         repaid_fee_amount=100000, fee_amount=100000, repaid_amount=612001,
                         balance_amount=1999, asset_status="repay")

        coupon_num = "coupon_" + get_random_str(10)
        resp = self.loan_active_repay_apply(0, period_list=[4], coupon_amount=2000, coupon_num=coupon_num)
        self.run_all_task_by_serial_no("COUPON_" + coupon_num)

        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=14000,
                         repaid_fee_amount=100000, fee_amount=100000, repaid_amount=614000, asset_status="payoff")
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "sign_company": "amberstar1",
            "withhold_channel": "coupon",
            "withhold_amount": 1999,
            "repay_type": "advance",
            "withhold_sub_status": "normal",
            "payment_type": "paycode",
            "withhold_third_serial_no": resp["content"]["data"]["project_list"][0]["order_no"]
        }
        check_withhold_success_data("COUPON_" + coupon_num, **withhold)

    # def test_asset_coupon_collect_repay_first_period(self, setup_4):
    #     self.update_asset_due_at(-1, period=1, refresh=True)
    #     coupon_num = "coupon_" + get_random_str(10)
    #     self.loan_active_repay_apply(0, period_list=[1], coupon_amount=1000, coupon_num=coupon_num)
    #     self.repay_collect({"item_no": self.item_no, "repay_type": "asset", "amount": 152625, "status": 2})
    #     check_asset_data(self.item_no, repaid_principal_amount=124000, repaid_interest_amount=3500,
    #                      repaid_fee_amount=25000, repaid_late_amount=125, late_amount=125, fee_amount=100000,
    #                      repaid_amount=152625, balance_amount=461500, asset_status="repay")
    #
    # def test_asset_coupon_collect_repay_all_period(self, setup_4):
    #     self.update_asset_due_at(-1, period=1, refresh=True)
    #     coupon_num = "coupon_" + get_random_str(10)
    #     self.loan_active_repay_apply(0, period_list=[1], coupon_amount=1000, coupon_num=coupon_num)
    #     self.repay_collect({"item_no": self.item_no, "repay_type": "asset", "amount": 152625, "status": 2})
    #     check_asset_data(self.item_no, repaid_principal_amount=124000, repaid_interest_amount=3500,
    #                      repaid_fee_amount=25000, repaid_late_amount=125, late_amount=125, fee_amount=100000,
    #                      repaid_amount=152625, balance_amount=461500, asset_status="repay")
    #
    #     self.update_asset_due_at(-1, period=2, refresh=True)
    #     self.repay_collect(
    #         {"item_no": self.item_no, "repay_type": "asset", "amount": 460000, "status": 2})
    #     self.run_all_task_by_serial_no("COUPON_" + coupon_num)
    #
    #     check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=14000,
    #                      decrease_late_amount=116, late_amount=0, repaid_amount=514000, asset_status="payoff")
    #     account = get_account_by_item_no(self.item_no)
    #     Assert.assert_equal(1000, account["account_balance_amount"], "account余额正确")
