#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.util.task.task import DepositTask


class BaseTestDeposit(object):
    task = DepositTask()

    def trade_task_process(self, order_no, trade_no):
        self.task.run_task(order_no, "TradeNew", excepts={"code": 0})
        self.task.run_task(trade_no, "TradeApply", excepts={"code": 0})
        self.task.run_task(trade_no, "QueryTrade", excepts={"code": 0})
        self.task.run_task(trade_no, "AcctRecharge", excepts={"code": 0})
        self.task.run_task(order_no, "QueryOrder", excepts={"code": 0})
