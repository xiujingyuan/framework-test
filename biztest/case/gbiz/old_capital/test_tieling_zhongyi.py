from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.tieling_zhongyi import TielingZhongyiMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest
from biztest.util.tools.tools import get_four_element


class TestTielingZhonyi(BaseTestCapital):

    def init(self):
        super(TestTielingZhonyi, self).init()
        self.channel = "tieling_zhongyi"
        self.capital_mock = TielingZhongyiMock(gbiz_mock)
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
        self.capital_mock.update_credit_apply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_query_success()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_query_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_repay_plan(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tieling_zhongyi
    @pytest.mark.gbiz_tieling_zhongyi_loan_success
    @pytest.mark.parametrize("count", [12])
    def test_tieling_zhongyi_loan_success(self, case, count):
        """
        放款成功
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "香蕉", "", '', '110000')
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        item_no_noloan, asset_info_noloan = asset_import_noloan(asset_info)
        self.noloan_to_success(item_no_noloan)

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tieling_zhongyi
    @pytest.mark.parametrize("count", [12])
    def test_credit_fail(self, case, count):
        """
        风控分失败切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "香蕉", "", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_credit_apply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_query_fail()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 100015, "中裔分获取失败")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tieling_zhongyi
    @pytest.mark.parametrize("count", [12])
    def test_grant_fail(self, case, count):
        """
        资方放款失败切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "香蕉", "", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_credit_apply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_query_success()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_query_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 12009, "TR002:放款失败")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tieling_zhongyi
    @pytest.mark.parametrize("count", [12])
    def test_grant_fail_order_not_exist(self, case, count):
        """
        资方放款失败切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "香蕉", "", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_credit_apply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_query_success()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_query_fail_not_exist()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 299, "订单不存在")
