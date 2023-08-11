#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import update_withdraw_order, get_task_by_item_no_and_task_type, \
    update_all_channel_amount
from biztest.function.gbiz.gbiz_check_function import check_withdraw_data, check_sendmsg_exist
from biztest.interface.gbiz.gbiz_interface import asset_import, payment_callback
from biztest.config.gbiz.gbiz_kv_config import update_gbiz_payment_config
from biztest.config.gbiz.gbiz_tongrongqianjingjing_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.util.easymock.deposit import DepositMock
from biztest.util.easymock.gbiz.tongrongqianjingjing import TongrongqianjingjingMock
from biztest.util.tools.tools import get_four_element, get_calc_date_base_today
from biztest.util.asserts.assert_util import Assert
import pytest


class TestPaymentWithdraw(BaseTestCapital):
    """
    测试代付流程
    1.代付：PaymentWithdrawNew、PaymentWithdraw、PaymentWithdrawQuery
    2.转账：PaymentTransferNew、PaymentTransfer、PaymentTransferQuery
    """
    def init(self):
        super(TestPaymentWithdraw, self).init()
        self.payment_mock = PaymentMock(gbiz_mock)
        self.deposit_mock = DepositMock(gbiz_mock)
        self.capital_mock = TongrongqianjingjingMock(gbiz_mock)
        update_gbiz_capital_tongrongqianjingjing()
        update_gbiz_capital_tongrongqianjingjing_const()
        update_gbiz_payment_config(self.payment_mock.url)
        update_all_channel_amount()
        self.channel = "tongrongqianjingjing"
        self.period = 12
        self.amount = 5000

    @pytest.fixture()
    def case(self):
        self.init()

    def process_to_withdraw(self):
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, self.period, self.amount)
        self.payment_register(self.payment_mock, self.channel, four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_bk2001(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_bk2002(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_bk2003()
        self.capital_mock.update_bk3001()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_bk3003(item_no)
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.payment_mock.update_withdraw_balance_enough()
        return item_no

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_withdraw
    def test_withdraw(self, case):
        """
        代付成功
        """
        item_no = self.process_to_withdraw()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        check_withdraw_data(item_no + 'w', "ready", "ready")
        # 余额不足
        self.payment_mock.update_withdraw_balance_enough(1000)
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 2, "message": "返回总可用金额.*小于本次代付金额.*,延迟代付"})
        # 余额低于预警值
        self.payment_mock.update_withdraw_balance_enough(1000000)
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 2, "message": "可用余额.*,已小于预警值.*,延迟代付"})
        # 余额充足，代付成功
        self.payment_mock.update_withdraw_balance_enough()
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no + 'w', "process", "process")
        self.payment_mock.update_withdraw_query_status(item_no + 'w', "success", "success")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0, "message": ".*代付成功"})
        check_withdraw_data(item_no + 'w', "success", "success", "E20000", "自动化测试成功")
        check_sendmsg_exist(item_no, "PaymentWithdrawSuccess")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_withdraw
    def test_withdraw_apply_fail(self, case):
        """
        代付-申请失败
        """
        item_no = self.process_to_withdraw()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_fail()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 1})
        check_withdraw_data(item_no + 'w', "fail", "fail", "2", "脱敏服务异常")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_withdraw
    def test_withdraw_retry_payment(self, case):
        """
        代付-单次失败，重新发起代付
        """
        item_no = self.process_to_withdraw()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw")
        self.payment_mock.update_withdraw_query_status(item_no + "w", "fail", "fail", retry=True)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1, "message": ".*代付查询为失败,延迟至.*创建下次代付.*"})
        check_withdraw_data(item_no + 'w', "ready", "fail")
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdraw")
        self.payment_mock.update_withdraw_query_status(item_no + 'w', "success", "success")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        check_withdraw_data(item_no + 'w', "success", "success", "E20000", "自动化测试成功")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_withdraw
    def test_withdraw_fail_max_times(self, case):
        """
        代付-失败超过最大次数
        """
        item_no = self.process_to_withdraw()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "w", "fail", "fail", retry=True)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        check_withdraw_data(item_no + 'w', "ready", "fail")
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "w", "fail", "fail", retry=True)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1, "message": ".*已超过最大允许的失败次数"})
        check_withdraw_data(item_no + 'w', order_status="fail", order_resp_code="G00022", order_resp_message="超过最大失败次数{[FAILED]放款失败}",
                                     record_status="fail", record_resp_code="FAILED", record_resp_message="放款失败")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_withdraw
    def test_withdraw_fail_over_time(self, case):
        """
        代付-失败超过最大时长
        """
        item_no = self.process_to_withdraw()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        update_withdraw_order(item_no + "w", withdraw_order_create_at=get_calc_date_base_today(day=-2))
        self.payment_mock.update_withdraw_query_status(item_no + "w", "fail", "fail", retry=True)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1, "message": ".*已超过最大允许代付时间"})
        check_withdraw_data(item_no + 'w', order_status="fail", order_resp_code="G00023", order_resp_message="超过最大代付时长{[FAILED]放款失败}",
                                     record_status="fail", record_resp_code="FAILED", record_resp_message="放款失败")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_withdraw
    def test_withdraw_final_fail(self, case):
        """
        代付-最终失败
        """
        item_no = self.process_to_withdraw()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "w", "fail", "fail")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1, "message": ".*代付失败为最终失败消息.*"})
        check_withdraw_data(item_no + 'w', "fail", "fail", "KN_RISK_CONTROL", "")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_withdraw
    def test_withdraw_terminated(self, case):
        """
        代付-终止代付
        """
        item_no = self.process_to_withdraw()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "w", "fail", "fail_terminated")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1, "message": ".*请人工核对!.*"})
        check_withdraw_data(item_no + 'w', "ready", "void")
        task = get_task_by_item_no_and_task_type(item_no, 'PaymentWithdrawNew')
        Assert.assert_equal('terminated', task['task_status'], '数据有误')

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_withdraw
    def test_withdraw_reverse(self, case):
        """
        代付冲正，国内不处理
        """
        item_no = self.process_to_withdraw()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_balance_enough()
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + 'w', "success", "success")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0, "message": ".*代付成功"})
        check_withdraw_data(item_no + 'w', "success", "success", "E20000", "自动化测试成功")
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})
        # 冲正回调，国内不处理
        resp = payment_callback(item_no + 'w', "reverse")
        Assert.assert_equal(1, resp["code"], "代付冲正回调异常")
        Assert.assert_match(resp["message"], ".*接收到冲正通知,国内不处理.*", "代付冲正回调异常")

    def process_to_transfer(self):
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, self.period, self.amount)
        self.payment_register(self.payment_mock, self.channel, four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_bk2001(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_bk2002(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_bk2003()
        self.capital_mock.update_bk3001()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_bk3003(item_no)
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_balance_enough()
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + 'w', "success", "success")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0, "message": ".*代付成功"})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.capital_mock.update_bk4001()
        self.task.run_task(item_no, "LoanGrantStatusPush")
        self.task.run_task(item_no, "BondTransfer", excepts={"code": 0})
        self.payment_mock.update_withdraw_balance_enough()
        return item_no

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_transfer
    def test_transfer(self, case):
        """
        债转成功
        """
        item_no = self.process_to_transfer()
        self.task.run_task(item_no, "PaymentTransferNew", excepts={"code": 0})
        check_withdraw_data(item_no + 't', "ready", "ready")
        # 余额不足
        self.payment_mock.update_withdraw_balance_enough(1000)
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 2, "message": "返回总可用金额.*小于本次代付金额.*,延迟代付"})
        # 余额低于预警值
        self.payment_mock.update_withdraw_balance_enough(1000000)
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 2, "message": "可用余额.*,已小于预警值.*,延迟代付"})
        # 余额0
        self.payment_mock.update_withdraw_balance_enough(0)
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 2, "message": ".*代付账户余额为0"})
        # 余额充足，代付成功
        self.payment_mock.update_withdraw_balance_enough()
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 0})
        check_withdraw_data(item_no + 't', "process", "process")
        self.payment_mock.update_withdraw_query_status(item_no + 't', "success", "success")
        self.task.run_task(item_no, "PaymentTransferQuery", excepts={"code": 0, "message": ".*代付成功"})
        check_withdraw_data(item_no + 't', "success", "success", "E20000", "自动化测试成功")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_transfer
    def test_transfer_apply_fail(self, case):
        """
        债转-申请失败
        """
        item_no = self.process_to_transfer()
        self.task.run_task(item_no, "PaymentTransferNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_fail()
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 1})
        check_withdraw_data(item_no + 't', "fail", "fail", "2", "脱敏服务异常")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_transfer
    def test_transfer_retry_payment(self, case):
        """
        债转-单次失败，重新发起债转
        """
        item_no = self.process_to_transfer()
        self.task.run_task(item_no, "PaymentTransferNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "t", "fail", "fail", retry=True)
        self.task.run_task(item_no, "PaymentTransferQuery", excepts={"code": 1, "message": ".*代付查询为失败,延迟至.*创建下次代付.*"})
        check_withdraw_data(item_no + 't', "ready", "fail")
        self.task.run_task(item_no, "PaymentTransferNew", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + 't', "success", "success")
        self.task.run_task(item_no, "PaymentTransferQuery", excepts={"code": 0})
        check_withdraw_data(item_no + 't', "success", "success", "E20000", "自动化测试成功")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_transfer
    def test_transfer_final_fail(self, case):
        """
        债转-最终失败
        """
        item_no = self.process_to_transfer()
        self.task.run_task(item_no, "PaymentTransferNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "t", "fail", "fail")
        self.task.run_task(item_no, "PaymentTransferQuery", excepts={"code": 1, "message": ".*代付失败为最终失败消息.*"})
        check_withdraw_data(item_no + 't', "fail", "fail", "KN_RISK_CONTROL", "")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_transfer
    def test_transfer_terminated(self, case):
        """
        债转-终止
        """
        item_no = self.process_to_transfer()
        self.task.run_task(item_no, "PaymentTransferNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + "t", "fail", "fail_terminated")
        self.task.run_task(item_no, "PaymentTransferQuery", excepts={"code": 1, "message": ".*请人工核对!.*"})
        check_withdraw_data(item_no + 't', "ready", "void")
        task = get_task_by_item_no_and_task_type(item_no, 'PaymentTransferNew')
        Assert.assert_equal('terminated', task['task_status'], '数据有误')
