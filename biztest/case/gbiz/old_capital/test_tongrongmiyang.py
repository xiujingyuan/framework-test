from biztest.function.biz.biz_db_function import wait_biz_asset_appear
from biztest.function.gbiz.gbiz_db_function import update_withdraw_code_msg, update_confirm_data_by_item_no
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.tongrongmiyang import TongrongmiyangMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import get_invoked_api
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest
from biztest.util.xxl_job.xxl_job import XxlJob
from biztest.config.gbiz.xxl_job_group_mapping_env import job_group_mapping_env
from biztest.util.tools.tools import get_four_element
import common.global_const as gc


class TestTongrongmiyang(BaseTestCapital):
    def init(self):
        super(TestTongrongmiyang, self).init()
        self.channel = "tongrongmiyang"
        self.capital_mock = TongrongmiyangMock(gbiz_mock, check_req=True, return_req=True)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_payment_config(self.payment_mock.url)

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.payment_register(self.payment_mock, self.channel, four_element, item_no)

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_apply_query_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.check_after_LoanApplyQuery(asset_info)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.check_after_PaymentWithdraw(asset_info)
        self.payment_mock.update_withdraw_query_status(item_no + 'w', "success", "success")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})

    def trans_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "BondTransfer", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentTransferNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + 't', "success", "success")
        self.task.run_task(item_no, "PaymentTransferQuery", excepts={"code": 0})
        self.task.run_task(item_no, "BondTransferQuery", excepts={"code": 0})
        self.capital_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "BondContractSign", excepts={"code": 0})
        self.capital_mock.update_apply_query_success()
        self.task.run_task(item_no, "BondContractDown", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    def loan_to_fail(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_apply_query_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        time.sleep(1)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.payment_mock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "w", "fail", "fail")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})

    def check_after_LoanApplyQuery(self, asset_info):
        item_no = asset_info["data"]["asset"]["item_no"]
        should_api = get_invoked_api(self.channel, "LoanApplyQuery", self.capital_mock.path_prefix)
        # 从jaeger拿到请求日志
        req_log = self.jaeger.get_request_log(item_no, "LoanApplyQuery", should_api)
        Assert.assert_equal(len(should_api), len(req_log), "调用接口数量不匹配")
        check_data(req_log[should_api[0]], http_path=should_api[0])
        req_data = json.loads(req_log[should_api[0]]["feign_request"])
        check_data(req_data, orderId=item_no)

    def check_after_PaymentWithdraw(self, asset_info):
        item_no = asset_info["data"]["asset"]["item_no"]
        should_api = get_invoked_api(self.channel, "PaymentWithdraw", self.capital_mock.path_prefix)
        # 从es拿到请求日志
        req_log = self.es.get_request_log(item_no, "PaymentWithdraw", should_api)
        Assert.assert_equal(len(should_api), len(req_log), "调用接口数量不匹配")
        # --1.查询余额
        check_data(req_log[should_api[0]], http_path=should_api[0])
        req_data = json.loads(req_log[should_api[0]]["feign_request"])
        check_data(req_data, account="qsq_cpcn_tr_quick", sign_company="tr", merchant_name="gbiz")
        # --2.发起代付
        check_data(req_log[should_api[1]], http_path=should_api[1])
        req_data = json.loads(req_log[should_api[1]]["feign_request"])
        check_data(req_data,
                   merchant_key=item_no+"w",
                   account="qsq_cpcn_tr_quick",
                   amount=asset_info["data"]["asset"]["amount"]*100,
                   receiver_account_encrypt=asset_info["data"]["receive_card"]["num_encrypt"]
                   )

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_tongrongmiyang
    @pytest.mark.parametrize("app, source_type, period",
                             [("草莓", "lieyin_bill", 6)
                              ])
    def test_tongrongmiyang_success(self, case, app, source_type, period):
        """
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, period, 4000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        self.trans_to_success(item_no)
        check_asset_tran_data(item_no)
        if app != "火龙果":
            item_no_noloan, asset_info_noloan = asset_import_noloan(asset_info)
            self.noloan_to_success(item_no_noloan)

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_tongrongmiyang
    @pytest.mark.parametrize("count", [6, 12])
    def test_tongrongmiyang_order_fail(self, case, count):
        """
        生成订单失败，切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "草莓", "", '')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_apply_query_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, -1, "200:订单失败")

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_tongrongmiyang
    @pytest.mark.parametrize("count", [6])
    def test_tongrongmiyang_grant_fail(self, case, count):
        """代付结果未命中换卡白名单，放款失败，切资方"""
        incremental_update_config("grant", "gbiz_payment_config", change_card_codes_white_list=[])
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "草莓", "", '')
        self.register(item_no, four_element)
        self.loan_to_fail(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "\\[KN_RISK_CONTROL\\]")

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_tongrongmiyang
    @pytest.mark.parametrize("count", [6])
    def test_tongrongmiyang_updatecard_success(self, case, count):
        """代付结果命中换卡白名单，通知换卡，换卡后放款成功"""
        incremental_update_config("grant", "gbiz_payment_config", change_card_codes_white_list=["1003", "KN_RISK_CONTROL"])
        four_element = get_four_element()
        old_element = four_element
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "草莓", "", '')
        self.register(item_no, four_element)
        self.loan_to_fail(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        # 换卡通知
        self.msg.run_msg(item_no, "UpdateCardRequestMQ", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        # 用户换卡
        new_element = get_four_element()
        update_receive_card(asset_info, new_element, old_element)
        check_confirm_data(item_no, self.channel, 0, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        # 换卡后继续代付
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.payment_mock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "w", "success", "success")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_tongrongmiyang
    def test_tongrongmiyang_updatecard_time_out_xxljob(self, case):
        """通融代付最终失败，换卡超时,xxl-job方式捞取"""
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, 6, 8000, "草莓", "", '')
        self.register(item_no, four_element)
        self.loan_to_fail(item_no)
        update_withdraw_code_msg("E20012", "该卡暂无法支付，请换卡，或联系银行", item_no + "w")
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.msg.run_msg(item_no, "UpdateCardRequestMQ", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        update_confirm_data_by_item_no(item_no)
        xxl_job = XxlJob(job_group_mapping_env['grant{}'.format(gc.ENV)],
                         'updateCardTimeOutJob', user_name="admin", password="123456", xxl_job_type="xxl_job_k8s")
        xxl_job.trigger_job()
        time.sleep(3)
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 3, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_wait_assetvoid_data(item_no, 10005, "换卡超时,作废资产")

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_tongrongmiyang
    def test_tongrongmiyang_updatecard_time_out_task(self, case):
        """
        通融代付最终失败，换卡超时，任务驱动方式取消
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, 6, 8000, "草莓", "", '')
        self.register(item_no, four_element)
        self.loan_to_fail(item_no)
        update_withdraw_code_msg("E20012", "该卡暂无法支付，请换卡，或联系银行", item_no + "w")
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.msg.run_msg(item_no, "UpdateCardRequestMQ", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 2, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        update_confirm_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 0})
        check_confirm_data(item_no, self.channel, 3, "WITHDRAW_FINAL_FAIL_UPDATE_CARD")
        check_wait_assetvoid_data(item_no, 10005, "换卡超时,作废资产")


if __name__ == "__main__":
    pytest.main(["-s", "/Users/fenlai/code/framework-test/biztest/case/gbiz/jining.py", "--env=9" "--junt"])
