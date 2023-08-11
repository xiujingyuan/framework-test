from biztest.function.gbiz.gbiz_db_function import update_router_capital_plan_amount
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.haishengtong_daqin import HaishengtongDaqinMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import prepare_attachment
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import time
import pytest
from biztest.util.tools.tools import get_four_element


# @pytest.mark.gbiz_auto_test
# @pytest.mark.gbiz_haishengtong_daqin
class TestHaishengtongDaqin(BaseTestCapital):
    """
       gbiz_haishengtong_daqin
       author: zhimengxue
       date: 20210926
       """

    def init(self):
        super(TestHaishengtongDaqin, self).init()
        self.channel = "haishengtong_daqin"
        self.haishengtong_mock = HaishengtongDaqinMock(gbiz_mock)
        update_gbiz_capital_haishengtong_daqin()
        update_gbiz_capital_haishengtong_daqin_const()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.haishengtong_mock.update_queryProtocolstatus_need_openaccount()
        self.haishengtong_mock.update_getProtocolsms_success()
        self.haishengtong_mock.update_Protocolconfirm_success()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='1', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='1', step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.haishengtong_mock.update_querybalance_success()
        self.haishengtong_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.haishengtong_mock.update_applyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.haishengtong_mock.update_applyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.haishengtong_mock.update_applyconfirmquery_success()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.haishengtong_mock.update_repayplan_success(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)
        # self.haishengtong_mock.update_contract_success()
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})

    @pytest.mark.gbiz_haishengtong_daqin_loan_success
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                                 ("香蕉", "irr36_quanyi", 6),
                                 # ("草莓", "irr36_quanyi", 12),
                             ])
    def test_haishengtong_daqin_loan_success(self, case, app, source_type, count):
        """
        放款成功
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type, '', '110000')

        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # check_request_log_by_channel(item_no, self.channel)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("count", [12])
    def test_haishengtong_daqin_canloan_fail(self, case, count):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, "香蕉", "irr36_quanyi", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        # canloan失败准备工作
        today = time.strftime("%Y-%m-%d", time.localtime())
        update_router_capital_plan_amount(0, today, self.channel)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # canloan执行之后恢复
        update_router_capital_plan_amount(3333333333, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "haishengtong_daqin->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("count", [6])
    def test_haishengtong_daqin_apply_fail(self, case, count):
        """
        同步进件失败切资方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, "香蕉", "irr36_quanyi", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.haishengtong_mock.update_querybalance_success()
        self.haishengtong_mock.update_apply_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.haishengtong_mock.update_applyquery_code_fail()
        check_wait_change_capital_data(item_no, 100400, "资方返回code:0040,msg:mock操作失败，系统异常", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 # ("草莓", "apr36", 12),
                                 ("香蕉", "irr36_quanyi", 6),
                                 # ("草莓", "irr36_quanyi", 12),
                             ])
    def test_haishengtong_daqin_apply_banlace_fail(self, case, app, source_type, count):
        """
        授信金额小于进件金额
        :param case:
        :param app:
        :param source_type:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.haishengtong_mock.update_querybalance_success(True)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.haishengtong_mock.update_applyquery_code_fail()
        check_wait_change_capital_data(item_no, 99, "余额查询返回的可放余额小于放款金额", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 # ("草莓", "apr36", 12),
                                 ("草莓", "irr36_quanyi", 6),
                                 # ("草莓", "irr36_quanyi", 12),
                             ])
    def test_haishengtong_daqin_apply_query_fail(self, case, app, source_type, count):
        """
        LoanApplyConfirm返回状态为5
        :param case:
        :param app:
        :param source_type:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '', '110000')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.haishengtong_mock.update_querybalance_success()
        self.haishengtong_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.haishengtong_mock.update_applyquery_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2000015, "资方返回code:0000,msg:审核未通过", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 # ("草莓", "apr36", 12),
                                 ("香蕉", "irr36_quanyi", 6),
                                 # ("草莓", "irr36_quanyi", 12),
                             ])
    def test_haishengtong_daqin_apply_query_code_fail(self, case, app, source_type, count):
        """
        LoanApplyConfirm 返回异常错误码
        :param case:
        :param app:
        :param source_type:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '', '110000')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.haishengtong_mock.update_querybalance_success()
        self.haishengtong_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.haishengtong_mock.update_applyquery_code_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 200201, "资方返回code:0020,msg:mock操作失败,参数错误", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 # ("草莓", "apr36", 12),
                                 ("香蕉", "irr36_quanyi", 6),
                                 # ("草莓", "irr36_quanyi", 12),
                             ])
    def test_haishengtong_daqin_apply_confirm_fail(self, case, app, source_type, count):
        """
        LoanApplyConfirm失败
        :param case:
        :param app:
        :param source_type:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '', '110000')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.haishengtong_mock.update_querybalance_success()
        self.haishengtong_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.haishengtong_mock.update_applyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.haishengtong_mock.update_applyconfirm_fail()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.haishengtong_mock.update_applyconfirmquery_code_fail()
        check_wait_change_capital_data(item_no, 300201, "资方返回code:0020,msg:mock操作失败,参数错误",
                                       "ConfirmApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 # ("草莓", "apr36", 12),
                                 ("香蕉", "irr36_quanyi", 6),
                                 # ("草莓", "irr36_quanyi", 12),
                             ])
    def test_haishengtong_daqin_apply_confirm_query_fail(self, case, app, source_type, count):
        """
        LoanConfirmQuery返回状态为7
        :param case:
        :param app:
        :param source_type:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '', '110000')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.haishengtong_mock.update_querybalance_success()
        self.haishengtong_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.haishengtong_mock.update_applyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.haishengtong_mock.update_applyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.haishengtong_mock.update_applyconfirmquery_fail()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 4000017, "资方返回code:0000,msg:放款失败", "GrantFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 # ("草莓", "apr36", 12),
                                 ("香蕉", "irr36_quanyi", 6),
                                 # ("草莓", "irr36_quanyi", 12),
                             ])
    def test_haishengtong_daqin_apply_confirm_query_code_fail(self, case, app, source_type, count):
        """
        LoanConfirmQuery 返回异常错误码
        :param case:
        :param app:
        :param source_type:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, app, source_type, '', '110000')
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.haishengtong_mock.update_querybalance_success()
        self.haishengtong_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.haishengtong_mock.update_applyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.haishengtong_mock.update_applyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.haishengtong_mock.update_applyconfirmquery_code_fail()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 400501, "资方返回code:0050,msg:mock返回非文档中错误码", "GrantFailedEvent")
