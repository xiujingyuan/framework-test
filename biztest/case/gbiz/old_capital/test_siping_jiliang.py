import time
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.config.gbiz.gbiz_kv_config import update_gbiz_capital_siping_jiliang
from biztest.function.biz.biz_db_function import wait_biz_asset_appear
from biztest.function.gbiz.gbiz_check_function import check_asset_tran_data, check_wait_change_capital_data
from biztest.function.gbiz.gbiz_common_function import prepare_attachment
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_router_capital_plan_amount
from biztest.util.easymock.gbiz.siping_jiliang import SiPingJiLiangMock
import pytest

from biztest.interface.gbiz.gbiz_interface import capital_regiest_query, capital_regiest, asset_import, \
    common_noloan_import
from biztest.util.tools.tools import get_four_element


# @pytest.mark.gbiz_auto_test
# @pytest.mark.test_siping_jiliang
class TestSipingJiliang(BaseTestCapital):
    def init(self):
        super(TestSipingJiliang, self).init()
        self.channel = "siping_jiliang"
        self.capital_mock = SiPingJiLiangMock(gbiz_mock)
        update_gbiz_capital_siping_jiliang()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.capital_mock.update_bind_card_result_query_success()
        self.capital_mock.update_pre_bind_card_success()
        self.capital_mock.update_bind_card_result_query_success()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='siping_jiliang', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='siping_jiliang', step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_result_not_exist()
        self.capital_mock.update_credit_apply_success(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_result_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_result_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repay_plan(item_no)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.capital_mock.update_contract_success()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_loan_success
    @pytest.mark.test_siping_jiliang_success
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 # ("草莓", "apr36", 12),
                                 ("香蕉", "irr36_quanyi", 6),
                                 # ("草莓", "irr36_quanyi", 12),
                             ])
    def test_siping_jiliang_loan_success(self, case, app, source_type, count):
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "irr36_quanyi", 12),
                             ])
    def test_siping_jiliang_canloan_fail(self, case, count,app,source_type):
        # canloan失败
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)
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
        check_wait_change_capital_data(item_no, 4, "siping_jiliang->校验资金量失败;")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "irr36_quanyi", 6),
                             ])
    def test_siping_jiliang_credit_fail(self, case, count,app,source_type):
        # LoanApplyNew 失败
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 5000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply_fail(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_result_not_exist()

        check_wait_change_capital_data(item_no, 21, "授信申请同步失败")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_siping_jiliang_credit_result_fail(self, case, count,app,source_type):
        # LoanApplyQuery失败
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply_success(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_result_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 3, "mock approvalStatus失败")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_siping_jiliang_loan_apply_fail(self, case, count,app,source_type):
        # LoanApplyConfirm 失败
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 5000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply_success(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_result_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loan_apply_fail()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_result_fail(asset_info)
        check_wait_change_capital_data(item_no, 1111111, "这是mockcode返回失败")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "irr36_quanyi", 12),
                             ])
    def test_siping_jiliang_loan_result_fail(self, case, count,app,source_type):
        # LoanConfirmQuery 失败
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_upload_file_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply_success(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_result_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_result_fail(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1008, "放款失败")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "irr36_quanyi", 12),
                             ])
    def test_siping_jiliang_photo_camloan_fail(self,case,count,app,source_type):
        """
        :return:活体照超过3天camloan失败
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6666, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 4, 'siping_jiliang->资方校验失败: 校验活体照是否过期;')
