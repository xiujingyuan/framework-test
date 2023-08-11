#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.interface.gbiz_global.gbiz_global_interface import asset_import, asset_import_noloan
from biztest.interface.rbiz.rbiz_global_interface import asset_grant_success_to_rbiz, capital_asset_success_to_rbiz
from biztest.util.msgsender.msgsender import Msgsender
from biztest.util.task.task import TaskGlobal
from biztest.util.log.log_util import LogUtil


def asset_import_auto(loan_channel, day, from_system, from_app, source_type, element, period=1, amount=500000, fees=None, late_num=None):
    item_no, asset_info = asset_import(loan_channel, period, day, "day", amount, from_system, from_app, source_type,
                                       element, withdraw_type='offline', fees=fees, late_num=late_num)
    gbiz_task = TaskGlobal()
    gbiz_task.run_task(item_no, "AssetImport", excepts={"code": 0})
    asset_grant_success_to_rbiz(item_no)
    capital_asset_success_to_rbiz(item_no)
    Msgsender("rbiz").run_msg_by_order_no(item_no)
    LogUtil.log_info("%s, 放款成功" % item_no)
    return item_no, asset_info


def asset_import_auto_no_loan(asset_info):
    item_no_no_loan, asset_info_no_loan = asset_import_noloan(asset_info)
    gbiz_task = TaskGlobal()
    gbiz_task.run_task(item_no_no_loan, "AssetImport", excepts={"code": 0})
    asset_grant_success_to_rbiz(item_no_no_loan)
    Msgsender("rbiz").run_msg_by_order_no(item_no_no_loan)
    LogUtil.log_info("%s, 放款成功" % item_no_no_loan)
    return item_no_no_loan
