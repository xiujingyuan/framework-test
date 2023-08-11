from biztest.function.gbiz.gbiz_check_function import *
from biztest.function.gbiz.gbiz_db_function import update_asset_by_item_no
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.shoujin import ShoujinMock
from biztest.function.contract.contract_db_function import create_contract
from biztest.function.gbiz.gbiz_common_function import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest
from biztest.util.tools.tools import get_four_element


class TestShoujin(BaseTestCapital):
    def init(self):
        super(TestShoujin, self).init()
        self.channel = "shoujin"
        self.mock = ShoujinMock(gbiz_mock)

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.mock.update_account_query_success()
        create_contract(item_no, "30150", "首金-平台注册协议", "http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ111276200422034951.file", "BeforeRegister")
        capital_regiest_query(self.channel, four_element, item_no)

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.mock.update_upload_file_success()
        self.mock.update_commit_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.mock.update_audit_success()
        self.mock.update_repay_plan(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_shoujin
    # @pytest.mark.parametrize("count", [6])
    def test_shoujin_loan_success(self, case, count):
        """
        放款成功
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "草莓", "")

        self.register(item_no, four_element)

        self.mock.update_audit_wait_confirm()
        preloan_confirm(asset_info, four_element)
        check_asset_confirm(item_no, "WITHDRAW_ADVANCE_APPOINTMENT", 2)
        self.mock.update_audit_confirm_success()
        preloan_confirm(asset_info, four_element)
        check_asset_confirm(item_no, "WITHDRAW_ADVANCE_APPOINTMENT", 0)

        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        item_no_noloan, asset_info_noloan = asset_import_noloan(asset_info)
        self.noloan_to_success(item_no_noloan)


    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_shoujin
    # @pytest.mark.parametrize("count", [6])
    def test_shoujin_no_confirm_fail(self, case, count):
        """
        未提现预约切资方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "草莓", "")

        self.register(item_no, four_element)
        self.mock.update_audit_wait_confirm()
        preloan_confirm(asset_info, four_element)
        check_asset_confirm(item_no, "WITHDRAW_ADVANCE_APPOINTMENT", 2)

        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})

        prepare_attachment(self.channel, item_no)
        self.mock.update_upload_file_success()
        self.mock.update_commit_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.mock.update_audit_wait_confirm()
        # 待提现预约时，有1小时等待时间
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 2, "message": "待提现预约,1小时内,继续等待用户提现预约"})
        # 修改asset_create_at，等待超时切资方
        update_asset_by_item_no(item_no, asset_create_at="2020-05-28 00:00:00")
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 11, "未进行提现预约成功")


    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_shoujin
    # @pytest.mark.parametrize("count", [6])
    def test_shoujin_audit_fail(self, case, count):
        """
        审核失败切资方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "草莓", "")

        self.register(item_no, four_element)
        self.mock.update_audit_wait_confirm()
        preloan_confirm(asset_info, four_element)
        check_asset_confirm(item_no, "WITHDRAW_ADVANCE_APPOINTMENT", 2)
        self.mock.update_audit_confirm_success()
        preloan_confirm(asset_info, four_element)
        check_asset_confirm(item_no, "WITHDRAW_ADVANCE_APPOINTMENT", 0)

        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})

        prepare_attachment(self.channel, item_no)
        self.mock.update_upload_file_success()
        self.mock.update_commit_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.mock.update_audit_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})

        check_wait_change_capital_data(item_no, 1004, "审核失败")
