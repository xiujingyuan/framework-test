import pytest

from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.global_rbiz.global_rbiz_kv_config import update_rbiz_decrease_config, update_rbiz_config_withhold
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto, asset_import_auto_no_loan
from biztest.function.global_rbiz.rbiz_global_check_function import check_asset_data
from biztest.function.global_rbiz.rbiz_global_db_function import update_asset, \
    get_asset, get_withhold, get_account_by_id_num, get_asset_delay
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback, trade_withhold, asset_void_withhold, \
    paysvr_smart_collect_callback
from biztest.util.asserts.assert_util import Assert
from biztest.util.db.db_util import DataBase
from biztest.util.tools.tools import get_four_element_global, get_date

"""
资产取消用例集



"""


@pytest.mark.global_rbiz_thailand
@pytest.mark.asset_void
class TestRbizAssetVoid(BaseGlobalRepayTest):

    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        update_rbiz_decrease_config(can_decrease_day=3)
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    @pytest.fixture(scope="function")
    def setup_4(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        update_rbiz_decrease_config(can_decrease_day=3)
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element, 4)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    def test_asset_void_apply_fail(self, setup_4):
        # 小单不可取消
        resp = asset_void_withhold(item_no=self.item_no_x, amount=1212, four_element=self.four_element)
        Assert.assert_match_json({"code": 1, "message": "Do not void  noloan.*",
                                  "data": None},
                                 resp["content"])

        # 金额不等于借款本金
        resp = asset_void_withhold(item_no=self.item_no, amount=1212, four_element=self.four_element)
        Assert.assert_match_json(resp["content"],
                                 {"code": 1, "message": "The amount is not equal to the contract principal amount",
                                  "data": None})

        # 已有还款记录
        self.combo_active_repay_apply(0, 0, period_list=[1])
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        resp = asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        Assert.assert_match_json(resp["content"],
                                 {"code": 1, "message": "There are repayment plans that have been repaid",
                                  "data": None})

        # 资产已经被取消
        update_asset(self.item_no, asset_status="writeoff")
        update_asset(self.item_no_x, asset_status="void")
        resp = asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        Assert.assert_match_json(resp["content"], {"code": 1, "message": "asset status is not correct", "data": None})

        update_asset(self.item_no, asset_status="repay")
        update_asset(self.item_no_x, asset_status="repay")

        # 超过可取消时间
        self.update_asset_due_at(2)
        update_rbiz_config_withhold()
        resp = asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        Assert.assert_match_json(resp["content"],
                                 {"code": 1, "message": "The time interval cannot be greater than 36 hours",
                                  "data": None})

        # 资产已经结清
        self.update_asset_due_at(6)
        self.combo_active_repay_apply(0, 0, period_list=[2, 3, 4])
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        resp = asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        Assert.assert_match_json(resp["content"], {"code": 1, "message": "asset status is not correct", "data": None})
        Assert.assert_equal("payoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("payoff", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])

    def test_asset_void_with_withhold_and_delay(self, setup_4):
        # 有资产代扣的时候，不能取消
        self.mock.update_withhold_autopay_ebank_url_success()
        self.combo_active_repay_apply(0, 0, period_list=[1])
        resp = asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        Assert.assert_match_json(resp["content"],
                                 {"code": 1, "message": "The asset has unfinished withholding and cannot be cancelled",
                                  "data": None})
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 3})

        # 展期期间，可以取消
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        resp = asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        Assert.assert_match_json({"code": 0, "message": "Transaction Processing"}, resp["content"])

        # 取消过程中，不可发起代扣
        resp = self.combo_active_repay_apply(0, 0, period_list=[1])
        Assert.assert_match_json({"code": 1, "message": ".*正在进行中，请勿重复发起"}, resp["content"])

        # 重复发起取消
        resp = asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        Assert.assert_match_json(resp["content"],
                                 {"code": 1, "message": "The asset has unfinished withholding and cannot be cancelled",
                                  "data": None})

    def test_asset_void_repay_fail(self, setup_4):
        asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        order_no = self.repay_void({"item_no": self.item_no, "amount": 0, "status": 3})
        Assert.assert_equal("repay", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("repay", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])
        withhold = get_withhold(withhold_serial_no=order_no)[0]
        Assert.assert_equal("fail", withhold["withhold_status"])

    def test_asset_void_repay_success(self, setup_4):
        # 先进行展期
        trade_withhold(self.item_no, "asset_delay", 1500, "qrcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-2)})
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key, asset_delay_status="success")
        Assert.assert_equal(len(asset_delay) != 0, True, "展期成功")
        # 进行资产取消
        asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        self.repay_void({"item_no": self.item_no, "amount": 0, "status": 2})
        self.task.run_task(self.item_no_x, "noLoanAssetVoid", {"code": 0, "message": "作废小单成功"})

        Assert.assert_equal("writeoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("void", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account余额正确")

    def test_asset_void_fail_asset_already_payoff(self, setup_4):
        resp = asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        order_no_void = resp["content"]["data"]["order_no"]
        paysvr_callback(order_no_void, 500000, 3)

        resp = self.combo_active_repay_apply(0, 0, period_list=[1, 2, 3, 4])
        order_no_withhold = resp["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no_withhold, 564000, 2)

        self.run_all_task_by_serial_no(order_no_withhold)
        Assert.assert_equal("payoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("payoff", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])

        paysvr_callback(order_no_void, 500000, 2)
        self.task.run_task(order_no_void, "assetWithholdOrderRecharge", {"code": 0})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": ".*没有对应的withhold_detail"})

        Assert.assert_equal("payoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("payoff", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(500000, account["account_balance_amount"], "account余额正确")

    def test_asset_void_fail_asset_already_void(self, setup_4):
        resp = asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        order_no_void = resp["content"]["data"]["order_no"]
        paysvr_callback(order_no_void, 500000, 3)

        resp = asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        order_no_void_new = resp["content"]["data"]["order_no"]
        paysvr_callback(order_no_void_new, 500000, 2)

        self.run_all_task_by_serial_no(order_no_void_new)
        self.task.run_task(self.item_no_x, "noLoanAssetVoid", {"code": 0, "message": "作废小单成功"})
        Assert.assert_equal("writeoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("void", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])

        paysvr_callback(order_no_void, 500000, 2)
        self.task.run_task(order_no_void, "assetWithholdOrderRecharge", {"code": 0})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": ".*没有对应的withhold_detail"})

        Assert.assert_equal("writeoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("void", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(500000, account["account_balance_amount"], "account余额正确")

    def test_asset_void_fail_asset_already_repay_part(self, setup_4):
        resp = asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        order_no_void = resp["content"]["data"]["order_no"]
        paysvr_callback(order_no_void, 500000, 3)

        self.repay_collect({"item_no": self.item_no, "amount": 1600, "repay_type": "asset"})
        Assert.assert_equal("repay", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("repay", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])

        paysvr_callback(order_no_void, 500000, 2)
        self.task.run_task(order_no_void, "assetWithholdOrderRecharge", {"code": 0})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "data": None, "message": "资产还款成功"})
        self.task.run_task(self.item_no_x, "assetWithholdOrderRepay", {"code": 0, "data": None, "message": "资产还款成功"})

        check_asset_data(self.item_no, repaid_principal_amount=437600, repaid_interest_amount=14000,
                         repaid_amount=451600, balance_amount=62400, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account余额正确")

    def test_asset_void_fail_belong_time(self, setup_4):
        resp = asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        order_no_void = resp["content"]["data"]["order_no"]
        self.update_asset_due_at(5)
        paysvr_callback(order_no_void, 500000, 2)
        self.task.run_task(order_no_void, "assetWithholdOrderRecharge", {"code": 0})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "data": None, "message": "资产还款成功"})
        self.task.run_task(self.item_no_x, "assetWithholdOrderRepay", {"code": 0, "data": None, "message": "资产还款成功"})

        check_asset_data(self.item_no, repaid_principal_amount=436000, repaid_interest_amount=14000,
                         repaid_amount=450000, balance_amount=64000, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account余额正确")

    def test_asset_void_normal_repay_amount_less(self, setup_4):
        asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        self.repay_void({"item_no": self.item_no, "amount": 121212, "status": 2})

        Assert.assert_equal("repay", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("repay", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])
        check_asset_data(self.item_no, repaid_principal_amount=105212, repaid_interest_amount=3500,
                         repaid_amount=108712, balance_amount=405288)
        check_asset_data(self.item_no_x, repaid_principal_amount=12500, repaid_amount=12500, balance_amount=37500)
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account余额正确")

    def test_asset_void_normal_repay_amount_equal(self, setup_4):
        asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        self.repay_void({"item_no": self.item_no, "amount": 500000, "status": 2})
        self.task.run_task(self.item_no_x, "noLoanAssetVoid", {"code": 0, "message": "作废小单成功"})

        Assert.assert_equal("writeoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("void", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account余额正确")

    def test_asset_void_normal_repay_amount_more(self, setup_4):
        asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        self.repay_void({"item_no": self.item_no, "amount": 510000, "status": 2})
        self.task.run_task(self.item_no_x, "noLoanAssetVoid", {"code": 0, "message": "作废小单成功"})

        Assert.assert_equal("writeoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("void", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(10000, account["account_balance_amount"], "account余额正确")

    def test_asset_void_collect_repay_amount_less(self, setup_4):
        asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element, payment_type="collect")
        resp, req = paysvr_smart_collect_callback("assetVoid" + self.item_no, 121212)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "还款金额小于本金额总和进行共债资产还款"})
        self.run_all_task_after_repay_success()
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})

        Assert.assert_equal("repay", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("repay", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])
        check_asset_data(self.item_no, repaid_principal_amount=117712, repaid_interest_amount=3500,
                         repaid_amount=121212, balance_amount=392788)
        check_asset_data(self.item_no_x, balance_amount=50000)
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account余额正确")

    def test_asset_void_collect_repay_amount_equal(self, setup_4):
        asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element, payment_type="collect")
        resp, req = paysvr_smart_collect_callback("assetVoid" + self.item_no, 500000)
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success()
        self.task.run_task(self.item_no_x, "noLoanAssetVoid", {"code": 0, "message": "作废小单成功"})

        Assert.assert_equal("writeoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("void", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account余额正确")

    def test_asset_void_collect_repay_amount_more(self, setup_4):
        asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element, payment_type="collect")
        resp, req = paysvr_smart_collect_callback("assetVoid" + self.item_no, 510000)
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success()
        self.task.run_task(self.item_no_x, "noLoanAssetVoid", {"code": 0, "message": "作废小单成功"})

        Assert.assert_equal("writeoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("void", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(10000, account["account_balance_amount"], "account余额正确")

    def test_asset_void_delay_repay_after_void(self, setup_4):
        # 先申请展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        # 资产取消
        asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        self.repay_void({"item_no": self.item_no, "amount": 500000, "status": 2})
        self.task.run_task(self.item_no_x, "noLoanAssetVoid", {"code": 0, "message": "作废小单成功"})

        Assert.assert_equal("writeoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("void", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account余额正确")

        # 展期通知
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-2)})
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key, asset_delay_status="success")
        Assert.assert_equal(len(asset_delay) == 0, True, "展期成功")

    def test_asset_void_asset_repay_after_void(self, setup_4):
        # 先申请还款
        resp = self.combo_active_repay_apply(0, 0, period_list=[1, 2, 3, 4])
        paysvr_callback(resp["content"]["data"]["project_list"][0]["order_no"], 564000, 3)
        # 资产取消
        asset_void_withhold(item_no=self.item_no, amount=500000, four_element=self.four_element)
        self.repay_void({"item_no": self.item_no, "amount": 500000, "status": 2})
        self.task.run_task(self.item_no_x, "noLoanAssetVoid", {"code": 0, "message": "作废小单成功"})

        Assert.assert_equal("writeoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"])
        Assert.assert_equal("void", get_asset(asset_item_no=self.item_no_x)[0]["asset_status"])
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account余额正确")

        # 资产还款
        self.repay_normal({"item_no": self.item_no, "amount": 500000, "status": 2})
