from biztest.interface.gbiz.gbiz_interface import *
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_zhenxing_zhongzhixin_jx_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_all_channel_amount
import pytest
from biztest.util.easymock.gbiz.zhenxing_zhongzhixin_jx import ZhenxingZhongzhixinJxMock
from biztest.util.tools.tools import get_four_element

@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_zhenxing_zhongzhixin_jx
class TestZhenxingZhongzhixinJx(BaseTestCapital):
    """
       gbiz_zhenxing_zhongzhixin_jx
       author: zhimengxue
       date: 20230130
    """
    def init(self):
        super(TestZhenxingZhongzhixinJx, self).init()
        self.channel = "zhenxing_zhongzhixin_jx"
        self.capital_mock = ZhenxingZhongzhixinJxMock(gbiz_mock)
        update_gbiz_capital_zhenxing_zhongzhixin_jx()
        update_gbiz_capital_zhenxing_zhongzhixin_jx_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()


    def register(self, four_element, item_no):
        self.capital_mock.update_accountquery_new_user()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_accountquery_new_user()
        self.capital_mock.update_get_sessionid()  # 新用户开户走到这里就需要走这个接口，老用户不会走开户，则会在LoanPreApply任务中调用这个接口
        self.capital_mock.update_get_uniquecode()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        check_asset_event_exist(item_no, self.channel, "JX_GET_SESSION_ID_SUCCESS")
        self.capital_mock.update_accountquery_new_user()
        self.capital_mock.update_get_uniquecode()
        self.capital_mock.update_confirm_bpauth()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_ftp_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "JX_PRE_LOAN_UPLOAD_FILE_SUCCESS")
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loancreditapply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_loanpostcredit()
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loancreditquery(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        check_asset_event_exist(item_no, self.channel, "JX_PRE_AUDIT_SUSCCESS")
        check_asset_confirm(item_no, "CONTRACT_VIA_URL", 2)
        # BC 发起确认
        user_change_product_confirm(asset_info, "CONTRACT_VIA_URL", 0)
        check_asset_confirm(item_no, "CONTRACT_VIA_URL", 0)
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 1})
        self.capital_mock.update_loanapplyconfirm()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirmquery(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_queryrepayplan_success(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=0)
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_zhenxing_zhongzhixin_jx_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [("香蕉", "apr36", 12),
                              # ("草莓", "irr36", 12),
                              ])
    def test_zhenxing_zhongzhixin_jx_loan_success(self, case, app, source_type, period):
        """
        放款成功，只允许户籍地址是辽宁的用户路由进件
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 13000, app, source_type)
        self.register(four_element, item_no)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhenxing_zhongzhixin_jx_old_user(self, case, app, source_type, period):
        """
        已经开户成功的老用户。会在LoanPreApply任务中调用获取sessionId接口
        """
        four_element = get_four_element(id_num_begin="16")
        # 模拟已经开户成功的老用户，查询开户即可成功，再使用这个四要素进行借款，这就是老用户借款
        item_no_old = get_item_no()
        self.register(four_element, item_no_old)
        # 老用户进件
        item_no, asset_info = asset_import(self.channel, four_element, period, 5000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_ftp_upload()
        self.capital_mock.update_get_sessionid()  # 老用户不会走开户，则会在LoanPreApply任务中调用这个接口
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "JX_GET_SESSION_ID_SUCCESS")
        check_asset_event_exist(item_no, self.channel, "JX_PRE_LOAN_UPLOAD_FILE_SUCCESS")
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhenxing_zhongzhixin_jx_canloan_fail(self, case, app, source_type, period):
        """
        canloan失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="16")
        item_no, asset_info = asset_import(self.channel, four_element, period, 5000, app, source_type)
        self.register(four_element, item_no)
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
        check_wait_change_capital_data(item_no, 4, "zhenxing_zhongzhixin_jx->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhenxing_zhongzhixin_jx_apply_fail(self, case, app, source_type, period):
        """
        LoanApplyNew 失败（授信申请失败）切资方
        """
        four_element = get_four_element(id_num_begin="15")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_ftp_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_fail()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_fail()
        check_wait_change_capital_data(item_no, 1, "mock 进件失败-null-null-null", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhenxing_zhongzhixin_jx_applyquery_fail(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败(授信查询拒绝失败)切资方
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_ftp_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "mock失败测试-FAIL-null-null", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhenxing_zhongzhixin_jx_applyquery_not_balance(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败
        授信额度不足，失败切换资金方
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_ftp_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery(creditamount='0', validto='2036-12-12 00:00:00')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9999, "授信金额小于资产本金", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhenxing_zhongzhixin_jx_applyquery_overdue(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败
        授信过期，切换资金方
        """
        four_element = get_four_element(id_num_begin="24")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_ftp_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery(creditamount='20000', validto='2022-12-12 00:00:00')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9999, "授信额度已过期", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhenxing_zhongzhixin_jx_creditapply_fail(self, case, app, source_type, period):
        """
        LoanCreditApply 失败切资方
        预审申请失败
        """
        four_element = get_four_element(id_num_begin="31")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_ftp_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "JX_PRE_LOAN_UPLOAD_FILE_SUCCESS")
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loancreditapply_fail()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 1})
        self.capital_mock.update_loancreditquery(asset_info, code=1, status='FAIL', message='mock预审查询失败')
        check_wait_change_capital_data(item_no, 1, "mock失败测试-null-null-null", "LoanCreditApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhenxing_zhongzhixin_jx_loanpostcredit_fail(self, case, app, source_type, period):
        """
        LoanPostCredit 失败切资方
         增信结果查询失败
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_ftp_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "JX_PRE_LOAN_UPLOAD_FILE_SUCCESS")
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loancreditapply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_loanpostcredit(code=1, status='FAIL', message='mock失败测试')
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "mock失败测试-FAIL", "LoanPostCreditFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhenxing_zhongzhixin_jx_loancreditquery_fail(self, case, app, source_type, period):
        """
        LoanCreditQuery 失败切资方
         增信结果查询失败
        """
        four_element = get_four_element(id_num_begin="26")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_ftp_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "JX_PRE_LOAN_UPLOAD_FILE_SUCCESS")
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loancreditapply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_loanpostcredit()
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loancreditquery(asset_info, code=1, status='FAIL', message='mock预审查询失败')
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "mock预审查询失败-null-null-FAIL", "LoanCreditFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhenxing_zhongzhixin_jx_loanapplyconfirm_fail(self, case, app, source_type, period):
        """
        LoanApplyConfirm 失败切资方
         用信申请失败
        """
        four_element = get_four_element(id_num_begin="26")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_ftp_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "JX_PRE_LOAN_UPLOAD_FILE_SUCCESS")
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loancreditapply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_loanpostcredit()
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loancreditquery(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        check_asset_confirm(item_no, "CONTRACT_VIA_URL", 2)
        # BC 发起确认
        user_change_product_confirm(asset_info, "CONTRACT_VIA_URL", 0)
        check_asset_confirm(item_no, "CONTRACT_VIA_URL", 0)
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 1})
        self.capital_mock.update_loanapplyconfirm(status='FAIL', message='mock 用信失败')
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirmquery(asset_info, status='FAIL', message='mock 放款失败')
        check_wait_change_capital_data(item_no, 0, "mock 用信失败-FAIL-null-null", "ConfirmApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhenxing_zhongzhixin_jx_loanconfirmquery_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery 失败切资方
        用信结果查询失败
        """
        four_element = get_four_element(id_num_begin="26")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_ftp_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "JX_PRE_LOAN_UPLOAD_FILE_SUCCESS")
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loancreditapply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_loanpostcredit()
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loancreditquery(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        check_asset_confirm(item_no, "CONTRACT_VIA_URL", 2)
        # BC 发起确认
        user_change_product_confirm(asset_info, "CONTRACT_VIA_URL", 0)
        check_asset_confirm(item_no, "CONTRACT_VIA_URL", 0)
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 1})
        self.capital_mock.update_loanapplyconfirm()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirmquery(asset_info, status='FAIL', message='mock 放款失败')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "mock 放款失败-FAIL-null-null-nul", "GrantFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_zhenxing_zhongzhixin_jx_comfirmtimeout_fail(self, case, app, source_type, period):
            """
            AssetConfirmOverTimeCheck 超时失败切资方，我方确认超时（BC不管是否超时）
            """
            update_gbiz_capital_zhenxing_zhongzhixin_jx(raise_limit_over_time_seconds=0)
            four_element = get_four_element(id_num_begin="26")
            item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
            self.register(four_element, item_no)
            self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
            self.msg.run_msg(item_no, "AssetImportSync")
            self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
            self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
            prepare_attachment(self.channel, item_no)
            self.capital_mock.update_ftp_upload()
            self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
            check_asset_event_exist(item_no, self.channel, "JX_PRE_LOAN_UPLOAD_FILE_SUCCESS")
            self.capital_mock.update_loanapplynew_success()
            self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
            self.capital_mock.update_loanapplyquery()
            self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
            self.capital_mock.update_loancreditapply()
            self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
            self.capital_mock.update_loanpostcredit()
            self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
            self.capital_mock.update_loancreditquery(asset_info)
            self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
            check_asset_confirm(item_no, "CONTRACT_VIA_URL", 2)
            self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 0})
            check_asset_confirm(item_no, "CONTRACT_VIA_URL", 3)
            check_wait_change_capital_data(item_no, 10005, "确认类型\\[CONTRACT_VIA_URL\\]已超时", "UserConfirmTimeOutEvent")
            # 恢复超时时间配置
            update_gbiz_capital_zhenxing_zhongzhixin_jx()
