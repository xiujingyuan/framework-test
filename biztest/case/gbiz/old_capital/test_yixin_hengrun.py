from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.yixin_hengrun import YiXinHengRunMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_all_channel_amount
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock


class TestYixinHengrun(BaseTestCapital):
    """
       gbiz_yixin_hengrun
       author: zhimengxue
       date: 20220710
       """

    def init(self):
        super(TestYixinHengrun, self).init()
        self.channel = "yixin_hengrun"
        self.capital_mock = YiXinHengRunMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_yixin_hengrun()
        update_gbiz_capital_yixin_hengrun_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.capital_mock.update_query_bankcard_new_user()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_account_get_msg_code_success(four_element)
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='yixin_hengrun', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_account_bind_verify(four_element)
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='yixin_hengrun', step_type='PROTOCOL', seq=sms_seq)
        self.capital_mock.update_query_bankcard_success(four_element)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 此时会生成 AssetConfirmOverTimeCheck但此时不可执行
        # self.task.run_task(item_no, "AssetConfirmOverTimeCheck")
        # 检查asset_confirm记录"2-处理中"
        check_asset_confirm(item_no, "LOAN_PRODUCT_CHANGE", 2)
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        user_change_product_confirm(asset_info, "LOAN_PRODUCT_CHANGE", 0)
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 1})
        self.msg.run_msg(item_no, "AssetApplyTrailSuccess")
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirmquery_success()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayplan_success(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        # self.capital_mock.update_contractpush_success()
        # self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_yixin_hengrun
    # @pytest.mark.gbiz_loan_success
    # @pytest.mark.gbiz_yixin_hengrun_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12),
                                 ("草莓", "irr36", 12),
                                 # ("火龙果", "real36", 12),
                                 # ("火龙果", "real36", 6),
                             ])
    def test_yixin_hengrun_loan_success(self, case, app, source_type, period):
        """
        放款成功，该资金方涉及产品线变更，实际上该资金方只放6期的！！！12期费率编号实际是假的只是为了路由进件，资金方不支持放款12期
        """
        four_element = get_four_element(id_num_begin="31")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_yixin_hengrun
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_yixin_hengrun_conloan_fail(self, case, app, source_type, period):
        """
        canloan fail
        :return:
        """
        four_element = get_four_element(id_num_begin="42")
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
        check_wait_change_capital_data(item_no, 4, "yixin_hengrun->校验资金量失败;", "AssetCanLoanFailedEvent")


    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_yixin_hengrun
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_yixin_hengrun_loanapplynew_fail(self, case, app, source_type, period):
        """
        进件同步失败
        :return:
        """
        four_element = get_four_element(id_num_begin="63")
        item_no, asset_info = asset_import(self.channel, four_element, period, 5000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_fail()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "mock失败--1-mock的", 'LoanApplySyncFailedEvent')

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_yixin_hengrun
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("草莓", "apr36", 12)
                             ])
    def test_yixin_hengrun_loanapplyquery_fail(self, case, app, source_type, period):
        """
        进件查询失败
        :return:
        """
        four_element = get_four_element(id_num_begin="50")
        item_no, asset_info = asset_import(self.channel, four_element, period, 7000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "mock失败-REFUSE-null", 'LoanApplyAsyncFailedEvent')

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_yixin_hengrun
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("草莓", "apr36", 12)
                             ])
    def test_yixin_hengrun_loanapplyconfirm_fail(self, case, app, source_type, period):
        """
        放款申请同步失败
        :return:
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, period, 9000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_asset_confirm(item_no, "LOAN_PRODUCT_CHANGE", 2)
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        user_change_product_confirm(asset_info, "LOAN_PRODUCT_CHANGE", 0)
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 1})
        self.msg.run_msg(item_no, "AssetApplyTrailSuccess")
        self.capital_mock.update_loanapplyconfirm_fail()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "mock 失败-1-mock 失败")


    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_yixin_hengrun
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_yixin_hengrun_loanaconfirmquery_fail(self, case, app, source_type, period):
        """
        放款失败
        :return:
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_asset_confirm(item_no, "LOAN_PRODUCT_CHANGE", 2)
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        user_change_product_confirm(asset_info, "LOAN_PRODUCT_CHANGE", 0)
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 1})
        self.msg.run_msg(item_no, "AssetApplyTrailSuccess")
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirmquery_fail()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "mock失败-LEND_FAILED-放款失败", 'GrantFailedEvent')


    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_yixin_hengrun
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_yixin_hengrun_assetconfirmovertimecheck_fail(self, case, app, source_type, period):
        """
        用户确认超时失败切换资方
        :return:
        """
        four_element = get_four_element(id_num_begin="66")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(item_no, four_element)
        #修改超时配置以便失败
        update_gbiz_capital_yixin_hengrun(raise_limit_over_time_seconds=0)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_asset_confirm(item_no, "LOAN_PRODUCT_CHANGE", 2)
        self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10005, "确认类型\\[LOAN_PRODUCT_CHANGE\\]已超时", 'UserConfirmTimeOutEvent')
        # case跑完恢复配置
        update_gbiz_capital_yixin_hengrun()
