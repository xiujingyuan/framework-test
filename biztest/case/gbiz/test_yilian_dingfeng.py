from biztest.function.contract.contract_check_function import check_contract
from biztest.interface.gbiz.gbiz_interface import asset_import, common_noloan_import, certificate_apply
from biztest.util.asserts.assert_util import Assert
from biztest.util.easymock.gbiz.yilian_dingfeng import YilianDingfengMock
from biztest.function.gbiz.gbiz_check_function import check_asset_tran_data,check_wait_change_capital_data,\
    check_wait_blacklistcollect_data, check_asset_event_exist, check_sendmsg_exist, check_asset_tran_valid_status
from biztest.config.gbiz.gbiz_kv_config import update_gbiz_payment_config
from biztest.config.gbiz.gbiz_yilian_dingfeng_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import prepare_attachment, fake_asset_data
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_all_channel_amount, \
    update_asset_due_bill_no
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_yilian_dingfeng
class TestYilianDingfeng(BaseTestCapital):
    def init(self):
        super(TestYilianDingfeng, self).init()
        self.channel = "yilian_dingfeng"
        self.capital_mock = YilianDingfengMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_payment_config(self.payment_mock.url)
        update_gbiz_capital_yilian_dingfeng()
        update_gbiz_capital_yilian_dingfeng_const()
        update_gbiz_guarantee_dingfeng_const()
        update_all_channel_amount()


    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.payment_register(self.payment_mock, self.channel, four_element, item_no, way='tq')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_query_success()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repay_plan(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)
        self.task.run_task(item_no, "CapitalRepayPlanPush", excepts={"code": 0})
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        # self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 0})
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        # self.task.run_task(item_no, "GuaranteeUpload", excepts={"code": 0})

    @pytest.mark.parametrize("app, source_type, count, product_code",
                             [
                                 # ("香蕉", "apr36", 6, "df"),
                                 ("重庆草莓", "apr36", 12, "df2"),
                                 # ("香蕉", "irr36", 6, "df2"),
                                 ("草莓", "irr36", 12, "df"),
                             ])
    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_yilian_dingfeng_loansuccess
    def test_yilian_dingfeng_loan_success(self, case, app, source_type, count, product_code):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="10")
        item_no, asset_info = asset_import(self.channel, four_element, count, 5000, app, source_type, product_code=product_code)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # check_request_log_by_channel(item_no, self.channel)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    def test_yilian_dingfeng_loancreditquery_fail(self, case):
        """
        授信失败切资方
        """
        four_element = get_four_element(id_num_begin="10")
        item_no, asset_info = asset_import(self.channel, four_element, 12, 6000)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_query_fail()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1000000, "02-0005-成功-银行风控拒绝")
        check_wait_blacklistcollect_data(item_no, asset_info, 1000000, "02-0005-成功-银行风控拒绝",capital_blacklist_type='id_card')

    def test_yilian_dingfeng_loan_fail(self, case):
        """
        放款支用失败切资方
        """
        four_element = get_four_element(id_num_begin="10")
        item_no, asset_info = asset_import(self.channel, four_element, 12, 6000)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_ftp_upload_success()
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_query_success()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query_fail()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1000000, "02-0006-成功-交易处理失败")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_yilian_dingfeng
    @pytest.mark.gbiz_certificate
    def test_yilian_dingfeng_certificate(self, case):
        item_no = fake_asset_data(self.channel, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        update_asset_due_bill_no(item_no)
        self.capital_mock.update_certificate_apply()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        self.capital_mock.update_certificate_download()
        self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        check_contract(item_no, "ContractDownload", [24])
        check_sendmsg_exist(item_no, "CertificateSuccessNotify")
