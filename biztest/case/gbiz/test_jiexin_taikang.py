from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.jiexin_taikang import JiexinTaikangMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_jiexin_taikang_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, get_four_element_by_item_no, update_all_channel_amount, \
    update_asset_individual_extend_info
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock


# @pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_jiexin_taikang
class TestJiexinTaikang(BaseTestCapital):
    """
       gbiz_jiexin_taikang
       author: zhimengxue
       date: 20220925
       """

    def init(self):
        super(TestJiexinTaikang, self).init()
        self.channel = "jiexin_taikang"
        self.capital_mock = JiexinTaikangMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_jiexin_taikang()
        update_gbiz_capital_jiexin_taikang_const()
        update_all_channel_amount()


    @pytest.fixture()
    def case(self):
        self.init()

    # 后置开户，只是开户流程后置，开户还是用的前置开户的方法
    def register(self, item_no, four_element):
        self.capital_mock.update_newuser_openaccount()
        self.capital_mock.update_newuser_query_insurestatus()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_get_sms_success()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='jiexin_taikang', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_newuser_openaccount()
        self.capital_mock.update_confirm_protocol_success()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='jiexin_taikang', step_type='PROTOCOL', seq=sms_seq)

        self.capital_mock.update_pre_confirm_insure_success()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_get_insureurl_success()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='GetUrl', way='jiexin_taikang', step_type='URL',
                        seq='')
        #check_asset_event_exist(item_no, self.channel, "JXTK_GET_INSURE_URL_SUCCESS")
        self.capital_mock.update_openaccount_success(four_element)
        self.capital_mock.update_query_insurestatus_success(four_element)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        check_asset_event_exist(item_no, self.channel, "JXTK_INSURE_SUSCCESS")


    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        four_element = get_four_element_by_item_no(item_no)
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanpreapply_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "JXTK_SESSION_SUCCESS")
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success()
        # # 新用户开户此处会调用这个接口，如已经开户成功的老用户这里不会调用开户查询接口
        self.capital_mock.update_newuser_openaccount()
        self.capital_mock.update_newuser_query_insurestatus()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "JXTK_CREDIT_SUCCESS")
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        # 后置开户
        self.register(item_no, four_element)
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirmquery_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_queryrepayplan_success(asset_info)
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


    # @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_jiexin_taikang_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12),
                                 # ("草莓", "irr36", 12),
                             ])
    def test_jiexin_taikang_loan_success(self, case, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_jiexin_taikang_conloan_fail(self, case, app, source_type, period):
        """
        canloan fail
        :return:
        """
        four_element = get_four_element(id_num_begin="22")
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
        check_wait_change_capital_data(item_no, 4, "jiexin_taikang->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_jiexin_taikang_Loanpreapply_fail(self, case, app, source_type, period):
        """
        LoanPreApply fail
        :return:
        """
        four_element = get_four_element(id_num_begin="42")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanpreapply_fail()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "success-null-null", "LoanPreApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_jiexin_taikang_loanpreapply_fail_city_code(self, case, app, source_type, period):
        """
        LoanPreApply fail ，因为citycode查询不到
        :return:
        """
        four_element = get_four_element(id_num_begin="42")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanpreapply_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        update_asset_individual_extend_info(item_no)  # 将进件之后的address_district_code修改为不存在的，以便失败
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 为切换资金方任务成功，此处需要mock query
        self.capital_mock.update_loanapplyquery_fail()
        check_wait_change_capital_data(item_no, 9999, "地区code为空 或者 查询不到对应省市", "LoanApplySyncFailedEvent")


    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_jiexin_taikang_applynew_fail(self, case, app, source_type, period):
        """
        LoanApplyNew fail
        :return:
        """
        four_element = get_four_element(id_num_begin="42")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanpreapply_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_fail()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 为切换资金方任务成功，此处需要mock query
        self.capital_mock.update_loanapplyquery_fail()
        check_wait_change_capital_data(item_no, 9999, "mock失败-null-null-null", "LoanApplySyncFailedEvent")


    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_jiexin_taikang_applynewquery_fail_01(self, case, app, source_type, period):
        """
        LoanApplyQuery fail
        :return:
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanpreapply_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "success-FAIL-null-null", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 0, "success-FAIL-null-null", "id_card")

    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_jiexin_taikang_applynewquery_fail_02(self, case, app, source_type, period):
        """
        授信额度不足失败
        :return:
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanpreapply_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success(creditamount='0.00', validto='2036-12-12 00:00:00')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9999, "授信金额小于资产本金", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 9999, "授信金额小于资产本金", "id_card")


    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_jiexin_taikang_applynewquery_fail_03(self, case, app, source_type, period):
        """
        授信额度已过期失败
        :return:
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanpreapply_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success(creditamount='100000', validto='2021-12-12 00:00:00')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9999, "授信额度已过期", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 9999, "授信额度已过期", "id_card")


    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_jiexin_taikang_loanapplyconfirm_fail(self, case, app, source_type, period):
        """
        LoanApplyConfirm fail
        :return:
        """
        four_element = get_four_element(id_num_begin="61")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanpreapply_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success()
        # # 新用户开户此处会调用这个接口，如已经开户成功的老用户这里不会调用开户查询接口
        self.capital_mock.update_newuser_openaccount()
        self.capital_mock.update_newuser_query_insurestatus()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "JXTK_CREDIT_SUCCESS")
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        # 后置开户
        self.register(item_no, four_element)
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_fail()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        # 为切换资金方任务成功，此处需要mock query
        self.capital_mock.update_loanconfirmquery_fail()
        check_wait_change_capital_data(item_no, 0, "success-FAIL-null-null", "ConfirmApplySyncFailedEvent")


    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_jiexin_taikang_loanconfirmquery_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery fail
        :return:
        """
        four_element = get_four_element(id_num_begin="41")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        four_element = get_four_element_by_item_no(item_no)
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanpreapply_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        self.register(item_no, four_element)
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirmquery_fail()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "success-FAIL-mock放款失败-null-null", "GrantFailedEvent")


    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_jiexin_taikang_checkaccount_timeout(self, case, app, source_type, period):
        """
        checkaccount 超时
        :return:
        """
        four_element = get_four_element(id_num_begin="25")
        update_gbiz_capital_jiexin_taikang(account_register_duration_min=0)
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanpreapply_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 1})
        check_wait_change_capital_data(item_no, 1, "开户超时", "CapitalAccountCheckFailEvent")
        update_gbiz_capital_jiexin_taikang()

    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_jiexin_taikang_openaccount_fail(self, case, app, source_type, period):
        """
        openaccount fail
        :return:
        """
        four_element = get_four_element(id_num_begin="27")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanpreapply_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})

        # 以下为开户流程，此处重写为：投保失败
        self.capital_mock.update_newuser_openaccount()
        self.capital_mock.update_newuser_query_insurestatus()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_get_sms_success()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='jiexin_taikang', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_newuser_openaccount()
        self.capital_mock.update_confirm_protocol_success()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='jiexin_taikang', step_type='PROTOCOL', seq=sms_seq)

        self.capital_mock.update_pre_confirm_insure_success()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_get_insureurl_fail()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='GetUrl', way='jiexin_taikang', step_type='URL',
                        seq='')
        self.capital_mock.update_openaccount_success(four_element)
        self.capital_mock.update_query_insurestatus_process()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

        self.task.run_task(item_no, "CheckAccountStatus", excepts={"code": 1})
        check_wait_change_capital_data(item_no, 1, "用户开户失败", "CapitalAccountCheckFailEvent")