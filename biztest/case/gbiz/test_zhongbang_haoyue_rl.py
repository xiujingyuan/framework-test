from biztest.interface.gbiz.gbiz_interface import *
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.gbiz.gbiz_zhongbang_haoyue_rl_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_all_channel_amount
import pytest
from biztest.util.easymock.gbiz.zhongbang_haoyue_rl import ZhongbangHaoyueRlMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.util.tools.tools import get_four_element

@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_zhongbang_haoyue_rl
class TestZhongbangHaoyueRl(BaseTestCapital):

    def init(self):
        super(TestZhongbangHaoyueRl, self).init()
        self.channel = "zhongbang_haoyue_rl"
        self.capital_mock = ZhongbangHaoyueRlMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_payment_config(self.payment_mock.url)
        update_gbiz_capital_zhongbang_haoyue_rl()
        update_gbiz_capital_zhongbang_haoyue_rl_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()
    # 走paysvr开户
    def register(self, item_no, four_element):
        self.payment_register(self.payment_mock, self.channel, four_element, item_no, way='tq')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_file_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "ZBHYRL_FILE_ID_101")
        check_asset_event_exist(item_no, self.channel, "ZBHYRL_FILE_ID_102")
        check_asset_event_exist(item_no, self.channel, "ZBHYRL_FILE_ID_103")
        check_asset_event_exist(item_no, self.channel, "ZBHYRL_FILE_ID_106")
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_agree_share_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_disbursement_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_disbursement_query()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayment_plan_query(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=0)
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        # 合同下载会调用3个接口，前面的查询接口是之前调用过的，此处重复调用为了查询到合同，然后下载，但是base64太长不好mock，此处屏蔽
        # self.capital_mock.update_credit_query(item_no)
        # self.capital_mock.update_disbursement_query()
        # self.capital_mock.update_file_download()
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_zhongbang_haoyue_rl_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [
                              ("香蕉", "apr36", 12),
                              # ("草莓", "irr36", 12),
                              # ("火龙果", "real24", 12)
                              ])
    def test_zhongbang_haoyue_rl_loan_success(self, case, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 5000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhongbang_haoyue_rl_canloan_fail(self, case, app, source_type, period):
        """
        canloan失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="16")
        item_no, asset_info = asset_import(self.channel, four_element, period, 5000, app, source_type)
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
        update_router_capital_plan_amount(10000000000, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "zhongbang_haoyue_rl->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhongbang_haoyue_rl_apply_fail(self, case, app, source_type, period):
        """
        LoanApplyNew 失败（授信申请失败）切资方
        """
        four_element = get_four_element(id_num_begin="15")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_file_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(status='F')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, status='F')
        check_wait_change_capital_data(item_no, 10000, "F-Success", "LoanApplySyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 10000, "F-Success", "id_card")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhongbang_haoyue_rl_applyquery_fail(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败(授信查询拒绝失败)切资方
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_file_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no,status='F')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10000, "F-Success", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 10000, "F-Success", "id_card")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhongbang_haoyue_rl1_applyquery_not_balance(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败
        授信额度不足，失败切换资金方
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_file_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, availableAmount=0)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10000, "\\[众邦昊悦润楼\\]资产\\[" + item_no + "\\],资产本金\\[6000.00\\]授信可用余额不足\\[0\\]-Success", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 10000, "\\[众邦昊悦润楼\\]资产\\[" + item_no + "\\],资产本金\\[6000.00\\]授信可用余额不足\\[0\\]-Success", "id_card")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhongbang_zhongji_applyquery_overdue(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败
        授信过期，切换资金方
        """
        four_element = get_four_element(id_num_begin="24")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_file_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, creditEndDate='20221212')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10000, "\\[众邦昊悦润楼\\]资产\\[" + item_no + "\\],授信额度已过期，授信时间\\[20221212\\], 当前时间\\["+ get_date(fmt='%Y%m%d') +"\\]-Success", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 10000, "\\[众邦昊悦润楼\\]资产\\[" + item_no + "\\],授信额度已过期，授信时间\\[20221212\\], 当前时间\\["+ get_date(fmt='%Y%m%d') +"\\]-Success", "id_card")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhongbang_haoyue_rl_confirm_fail(self, case, app, source_type, period):
        """
        LoanApplyConfirm 失败切资方
        用信失败
        """
        four_element = get_four_element(id_num_begin="31")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_file_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_agree_share_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_disbursement_apply(status='F')
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_disbursement_query(status='F')
        check_wait_change_capital_data(item_no, 30000, "F-Success", "ConfirmApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_gbiz_zhongbang_haoyue_rl_confirmquery_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery 失败切资方
        用信失败
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_file_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_agree_share_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_disbursement_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_disbursement_query(status='F')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 30000, "F-Success", "GrantFailedEvent")

    # 因为结清证明下载的返回需要mock base64（不好mock），所以此处屏蔽
    # @pytest.mark.gbiz_certificate
    # def test_zhongbang_haoyue_rl_certificate(self, case):
    #     item_no = fake_asset_data(self.channel, status="payoff")
    #     resp = certificate_apply(item_no)
    #     Assert.assert_equal(0, resp["code"])
    #     update_asset_due_bill_no(item_no)
    #     update_asset_loan_record_extend_info(item_no)
    #     check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
    #     self.capital_mock.update_certificateapply_success()
    #     self.capital_mock.update_certificate_download_success()
    #     self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
    #     check_contract(item_no, "ContractDownload", [24])
    #     check_sendmsg_exist(item_no, "CertificateSuccessNotify")
