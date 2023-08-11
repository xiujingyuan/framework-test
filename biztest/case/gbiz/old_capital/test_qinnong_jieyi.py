from biztest.function.biz.biz_db_function import wait_biz_asset_appear
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.qinnong import QinNong
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.function.gbiz.gbiz_check_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.function.contract.contract_check_function import check_contract


# @pytest.mark.gbiz_auto_test
# @pytest.mark.gbiz_qinnong_jieyi
class TestQinnongJieyi(BaseTestCapital):
    def init(self):
        super(TestQinnongJieyi, self).init()
        self.channel = "qinnong_jieyi"
        self.qinnong_mock = QinNong(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_qinnong_jieyi()
        update_gbiz_capital_qinnong_jieyi_const()
        update_gbiz_payment_config(self.payment_mock.url)

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.payment_register(self.payment_mock, self.channel, four_element, item_no)

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.qinnong_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.qinnong_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.qinnong_mock.update_apply_query_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.qinnong_mock.update_post_apply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.qinnong_mock.update_confirm_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.qinnong_mock.update_confirm_query_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.qinnong_mock.update_repay_plan_success(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        wait_biz_asset_appear(item_no)
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)
        # check_asset_tran_data(item_no)

    # @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_qinnong_jieyi_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 # ("草莓", "", 6),
                                 # ("香蕉", "irr36", 6),
                                 ("草莓", "irr36_quanyi", 12),
                                 # ("火龙果", "real36", 12),
                             ])
    def test_qinnong_jieyi_loan_success(self, case, app, source_type, period):
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 5000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        # check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_qinnong_jieyi
    # @pytest.mark.parametrize("count", [12])
    # def test_qinnong_jieyi_raise_limit(self, case, count):
    #     update_qinnong_jieyi_paydayloan(raise_limit_allowed=True)
    #     #新的
    #     update_gbiz_capital_qinnong_jieyi()
    #     update_gbiz_capital_qinnong_jieyi_const(raise_limit_allowed=True)
    #     four_element = get_four_element()
    #     item_no, asset_info = asset_import(self.channel, four_element, count, 8000)
    #     self.register(item_no, four_element)
    #     self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
    #     self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
    #     self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
    #     self.msg.run_msg(item_no, "AssetImportSync")
    #     self.qinnong_mock.update_upload_success()
    #     self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
    #     self.qinnong_mock.update_apply_success()
    #     self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
    #     self.qinnong_mock.update_apply_query_success(asset_info)
    #     self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
    #     # 检查asset_confirm记录"2-处理中"，提额通知msg生成
    #     check_asset_confirm(item_no, "CONFIRM_LOAN_AMOUNT", 2)
    #     check_sendmsg_exist(item_no, "UserLoanConfirmNotifyMQ")
    #     # 用户确认提额，confirm记录更新成"0-成功"状态
    #     new_amount = 1000000
    #     asset_info["data"]["asset"]["amount"] = new_amount / 100
    #     resp = userloan_confirm(asset_info)
    #     Assert.assert_equal(0, resp["code"], "用户确认接口异常")
    #     check_asset_confirm(item_no, "CONFIRM_LOAN_AMOUNT", 0)
    #     # 试算，金额变更
    #     self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
    #     check_asset(item_no, asset_principal_amount=new_amount)
    #     check_asset_loan_record(item_no, asset_loan_record_amount=new_amount)
    #     # 后续流程
    #     prepare_attachment(self.channel, item_no)
    #     self.qinnong_mock.update_post_apply_success()
    #     self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
    #     self.qinnong_mock.update_confirm_apply_success(asset_info)
    #     self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
    #     self.qinnong_mock.update_confirm_query_success(asset_info)
    #     self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
    #     self.qinnong_mock.update_repay_plan_success(asset_info)
    #     self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
    #     self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
    #     wait_biz_asset_appear(item_no)
    #     # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
    #     self.msg.run_msg_by_order_no(item_no)
    #     # check_asset_tran_data(item_no)

    @pytest.mark.gbiz_qinnong_jieyi
    @pytest.mark.gbiz_certificate
    def test_qinnong_jieyi_certificate(self, case):
        item_no = fake_asset_data(self.channel, source_type="irr36_quanyi", status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        self.qinnong_mock.update_certificate_apply_success()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        check_contract(item_no, "ContractDownload", [24])
        check_sendmsg_exist(item_no, "CertificateSuccessNotify")
