#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.interface.gbiz.gbiz_interface import *
from biztest.interface.contract.contract_interface import *
from biztest.function.biz.biz_db_function import *
from biztest.function.contract.contract_db_function import create_asset_import_task
from biztest.util.task.task import GbizTask
from biztest.util.msg.msg import GbizMsg


def make_asset_data(status, channel="yumin_zhongbao", period=12, from_system_name="香蕉", loan_source_type="", noloan_source_type="rongdan"):
    """
    造进件数据
    :param status: 期望的资产状态import/repay
    :param channel:
    :param period:
    :param from_system_name:
    :param source_type:
    :return:
    """
    if channel in ["qinnong", "qinnong_jieyi", "qinnong_dingfeng"]:
        source_type = "irr36"
    else:
        source_type = "apr36"
    four_element = get_four_element()
    item_no, asset_info = asset_import(channel, four_element, period, 5000, from_system_name, source_type)
    msg = GbizMsg()
    task = GbizTask()
    task.run_task(item_no, "AssetImport", excepts={"code": 0})
    msg.run_msg(item_no, "AssetImportSync", excepts={"code": 0})
    wait_biz_asset_appear(item_no)
    item_no_noloan, asset_info_noloan = None, None
    if from_system_name != "火龙果":
        item_no_noloan, asset_info_noloan = asset_import_noloan(asset_info, noloan_source_type)
        task.run_task(item_no_noloan, "AssetImport", excepts={"code": 0})
        msg.run_msg(item_no_noloan, "AssetImportSync", excepts={"code": 0})
        wait_biz_asset_appear(item_no_noloan)
        set_asset_contract_subject(item_no_noloan, "云智")
    set_asset_status(item_no, status)
    insert_asset_loan_record(item_no, channel)
    update_asset(item_no, asset_actual_grant_at=get_date())
    update_asset(item_no_noloan, asset_actual_grant_at=get_date())
    set_asset_status(item_no_noloan, status)
    return item_no, asset_info, item_no_noloan, asset_info_noloan


def do_change_capital(item_no, old_channel, new_channel):
    # 合同切资方接口，生成ChangeChannelTask
    change_channel(item_no, old_channel, new_channel)
    # 手动修改biz.asset的channel
    set_asset_loan_channel(item_no, new_channel)
    # 手动生成新资方AssetImportTask
    create_asset_import_task(item_no, new_channel)
