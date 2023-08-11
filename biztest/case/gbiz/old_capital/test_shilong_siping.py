from biztest.function.biz.biz_db_function import wait_biz_asset_appear
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.shilong_siping import ShilongSipingMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest
from biztest.util.tools.tools import get_four_element


class TestShilongSiping(BaseTestCapital):
    def init(self):
        super(TestShilongSiping, self).init()
        self.channel = "shilong_siping"
        self.capital_mock = ShilongSipingMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        #update_shilong_siping_paydayloan()
        #新的
        update_gbiz_capital_shilong_siping()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.payment_register(self.payment_mock, self.channel, four_element, item_no)

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_result_not_exist()
        self.capital_mock.update_credit_apply_success(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_result_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_result_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.capital_mock.update_repay_plan(item_no)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.capital_mock.update_contract_success()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shilong_siping
    @pytest.mark.gbiz_shilong_siping_loan_success
    @pytest.mark.parametrize("count", [6, 12])
    def test_shilong_siping_loan_success(self, case, count):
        """
        放款成功
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 5000, "香蕉")

        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        item_no_noloan, asset_info_noloan = asset_import_noloan(asset_info)
        self.noloan_to_success(item_no_noloan)

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shilong_siping
    @pytest.mark.parametrize("count", [12])
    def test_shilong_siping_apply_fail(self, case, count):
        """
        授信失败切资方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "草莓")

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_result_not_exist()
        self.capital_mock.update_credit_apply_already_exist(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 21, "客户已授信")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shilong_siping
    @pytest.mark.parametrize("count", [12])
    def test_shilong_siping_audit_fail(self, case, count):
        """
        审核失败切资方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "草莓")

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})

        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 2})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_fail()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 2})
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})

        self.capital_mock.update_credit_result_wait(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_result_wait(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 2})
        self.capital_mock.update_credit_result_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 3, "审核拒绝")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shilong_siping
    @pytest.mark.parametrize("count", [12])
    def test_shilong_siping_loan_fail(self, case, count):
        """
        放款失败切资方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "火龙果", "real36", '')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_result_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_result_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_result_wait(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 2})
        self.capital_mock.update_loan_result_fail(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 1008, "放款失败")
