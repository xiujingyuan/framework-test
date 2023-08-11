from biztest.function.global_gbiz.gbiz_global_db_function import update_terminated_task
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.beiyin_tianbang import BeiyinTianbangMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_router_capital_plan_amount, \
    update_router_capital_plan_amount_all_to_zero
from biztest.util.easymock.gbiz.payment import PaymentMock
import pytest
from biztest.util.tools.tools import get_four_element


# @pytest.mark.gbiz_auto_test
# @pytest.mark.gbiz_beiyin_tianbang
class TestBeiyinTianbang(BaseTestCapital):
    def init(self):
        super(TestBeiyinTianbang, self).init()
        self.channel = "beiyin_tianbang"
        self.capital_mock = BeiyinTianbangMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_beiyin_tianbang()
        update_gbiz_capital_mozhi_beiyin_const()
        update_gbiz_payment_config(self.payment_mock.url)
        update_gbiz_manual_task_auto_process_config()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.capital_mock.update_accountquery_nodata()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_get_sms_code_success()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='BAOFU_KUAINIU2', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_verify_sms_success()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='BAOFU_KUAINIU2', step_type='PROTOCOL', seq=sms_seq)
        self.capital_mock.update_accountquery_success_only_baofu(asset_info)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

        self.capital_mock.update_get_sms_code_success()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='BEIYIN', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_verify_sms_success()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='BEIYIN', step_type='PROTOCOL', seq=sms_seq)
        self.capital_mock.update_accountquery_success(asset_info)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_user_credit_info_noactive()
        self.capital_mock.update_user_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_credit_apply_result_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_user_credit_info_active()
        self.capital_mock.update_user_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_user_loan_result_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.capital_mock.update_repayPlanquery_success_tianbang(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        # 风控预审加的任务
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.capital_mock.update_contractpush_ftp_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_beiyin_tianbang_loan_success
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 # ("草莓", "apr36", 12),
                                 ("草莓", "irr36_quanyi", 12),
                             ])
    def test_beiyin_tianbang_loan_success(self, case, app, source_type, count):
        """
        放款成功
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 10000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        # check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("count", [12])
    def test_beiyin_tianbang_canloan_fail(self, case, count):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000)
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
        update_router_capital_plan_amount(3333333333, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "beiyin_tianbang->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("count", [6])
    def test_beiyin_tianbang_loan_fail(self, case, count):
        """
        放款失败切资方
        :param case:
        :param count:
        :return:
        """
        self.four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, self.four_element, count, 6000)
        self.register(item_no, self.four_element)

        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # 无进件之前需要的附件，屏蔽掉
        # prepare_attachment(self.channel, item_no)
        self.capital_mock.update_user_credit_info_noactive()
        self.capital_mock.update_user_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_credit_apply_result_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_user_credit_info_active()
        self.capital_mock.update_user_loan_apply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_user_loan_result_fail(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 101002, "REFUSE", "GrantFailedEvent")

    @pytest.mark.parametrize("count", [12])
    def test_beiyin_tianbang_apply_fail(self, case, count):
        """
        老用户授信额度不足进件时切换资金方
        :param case:
        :param count:
        :return:
        """
        self.four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, self.four_element, count, 8000)
        self.register(item_no, self.four_element)

        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # 无进件之前需要的附件，屏蔽掉
        # prepare_attachment(self.channel, item_no)
        self.capital_mock.update_user_credit_info_no_amount()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 998, "可用授信额度不足", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("count", [12])
    def test_beiyin_tianbang_apply_query_fail(self, case, count):
        """
        新用户授信失败切换资金方
        :param case:
        :param count:
        :return:
        """
        self.four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, self.four_element, count, 8000)
        self.register(item_no, self.four_element)

        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # 无进件之前需要的附件，屏蔽掉
        # prepare_attachment(self.channel, item_no)
        self.capital_mock.update_user_credit_info_noactive()
        self.capital_mock.update_user_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_credit_apply_result_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 100101, "拒绝", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("count", [12])
    def test_beiyin_tianbang_applycomfirm_fail(self, case, count):
        """
        老用户额度不足，但是在确认进件时才被发现，此时切换资金方
        :param case:
        :param count:
        :return:
        """
        self.four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, self.four_element, count, 8000)
        self.register(item_no, self.four_element)

        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # 无进件之前需要的附件，屏蔽掉
        # prepare_attachment(self.channel, item_no)
        self.capital_mock.update_user_credit_info_noactive()
        self.capital_mock.update_user_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_credit_apply_result_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_user_credit_info_no_amount()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})

        # 先mock为失败让切换资金方任务得以切走
        self.capital_mock.update_user_loan_result_fail(asset_info)
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 998, "可用授信额度不足", "ConfirmApplySyncFailedEvent")

    @pytest.mark.parametrize("count", [6])
    def test_beiyin_tianbang_apply_refuse_fail(self, case, count):
        """
        曾经授信拒绝的用户，进件失败切换资金方
        :param case:
        :param count:
        :return:
        """
        self.four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, self.four_element, count, 6000)
        self.register(item_no, self.four_element)

        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # 无进件之前需要的附件，屏蔽掉
        # prepare_attachment(self.channel, item_no)
        self.capital_mock.update_user_credit_info_refuse()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})

        # 先修改mock，以便切走
        self.capital_mock.update_user_credit_info_refuse()
        self.capital_mock.update_user_credit_apply_result_no_record()
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 1500000, "额度查询:额度状态\\[REFUSE\\]", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("count", [12])
    def test_beiyin_tianbang_apply_success(self, case, count):
        """
        针对线上出现的异常情况，优化的流程case
        在额度查询时直接返回授信中，会继续调用授信查询接口，若返回无记录则继续调用授信接口
        :param case:
        :param count:
        :return:
        """
        self.four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, self.four_element, count, 8000)
        self.register(item_no, self.four_element)

        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # 无进件之前需要的附件，屏蔽掉
        # prepare_attachment(self.channel, item_no)
        # 若在额度查询时直接返回授信中，会继续调用授信查询接口，若返回无记录则继续调用授信接口，如下mock
        self.capital_mock.update_user_credit_info_auditing()
        self.capital_mock.update_user_credit_apply_result_no_record()
        self.capital_mock.update_user_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_credit_apply_result_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})

    @pytest.mark.parametrize("count", [12])
    def test_beiyin_tianbang_changecapital_success(self, case, count):
        '''
        匹配到ChangeCapital的success策略,成功切资方
        :return:
        '''
        self.four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, self.four_element, count, 8000)
        self.register(item_no, self.four_element)

        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.updare_user_credit_info_loan_refuse_in30day()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_credit_apply_result_no_record()
        check_wait_change_capital_data(item_no, 1010005,
                                       "额度查询:额度状态\\[ACTIVE\\],额度使用状态\\[OTHER_ERR\\],额度使用描述\\[很抱歉，暂时无法提供借款服务。\\]",
                                       "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("count", [12])
    def test_beiyin_tianbang_changecapital_finalfail(self, case, count):
        '''
        匹配到ChangeCapital的finalFail策略，资产作废
        :return:
        '''
        self.four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, self.four_element, count, 8000)
        self.register(item_no, self.four_element)

        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.updare_user_credit_info_loan_refuse_in30day()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_credit_apply_result_no_record()
        update_router_capital_plan_amount_all_to_zero(self.channel)
        update_task_by_item_no_task_type(item_no, "ChangeCapital", task_status="open")
        self.task.run_task(item_no, "ChangeCapital", excepts={"code": 1})
        check_wait_assetvoid_data(item_no, 12, "切资方,路由系统返回空")

    @pytest.mark.parametrize("count", [12])
    def test_beiyin_tianbang_changecapital_fail_auto_rollback_canloan(self, case, count):
        '''
        匹配到ChangeCapital的fail策略，生成新的ChangeCapital任务，通过job执行成功
        :return:
        '''
        self.four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, self.four_element, count, 8000)
        self.register(item_no, self.four_element)

        update_terminated_task(task_status='close')
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.updare_user_credit_info_loan_refuse_in30day()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_credit_info_active()
        check_wait_change_capital_data(item_no, 1010005,
                                       "额度查询:额度状态\\[ACTIVE\\],额度使用状态\\[OTHER_ERR\\],额度使用描述\\[很抱歉，暂时无法提供借款服务。\\]",
                                       "LoanApplySyncFailedEvent")
        time.sleep(3)
        run_job("manualTaskAutoProcessJob",
                {"taskTypeList": ["ChangeCapital"]})
        check_rollback_applycanloan(item_no, self.channel)
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_user_credit_info_noactive()
        self.capital_mock.update_user_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_credit_apply_result_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_user_credit_info_active()
        self.capital_mock.update_user_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_user_loan_result_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.capital_mock.update_repayPlanquery_success_tianbang(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        # 风控预审加的任务
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.capital_mock.update_contractpush_ftp_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)
