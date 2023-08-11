from biztest.interface.gbiz.gbiz_interface import *
from biztest.config.gbiz.gbiz_kv_config import update_gbiz_payment_config
from biztest.interface.gbiz.gbiz_interface import asset_import, common_noloan_import
from biztest.util.easymock.gbiz.hebei_jiahexing_ts import HebeiJiahexingTsMock
from biztest.function.gbiz.gbiz_check_function import check_wait_change_capital_data, check_asset_tran_valid_status,\
    check_wait_blacklistcollect_data, check_asset_event_exist
from biztest.config.gbiz.gbiz_hebei_jiahexing_ts_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import prepare_attachment, fake_asset_data
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_all_channel_amount,\
    update_router_capital_plan_amount, update_asset_due_bill_no
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_hebei_jiahexing_ts
class TestHebeiJiaxingTs(BaseTestCapital):
    '''
    该资金方与河北稳顺泰山接口参数等都一样，只是融担合同不一样
    '''
    def init(self):
        super(TestHebeiJiaxingTs, self).init()
        self.channel = "hebei_jiahexing_ts"
        self.capital_mock = HebeiJiahexingTsMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_payment_config(self.payment_mock.url)
        update_gbiz_capital_hebei_jiahexing_ts()
        update_gbiz_capital_hebei_jiahexing_ts_const()
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
        prepare_attachment(self.channel, item_no)
        # 该任务仅上传文件到资金方sftp，不调用接口，文件：身份证正反面，活体照，35000、35001、35002、35003
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # LoanApplyTrial 空实现，主要是发送签约合同的通知
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        # 仅上传合同35006(河北嘉合兴-河北银行借款协议)到资金方sftp
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayplan_query(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        #去资方sftp下载
        #self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                                 # ("草莓", "irr36", 12),
                             ])
    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_hebei_jiahexing_ts_loansuccess
    def test_hebei_jiahexing_ts_loan_success(self, case, app, source_type, count):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_hebei_jiahexing_ts_conloan_fail(self, case, app, source_type, count):
        """
        canloan fail
        :return:
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        # canloan失败准备工作
        today = time.strftime("%Y-%m-%d", time.localtime())
        update_router_capital_plan_amount(0, today, self.channel)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        time.sleep(2)
        # canloan执行之后恢复
        update_router_capital_plan_amount(10000000000, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "hebei_jiahexing_ts->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_hebei_jiahexing_ts_applynew_fail(self, case, app, source_type, count):
        """
        授信申请失败切资方
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no, respcode='9000', respmesg='交易处理失败')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query_notorder()
        check_wait_change_capital_data(item_no, 19999, "9000_交易处理失败")
        check_wait_blacklistcollect_data(item_no, asset_info,  19999, "9000_交易处理失败", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_hebei_jiahexing_ts_applyquery_fail(self, case, app, source_type, count):
        """
        授信查询失败切资方
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, respcode='9999', respmesg='交易处理成功', result='0')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10000, "9999_交易处理成功_0_null_null")
        check_wait_blacklistcollect_data(item_no, asset_info, 10000, "9999_交易处理成功_0_null_null", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_hebei_jiahexing_ts_applyconfirm_fail(self, case, app, source_type, count):
        """
        申请借款失败切资方
        """
        four_element = get_four_element(id_num_begin="44")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # LoanApplyTrial 空实现，主要是发送签约合同的通知
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply(respcode='9999', respmesg='交易接收失败')
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query_notorder()
        check_wait_change_capital_data(item_no, 20000, "9999_交易接收失败")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_hebei_jiahexing_ts_confirmquery_fail(self, case, app, source_type, count):
        """
        放款查询失败切资方
        """
        four_element = get_four_element(id_num_begin="52")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # LoanApplyTrial 空实现，主要是发送签约合同的通知
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query(item_no, respcode='9999', respmesg='交易处理成功', status='0')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 20000, "9999_交易处理成功_0_null_null")


    @pytest.mark.gbiz_certificate
    def test_hebei_jiahexing_ts_certificate(self, case):
        item_no = fake_asset_data(self.channel, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        update_asset_due_bill_no(item_no)
        self.capital_mock.update_certificate_apply()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        # # 从资金方的SFTP下载结清证明，不好mock, 所以屏蔽
        # self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        # check_contract(item_no, "ContractDownload", [24])
        # check_sendmsg_exist(item_no, "CertificateSuccessNotify")
