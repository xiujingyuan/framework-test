from biztest.function.gbiz.gbiz_db_function import update_router_capital_plan_amount, update_all_channel_amount
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.shanxixintuo import ShanxiXintuoMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest
from biztest.util.tools.tools import get_four_element


class TestShanxiXintuo(BaseTestCapital):

    def setup_class(self):
        self.channel = "shanxixintuo"
        self.sxxt_mock = ShanxiXintuoMock(gbiz_mock)

    def setup(self):
        super(TestShanxiXintuo, self).init()
        update_gbiz_capital_shanxixintuo_const()
        update_gbiz_capital_shanxixintuo()
        update_all_channel_amount()

    def teardown(self):
        update_gbiz_capital_shanxixintuo()
        update_all_channel_amount()

    def register(self, item_no, four_element):
        self.sxxt_mock.update_signconfirmquery()
        self.sxxt_mock.update_signapply()
        self.sxxt_mock.update_signconfirm()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='shanxixintuo', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='shanxixintuo', step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        get_asset_loan_record_by_item_no(item_no)
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.sxxt_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.sxxt_mock.update_creditapply(asset_info)
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.sxxt_mock.update_creditquery(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.sxxt_mock.update_trustplanquery_success()
        self.sxxt_mock.update_loanprecheck(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.sxxt_mock.update_precheckquery(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.sxxt_mock.update_upload_zip(item_no)
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "OTP_INTERACTION")
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        # 合同签约相关操作
        self.sxxt_mock.update_loancontractsign(item_no)
        userloan_confirm(asset_info, action="OTP_INTERACTION", sub_action='SendSmsCode')
        check_confirm_data(item_no, self.channel, 4, "OTP_INTERACTION")
        self.sxxt_mock.update_contractsignconfirm(item_no)
        userloan_confirm(asset_info, action="OTP_INTERACTION", sub_action='ConfirmSmsCode')
        check_confirm_data(item_no, self.channel, 0, "OTP_INTERACTION")

        self.sxxt_mock.update_loanconfirm(item_no)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.sxxt_mock.update_loanconfirmquery(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.sxxt_mock.update_queryplan(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shanxixintuo
    @pytest.mark.gbiz_shanxixintuo_loan_success
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 6),
                                 ("草莓", "apr36", 12),
                                 ("香蕉", "irr36_quanyi", 6),
                                 ("草莓", "irr36_quanyi", 12)
                             ])
    def test_shanxixintuo_loan_success(self, app, source_type, count):
        """
        放款成功
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type, '')

        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # check_request_log_by_channel(item_no, self.channel)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shanxixintuo
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 6),
                                 ("草莓", "irr36_quanyi", 12),
                             ])
    def test_shanxixintuo_canloan_fail(self, app, source_type, count):
        '''
        canloan失败切资方
        :return:
        '''
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        today = time.strftime("%Y-%m-%d", time.localtime())
        update_router_capital_plan_amount(0, today, self.channel)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        time.sleep(2)
        # canloan执行之后恢复
        update_router_capital_plan_amount(3333333333, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "shanxixintuo->校验资金量失败;", "AssetCanLoanFailedEvent")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shanxixintuo
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 6),
                                 ("草莓", "irr36_quanyi", 12),
                             ])
    def test_shanxixintuo_creditapply_fail(self, app, source_type, count):
        '''
        LoanCreditApply,授信申请失败切资方
        :return:
        '''
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.sxxt_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.sxxt_mock.update_creditapply(asset_info, status="01", message="mock失败")
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 1})
        self.sxxt_mock.update_creditquery(asset_info, status="01", message="mock失败")

        check_wait_change_capital_data(item_no, 1001, "mock失败", "LoanCreditApplySyncFailedEvent")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shanxixintuo
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 6),
                                 ("草莓", "irr36_quanyi", 12),
                             ])
    def test_shanxixintuo_creditquery_fail(self, app, source_type, count):
        '''
        LoanCreditQuery，授信查询失败切资方
        :return:
        '''
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.sxxt_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.sxxt_mock.update_creditapply(asset_info)
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.sxxt_mock.update_creditquery(asset_info, status="01", message="mock失败")
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10015, "mock失败", "LoanCreditFailedEvent")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shanxixintuo
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 6),
                                 ("草莓", "irr36_quanyi", 12),
                             ])
    def test_shanxixintuo_creditquery_noorder(self, app, source_type, count):
        '''
        LoanCreditQuery，授信查询订单不存在
        :return:
        '''
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.sxxt_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.sxxt_mock.update_creditapply(asset_info)
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.sxxt_mock.update_creditquery_noorder()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 100522, "\\[00400\\]流水不存在", "LoanCreditFailedEvent")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shanxixintuo
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 6),
                                 ("草莓", "irr36_quanyi", 12),
                             ])
    def test_shanxixintuo_applynew_fail(self, app, source_type, count):
        '''
        LoanApplyNew，放款预审申请失败切资方
        :return:
        '''
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.sxxt_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.sxxt_mock.update_creditapply(asset_info)
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.sxxt_mock.update_creditquery(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.sxxt_mock.update_trustplanquery_success()
        self.sxxt_mock.update_loanprecheck(asset_info, status='01', message="mock失败")
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.sxxt_mock.update_precheckquery(item_no, status='01', message="mock失败")
        check_wait_change_capital_data(item_no, 2001, "mock失败", "LoanApplySyncFailedEvent")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shanxixintuo
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12)
                             ])
    def test_shanxixintuo_applyquery_fail(self, app, source_type, count):
        '''
        LoanApplyQuery，放款预审查询失败切资方
        :return:
        '''
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # prepare_attachment(self.channel, item_no)
        self.sxxt_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.sxxt_mock.update_creditapply(asset_info)
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.sxxt_mock.update_trustplanquery_success()
        self.sxxt_mock.update_loanprecheck(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.sxxt_mock.update_precheckquery(item_no, status="01", message="mock失败")
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2001, "mock失败", "LoanApplyAsyncFailedEvent")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shanxixintuo
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12)
                             ])
    def test_shanxixintuo_applyconfirm_fail(self, app, source_type, count):
        '''
        LoanApplyConfirm，放款申请失败切资方
        :return:
        '''
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.sxxt_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.sxxt_mock.update_creditapply(asset_info)
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.sxxt_mock.update_creditquery(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.sxxt_mock.update_trustplanquery_success()
        self.sxxt_mock.update_loanprecheck(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.sxxt_mock.update_precheckquery(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.sxxt_mock.update_upload_zip(item_no)
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "OTP_INTERACTION")
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        self.sxxt_mock.update_loancontractsign(item_no)
        userloan_confirm(asset_info, action="OTP_INTERACTION", sub_action='SendSmsCode')
        check_confirm_data(item_no, self.channel, 4, "OTP_INTERACTION")
        self.sxxt_mock.update_contractsignconfirm(item_no)
        userloan_confirm(asset_info, action="OTP_INTERACTION", sub_action='ConfirmSmsCode')
        check_confirm_data(item_no, self.channel, 0, "OTP_INTERACTION")
        self.sxxt_mock.update_loanconfirm(item_no, status="01", message="mock放款申请失败")
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.sxxt_mock.update_loanconfirmquery(item_no, status="05", message="流水不存在")
        check_wait_change_capital_data(item_no, 3001, "mock放款申请失败", "ConfirmApplySyncFailedEvent")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shanxixintuo
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12)
                             ])
    def test_shanxixintuo_confirmquery_fail(self, app, source_type, count):
        '''
        LoanConfirmQuery，放款查询失败切资方
        :return:
        '''
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.sxxt_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.sxxt_mock.update_creditapply(asset_info)
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.sxxt_mock.update_creditquery(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.sxxt_mock.update_trustplanquery_success()
        self.sxxt_mock.update_loanprecheck(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.sxxt_mock.update_precheckquery(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.sxxt_mock.update_upload_zip(item_no)
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "OTP_INTERACTION")
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        self.sxxt_mock.update_loancontractsign(item_no)
        userloan_confirm(asset_info, action="OTP_INTERACTION", sub_action='SendSmsCode')
        check_confirm_data(item_no, self.channel, 4, "OTP_INTERACTION")
        self.sxxt_mock.update_contractsignconfirm(item_no)
        userloan_confirm(asset_info, action="OTP_INTERACTION", sub_action='ConfirmSmsCode')
        check_confirm_data(item_no, self.channel, 0, "OTP_INTERACTION")
        self.sxxt_mock.update_loanconfirm(item_no)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.sxxt_mock.update_loanconfirmquery(item_no, status="01", message="放款失败")
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 3001, "放款失败", "GrantFailedEvent")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shanxixintuo
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12)
                             ])
    def test_shanxixintuo_contractsign_fail(self, app, source_type, count):
        '''
        ContractSign，合同签约申请失败切资方(status=05订单不存在)
        :return:
        '''
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.sxxt_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.sxxt_mock.update_creditapply(asset_info)
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.sxxt_mock.update_creditquery(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.sxxt_mock.update_trustplanquery_success()
        self.sxxt_mock.update_loanprecheck(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.sxxt_mock.update_precheckquery(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.sxxt_mock.update_upload_zip(item_no)
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "OTP_INTERACTION")
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        # 合同签约相关操作
        self.sxxt_mock.update_loancontractsign(item_no, status="05", message="mock签约订单不存在")
        userloan_confirm(asset_info, action="OTP_INTERACTION", sub_action='SendSmsCode')
        check_confirm_data(item_no, self.channel, 1, "OTP_INTERACTION")
        self.sxxt_mock.update_loanconfirmquery(item_no,status="05", message="流水不存在")
        check_wait_change_capital_data(item_no, 1, "mock签约订单不存在", "UserConfirmFailedEvent")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shanxixintuo
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12)
                             ])
    def test_shanxixintuo_signconfirm_fail(self, app, source_type, count):
        '''
        SignConfirm，合同签约确认失败切资方(status=05订单不存在)
        :return:
        '''
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.sxxt_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.sxxt_mock.update_creditapply(asset_info)
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.sxxt_mock.update_creditquery(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.sxxt_mock.update_trustplanquery_success()
        self.sxxt_mock.update_loanprecheck(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.sxxt_mock.update_precheckquery(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.sxxt_mock.update_upload_zip(item_no)
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "OTP_INTERACTION")
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        # 合同签约相关操作
        self.sxxt_mock.update_loancontractsign(item_no)
        userloan_confirm(asset_info, action="OTP_INTERACTION", sub_action='SendSmsCode')
        check_confirm_data(item_no, self.channel, 4, "OTP_INTERACTION")
        self.sxxt_mock.update_contractsignconfirm(item_no,status="05", message="mock签约订单不存在")
        userloan_confirm(asset_info, action="OTP_INTERACTION", sub_action='ConfirmSmsCode')
        check_confirm_data(item_no, self.channel, 1, "OTP_INTERACTION")
        self.sxxt_mock.update_loanconfirmquery(item_no, status="05", message="流水不存在")
        check_wait_change_capital_data(item_no, 1, "mock签约订单不存在", "UserConfirmFailedEvent")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_shanxixintuo
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12)
                             ])
    def test_shanxixintuo_signcontract_timeout(self, app, source_type, count):
        '''
        合同签约超时,切资方
        :return:
        '''
        # 设置超时时间
        update_gbiz_capital_shanxixintuo(timeout=0)
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.sxxt_mock.update_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.sxxt_mock.update_creditapply(asset_info)
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.sxxt_mock.update_creditquery(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.sxxt_mock.update_trustplanquery_success()
        self.sxxt_mock.update_loanprecheck(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.sxxt_mock.update_precheckquery(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.sxxt_mock.update_upload_zip(item_no)
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "OTP_INTERACTION")
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 3, "OTP_INTERACTION")
        check_wait_change_capital_data(item_no, 10005, "签署借款合同超时", "UserConfirmTimeOutEvent")

