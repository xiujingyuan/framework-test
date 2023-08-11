from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.jinmeixin_daqin import JinmeixinDaqinMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.gbiz.gbiz_jinmeixin_daqin_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_router_capital_plan_amount,\
    update_all_channel_amount
import pytest
from biztest.util.tools.tools import get_four_element


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_jinmeixin_daqin
class TestJinmeixinDaqin(BaseTestCapital):
    def init(self):
        super(TestJinmeixinDaqin, self).init()
        self.channel = "jinmeixin_daqin"
        self.capital_mock = JinmeixinDaqinMock(gbiz_mock)
        update_gbiz_capital_jinmeixin_daqin()
        update_gbiz_capital_jinmeixin_daqin_const()
        update_all_channel_amount()
        update_gbiz_base_config()
        
    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, four_element, item_no):
        self.capital_mock.update_bindCard_ceck()
        self.capital_mock.update_bindCard_verify()
        self.capital_mock.update_bindCard_confirm()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_user_infoPush()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_infoPushQuery()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loan_trial()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_loan_request(item_no)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_results_query(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.upate_repayplan_query(asset_info, item_no)
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.capital_mock.updat_contract_query()
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        # self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        # self.task.run_task(item_no, "GuaranteeUpload", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_jinmeixin_daqin_loan_success
    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_jinmeixin_daqin_loan_success(self, case, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_jinmeixin_daqin_canloan_fail(self, case, app, source_type, period):
        """
        canloan失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
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
        check_wait_change_capital_data(item_no, 4, "jinmeixin_daqin->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_jinmeixin_daqin_apply_fail(self, case, app, source_type, period):
        """
        LoanApplyNew 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_user_infoPush(code='999999', msg='mock_资料推送同步失败')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_infoPushQuery(code='00067', msg='流水号不存在')
        check_wait_change_capital_data(item_no, 1999999, "mock_资料推送同步失败", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_jinmeixin_daqin_applequery_fail(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_user_infoPush()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_infoPushQuery(handleStatus="FAIL", failMsg="mock_资料推送查询失败")
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1000000, "成功-FAIL-mock_资料推送查询失败", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_jinmeixin_daqin_creditapply_fail(self, case, app, source_type, period):
        """
        LoanCreditApply 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_user_infoPush()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_infoPushQuery()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loan_trial(code='999999', msg='mock_试算失败')
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 1})
        check_wait_change_capital_data(item_no, 2999999, "mock_试算失败", "LoanCreditApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_jinmeixin_daqin_confirm_fail(self, case, app, source_type, period):
        """
        LoanApplyConfirm 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_user_infoPush()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_infoPushQuery()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loan_trial()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_loan_request(item_no, code='999999', msg='mock_放款申请失败')
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_results_query(item_no, code='000067', msg='流水号不存在')
        check_wait_change_capital_data(item_no, 3999999, "mock_放款申请失败", "ConfirmApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_jinmeixin_daqin_confirmquery_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_user_infoPush()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_user_infoPushQuery()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loan_trial()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_loan_request(item_no)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_results_query(item_no, applyStatus='LOAN_FAILURE', applyResult='mock_放款失败')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 3000000, "成功-LOAN_FAIL", "GrantFailedEvent")
