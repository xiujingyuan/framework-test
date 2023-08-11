from biztest.interface.gbiz.gbiz_interface import *
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_lanhai_zhongbao_rl_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_all_channel_amount, get_four_element_by_item_no
import pytest
from biztest.util.easymock.gbiz.lanhai_zhongbao_rl import LanhaiZhongbaoRlMock
from biztest.util.tools.tools import get_four_element

@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_lanhai_zhongbao_rl
class TestLanhaiZhongbaoRl(BaseTestCapital):

    def init(self):
        super(TestLanhaiZhongbaoRl, self).init()
        self.channel = "lanhai_zhongbao_rl"
        self.capital_mock = LanhaiZhongbaoRlMock(gbiz_mock)
        update_gbiz_capital_lanhai_zhongbao_rl()
        update_gbiz_capital_lanhai_zhongbao_rl_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element, action_type=None, smscode=None, sms_seq=None):
        if action_type == 'GetSmsVerifyCode' or action_type is None:
            capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
            self.capital_mock.bind_card_sign()
            sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                      action_type='GetSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq='')[
                'data']['actions'][0]['extra_data']['seq']

        if action_type == 'CheckSmsVerifyCode' or action_type is None:
            self.capital_mock.bind_card_sign_check()
            sms = smscode if smscode else '123456'
            capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                            action_type='CheckSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq=sms_seq,
                            code=sms)
            capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        four_element = get_four_element_by_item_no(item_no)
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # self.capital_mock.update_file_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LHZBRL_CREDIT_FILE_ID_LIST")
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LHZBRL_IP_RANDOM")
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        # 后置开户
        self.register(item_no, four_element)
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 0})
        # self.capital_mock.update_agree_share_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LHZBRL_LOAN_FILE_ID_LIST")
        self.capital_mock.update_disbursement_apply(item_no)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_disbursement_query(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayment_plan_query(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=0)
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        # 合同下载会调用3个接口，前面的查询接口是之前调用过的，此处重复调用为了查询到合同，然后下载，但是base64太长不好mock，此处屏蔽
        # self.capital_mock.update_credit_query(item_no)
        # self.capital_mock.update_disbursement_query(item_no)
        # self.capital_mock.update_file_download()
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        # # 合同下载任务执行成功之后会同时生成以下两个任务，上传影像文件到担保方的sftp去，因为合同下载被屏蔽了，所以这两个任务只能屏蔽
        # self.task.run_task(item_no, "GuaranteeUpload", excepts={"code": 0})
        # self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_lanhai_zhongbao_rl_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [
                              ("香蕉", "apr36", 12),
                              # ("草莓", "irr36", 12),
                              ])
    def test_lanhai_zhongbao_rl_loan_success(self, case, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 5000, app, source_type)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_lanhai_zhongbao_rl_canloan_fail(self, case, app, source_type, period):
        """
        canloan失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="16")
        item_no, asset_info = asset_import(self.channel, four_element, period, 5000, app, source_type)
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
        check_wait_change_capital_data(item_no, 4, "lanhai_zhongbao_rl->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_lanhai_zhongbao_rl_apply_fail(self, case, app, source_type, period):
        """
        LoanApplyNew 失败（授信申请失败）切资方
        """
        four_element = get_four_element(id_num_begin="15")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # self.capital_mock.update_file_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LHZBRL_CREDIT_FILE_ID_LIST")
        self.capital_mock.update_credit_apply(item_no, status='F')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query_notorder()
        check_wait_change_capital_data(item_no, 1, "0_Success_F", "LoanApplySyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 1, "0_Success_F", "id_card")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_lanhai_zhongbao_rl_applyquery_fail(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败(授信查询拒绝失败)切资方
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, status='F')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "0_Success_F_null", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 1, "0_Success_F_null", "id_card")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_lanhai_zhongbao_rl_applyquery_not_balance(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败
        授信额度不足，失败切换资金方
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, availableAmount=0)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "0_Success_S_null_剩余授信额度小于借款本金", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 1, "0_Success_S_null_剩余授信额度小于借款本金", "id_card")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_lanhai_zhongbao_rl_applyquery_overdue(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败
        授信过期，切换资金方
        """
        four_element = get_four_element(id_num_begin="24")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, creditEndDate='2022-12-12')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "0_Success_S_null_当前日期不在授信有效期内", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 1, "0_Success_S_null_当前日期不在授信有效期内", "id_card")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_lanhai_zhongbao_rl_confirm_fail(self, case, app, source_type, period):
        """
        LoanApplyConfirm 失败切资方
        用信失败
        """
        four_element = get_four_element(id_num_begin="31")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
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
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        # 后置开户
        self.register(item_no, four_element)
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LHZBRL_LOAN_FILE_ID_LIST")
        self.capital_mock.update_disbursement_apply(item_no, status='F')
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_disbursement_query(item_no, status='F')
        check_wait_change_capital_data(item_no, 2, "0_Success_F", "ConfirmApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_lanhai_zhongbao_rl_confirmquery_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery 失败切资方
        用信失败
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        four_element = get_four_element_by_item_no(item_no)
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # self.capital_mock.update_file_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LHZBRL_CREDIT_FILE_ID_LIST")
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LHZBRL_IP_RANDOM")
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        # 后置开户
        self.register(item_no, four_element)
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 0})
        # self.capital_mock.update_agree_share_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LHZBRL_LOAN_FILE_ID_LIST")
        self.capital_mock.update_disbursement_apply(item_no)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_disbursement_query(item_no, status='F')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2, "0_Success_F", "GrantFailedEvent")


