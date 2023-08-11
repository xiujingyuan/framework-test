#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pytest
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.config.gbiz.gbiz_kv_config import incremental_update_config
from biztest.config.gbiz.gbiz_tongrongqianjingjing_config import *
from biztest.interface.gbiz.gbiz_interface import asset_import, data_cancel
from biztest.function.gbiz.gbiz_check_function import check_asset_event_exist, check_asset_loan_record, \
    check_wait_assetvoid_data
from biztest.function.gbiz.gbiz_common_function import init_capital_plan
from biztest.util.easymock.gbiz.tongrongqianjingjing import TongrongqianjingjingMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.util.tools.tools import get_four_element
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.util.asserts.assert_util import Assert


class TestCancel(BaseTestCapital):
    def init(self):
        super(TestCancel, self).init()
        self.mock = TongrongqianjingjingMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        self.channel = "tongrongqianjingjing"
        self.period = 12
        self.amount = 5000

    @classmethod
    def teardown_class(cls):
        update_gbiz_capital_tongrongqianjingjing()

    def setup_method(self):
        self.init()
        init_capital_plan(self.channel)
        update_gbiz_capital_tongrongqianjingjing()

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_cancel
    def test_cancel_01(self):
        """0/1/5状态直接取消"""
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, self.period, self.amount)
        self.payment_register(self.payment_mock, self.channel, four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        # 发起取消
        resp = data_cancel(item_no)
        Assert.assert_equal(0, resp['code'], "接口异常")
        Assert.assert_equal("取消成功", resp['message'], "接口异常")
        check_asset_event_exist(item_no, self.channel, "USER_CANCEL")
        check_asset_loan_record(item_no, asset_loan_record_status=5, asset_loan_record_memo="用户取消")
        check_wait_assetvoid_data(item_no, code=16, message="用户取消")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_cancel
    def test_cancel_02(self):
        """3状态取消，后续任务不允许取消"""
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, self.period, self.amount)
        self.payment_register(self.payment_mock, self.channel, four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.mock.update_bk2001()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 发起取消
        resp = data_cancel(item_no)
        Assert.assert_equal(0, resp['code'], "接口异常")
        Assert.assert_equal("资产取消拦截中，请稍后查看", resp['message'], "接口异常")
        check_asset_event_exist(item_no, self.channel, "USER_CANCEL")
        # LoanApplyQuery不可取消，继续放款流程
        self.mock.update_bk2002()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_asset_loan_record(item_no, asset_loan_record_status=3)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_cancel
    def test_cancel_03(self):
        """3状态取消，被后续任务拦截，取消成功"""
        incremental_update_config("grant", "gbiz_capital_%s" % self.channel, cancelable_task_list=["LoanApplyQuery"])
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, self.period, self.amount)
        self.payment_register(self.payment_mock, self.channel, four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.mock.update_bk2001()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 发起取消
        resp = data_cancel(item_no)
        Assert.assert_equal(0, resp['code'], "接口异常")
        Assert.assert_equal("资产取消拦截中，请稍后查看", resp['message'], "接口异常")
        check_asset_event_exist(item_no, self.channel, "USER_CANCEL")
        # LoanApplyQuery可取消，拦截执行，取消成功
        self.mock.update_bk2002()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_asset_loan_record(item_no, asset_loan_record_status=5, asset_loan_record_memo="用户取消")
        check_wait_assetvoid_data(item_no, code=16, message="用户取消")
