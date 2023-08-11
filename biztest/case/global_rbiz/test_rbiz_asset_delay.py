import pytest

from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.global_rbiz.global_rbiz_kv_config import update_rbiz_config, update_rbiz_config_withhold
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto, asset_import_auto_no_loan
from biztest.function.global_rbiz.rbiz_global_check_function import check_asset_data, check_withhold_success_data, \
    check_asset_delay_data
from biztest.function.global_rbiz.rbiz_global_db_function import get_asset_tran_balance_amount_by_item_no, \
    get_asset_delay, get_withhold, get_asset, update_withhold, \
    get_account_by_id_num
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback, paysvr_smart_collect_callback, \
    trade_withhold, asset_repay_reverse, asset_settle_debt, run_withholdTimeout_by_api, transaction_confirm, \
    run_accountStatementSync_by_api, run_initStatusAccountStatementMatchWithholdRecord_by_api
from biztest.util.asserts.assert_util import Assert
from biztest.util.db.db_util import DataBase
from biztest.util.tools.tools import get_four_element_global, get_date, get_tz
import common.global_const as gc

"""
展期：先还展期(够的情况)，再还资产，再还共债，再放到虚户

展期申请
之前无展期，本金未逾期，支付成功，展期开始日期本金due_at+1
之前无展期，本金今天到期，支付成功，展期开始日期本金due_at+1
之前无展期，本金已经逾期，支付成功，不支持减免，展期开始日期D+1
之前无展期，本金已经逾期，支付成功，支持减免，finish_at>=本金due_at，展期开始日期finish_at+1
之前无展期，本金已经逾期，支付成功，支持减免，finish_at<本金due_at，展期开始日期本金due_at+1

之前有展期，end_at未逾期，支付成功，展期开始日期end_at+1
之前有展期，end_at今天到期，支付成功，展期开始日期end_at+1
之前有展期，end_at已经逾期，支付成功，不支持减免，展期开始日期D+1
之前有展期，end_at已经逾期，支付成功，支持减免，finish_at>=end_at，展期开始日期finish_at+1
之前有展期，end_at已经逾期，支付成功，支持减免，finish_at<end_at，展期开始日期end_at+1

正常trade还款，展期成功，多次展期时间累积
正常trade还款，trade失败后又成功

正常trade还款，还款金额小于申请金额，资产未结清，留在账户中
正常trade还款，还款金额小于申请金额，资产未结清，还到资产上
正常trade还款，还款金额等于申请金额，资产未结清，展期成功
正常trade还款，还款金额大于申请金额，资产未结清，展期成功，多余钱留在账户中
正常trade还款，还款金额大于申请金额，资产未结清，展期成功，多余钱还到资产上面
正常trade还款，还款金额大于申请金额，资产未结清，展期成功，多余钱还到资产上面，若仍多余，人工还到共债资产上
正常trade还款，资产已经结清，有共债资产，但是不还共债，充值到虚户，后续人工充值到本资产
正常trade还款，资产已经结清，有共债资产，但是不还共债，充值到虚户，后续人工充值到共债资产

线下还款，首次还款金额小于申请金额，资产未结清，优先还到资产上，若仍多余，还到共债资产上
线下还款，首次还款金额等于申请金额，资产未结清，展期成功
线下还款，首次还款金额大于申请金额，资产未结清，展期成功，多余钱还到资产上面
线下还款，首次还款金额大于申请金额，资产未结清，展期成功，多余钱还到资产上面，若仍多余，还到共债资产上
线下还款，非首次还款金额小于申请金额，资产未结清，优先还到资产上，若仍多余，还到共债资产上
线下还款，非首次还款金额等于申请金额，资产未结清，展期成功
线下还款，非首次还款金额大于申请金额，资产未结清，展期成功，多余钱还到资产上面
线下还款，非首次还款金额大于申请金额，资产未结清，展期成功，多余钱还到资产上面，若仍多余，还到共债资产上
线下还款，资产已经结清，无共债资产，还到虚户，后续可手动分配至新共债资产
线下还款，资产已经结清，有共债资产，还到共债资产上
线下还款，无非成功的代扣记录，新建代扣
线下还款，找不到展期账号

卡对卡还款，还款金额小于申请金额，资产未结清，留在账户中
卡对卡还款，还款金额小于申请金额，资产未结清，还到资产上
卡对卡还款，还款金额等于申请金额，资产未结清，展期成功
卡对卡还款，还款金额大于申请金额，资产未结清，展期成功，多余钱留在账户中
卡对卡还款，还款金额大于申请金额，资产未结清，展期成功，多余钱还到资产上面
卡对卡还款，还款金额大于申请金额，资产未结清，展期成功，多余钱还到资产上面，若仍多余，还到共债资产上

展期订单超时
"""


@pytest.mark.global_rbiz_thailand
@pytest.mark.asset_delay
class TestRbizAssetDelay(BaseGlobalRepayTest):

    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        super(TestRbizAssetDelay, self).init()
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element, 4)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    def test_asset_no_delay_not_due_start_due_at_add_1(self, setup):
        self.update_asset_due_at(3)
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-2)})
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=4, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=6, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=4, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=6, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")

    def test_asset_no_delay_equal_due_start_due_at_add_1(self, setup):
        self.update_asset_due_at(0)
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-2)})
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=3, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=3, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")

    def test_asset_no_delay_after_due_no_decrease_start_today_add_1(self, setup):
        update_rbiz_config(need_decrease_late=False)
        late_day = 2
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-2)})
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=3, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=3, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")

    def test_asset_no_delay_after_due_no_can_decrease_finish_at_big_start_finish_at_add_1(self, setup):
        update_rbiz_config(need_decrease_late=True)
        late_day = 5
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-3)})
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=-2, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=0, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=-2, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=0, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, late_amount=250, decrease_late_amount=375, balance_amount=514250)
        check_asset_data(self.item_no_x, late_amount=24, decrease_late_amount=36, balance_amount=50024)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")

    def test_asset_no_delay_after_due_no_can_decrease_due_at_big_start_due_at_add_1(self, setup):
        update_rbiz_config(need_decrease_late=True)
        late_day = 5
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-8)})
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=-4, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=-2, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=-4, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=-2, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, late_amount=250, decrease_late_amount=375, balance_amount=514250)
        check_asset_data(self.item_no_x, late_amount=24, decrease_late_amount=36, balance_amount=50024)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")

    def test_asset_with_delay_not_due_start_end_at_add_1(self, setup):
        # 进行一次展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2})
        self.update_asset_due_at(-2, refresh=False)
        # 再次展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-2)})
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=2, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=4, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=2, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=4, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")

    def test_asset_with_delay_equal_due_start_end_at_add_1(self, setup):
        # 进行一次展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2})
        self.update_asset_due_at(-3, refresh=False)
        # 再次展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-2)})
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=3, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=3, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")

    def test_asset_with_delay_after_due_no_decrease_start_today_add_1(self, setup):
        update_rbiz_config(need_decrease_late=False)
        # 进行一次展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2})
        late_day = 6
        for i in range(4, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 再次展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-2)})
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=3, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=3, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")

    def test_asset_with_delay_after_due_no_can_decrease_finish_at_big_start_finish_at_add_1(self, setup):
        update_rbiz_config(need_decrease_late=True)
        # 进行一次展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2})
        late_day = 6
        for i in range(4, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 再次展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-2)})
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=-1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=-1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, late_amount=125, decrease_late_amount=250, balance_amount=514125)
        check_asset_data(self.item_no_x, late_amount=12, decrease_late_amount=24, balance_amount=50012)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")

    def test_asset_with_delay_after_due_no_can_decrease_end_at_big_start_end_at_add_1(self, setup):
        update_rbiz_config(need_decrease_late=True)
        # 进行一次展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2})
        late_day = 6
        for i in range(4, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 再次展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-8)})
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=-2, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=0, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=-2, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=0, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, decrease_late_amount=375, balance_amount=514000)
        check_asset_data(self.item_no_x, decrease_late_amount=36, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")

    def test_normal_repay_multiple(self, setup):
        update_rbiz_config(need_decrease_late=False)
        self.update_asset_due_at(3)
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2})
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=4, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=6, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        # 第二次展期
        self.update_asset_due_at(-8)
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1, 2], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-1)})
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=3, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 750,
                                  "asset_delay_apply_amount": 750},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 2,
                                  "asset_delay_days": 3,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=1, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=3, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 750,
                                  "asset_delay_apply_amount": 750},
                                 asset_delay[1])

    def test_normal_repay_reverse(self, setup):
        self.update_asset_due_at(3)
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key1 = self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 3})

        # 第二次展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key2 = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2})
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key2)
        withhold = get_withhold(withhold_serial_no=merchant_key2)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=4, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=6, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])

        # 失败的展期，变成功
        paysvr_callback(merchant_key1, 1500, 2)
        self.run_all_task_by_serial_no(merchant_key1)
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key1)
        withhold = get_withhold(withhold_serial_no=merchant_key1)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=7, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=9, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])

    def test_normal_repay_amount_less_than_apply_repay_asset_normal(self, setup):
        update_rbiz_config(special_service_name=None)
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = self.repay_trade({"item_no": self.item_no, "amount": 1400, "status": 2})

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_status": "fail",
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        check_asset_data(self.item_no, repaid_interest_amount=1400, repaid_amount=1400, balance_amount=512600)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1400, pay_status="success",
                               delay_status="fail", balance_amount=0)
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account_balance_amount不正确")

    def test_normal_repay_amount_less_than_apply_repay_asset_ind(self, setup):
        update_rbiz_config(special_service_name="ind_special_service")
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = self.repay_trade({"item_no": self.item_no, "amount": 1400, "status": 2})

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_status": "fail",
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        check_asset_data(self.item_no, repaid_interest_amount=1400, repaid_amount=1400, balance_amount=512600)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1400, pay_status="success",
                               delay_status="fail", balance_amount=0)
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account_balance_amount不正确")

    def test_normal_repay_amount_equal_than_apply_normal(self, setup):
        update_rbiz_config(special_service_name=None)
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2})

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, balance_amount=514000)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success", balance_amount=0)
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account_balance_amount不正确")

    def test_normal_repay_amount_equal_than_apply_ind(self, setup):
        update_rbiz_config(special_service_name="ind_special_service")
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2})

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, balance_amount=514000)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success", balance_amount=0)
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account_balance_amount不正确")

    def test_normal_repay_amount_more_than_apply_repay_asset_normal(self, setup):
        update_rbiz_config(special_service_name=None)
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = self.repay_trade({"item_no": self.item_no, "amount": 1600, "status": 2})

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, repaid_interest_amount=100, repaid_amount=100, balance_amount=513900)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1600, pay_status="success",
                               delay_status="success", balance_amount=0)
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account_balance_amount不正确")

    def test_normal_repay_amount_more_than_apply_repay_asset_ind(self, setup):
        update_rbiz_config(special_service_name="ind_special_service")
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = self.repay_trade({"item_no": self.item_no, "amount": 1600, "status": 2})

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, repaid_interest_amount=100, repaid_amount=100, balance_amount=513900)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1600, pay_status="success",
                               delay_status="success", balance_amount=0)
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account_balance_amount不正确")

    def test_normal_repay_amount_more_than_apply_manual_repay_debt_asset_normal(self, setup):
        update_rbiz_config(special_service_name=None)
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type, self.four_element, 4)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 申请展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = self.repay_trade({"item_no": self.item_no, "amount": 600000, "status": 2})

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, repaid_interest_amount=14000, repaid_principal_amount=500000,
                         repaid_amount=514000, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")
        check_asset_data(self.item_no_new, balance_amount=514000)
        check_asset_data(self.item_no_x_new, balance_amount=50000)
        # check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=600000, pay_status="success",
        #                        delay_status="success", balance_amount=34500)
        # 手动还给共债
        channel_key_delay = get_withhold(withhold_serial_no=merchant_key)[0]["withhold_channel_key"]
        asset_settle_debt(self.item_no, channel_key_delay)
        check_asset_data(self.item_no_new, repaid_interest_amount=3500, repaid_principal_amount=32500,
                         repaid_amount=36000, balance_amount=478000)
        check_asset_data(self.item_no_x_new, balance_amount=50000)
        # check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=600000, pay_status="success",
        #                        delay_status="success")

    def test_normal_repay_manual_to_asset(self, setup):
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type, self.four_element, 4)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 还款申请
        self.update_asset_due_at(3)
        self.combo_active_repay_apply(0, 0, period_list=[1, 2, 3, 4])
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        # 资产结清
        asset_merchant_key = self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        # 展期还款
        trade_merchant_key = self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2})
        Assert.assert_equal(
            self.task.get_task(task_order_no=self.item_no, task_type="tradeWithholdOrderRepay")[0]["task_memo"],
            "The asset state is not repay state, do not extend repayment")
        # 资产还款逆操作
        channel_key = get_withhold(withhold_serial_no=asset_merchant_key)[0]["withhold_channel_key"]
        asset_repay_reverse(self.item_no, channel_key)
        # 手动还到本资产
        channel_key_delay = get_withhold(withhold_serial_no=trade_merchant_key)[0]["withhold_channel_key"]
        asset_settle_debt(self.item_no, channel_key_delay)
        # 进行数据检查
        withhold = {"withhold_channel": "cashfree_yomoyo_ebank",
                    "payment_type": "ebank",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": 1500,
                    "trade_amount": 1500,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "TRADE_WITHHOLD",
                    "order_operate_type": "active",
                    "withhold_sub_status": "asset_delay"}
        check_withhold_success_data(trade_merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_interest_amount=1500, repaid_amount=1500, balance_amount=512500)
        check_asset_data(self.item_no_new, balance_amount=514000)

    def test_normal_repay_manual_to_debt(self, setup):
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type, self.four_element, 4)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 还款申请
        self.update_asset_due_at(3)
        self.combo_active_repay_apply(0, 0, period_list=[1, 2, 3, 4])
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        # 资产结清
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        # 展期还款
        trade_merchant_key = self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2})
        Assert.assert_equal(
            self.task.get_task(task_order_no=self.item_no, task_type="tradeWithholdOrderRepay")[0]["task_memo"],
            "The asset state is not repay state, do not extend repayment")
        # 手动还到公债资产
        channel_key_delay = get_withhold(withhold_serial_no=trade_merchant_key)[0]["withhold_channel_key"]
        asset_settle_debt(self.item_no, channel_key_delay)
        # 进行数据检查
        withhold = {"withhold_channel": "cashfree_yomoyo_ebank",
                    "payment_type": "ebank",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": 1500,
                    "trade_amount": 1500,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "TRADE_WITHHOLD",
                    "order_operate_type": "active",
                    "withhold_sub_status": "asset_delay"}
        check_withhold_success_data(trade_merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_interest_amount=14000, repaid_principal_amount=500000,
                         repaid_amount=514000, asset_status="payoff")
        check_asset_data(self.item_no_new, repaid_interest_amount=1500, repaid_amount=1500, balance_amount=512500)

    def test_offline_first_repay_amount_less_than_apply_amount(self, setup):
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)

        merchant_key = self.repay_collect({"item_no": self.item_no, "amount": 1400,
                                           "repay_type": "delay", "finish_at": get_date()})
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json(
            self.task.get_task(task_order_no=withhold["withhold_channel_key"],
                               task_type="offline_withhold_process")[0]["task_response_data"],
            {"code": 0, "message": "不存在展期记录进行共债资产还款"})
        check_asset_data(self.item_no, repaid_interest_amount=1400, repaid_amount=1400, balance_amount=512600)
        check_asset_data(self.item_no_x, balance_amount=50000)
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account_balance_amount不正确")

    def test_offline_first_repay_amount_equal_than_apply_amount(self, setup):
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)

        merchant_key = self.repay_collect({"item_no": self.item_no, "amount": 1500,
                                           "repay_type": "delay", "finish_at": get_date()})
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]

        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, balance_amount=514000)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")

    def test_offline_first_repay_amount_more_than_apply_amount_repay_asset(self, setup):
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type, self.four_element, 4)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 申请展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)

        merchant_key = self.repay_collect({"item_no": self.item_no, "amount": 1600,
                                           "repay_type": "delay", "finish_at": get_date()})
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, repaid_interest_amount=100, repaid_amount=100, balance_amount=513900)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1600, pay_status="success",
                               delay_status="success")

    def test_offline_first_repay_amount_more_than_apply_amount_repay_debt_asset(self, setup):
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type, self.four_element, 4)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 申请展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)

        merchant_key = self.repay_collect({"item_no": self.item_no, "amount": 600000,
                                           "repay_type": "delay", "finish_at": get_date()})
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)[0]
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay)
        check_asset_data(self.item_no, repaid_interest_amount=14000, repaid_principal_amount=500000,
                         repaid_amount=514000, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")
        check_asset_data(self.item_no_new, repaid_interest_amount=3500, repaid_principal_amount=31000,
                         repaid_amount=34500, balance_amount=479500)
        check_asset_data(self.item_no_x_new, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=600000, pay_status="success",
                               delay_status="success", check_account=False)

    def test_offline_second_repay_amount_less_than_apply_amount(self, setup):
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)

        self.repay_collect({"item_no": self.item_no, "amount": 1600,
                            "repay_type": "delay", "finish_at": get_date()})
        merchant_key = self.repay_collect({"item_no": self.item_no, "amount": 1000,
                                           "repay_type": "delay", "finish_at": get_date()})
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json(
            self.task.get_task(task_order_no=withhold["withhold_channel_key"],
                               task_type="offline_withhold_process")[0]["task_response_data"],
            {"code": 0, "message": "不存在展期记录进行共债资产还款"})
        check_asset_data(self.item_no, repaid_interest_amount=1100, repaid_amount=1100, balance_amount=512900)

    def test_offline_second_repay_amount_equal_than_apply_amount(self, setup):
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)

        self.repay_collect({"item_no": self.item_no, "amount": 1600,
                            "repay_type": "delay", "finish_at": get_date()})
        merchant_key = self.repay_collect({"item_no": self.item_no, "amount": 1500,
                                           "repay_type": "delay", "finish_at": get_date()})
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)[0]
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=11, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=13, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay)
        check_asset_data(self.item_no, repaid_interest_amount=100, repaid_amount=100, balance_amount=513900)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")

    def test_offline_second_repay_amount_more_than_apply_amount_repay_asset(self, setup):
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type, self.four_element, 4)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 申请展期
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)

        self.repay_collect({"item_no": self.item_no, "amount": 1600,
                            "repay_type": "delay", "finish_at": get_date()})
        merchant_key = self.repay_collect({"item_no": self.item_no, "amount": 3000,
                                           "repay_type": "delay", "finish_at": get_date()})
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)[0]
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=11, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=13, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay)
        check_asset_data(self.item_no, repaid_interest_amount=1600, repaid_amount=1600, balance_amount=512400)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=3000, pay_status="success",
                               delay_status="success")

    def test_offline_second_repay_amount_more_than_apply_amount_repay_debt_asset(self, setup):
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type, self.four_element, 4)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)

        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)

        self.repay_collect({"item_no": self.item_no, "amount": 1600,
                            "repay_type": "delay", "finish_at": get_date()})
        merchant_key = self.repay_collect({"item_no": self.item_no, "amount": 600000,
                                           "repay_type": "delay", "finish_at": get_date()})
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)[0]
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=11, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=13, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay)
        check_asset_data(self.item_no, repaid_interest_amount=14000, repaid_principal_amount=500000,
                         repaid_amount=514000, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")
        check_asset_data(self.item_no_new, repaid_interest_amount=3500, repaid_principal_amount=31100,
                         repaid_amount=34600, balance_amount=479400)
        check_asset_data(self.item_no_x_new, balance_amount=50000)
        # check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=600000, pay_status="success",
        #                        delay_status="success")

    def test_offline_repay_asset_already_payoff_manual_to_debt_asset(self, setup):
        self.combo_active_repay_apply(0, 0, period_list=[1, 2, 3, 4])

        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        Assert.assert_equal("payoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"], "资产状态正确")

        merchant_key = self.repay_collect({"item_no": self.item_no, "amount": 1600,
                                           "repay_type": "delay", "finish_at": get_date()})
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type, self.four_element, 4)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        asset_settle_debt(self.item_no, withhold["withhold_channel_key"])
        check_asset_data(self.item_no_new, repaid_interest_amount=1600, repaid_amount=1600, balance_amount=512400)

    def test_offline_repay_asset_already_payoff_auto_to_debt_asset(self, setup):
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type, self.four_element, 4)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)

        self.combo_active_repay_apply(0, 0, period_list=[1, 2, 3, 4])

        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        Assert.assert_equal("payoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"], "资产状态正确")

        self.repay_collect({"item_no": self.item_no, "amount": 1600, "repay_type": "delay", "finish_at": get_date()})
        check_asset_data(self.item_no_new, repaid_interest_amount=1600, repaid_amount=1600, balance_amount=512400)

    def test_offline_repay_create_new_withhold(self, setup):
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type, self.four_element, 4)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 申请还款和展期
        self.combo_active_repay_apply(0, 0, period_list=[1, 2, 3, 4])

        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        resp = trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                              four_element=self.four_element)
        collect_order_no = resp["content"]["data"]["order_no"]
        # 进行展期，并结清资产
        update_rbiz_config_withhold(intervalHour=72, assetDelayIntervalHour=24)
        update_withhold(collect_order_no, withhold_create_at=get_date(day=-1, timezone=get_tz(gc.COUNTRY)))
        run_withholdTimeout_by_api()
        Assert.assert_equal(1, len(self.task.get_task(task_type="withhold_timeout", task_order_no=collect_order_no)))
        self.task.run_task(collect_order_no, "withhold_timeout", {"code": 0, "message": "将订单设置为失败成功！"})
        self.repay_collect({"item_no": self.item_no, "amount": 1600, "repay_type": "delay", "finish_at": get_date()})
        self.repay_collect({"item_no": self.item_no, "amount": 1600, "repay_type": "delay", "finish_at": get_date()})
        asset_delay = get_asset_delay(asset_delay_item_no=self.item_no)
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_status": "success",
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[1])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_status": "success",
                                  "asset_delay_start_at": get_date(day=11, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=13, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[2])
        # 结清后再来
        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})
        Assert.assert_equal("payoff", get_asset(asset_item_no=self.item_no)[0]["asset_status"], "资产状态正确")
        # 再来一笔trade还款
        self.repay_collect({"item_no": self.item_no, "amount": 1600, "repay_type": "delay", "finish_at": get_date()})
        check_asset_data(self.item_no_new, repaid_interest_amount=1600, repaid_amount=1600, balance_amount=512400)

    def test_offline_repay_find_no_account(self, setup):
        account = self.item_no + "@asset_delay"
        resp, req = paysvr_smart_collect_callback(account, 1)
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "不存在展期记录进行共债资产还款"})

        account = "test"
        resp, req = paysvr_smart_collect_callback(account, 1)
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 1, "message": "test资产不存在"})

    def test_card_repay_amount_less_than_apply_repay_asset(self, setup):
        update_rbiz_config(special_service_name="ind_special_service")
        self.mock.update_withhold_autopay_ebank_account_success()
        resp = trade_withhold(self.item_no, "asset_delay", 1500, "ebank", period_list=[1], delay_days=3,
                              four_element=self.four_element)
        merchant_key = resp["content"]["data"]["order_no"]

        mock_data = self.mock.update_query_channel_reconci_data(1, amount=1400, finish_at=get_date(day=-3))
        transaction_no = mock_data["data"][0]["channel_order_no"]
        transaction_confirm(merchant_key, transaction_no)
        self.run_all_task_by_serial_no(merchant_key)

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        Assert.assert_match_json({"asset_delay_status": "fail",
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        check_asset_data(self.item_no, repaid_interest_amount=1400, repaid_amount=1400, balance_amount=512600)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1400, pay_status="success",
                               delay_status="fail", balance_amount=0)
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account_balance_amount不正确")

    def test_card_repay_amount_equal_than_apply(self, setup):
        update_rbiz_config(special_service_name=None)
        self.mock.update_withhold_autopay_ebank_account_success()
        resp = trade_withhold(self.item_no, "asset_delay", 1500, "ebank", period_list=[1], delay_days=3,
                              four_element=self.four_element)
        merchant_key = resp["content"]["data"]["order_no"]

        mock_data = self.mock.update_query_channel_reconci_data(1, amount=1500, finish_at=get_date(day=-3))
        transaction_no = mock_data["data"][0]["channel_order_no"]
        transaction_confirm(merchant_key, transaction_no)

        self.run_all_task_by_serial_no(merchant_key)
        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, balance_amount=514000)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account_balance_amount不正确")

    def test_card_repay_amount_more_than_apply_repay_asset(self, setup):
        update_rbiz_config(special_service_name="ind_special_service")
        self.mock.update_withhold_autopay_ebank_account_success()
        resp = trade_withhold(self.item_no, "asset_delay", 1500, "ebank", period_list=[1], delay_days=3,
                              four_element=self.four_element)
        merchant_key = resp["content"]["data"]["order_no"]

        mock_data = self.mock.update_query_channel_reconci_data(1, amount=1600, finish_at=get_date(day=-3))
        transaction_no = mock_data["data"][0]["channel_order_no"]
        transaction_confirm(merchant_key, transaction_no)
        self.run_all_task_by_serial_no(merchant_key)

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, repaid_interest_amount=100, repaid_amount=100, balance_amount=513900)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1600, pay_status="success",
                               delay_status="success")
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account_balance_amount不正确")

    def test_card_repay_amount_more_than_apply_manual_repay_debt_asset(self, setup):
        update_rbiz_config(special_service_name="ind_special_service")
        # 共债资产
        self.mock.update_withhold_autopay_ebank_account_success()
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type, self.four_element, 4)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 申请展期
        resp = trade_withhold(self.item_no, "asset_delay", 1500, "ebank", period_list=[1], delay_days=3,
                              four_element=self.four_element)
        merchant_key = resp["content"]["data"]["order_no"]

        mock_data = self.mock.update_query_channel_reconci_data(1, amount=600000, finish_at=get_date(day=-3))
        transaction_no = mock_data["data"][0]["channel_order_no"]
        transaction_confirm(merchant_key, transaction_no)
        self.run_all_task_by_serial_no(merchant_key)

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, repaid_interest_amount=14000, repaid_principal_amount=500000,
                         repaid_amount=514000, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")
        check_asset_data(self.item_no_new, balance_amount=514000)
        check_asset_data(self.item_no_x_new, balance_amount=50000)
        # check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=600000, pay_status="success",
        #                        balance_amount=34500)
        # 手动还给共债
        channel_key_delay = get_withhold(withhold_serial_no=merchant_key)[0]["withhold_channel_key"]
        asset_settle_debt(self.item_no, channel_key_delay)
        check_asset_data(self.item_no_new, repaid_interest_amount=3500, repaid_principal_amount=32500,
                         repaid_amount=36000, balance_amount=478000)
        check_asset_data(self.item_no_x_new, balance_amount=50000)

    def test_card_repay_amount_equal_than_apply_match_by_reverse_match(self, setup):
        update_rbiz_config(special_service_name="ind_special_service")
        self.mock.update_withhold_autopay_ebank_account_success()
        resp = trade_withhold(self.item_no, "asset_delay", 1500, "ebank", period_list=[1], delay_days=3,
                              four_element=self.four_element)
        merchant_key = resp["content"]["data"]["order_no"]

        mock_data = self.mock.update_query_channel_reconci_data(1, amount=1500, finish_at=get_date(day=-3))
        transaction_no = mock_data["data"][0]["channel_order_no"]
        transaction_confirm(merchant_key, transaction_no)

        run_accountStatementSync_by_api()
        self.task.run_task(get_date(day=-1, fmt="%Y-%m-%d"), "paysvr_pull_billing_data", {"code": 0, "message": "同步成功"})
        run_initStatusAccountStatementMatchWithholdRecord_by_api()
        self.task.run_task(transaction_no, "account_statement_record_match", {"code": 0, "message": ".*匹配成功.*"})
        self.run_all_task_by_serial_no(merchant_key)

        asset_delay = get_asset_delay(asset_delay_withhold_serial_no=merchant_key)
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 1500,
                                  "asset_delay_apply_amount": 1500},
                                 asset_delay[0])
        Assert.assert_match_json({"asset_delay_period": 1,
                                  "asset_delay_days": 3,
                                  "asset_delay_item_no": self.item_no_x,
                                  "asset_delay_status": "success",
                                  "asset_delay_pay_at": withhold["withhold_finish_at"],
                                  "asset_delay_start_at": get_date(day=8, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_end_at": get_date(day=10, fmt="%Y-%m-%d 00:00:00"),
                                  "asset_delay_amount": 0,
                                  "asset_delay_apply_amount": 0},
                                 asset_delay[1])
        check_asset_data(self.item_no, balance_amount=514000)
        check_asset_data(self.item_no_x, balance_amount=50000)
        check_asset_delay_data(merchant_key, apply_amount=1500, pay_amount=1500, pay_status="success",
                               delay_status="success")
        account = get_account_by_id_num(self.four_element["data"]["id_number_encrypt"])[0]
        Assert.assert_equal(0, account["account_balance_amount"], "account_balance_amount不正确")

    def test_delay_repay_timeout(self, setup):
        # 申请还款和展期
        project_num_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp = self.combo_active_repay_apply(project_num_loan_amount, project_num_no_loan_amount)
        asset_order_no = resp["content"]["data"]["project_list"][0]["order_no"]
        resp = trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                              four_element=self.four_element)
        trade_order_no = resp["content"]["data"]["order_no"]
        resp = trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                              four_element=self.four_element)
        collect_order_no = resp["content"]["data"]["order_no"]
        # 未超时
        update_rbiz_config_withhold(intervalHour=72, assetDelayIntervalHour=24)
        update_withhold(asset_order_no, withhold_create_at=get_date(day=-4, hour=-1, timezone=get_tz(gc.COUNTRY)))
        update_withhold(trade_order_no, withhold_create_at=get_date(day=-2, fmt="%Y-%m-%d 23:59:59"))
        update_withhold(collect_order_no, withhold_create_at=get_date(day=-2, fmt="%Y-%m-%d 23:59:59"))
        run_withholdTimeout_by_api()
        update_withhold(asset_order_no, withhold_create_at=get_date(day=-3, hour=1, timezone=get_tz(gc.COUNTRY)))
        update_withhold(trade_order_no, withhold_create_at=get_date(fmt="%Y-%m-%d 00:00:01"))
        update_withhold(collect_order_no, withhold_create_at=get_date(fmt="%Y-%m-%d 00:00:01"))
        run_withholdTimeout_by_api()
        Assert.assert_equal(0, len(self.task.get_task(task_type="withhold_timeout", task_order_no=asset_order_no)))
        Assert.assert_equal(0, len(self.task.get_task(task_type="withhold_timeout", task_order_no=trade_order_no)))
        Assert.assert_equal(0, len(self.task.get_task(task_type="withhold_timeout", task_order_no=collect_order_no)))
        # 超时关单
        update_withhold(asset_order_no, withhold_create_at=get_date(day=-3, hour=-1, timezone=get_tz(gc.COUNTRY)))
        update_withhold(trade_order_no, withhold_create_at=get_date(day=-1, timezone=get_tz(gc.COUNTRY)))
        update_withhold(collect_order_no, withhold_create_at=get_date(day=-1, timezone=get_tz(gc.COUNTRY)))
        run_withholdTimeout_by_api()
        Assert.assert_equal(1, len(self.task.get_task(task_type="withhold_timeout", task_order_no=asset_order_no)))
        Assert.assert_equal(1, len(self.task.get_task(task_type="withhold_timeout", task_order_no=trade_order_no)))
        Assert.assert_equal(1, len(self.task.get_task(task_type="withhold_timeout", task_order_no=collect_order_no)))

        self.task.run_task(asset_order_no, "withhold_timeout", {"code": 0, "message": "将订单设置为失败成功！"})
        self.task.run_task(trade_order_no, "withhold_timeout", {"code": 0, "message": "将订单设置为失败成功！"})
        self.task.run_task(collect_order_no, "withhold_timeout", {"code": 0, "message": "将订单设置为失败成功！"})
