from biztest.function.contract.contract_check_function import check_contract
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.zhongke_hegang import ZhongkeHegangMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_zhongke_hegang_config import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_all_channel_amount
from biztest.util.easymock.gbiz.payment import PaymentMock
import pytest
from biztest.util.tools.tools import get_four_element


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_zhongke_hegang
class TestZhongkeHegang(BaseTestCapital):
    """
          gbiz_zhongke_hegang
          author: zhimengxue
          date: 20210303
          """

    def init(self):
        super(TestZhongkeHegang, self).init()
        self.channel = "zhongke_hegang"
        self.capital_mock = ZhongkeHegangMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_zhongke_hegang()
        update_gbiz_capital_hegang_const()
        update_gbiz_payment_config(self.payment_mock.url)
        update_all_channel_amount()

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
        self.capital_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_useapply_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanquery_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repay_plan_query_success(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.capital_mock.update_file_sync_notify_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_zhongke_hegang_loan_success
    @pytest.mark.parametrize("app, source_type, count,product_code",
                             [
                                 ("香蕉", "apr36", 6, "KN1-CL-HLJ"),
                                 ("草莓", "apr36", 12, "KN1-CL-NOT-HLJ"),
                                 ("香蕉", "irr36", 6, "KN1-CL-NOT-HLJ"),
                                 ("草莓", "irr36", 12, "KN1-CL-HLJ"),
                                 # ("草莓", "irr36_quanyi", 12, "KN1-CL-NOT-HLJ"),
                                 # ("草莓", "irr36_quanyi", 12, "KN1-CL-HLJ"),
                             ])
    def test_zhongke_hegang_loan_success(self, case, app, source_type, count, product_code):
        """
        放款成功
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type,
                                           product_code=product_code)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # check_request_log_by_channel(item_no, self.channel)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("count,product_code", [(12, "KN1-CL-HLJ"), (12, "KN1-CL-NOT-HLJ")])
    def test_zhongke_hegang_canloan_fail(self, case, count, product_code):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, product_code=product_code)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        # canloan失败准备工作
        today = time.strftime("%Y-%m-%d", time.localtime())
        update_router_capital_plan_amount(0, today, self.channel)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        time.sleep(2)
        # canloan执行之后恢复
        update_router_capital_plan_amount(3333333333, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "zhongke_hegang->校验资金量失败;")

    @pytest.mark.parametrize("count,product_code", [(12, "KN1-CL-HLJ"), (12, "KN1-CL-NOT-HLJ")])
    def test_zhongke_hegang_loanapplynew_fail(self, case, count, product_code):
        """
        授信申请失败切资方，一般来说无这种情况出现，资金方说若线上出现则需要人工介入处理
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, product_code=product_code)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_fail()
        self.capital_mock.update_creditquery_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9000, "授信申请失败")

    @pytest.mark.parametrize("count,product_code", [(12, "KN1-CL-HLJ"), (12, "KN1-CL-NOT-HLJ")])
    def test_zhongke_hegang_loanapplyquery_fail(self, case, count, product_code):
        """
        授信查询失败切换资金方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, product_code=product_code)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditquery_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 190000, "交易处理失败--null")
        check_wait_blacklistcollect_data(item_no, asset_info, code=190000, message="交易处理失败--null")

    @pytest.mark.parametrize("count,product_code", [(12, "KN1-CL-HLJ"), (12, "KN1-CL-NOT-HLJ")])
    def test_zhongke_hegang_loanconfirmquery_fail(self, case, count, product_code):
        """
        放款结果查询失败切换资金方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, product_code=product_code)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_useapply_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanquery_fail(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2900000, "交易处理失败-E012-暂不支持该卡号-未查询到卡bin信息")
        check_wait_blacklistcollect_data(item_no, asset_info, code=2900000,
                                         message="交易处理失败-E012-暂不支持该卡号-未查询到卡bin信息")

    @pytest.mark.skip
    @pytest.mark.gbiz_certificate
    def test_zhongke_hegang_certificate(self, case):
        item_no = fake_asset_data(self.channel, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        self.capital_mock.update_certificate_apply()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        self.capital_mock.update_certificate_download(item_no)
        self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        check_contract(item_no, "ContractDownload", [24])
        check_sendmsg_exist(item_no, "CertificateSuccessNotify")
