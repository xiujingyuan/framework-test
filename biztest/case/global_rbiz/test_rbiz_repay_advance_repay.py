from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.global_rbiz.global_rbiz_kv_config import update_tha_rbiz_paysvr_config
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto
from biztest.function.global_rbiz.rbiz_global_check_function import *
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback, tran_decrease, withhold_cancel, repay_trial
from biztest.util.db.db_util import DataBase


"""
advance金额正常
advance金额不正常
提前一天还款
到期日还款，但是reoay_type是advance


"""


@pytest.mark.global_rbiz_thailand
@pytest.mark.advance_repay
class TestRbizAdvanceRepay(BaseGlobalRepayTest):
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
        super(TestRbizAdvanceRepay, self).init()
        update_tha_rbiz_paysvr_config("5e46037fd53ef1165b98246e")
        self.mock.update_withhold_autopay_ebank_url_success()
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element, 4)

    def test_advance_repay_trial(self, setup_4):
        self.update_asset_due_at(7, refresh=False)
        resp = repay_trial(self.item_no, period=1)
        Assert.assert_match_json(132071, resp["content"]["data"]["asset"]["trial_total_amount"])

        self.update_asset_due_at(3, refresh=False)
        resp = repay_trial(self.item_no, period=1)
        Assert.assert_match_json(146357, resp["content"]["data"]["asset"]["trial_total_amount"])

        self.update_asset_due_at(0, refresh=False)
        resp = repay_trial(self.item_no, period=1)
        Assert.assert_match_json(157071, resp["content"]["data"]["asset"]["trial_total_amount"])

        self.update_asset_due_at(-1, refresh=True)
        resp = repay_trial(self.item_no, period=1)
        Assert.assert_match_json(153625, resp["content"]["data"]["asset"]["trial_total_amount"])

        self.loan_active_repay_apply(0, period_list=[1])
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})

        self.update_asset_due_at(3, refresh=False)
        resp = repay_trial(self.item_no, period=2)
        Assert.assert_match_json(132071, resp["content"]["data"]["asset"]["trial_total_amount"])

        resp = repay_trial(self.item_no, period=None)
        Assert.assert_match_json(389071, resp["content"]["data"]["asset"]["trial_total_amount"])

        tran_decrease(self.item_no, "fin_service", 24000, 2)
        resp = repay_trial(self.item_no, period=2)
        Assert.assert_match_json(129500, resp["content"]["data"]["asset"]["trial_total_amount"])

    def test_advance_repay_amount_correct(self, setup_4):
        resp = self.loan_active_repay_apply(0, period_list=[1], repay_type="advance")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 132071,
            "repay_type": "advance",
            "withhold_sub_status": "advance"
        }
        check_withhold_success_data(order_no, **withhold)

    def test_advance_repay_amount_incorrect(self, setup_4):
        resp = self.loan_active_repay_apply(132072, period_list=[1], repay_type="advance")
        Assert.assert_match_json(
            ".*第[1]期不支持部分还款,还款输入金额[132072]小于应还金额[153500]", resp["content"]["message"])

    def test_active_advance_repay_before_3_day(self, setup_4):
        self.update_asset_due_at(3, refresh=False)
        resp = self.loan_active_repay_apply(0, period_list=[1], repay_type="advance")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 146357,
            "repay_type": "advance",
            "withhold_sub_status": "advance"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_fee_amount=25000, repaid_amount=153500,
                         fee_amount=100000, balance_amount=460500, asset_status="repay")

    def test_active_advance_repay_before_1_day(self, setup_4):
        self.update_asset_due_at(1, refresh=False)
        resp = self.loan_active_repay_apply(0, period_list=[1], repay_type="advance")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 153500,
            "repay_type": "advance",
            "withhold_sub_status": "advance"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_fee_amount=25000, repaid_amount=153500,
                         fee_amount=100000, balance_amount=460500, asset_status="repay")

    def test_active_advance_repay_before_0_day(self, setup_4):
        self.update_asset_due_at(0, refresh=False)
        resp = self.loan_active_repay_apply(0, period_list=[1], repay_type="advance")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 153500,
            "repay_type": "normal",
            "withhold_sub_status": "normal"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_fee_amount=25000, repaid_amount=153500,
                         fee_amount=100000, balance_amount=460500, asset_status="repay")

    def test_active_advance_repay_after_1_day(self, setup_4):
        self.update_asset_due_at(-1, refresh=True)
        resp = self.loan_active_repay_apply(0, period_list=[1], repay_type="advance")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 153625,
            "repay_type": "overdue",
            "withhold_sub_status": "normal"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_fee_amount=25000, repaid_late_amount=125, late_amount=125, repaid_amount=153625,
                         fee_amount=100000, balance_amount=460500, asset_status="repay")

    def test_active_advance_repay_before_14_day(self, setup_4):
        self.loan_active_repay_apply(0, period_list=[1])
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        resp = self.loan_active_repay_apply(0, period_list=[2], repay_type="advance")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 132071,
            "repay_type": "advance",
            "withhold_sub_status": "advance"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=250000, repaid_interest_amount=7000,
                         repaid_fee_amount=50000, repaid_amount=307000,
                         fee_amount=100000, balance_amount=307000, asset_status="repay")

    def test_active_advance_repay_before_0_day_decrease_late(self, setup_4):
        self.update_asset_due_at(0, refresh=False)
        resp = self.loan_active_repay_apply(0, period_list=[1], repay_type="advance")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        self.update_asset_due_at(-1, refresh=True)
        update_withhold(order_no, withhold_create_at=get_date(day=-1, fmt="%Y-%m-%d 23:59:59"))
        self.repay_normal(
            {"item_no": self.item_no, "amount": 0, "status": 2, "finish_at": get_date(fmt="%Y-%m-%d 11:59:59")})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 153500,
            "repay_type": "normal",
            "withhold_sub_status": "normal"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_fee_amount=25000, decrease_late_amount=125, repaid_amount=153500,
                         fee_amount=100000, balance_amount=460500, asset_status="repay")

    def test_active_advance_repay_amount_less(self, setup_4):
        self.update_asset_due_at(3, refresh=False)
        resp = self.loan_active_repay_apply(0, period_list=[1], repay_type="advance")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        self.repay_normal({"item_no": self.item_no, "amount": 146356, "status": 2})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 146356,
            "repay_type": "advance",
            "withhold_sub_status": "normal"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=117856, repaid_interest_amount=3500,
                         repaid_fee_amount=25000, repaid_amount=146356,
                         fee_amount=100000, balance_amount=467644, asset_status="repay")

    def test_active_advance_repay_amount_more(self, setup_4):
        self.update_asset_due_at(3, refresh=False)
        resp = self.loan_active_repay_apply(0, period_list=[1], repay_type="advance")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        self.repay_normal({"item_no": self.item_no, "amount": 146358, "status": 2})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 146358,
            "repay_type": "advance",
            "withhold_sub_status": "advance"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_fee_amount=25000, repaid_amount=153500,
                         fee_amount=100000, balance_amount=460500, asset_status="repay")

    def test_active_advance_repay_after_date(self, setup_4):
        self.loan_active_repay_apply(0, period_list=[1])
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        resp = self.loan_active_repay_apply(0, period_list=[2], repay_type="advance")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        update_withhold(order_no, withhold_create_at=get_date(day=-2, fmt="%Y-%m-%d 23:59:59"))
        self.repay_normal(
            {"item_no": self.item_no, "amount": 0, "status": 2, "finish_at": get_date(day=-1, fmt="%Y-%m-%d 12:00:01")})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 132071,
            "repay_type": "advance",
            "withhold_sub_status": "normal"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=228571, repaid_interest_amount=7000,
                         repaid_fee_amount=50000, repaid_amount=285571,
                         fee_amount=100000, balance_amount=328429, asset_status="repay")

    def test_active_advance_repay_fee_part_repay(self, setup_4):
        self.loan_active_repay_apply(0, period_list=[1])
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        resp = self.loan_active_repay_apply(0, period_list=[2], repay_type="advance")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        request_key = get_withhold_request_by_serial_no(order_no)[0]["withhold_request_req_key"]
        self.mock.mock_close_order_success()
        withhold_cancel(request_key, "")
        tran_decrease(self.item_no, "fin_service", 24000, 2)
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 132071,
            "repay_type": "advance",
            "withhold_sub_status": "advance"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=250000, repaid_interest_amount=7000,
                         repaid_fee_amount=28571, repaid_amount=285571, decrease_fee_amount=24000,
                         fee_amount=76000, balance_amount=304429, asset_status="repay")
        account = get_account_by_item_no(self.item_no)
        Assert.assert_equal(0, account["account_balance_amount"], "account余额正确")

    def test_active_advance_repay_fee_already_repay(self, setup_4):
        self.loan_active_repay_apply(0, period_list=[1])
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        resp = self.loan_active_repay_apply(0, period_list=[2], repay_type="advance")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        request_key = get_withhold_request_by_serial_no(order_no)[0]["withhold_request_req_key"]
        self.mock.mock_close_order_success()
        withhold_cancel(request_key, "")
        tran_decrease(self.item_no, "fin_service", 25000, 2)
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 132071,
            "repay_type": "advance",
            "withhold_sub_status": "advance"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=250000, repaid_interest_amount=7000,
                         repaid_fee_amount=28571, repaid_amount=285571, decrease_fee_amount=25000,
                         fee_amount=75000, balance_amount=303429, asset_status="repay")
        account = get_account_by_item_no(self.item_no)
        Assert.assert_equal(0, account["account_balance_amount"], "account余额正确")

    def test_active_advance_repay_current_period_already_repay(self, setup_4):
        resp = self.loan_active_repay_apply(0, period_list=[1])
        order_no_normal = resp["content"]["data"]["project_list"][0]["order_no"]
        request_key = get_withhold_request_by_serial_no(order_no_normal)[0]["withhold_request_req_key"]
        self.mock.mock_close_order_success()
        withhold_cancel(request_key, "")

        resp = self.loan_active_repay_apply(0, period_list=[1], repay_type="advance")
        order_no_advance = resp["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no_normal, 153500)
        self.run_all_task_by_serial_no(order_no_normal)

        paysvr_callback(order_no_advance, 132071)
        self.run_all_task_by_serial_no(order_no_advance)

        check_asset_data(self.item_no, repaid_principal_amount=228571, repaid_interest_amount=7000,
                         repaid_fee_amount=50000, repaid_amount=285571,
                         fee_amount=100000, balance_amount=328429, asset_status="repay")
        account = get_account_by_item_no(self.item_no)
        Assert.assert_equal(0, account["account_balance_amount"], "account余额正确")

    def test_active_advance_repay_mutile_amount_correct(self, setup_4):
        resp = self.loan_active_repay_apply(0, period_list=[1, 2, 3, 4], repay_type="advance_settle")
        order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 517571,
            "repay_type": "advance",
            "withhold_sub_status": "advance_settle"
        }
        check_withhold_success_data(order_no, **withhold)
