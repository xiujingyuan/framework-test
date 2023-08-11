from biztest.interface.gbiz.gbiz_interface import *
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_weipin_hanchen_jf_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_all_channel_amount
import pytest
from biztest.util.easymock.gbiz.weipin_hanchen_jf import WeipinHanchenJfMock
from biztest.util.tools.tools import get_four_element


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_weipin_hanchen_jf
class TestWeipinHanchenJf(BaseTestCapital):

    def init(self):
        super(TestWeipinHanchenJf, self).init()
        self.channel = "weipin_hanchen_jf"
        self.capital_mock = WeipinHanchenJfMock(gbiz_mock)
        update_gbiz_capital_weipin_hanchen_jf()
        update_gbiz_capital_weipin_hanchen_jf_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        ####  jingfa开户
        self.capital_mock.update_bindcard_query_new_user()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_bindcard_query_new_user()
        self.capital_mock.update_bindcard_get_sms_verify()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='jingfa', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_bindcard_query_success()
        self.capital_mock.update_bindcard_confirm()
        self.capital_mock.update_bindcard_query_old_user_success()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='jingfa', step_type='PROTOCOL', seq=sms_seq)
        #### wipin开户
        self.capital_mock.update_bindcard_query_new_user()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_bindcard_query_new_user()
        self.capital_mock.update_bindcard_get_sms_verify()
        sms_seq2 = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='weipin', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_bindcard_query_success()
        self.capital_mock.update_bindcard_confirm()
        self.capital_mock.update_bindcard_query_old_user_success()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='weipin', step_type='PROTOCOL', seq=sms_seq2)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "WP_HC_JF_LOAN_PRE_SUCCESS")
        self.capital_mock.update_quota_query()
        self.capital_mock.update_creditapply_status()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditresult_query()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "WP_HC_JF_LOAN_POST_SUCCESS")
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanresult_query(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.upate_repayplan_query(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=0)
        # self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_weipin_hanchen_jf_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [("香蕉", "apr36", 12),
                              # ("草莓", "irr36", 12),
                              ])
    def test_weipin_hanchen_jf_loan_success(self, case, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element(bank_name='建设银行', id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, period, 12000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        # check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_weipin_hanchen_jf_canloan_fail(self, case, app, source_type, period):
        """
        canloan失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="52")
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
        check_wait_change_capital_data(item_no, 4, "weipin_hanchen_jf->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_weipin_hanchen_jf_apply_fail(self, case, app, source_type, period):
        """
        LoanApplyNew 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="53")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_quota_query()
        self.capital_mock.update_creditapply_status(creditStatus='03', message='mock请求失败')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditresult_query(startDate='20221021', endDate='20291231', quota=2000000,
                                                    creditStatus='03',  message='mock请求失败')
        check_wait_change_capital_data(item_no, 1000000, "03-mock请求失败", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_weipin_hanchen_jf_apply_fail_01(self, case, app, source_type, period):
        """
        LoanApplyNew 失败切资方,因为授信额度不足
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="53")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_quota_query_old_user(availableQuota=100, endDate='20500522')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditresult_query(startDate='20221021', endDate='20291231', quota=2000000,
                                                    creditStatus='03',  message='mock请求失败')
        check_wait_change_capital_data(item_no, 9999, "授信可用余额小于资产本金", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_weipin_hanchen_jf_apply_fail_02(self, case, app, source_type, period):
        """
        LoanApplyNew 失败切资方,因为授信时间过期了
        """
        four_element = get_four_element(id_num_begin="53")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_quota_query_old_user(availableQuota=1000000, endDate='20230528')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditresult_query(startDate='20221021', endDate='20291231', quota=2000000,
                                                        creditStatus='03', message='mock请求失败')
        check_wait_change_capital_data(item_no, 9999, "授信额度已过期", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_weipin_hanchen_jf_applyquery_fail_01(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="21")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_quota_query()
        self.capital_mock.update_creditapply_status()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditresult_query(startDate='20221021', endDate='20291231', quota=2000000,
                                                    creditStatus='03', message='mock请求失败')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1000000, "03-mock请求失败", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 1000000, "03-mock请求失败", "id_card")


    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_weipin_hanchen_jf_applyquery_fail_02(self, case, app, source_type, period):
        """
        授信额度不足，失败切换资金方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="41")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_quota_query()
        self.capital_mock.update_creditapply_status()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditresult_query(startDate='20221021', endDate='20291231', quota=100,
                                                    creditStatus='02',
                                                    message='请求成功')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9999, "授信金额小于资产本金", "LoanApplyAsyncFailedEvent")


    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_weipin_hanchen_jf_applyquery_fail_03(self, case, app, source_type, period):
        """
        授信已过期，失败切换资金方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="55")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_quota_query()
        self.capital_mock.update_creditapply_status()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditresult_query(startDate='20221021', endDate='20220101', quota=2000000,
                                                    creditStatus='02', message='请求成功')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9999, "授信额度已过期", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_weipin_hanchen_jf_confirm_fail(self, case, app, source_type, period):
        """
        LoanApplyConfirm 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="32")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_quota_query()
        self.capital_mock.update_creditapply_status()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditresult_query()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_fail()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanresult_query(asset_info, loanstatus='03', rejectcode='00006', remark='用信审批不通过')
        check_wait_change_capital_data(item_no, 2000000, "03-审批拒绝", "ConfirmApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_weipin_hanchen_jf_confirmquery_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="33")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_quota_query()
        self.capital_mock.update_creditapply_status()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditresult_query()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanresult_query(asset_info, loanstatus='03', rejectcode='00007', remark='资方审批不通过')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2000000, "03-00007-资方审批不通过-请求成功",  "GrantFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 2000000, "03-00007-资方审批不通过-请求成功", "id_card")

