from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.zhongyuan_zunhao import ZhongYuanZunHaoMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_zhongyuan_zunhao_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, get_four_element_by_item_no, update_all_channel_amount
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock


class TestZhongyuanZunhao(BaseTestCapital):
    """
       gbiz_zhongyuan_zunhao
       author: zhimengxue
       date: 20220615
       """

    def init(self):
        super(TestZhongyuanZunhao, self).init()
        self.channel = "zhongyuan_zunhao"
        self.capital_mock = ZhongYuanZunHaoMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_zhongyuan_zunhao()
        update_gbiz_capital_zhongyuan_zunhao_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()

    # 后置开户，只是开户流程后置，开户还是用的前置开户的方法
    def register(self, item_no, four_element):
        self.capital_mock.update_query_bind_card_new_user()
        self.capital_mock.update_pre_bind_card()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_query_bind_card(four_element)
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='zhongyuan_zunhao', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_bind_card()
        self.capital_mock.update_query_bind_card_after_openaccount(four_element)
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='zhongyuan_zunhao', step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        four_element = get_four_element_by_item_no(item_no)
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success(asset_info)
        # 新用户开户此处会调用这个接口，如已经开户成功的老用户，这里不会调用开户查询接口
        self.capital_mock.update_query_bind_card_new_user()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        # 后置开户
        self.register(item_no, four_element)
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 0})
        self.capital_mock.update_querylpr_success()
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirmquery_success(asset_info, item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_queryrepayplan_success(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        # 从ftp下载资金方的zip，然后解压，上传到我方的ftp上
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.capital_mock.update_contractpush_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        self.msg.run_msg_by_order_no(item_no)
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        # ContractDown成功之后会生成以下任务，推送担保方文件，因为ContractDown很难成功，所以根本不会生成这两个任务
        # self.task.run_task(item_no, "GuaranteeUpload")
        # self.task.run_task(item_no, "GuaranteeApply")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_zhongyuan_zunhao
    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_zhongyuan_zunhao_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12),
                                 # ("草莓", "irr36", 12),
                             ])
    def test_zhongyuan_zunhao_loan_success(self, case, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 13000, app, source_type)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_zhongyuan_zunhao
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_zhongyuan_zunhao_conloan_fail(self, case, app, source_type, period):
        """
        canloan fail
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
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
        check_wait_change_capital_data(item_no, 4, "zhongyuan_zunhao->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_zhongyuan_zunhao
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_zhongyuan_zunhao_applynew_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery fail
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_fail()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_fail(asset_info)
        check_wait_change_capital_data(item_no, 10, "成功_N_ZYZR,9999_暂不符合授信政策，感谢您的关注。;不符合授信标准！",
                                       "LoanApplySyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 10, "成功_N_ZYZR,9999_暂不符合授信政策，感谢您的关注。;不符合授信标准！", "id_card")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_zhongyuan_zunhao
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_zhongyuan_zunhao_applyquery_fail(self, case, app, source_type, period):
        """
        LoanApplyQuery fail
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_fail(asset_info)
        self.capital_mock.update_query_bind_card_new_user()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10, "成功_99_02_mock拒绝码_mock拒绝原因", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 10, "成功_99_02_mock拒绝码_mock拒绝原因", "id_card")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_zhongyuan_zunhao
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_zhongyuan_zunhao_applyquery_fail_02(self, case, app, source_type, period):
        """
        LoanApplyQuery fail，线上异常情况，具体可见update_loanapplyquery_fail_02 mock中详解
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_fail_02()
        self.capital_mock.update_query_bind_card_new_user()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 20, "成功_返回业务data为空", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 20, "成功_返回业务data为空", "id_card")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_zhongyuan_zunhao
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_zhongyuan_zunhao_checkaccount_fail(self, case, app, source_type, period):
        """
        checkaccount fail
        :return:
        """
        four_element = get_four_element()
        update_gbiz_capital_zhongyuan_zunhao(account_register_duration_min=0)
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success(asset_info)
        self.capital_mock.update_query_bind_card_new_user()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 1})
        check_wait_change_capital_data(item_no, 1, "开户超时", "CapitalAccountCheckFailEvent")
        update_gbiz_capital_zhongyuan_zunhao()

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_zhongyuan_zunhao1
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_zhongyuan_zunhao_applyconform_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery fail
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
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
        self.capital_mock.update_querylpr_success()
        self.capital_mock.update_loanapplyconfirm_fail()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirmquery_fail(asset_info, item_no)
        check_wait_change_capital_data(item_no, 21, "mock失败",
                                       "ConfirmApplySyncFailedEvent")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_zhongyuan_zunhao
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_zhongyuan_zunhao_confirmquery_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery fail
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
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
        self.capital_mock.update_querylpr_success()
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirmquery_fail(asset_info, item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 20, "成功_99_02_mock拒绝码_mock拒绝原因", "GrantFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 20, "成功_99_02_mock拒绝码_mock拒绝原因", "id_card")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_zhongyuan_zunhao
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_zhongyuan_zunhao_checkaccount_timeout(self, case, app, source_type, period):
        """
        开户检查时资方接口报错
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success(asset_info)
        self.capital_mock.update_query_bind_card_new_user()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        self.capital_mock.update_query_bind_card_timeout()
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 2})
        self.register(item_no, four_element)
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 0})
        self.capital_mock.update_querylpr_success()
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirmquery_success(asset_info, item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_queryrepayplan_success(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.capital_mock.update_contractpush_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

