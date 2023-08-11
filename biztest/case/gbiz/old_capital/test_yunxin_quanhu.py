from biztest.function.biz.biz_db_function import wait_biz_asset_appear
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.yunxin_quanhu import YunxinQuanhuMock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.function.gbiz.gbiz_check_function import check_asset_tran_data, check_capital_transaction, \
    check_wait_change_capital_data
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest
from biztest.util.tools.tools import get_four_element


class TestYunxinQuanhu(BaseTestCapital):
    def init(self):
        super(TestYunxinQuanhu, self).init()
        self.channel = "yunxin_quanhu"
        self.mock = YunxinQuanhuMock(gbiz_mock)

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.mock.update_query_protocol_fail()
        capital_regiest_query(self.channel, four_element)
        capital_regiest(self.channel, four_element)
        self.mock.update_sign_apply_success()
        sms_seq = get_sms_verifycode(self.channel, four_element)['data']['seq']
        self.mock.update_sign_confirm_success()
        capital_regiest_with_sms_verifycode(self.channel, four_element, sms_seq, '111111')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.mock.update_query_balance_success()
        self.mock.update_loan_apply_success(asset_info["data"]["asset"]["amount"])
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.mock.update_loan_query_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.mock.update_apply_confirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.mock.update_confirm_query_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.mock.update_get_contract_success()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "ContractDown", wait_time=20, excepts={"code": 0})
        self.mock.update_replay_plan(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_yunxin_quanhu
    # @pytest.mark.gbiz_yunxin_quanhu_loan_success
    @pytest.mark.parametrize("count", [6])
    def test_yunxin_quanhu_loan_success(self, case, count):
        four_element = get_four_element("中国银行", bank_code_suffix="02")
        item_no, asset_info = asset_import(self.channel, four_element, count, 5000, "香蕉")
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        item_no_noloan, asset_info_noloan = asset_import_noloan(asset_info)
        self.noloan_to_success(item_no_noloan)

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_yunxin_quanhu
    @pytest.mark.parametrize("count", [6])
    def test_yunxin_quanhu_loan_confirm_fail(self, case, count):
        """
        放款失败切资方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element("中国银行", bank_code_suffix="06")
        item_no, asset_info = asset_import(self.channel, four_element, count, 5000, "香蕉")

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.mock.update_query_balance_success()
        self.mock.update_loan_apply_success(asset_info["data"]["asset"]["amount"])
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.mock.update_loan_query_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.mock.update_apply_confirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.mock.update_confirm_query_fail(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 1002, "失败")

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_yunxin_quanhu
    @pytest.mark.parametrize("count", [6])
    def test_yunxin_quanhu_loan_query_fail(self, case, count):
        """
        放款失败切资方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element("中国银行", bank_code_suffix="08")
        item_no, asset_info = asset_import(self.channel, four_element, count, 5000, "香蕉")

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.mock.update_query_balance_success()
        self.mock.update_loan_apply_success(asset_info["data"]["asset"]["amount"])
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.mock.update_loan_query_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 15, "审核未通过")

    def before_repayplan(self):
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, 6, 5000, "香蕉")
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.mock.update_query_balance_success()
        self.mock.update_loan_apply_success(asset_info["data"]["asset"]["amount"])
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.mock.update_loan_query_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.mock.update_apply_confirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.mock.update_confirm_query_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        return item_no, asset_info

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_repayplan
    def test_yunxin_quanhu_repayplan_01_diff_principal(self, case):
        item_no, asset_info = self.before_repayplan()
        self.mock.update_replay_plan_with_diff(asset_info, diff_type='diff_principal')
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 2, "message": "本金不一致"})

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_repayplan
    def test_yunxin_quanhu_repayplan_02_diff_period(self, case):
        item_no, asset_info = self.before_repayplan()
        self.mock.update_replay_plan_with_diff(asset_info, diff_type='diff_period')
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 2, "message": "总期次不等"})

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_repayplan
    def test_yunxin_quanhu_repayplan_03_diff_due_at(self, case):
        item_no, asset_info = self.before_repayplan()
        self.mock.update_replay_plan_with_diff(asset_info, diff_type='diff_due_at')
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 2, "message": "还款时间不匹配"})

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_repayplan
    def test_yunxin_quanhu_repayplan_04_diff_interest_intolerable(self, case):
        item_no, asset_info = self.before_repayplan()
        self.mock.update_replay_plan_with_diff(asset_info, diff_type='diff_interest_intolerable')
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 2, "message": "息费总额超过容差"})

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_repayplan
    def test_yunxin_quanhu_repayplan_05_diff_interest_tolerable(self, case):
        item_no, asset_info = self.before_repayplan()
        self.mock.update_replay_plan_with_diff(asset_info, diff_type='diff_interest_tolerable')
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        check_capital_transaction(item_no)


if __name__ == "__main__":
    pytest.main(["-s", "/Users/fenlai/code/framework-test/biztest/case/gbiz/qnn_lm.py", "--env=9"])
