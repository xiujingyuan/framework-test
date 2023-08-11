from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.yumin_zhongbao import YuMinZhongBaoMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_yumin_zhongbao_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import update_router_capital_plan_amount, update_all_channel_amount, \
    create_task_loancreditcancel, create_asset_event
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_yumin_zhongbao
class TestYuminZhongbao(BaseTestCapital):
    """
       gbiz_yumin_zhongbao
       author: zhimengxue
       date: 20220822
       """

    def init(self):
        super(TestYuminZhongbao, self).init()
        self.channel = "yumin_zhongbao"
        self.capital_mock = YuMinZhongBaoMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_yumin_zhongbao()
        update_gbiz_capital_yumin_zhongbao_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()


    def register(self, item_no, four_element):
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_card_pre_bind()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='yumin_zhongbao', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_card_bind()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='yumin_zhongbao', step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # prepare_attachment(self.channel, item_no)
        self.capital_mock.update_image_upload()
        self.capital_mock.update_image_live_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_status(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_status(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repay_plan(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        # 上传协议到担保方
        # self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        # 上传进件，放款信息到担保方
        # self.task.run_task(item_no, "GuaranteeUpload", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        self.msg.run_msg_by_order_no(item_no)
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        # 结清证明申请 空实现
        # self.task.run_task(item_no, ""CertificateApply", excepts={"code": 0})
        # 结清证明下载，调资方接口返回base64
        # self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_yumin_zhongbao_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12),
                                 # ("草莓", "irr36", 12),
                             ])
    def test_yumin_zhongbao_loan_success(self, case, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="36")  # 只要属于江西的用户
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_yumin_zhongbao_conloan_fail(self, case, app, source_type, period):
        """
        canloan fail
        :return:
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
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
        check_wait_change_capital_data(item_no, 4, "yumin_zhongbao->校验资金量失败;", "AssetCanLoanFailedEvent")


    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_yumin_zhongbao_loanapplynew_fail(self, case, app, source_type, period):
        """
        进件同步失败
        :return:
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 5000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_image_upload()
        self.capital_mock.update_image_live_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(status='Reject')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_status(item_no, creditApprovalStatus='002')
        check_wait_change_capital_data(item_no, 10, "成功_Reject", 'LoanApplySyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info, 10, "成功_Reject", "id_card")

    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("草莓", "apr36", 12)
                             ])
    def test_yumin_zhongbao_loanapplyquery_fail(self, case, app, source_type, period):
        """
        进件查询失败
        :return:
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 7000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_image_upload()
        self.capital_mock.update_image_live_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_status(item_no, creditApprovalStatus='002', creditStatus='null')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10, "成功_null_002", 'LoanApplyAsyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info, 10, "成功_null_002", "id_card")


    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("草莓", "apr36", 12)
                             ])
    def test_yumin_zhongbao_loanapplyconfirm_fail(self, case, app, source_type, period):
        """
        放款申请同步失败
        :return:
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 9000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_image_upload()
        self.capital_mock.update_image_live_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_status(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loan_apply(replyCode='Fail',replyMsg='失败')
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_status(item_no, loanResult='Fail', resultMsg ='失败')
        check_wait_change_capital_data(item_no, 20, "成功_Fail_失败", "ConfirmApplySyncFailedEvent")

    @pytest.mark.gbiz_yumin_zhongbao
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_yumin_zhongbao_loanaconfirmquery_fail(self, case, app, source_type, period):
        """
        放款失败
        :return:
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_image_upload()
        self.capital_mock.update_image_live_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_status(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_status(item_no, loanResult='Fail', resultMsg ='失败')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 20, "成功_Fail_失败", 'GrantFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info, 20, "成功_Fail_失败", "id_card")


    def test_yumin_zhongbao_limit_cancel(self, case):
        item_no = fake_asset_data(self.channel, status="payoff")
        # 以下是为了创建授信流水号
        create_asset_event(item_no, self.channel, asset_event_no="ym" + get_random_str(10))
        # 手动创建取消额度任务
        # LoanCreditCancel这个任务实际上是由AssetChangeNotice任务执行成功后创建出来的，
        # 创建条件：资产为payoff状态，事件表中存在裕民授信成功事件
        create_task_loancreditcancel(item_no)
        self.capital_mock.update_limit_cacel()
        self.task.run_task(item_no, "LoanCreditCancel", excepts={"code": 0})