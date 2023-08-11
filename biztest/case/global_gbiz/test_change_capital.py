import time
import pytest
from biztest.case.global_gbiz.global_base_test_capital import BaseTestCapital
from biztest.config.easymock.easymock_config import global_gbiz_mock
from biztest.config.global_gbiz.global_gbiz_kv_config import update_gbiz_payment_config, \
    update_gbiz_circuit_break_config, update_gbiz_manual_task_auto_process_config, update_grouter_channel_change_config
from biztest.function.global_gbiz.gbiz_global_check_function import check_asset_void_data, check_asset_loan_record, \
    check_rollback_changecapital_data, check_global_wait_assetvoid_data
from biztest.function.global_gbiz.gbiz_global_common_function import run_terminated_task
from biztest.function.global_gbiz.gbiz_global_db_function import update_all_channel_amount, \
    update_router_capital_plan_amount_all_to_zero, update_terminated_task
from biztest.util.easymock.payment_global import PaymentGlobalMock
from biztest.interface.gbiz_global.gbiz_global_interface import run_manualTaskAutoProcessJob_by_api



@pytest.mark.gbiz_changecapital
class TestChangeCapital(BaseTestCapital):
    def canloan_fail(self, item_no):
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        update_router_capital_plan_amount_all_to_zero("test")
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})

    def setup(self):
        super(TestChangeCapital, self).init()
        update_all_channel_amount()
        self.paymentmock = PaymentGlobalMock(global_gbiz_mock)
        update_gbiz_payment_config(self.paymentmock.url)
        update_gbiz_circuit_break_config(100)
        update_grouter_channel_change_config()

    @pytest.mark.global_gbiz_thailand
    @pytest.mark.global_gbiz_philippines
    def test_changecapital_success(self):
        """
        切资方成功，海外线上没有这种场景，测试环境只有菲律宾和泰国可以切，切成功就行，不需要检验太多
        :return:
        """
        item_no, asset_info = self.asset_import_data()
        self.loan_to_fail(item_no)
        update_all_channel_amount()
        run_terminated_task(item_no, "ChangeCapital", 0)

    @pytest.mark.global_gbiz_thailand
    @pytest.mark.global_gbiz_mexico
    @pytest.mark.global_gbiz_philippines
    @pytest.mark.global_gbiz_pakistan
    def test_changecapital_finalFail_to_void(self):
        """
        无资方可切，资产作废
        :return:
        """
        item_no, asset_info = self.asset_import_data()
        channel_name = asset_info.get("data").get("asset").get("loan_channel")
        self.loan_to_fail(item_no)
        update_router_capital_plan_amount_all_to_zero(channel_name)
        run_terminated_task(item_no, "ChangeCapital", 1)
        run_terminated_task(item_no, "AssetVoid")
        check_asset_void_data(item_no)

    @pytest.mark.global_gbiz_thailand2
    def test_changecapital_finalFail_to_canloan(self):
        """
        canloan资金量不足导致切资方，重新配置好资金量后回滚到canloan
        任务流转：ChangeCapital=>ApplyCanLoan
        :return:
        """
        update_terminated_task(task_status='close')
        item_no, asset_info = self.asset_import_data()
        channel = asset_info.get('data').get('asset').get('loan_channel')
        update_gbiz_manual_task_auto_process_config(channel)
        self.canloan_fail(item_no)
        run_manualTaskAutoProcessJob_by_api()
        time.sleep(3)
        update_all_channel_amount()
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        check_asset_loan_record(item_no, asset_loan_record_status=1)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        check_asset_loan_record(item_no, asset_loan_record_status=3)

    @pytest.mark.global_gbiz_thailand1
    def test_changecapital_finalFail_assetvoid_to_changecapital(self):
        """
        切资方失败，生成资产作废任务（AssetVoid），执行job后回滚到ChangeCapital(重新切资方)
        任务流转：ChangeCapital=>AssetVoid=>ChangeCapital
        :return:
        """
        item_no, asset_info = self.asset_import_data()
        channel_name = asset_info.get("data").get("asset").get("loan_channel")
        self.canloan_fail(item_no)
        update_router_capital_plan_amount_all_to_zero(channel_name)
        run_terminated_task(item_no, "ChangeCapital", 1)
        run_manualTaskAutoProcessJob_by_api()
        time.sleep(3)
        check_rollback_changecapital_data(item_no, 10000, "AssetVoid回滚到ChangeCapital自动执行",
                                          "AssetCanLoanFailedEvent")
    @pytest.mark.global_gbiz_thailand
    @pytest.mark.global_gbiz_philippines
    def test_changecapital_rollback_to_assetvoid(self):
        """
        失败切换资金方，因为匹配策略，回滚到AssetVoid任务后取消
        """
        update_all_channel_amount()
        item_no, asset_info = self.asset_import_data()
        channel = asset_info.get('data').get('asset').get('loan_channel')
        update_gbiz_manual_task_auto_process_config(channel)
        self.loan_to_fail(item_no)
        run_manualTaskAutoProcessJob_by_api()
        time.sleep(3)
        run_manualTaskAutoProcessJob_by_api()
        check_global_wait_assetvoid_data(item_no, 1,
                                         "\\[KN_INVALID_ACCOUNT\\]Risk control intercepts and exceeds trading limits")
