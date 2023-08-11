import pytest

from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.config.gbiz.gbiz_lanhai_zhilian_config import *
from biztest.function.gbiz.gbiz_check_function import *
from biztest.function.gbiz.gbiz_db_function import get_four_element_by_item_no, update_all_channel_amount
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.lanhai_zhilian import LanhaiZhilianMock
from biztest.util.tools.tools import get_four_element


class TestLanhaiZhilian(BaseTestCapital):

    def init(self):
        super(TestLanhaiZhilian, self).init()
        self.channel = "lanhai_zhilian"
        self.capital_mock = LanhaiZhilianMock(gbiz_mock)
        update_gbiz_capital_lanhai_zhilian()
        update_gbiz_capital_lanhai_zhilian_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()

    # 后置开户
    def register(self, item_no, four_element):
        self.capital_mock.update_query_bind_card_new_user()
        capital_regiest_query(self.channel, four_element, item_no)
        self.capital_mock.update_sms_send_success()
        sms_seq = capital_regiest(self.channel, four_element, item_no, action_type='GetSmsVerifyCode',
                                  way='lanhai_zhilian', step_type='PROTOCOL', seq='')['data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_sms_check_success()
        capital_regiest(self.channel, four_element, item_no, action_type='CheckSmsVerifyCode',
                        way='lanhai_zhilian', step_type='PROTOCOL', seq=sms_seq)
        self.capital_mock.update_query_bind_card_success()
        capital_regiest_query(self.channel, four_element, item_no)

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        four_element = get_four_element_by_item_no(item_no)
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        # 后置开户
        self.register(item_no, four_element)
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 0})
        self.capital_mock.update_loanacreditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirmquery_success(asset_info, item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_queryrepayplan_success(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        self.msg.run_msg_by_order_no(item_no)
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanhai_zhilian
    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_lanhai_zhilian_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_lanhai_zhilian_loan_success(self, case, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanhai_zhilian
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_lanhai_zhilian_applyquery_fail(self, case, app, source_type, period):
        """
        授信被拒
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 20000, "true_响应成功_3_0_null_授信总金额为空或授信金额小于借款金额", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 20000, "true_响应成功_3_0_null_授信总金额为空或授信金额小于借款金额", "id_card")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanhai_zhilian
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_lanhai_zhilian_applyquery_fail_02(self, case, app, source_type, period):
        """
        额度不足
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_fail_02()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 20000, "true_响应成功_2_1_null_授信可用金额为空或授信金额小于借款金额", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 20000, "true_响应成功_2_1_null_授信可用金额为空或授信金额小于借款金额", "id_card")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanhai_zhilian
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_lanhai_zhilian_checkaccount_fail(self, case, app, source_type, period):
        """
        开户超时
        """
        four_element = get_four_element()
        update_gbiz_capital_lanhai_zhilian(account_register_duration_min=0)
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 1})
        check_wait_change_capital_data(item_no, 1, "开户超时", "CapitalAccountCheckFailEvent")
        update_gbiz_capital_lanhai_zhilian()

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanhai_zhilian
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_lanhai_zhilian_confirmquery_fail(self, case, app, source_type, period):
        """
        放款失败
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success(asset_info)
        self.capital_mock.update_query_bind_card_new_user()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        self.register(item_no, four_element)
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 0})
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirmquery_fail(asset_info, item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 30000, "true_响应成功_21_对方行应答RJ01应答信息账号不存在", "GrantFailedEvent")
