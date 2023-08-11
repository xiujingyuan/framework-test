from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.easymock.easymock_config import global_rbiz_mock
from biztest.config.global_rbiz.global_rbiz_kv_config import update_phl_rbiz_paysvr_config, update_rbiz_config
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto
from biztest.function.global_rbiz.rbiz_global_check_function import *
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback, asset_repay_reverse, \
    paysvr_smart_collect_callback, trade_withhold, run_refreshLateFeeV1_by_api
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.payment_global import PaymentGlobalMock
from biztest.util.task.task import TaskGlobalRepay


class TestRbizMex(BaseGlobalRepayTest):
    """
       u_peso repay
    """
    from_system = "ginkgo"
    loan_channel = "mangguo"
    source_type = "pl01"
    principal_amount = 500000

    @classmethod
    def setup_class(cls):
        cls.task = TaskGlobalRepay()
        cls.mock = PaymentGlobalMock(global_rbiz_mock)
        update_rbiz_config(tolerance_amount=100, auto_tolerance=True)

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
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, "mex", self.from_system,
                                                     self.source_type, self.four_element, period=1,
                                                     fees={"fin_service": 30.00, "interest": 36.00}, late_num="late5%")
        self.item_no_new, asset_info_new = asset_import_auto(self.loan_channel, 7, "mex", self.from_system,
                                                             self.source_type, self.four_element, period=2,
                                                             fees={"fin_service": 30.00, "interest": 36.00},
                                                             late_num="late5%")

    @pytest.mark.global_rbiz_mexico11
    def test_active_normal_repay(self, setup):
        self.update_asset_due_at(-2, refresh=True)
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        resp_combo_active = self.loan_active_repay_apply(project_num_loan_channel_amount, 'barcode')
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]

        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=7,
                       four_element=self.four_element)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        self.repay_collect({"item_no": self.item_no, "amount": 1500, "repay_type": "delay"})
        self.repay_trade({"item_no": self.item_no, "amount": 1000, "status": 2})

        # self.update_asset_due_at(-2, refresh=True)
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        resp_combo_active = self.loan_active_repay_apply(project_num_loan_channel_amount, 'barcode')
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) - 100, 2)
        self.run_all_task_after_repay_success()
        provision = get_provision(provision_item_no=self.item_no)[0]
        asset_repay_reverse(self.item_no, provision["provision_recharge_serial_no"])

        resp, req = paysvr_smart_collect_callback(self.item_no, 110)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([channel_key])

        task = self.task.get_task(task_order_no=self.item_no, task_type="provisionRepay")[0]
        self.task.update_task(task["task_id"], task_status='open')
        self.task.run_task_by_id(task["task_id"])
