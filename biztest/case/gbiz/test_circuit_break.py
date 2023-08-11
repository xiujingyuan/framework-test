#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pytest
import time
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.config.gbiz.gbiz_kv_config import update_gbiz_circuit_break_config_v2, update_gbiz_payment_config,\
    update_gbiz_manual_task_auto_process_config
from biztest.config.gbiz.gbiz_haohanqianjingjing_config import *
from biztest.interface.gbiz.gbiz_interface import asset_import, circuit_break_update, run_job
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.util.tools.tools import get_four_element
from biztest.function.gbiz.gbiz_common_function import init_capital_plan, run_terminated_task
from biztest.function.gbiz.gbiz_check_function import check_circuit_break_data
from biztest.function.gbiz.gbiz_db_function import get_latest_circuit_break_record, clear_circuit_break_record, \
    clear_terminated_task, update_router_cp_amount_all_to_zero, update_all_channel_amount


class TestCircuitBreak(BaseTestCapital):

    channel = "haohanqianjingjing"
    period = 12
    amount = 5000

    @pytest.fixture(scope="class")
    def init(self):
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_haohanqianjingjing()
        update_gbiz_payment_config(self.payment_mock.url)
        update_gbiz_manual_task_auto_process_config()
        update_gbiz_circuit_break_config_v2(cnt=2)
        init_capital_plan(self.channel)
        clear_terminated_task()
        yield
        update_all_channel_amount()

    @pytest.fixture(scope="function")
    def case_init(self):
        super(TestCircuitBreak, self).init()
        clear_circuit_break_record()
        yield
        clear_circuit_break_record()

    @pytest.mark.gbiz_circuit_break
    def test_circuit_break_withdraw_balance(self, init, case_init):
        """
        代付余额不足熔断
        """
        circuit_break_name = "haohanqianjingjing_balance_not_enough"

        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, self.period, self.amount)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.payment_mock.update_withdraw_balance_enough()
        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.payment_mock.update_withdraw_apply_success()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.payment_mock.update_withdraw_query_status(item_no + 'w', "success", "success")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.task.run_task(item_no, "BondTransfer", excepts={"code": 0})
        # 余额低于预警值
        self.payment_mock.update_withdraw_balance_enough(1000000)
        self.task.run_task(item_no, "PaymentTransferNew", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 2, "message": "可用余额.*,已小于预警值.*,延迟代付"})
        # 发生熔断
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 2, "message": "业务熔断\\[.*\\]，导致任务挂起"})
        check_circuit_break_data(circuit_break_name, "open")
        # 手动解除熔断
        circuit_break_id = get_latest_circuit_break_record(circuit_break_name)[0]["circuit_break_record_id"]
        circuit_break_update(circuit_break_id, "close")
        check_circuit_break_data(circuit_break_name, "closed")
        self.task.run_task(item_no, "PaymentTransfer", excepts={"code": 2, "message": "可用余额.*,已小于预警值.*,延迟代付"})

    @pytest.mark.gbiz_circuit_break
    def test_circuit_break_manual_task(self, init, case_init):
        """
        手动任务自动处理熔断
        """
        circuit_break_name = "AssetVoid_Circuit_Break"
        update_router_cp_amount_all_to_zero()

        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, self.period, self.amount)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        run_terminated_task(item_no, "ChangeCapital", expect_code=1)
        # 加2s等待时间，避免job无法捞取到任务
        time.sleep(2)
        # 运行job
        run_job("manualTaskAutoProcessJob", {"taskTypeList": ["AssetVoid"]})
        # 发生熔断
        check_circuit_break_data(circuit_break_name, "open")
        # 手动解除熔断
        circuit_break_id = get_latest_circuit_break_record(circuit_break_name)[0]["circuit_break_record_id"]
        circuit_break_update(circuit_break_id, "close")
        check_circuit_break_data(circuit_break_name, "closed")

    @pytest.mark.gbiz_circuit_break
    def test_circuit_break_sql(self, init, case_init):
        """
        job方式熔断
        """
        circuit_break_name = "SQL_Circuit_Break_DEMO"
        # 运行job
        run_job("BizCircuitBreakJob", {"breakerNameList": [circuit_break_name]})
        # 发生熔断
        check_circuit_break_data(circuit_break_name, "open")
        # 手动解除熔断
        circuit_break_id = get_latest_circuit_break_record(circuit_break_name)[0]["circuit_break_record_id"]
        circuit_break_update(circuit_break_id, "close")
        check_circuit_break_data(circuit_break_name, "closed")
