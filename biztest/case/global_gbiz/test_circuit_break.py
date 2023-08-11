#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pytest
from biztest.case.global_gbiz.global_base_test_capital import BaseTestCapital
from biztest.config.global_gbiz.global_gbiz_kv_config import update_gbiz_circuit_break_config_v2
from biztest.function.global_gbiz.gbiz_global_common_function import run_terminated_task
from biztest.function.global_gbiz.gbiz_global_db_function import update_router_capital_plan_amount_all_to_zero, \
    update_all_channel_amount, update_terminated_task

from biztest.interface.gbiz.gbiz_interface import circuit_break_update, run_job
from biztest.function.gbiz.gbiz_check_function import check_circuit_break_data
from biztest.function.gbiz.gbiz_db_function import get_latest_circuit_break_record
from biztest.interface.gbiz_global.gbiz_global_interface import run_bizcircuitbreakJob_by_api, \
    run_manualTaskAutoProcessJob_by_api


@pytest.mark.global_gbiz_thailand
@pytest.mark.global_gbiz_mexico
@pytest.mark.global_gbiz_philippines
@pytest.mark.global_gbiz_pakistan
@pytest.mark.global_gbiz_circuit_break
class TestCircuitBreak(BaseTestCapital):

    def setup(self):
        super(TestCircuitBreak, self).init()
        update_gbiz_circuit_break_config_v2(succrate=100, errCount=0)
        circuit_break_list = ["Payment_WITHDRAW_FAILED_Circuit_Break",
                              "ASSET_VOID_Circuit_Break",
                              "Payment_Service_Exception_Circuit_Break"]
        for circuit_break_name in circuit_break_list:
            circuit_break = get_latest_circuit_break_record(circuit_break_name)
            # 执行前先判断是否有未关闭的熔断任务，有则关掉
            circuit_break_status = circuit_break[0]["circuit_break_record_status"] if len(circuit_break) > 0 else ""
            if circuit_break_status == 'open':
                circuit_break_id = circuit_break[0]["circuit_break_record_id"]
                circuit_break_update(circuit_break_id, "close")

    @classmethod
    def teardown(cls):
        update_gbiz_circuit_break_config_v2()
        update_all_channel_amount()

    def test_circuit_break_withdraw_fail(self):
        """
        代付最终失败熔断
        """
        circuit_break_name = "Payment_WITHDRAW_FAILED_Circuit_Break"
        item_no, asset_info = self.asset_import_data()
        self.loan_to_fail(item_no)

        # 发生熔断
        run_terminated_task(item_no, "ChangeCapital", 2)
        check_circuit_break_data(circuit_break_name, "open")
        # 手动解除熔断
        circuit_break_id = get_latest_circuit_break_record(circuit_break_name)[0]["circuit_break_record_id"]
        circuit_break_update(circuit_break_id, "close")
        check_circuit_break_data(circuit_break_name, "closed")

    def test_circuit_break_manual_task(self):
        """
        手动任务自动处理熔断
        """
        update_terminated_task(task_status='close')
        circuit_break_name = "ASSET_VOID_Circuit_Break"
        item_no, asset_info = self.asset_import_data()
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        update_router_capital_plan_amount_all_to_zero("test")
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        run_terminated_task(item_no, "ChangeCapital", expect_code=1)
        # 运行job
        run_manualTaskAutoProcessJob_by_api()
        # run_job("manualTaskAutoProcessJob", {"taskTypeList": ["AssetVoid"]})
        # 发生熔断
        check_circuit_break_data(circuit_break_name, "open")
        # 手动解除熔断
        circuit_break_id = get_latest_circuit_break_record(circuit_break_name)[0]["circuit_break_record_id"]
        circuit_break_update(circuit_break_id, "close")
        check_circuit_break_data(circuit_break_name, "closed")

    def test_circuit_break_sql(self):
        """
        job方式熔断
        """
        circuit_break_name = "Payment_Service_Exception_Circuit_Break"
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_balance_not_enouth()
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 2})
        # 运行job
        run_bizcircuitbreakJob_by_api(circuit_break_name)
        run_job("BizCircuitBreakJob", {"breakerNameList": [circuit_break_name]})
        # 发生熔断
        check_circuit_break_data(circuit_break_name, "open")
        # 手动解除熔断
        circuit_break_id = get_latest_circuit_break_record(circuit_break_name)[0]["circuit_break_record_id"]
        circuit_break_update(circuit_break_id, "close")
        check_circuit_break_data(circuit_break_name, "closed")
