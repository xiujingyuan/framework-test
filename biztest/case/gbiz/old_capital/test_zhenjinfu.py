from biztest.function.biz.biz_db_function import wait_biz_asset_appear
from biztest.function.gbiz.gbiz_check_function import check_asset_tran_data
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.zhengjinfu import ZhenJinFuMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest


class TestZhenjinfu(BaseTestCapital):
    def init(self):
        super(TestZhenjinfu, self).init()
        self.channel = "zhenjinfu"
        self.mock = ZhenJinFuMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)

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
        self.mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.mock.update_loan_query_success(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.mock.update_get_contract_success()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.mock.update_repayplan_success(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_zhenjinfu
    # @pytest.mark.parametrize("count", [6])
    def test_zhenjinfu(self, case, count):
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "草莓", "")
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)

        # 小单部分
        item_no_noloan, asset_info_noloan = asset_import_noloan(asset_info)
        self.noloan_to_success(item_no_noloan)


if __name__ == "__main__":
    pytest.main(["-s", "/Users/fenlai/code/framework-test/biztest/case/gbiz/qnn_lm.py", "--env=9"])
