#!/usr/bin/python
# -*- coding: UTF-8 -*-
from copy import deepcopy
import time

from biztest.config.global_rbiz.global_rbiz_interface_params_config import global_asset
from biztest.config.rbiz.params_config import capital_asset, refund_result
from biztest.function.global_dcs.dcs_global_db import get_dcs_asset_info_by_item_no
from biztest.function.global_gbiz.gbiz_global_db_function import get_asset_from_asset, \
    get_asset_info_by_item_no, get_capital_transaction_principal_from_asset_tran, \
    get_capital_transaction_fees_from_asset_tran, get_trans_from_asset_tran, get_loan_record_from_asset, \
    get_borrower_from_asset_card
from biztest.interface.dcs.dcs_global_interface import dcs_asset_payment_success_url, asset_withdraw, \
    dcs_asset_withdraw_success_url, dcs_capital_asset_url, dcs_refund_result_url
from biztest.interface.gbiz_global.gbiz_global_interface import asset_import, asset_import_noloan, get_random_str, \
    parse_resp_body, requests, json, get_date
from biztest.interface.rbiz.rbiz_global_interface import asset_grant_success_to_rbiz, capital_asset_success_to_rbiz
from biztest.util.msgsender.msgsender import Msgsender
from biztest.util.task.task import TaskGlobal
from biztest.util.log.log_util import LogUtil
import common.global_const as gc
from biztest.util.tools.tools import get_timestamp, get_guid


def asset_import_and_auto_loan(loan_channel, day, from_system, from_app, source_type, element, period=1):
    item_no, asset_info = asset_import(loan_channel, period, day, "day", 500000, from_system, from_app, source_type,
                                       element, withdraw_type='offline')
    gbiz_task = TaskGlobal()
    gbiz_task.run_task(item_no, "AssetImport", excepts={"code": 0})
    asset_payment_withdraw_success_to_dcs(item_no)
    asset_grant_success_to_dcs(item_no)
    asset_grant_success_to_rbiz(item_no)
    capital_asset_success_to_rbiz(item_no)
    capital_asset_success_to_dcs(item_no)
    Msgsender("rbiz").run_msg_by_order_no(item_no)
    LogUtil.log_info("%s, 放款成功" % item_no)
    return item_no, asset_info


def asset_import_and_auto_noloan(asset_info):
    item_no_no_loan, asset_info_no_loan = asset_import_noloan(asset_info)
    gbiz_task = TaskGlobal()
    gbiz_task.run_task(item_no_no_loan, "AssetImport", excepts={"code": 0})
    asset_grant_success_to_rbiz(item_no_no_loan)
    # asset_grant_success_to_dcs(item_no_no_loan)  #是否需要？
    LogUtil.log_info("%s, 放款成功" % item_no_no_loan)
    return item_no_no_loan


def asset_payment_withdraw_success_to_dcs(item_no):
    url = gc.DCS_URL + dcs_asset_payment_success_url
    asset = get_asset_from_asset(item_no)
    aseet_withdraw_info = deepcopy(asset_withdraw)
    aseet_withdraw_info["key"] = asset[0]['asset_item_no'] + "key"
    aseet_withdraw_info["data"]["merchant_key"] = asset[0]['asset_item_no'] + "w"
    aseet_withdraw_info["data"]["order_no"] = asset[0]['asset_item_no']
    aseet_withdraw_info["data"]["version"] = get_timestamp()
    aseet_withdraw_info["data"]["channel_key"] = "C" + get_timestamp()
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=aseet_withdraw_info))
    LogUtil.log_info(f"放款成功gbiz同步到dcs成功，url:{url}, request：{item_no}，resp：{resp}")
    print(json.dumps(aseet_withdraw_info))
    return item_no


def capital_asset_success_to_dcs(item_no):
    url = gc.DCS_URL + dcs_capital_asset_url
    capital_asset_info = deepcopy(capital_asset)
    asset = get_asset_info_by_item_no(item_no)
    time.sleep(10)
    dcs_asset = get_dcs_asset_info_by_item_no(item_no)
    capital_trans_principal = get_capital_transaction_principal_from_asset_tran(item_no)
    capital_trans_fees = get_capital_transaction_fees_from_asset_tran(item_no)
    capital_asset_info["channel"] = asset[0]['asset_loan_channel']
    capital_asset_info["version"] = dcs_asset[0]['version']
    capital_asset_info["item_no"] = item_no
    capital_asset_info["period_count"] = asset[0]['asset_period_count']
    capital_asset_info["due_at"] = asset[0]['asset_due_at']
    capital_asset_info["granted_amount"] = asset[0]['asset_principal_amount']
    capital_asset_info["cmdb_no"] = asset[0]['asset_cmdb_product_number']
    capital_asset_info['capital_transactions'].extend(capital_trans_principal)
    capital_asset_info["capital_transactions"].extend(capital_trans_fees)
    capital_asset_info["capital_transactions"][0]["actual_finished_at"] = capital_asset_info["capital_transactions"][1][
        "actual_finished_at"] = get_date()
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=capital_asset_info))
    LogUtil.log_info(f"资方还款计划同步dcs成功，url:{url},request：{item_no}，resp：{resp}")
    return item_no


def refund_result_success_to_dcs(amount, serial_no, withhold_serial_no, type, channel):
    url = gc.DCS_URL + dcs_refund_result_url
    refund_result_info = deepcopy(refund_result)
    refund_result_info["key"] = get_guid()
    refund_result_info['data']["type"] = type
    refund_result_info['data']["amount"] = amount
    refund_result_info['data']["serial_no"] = serial_no
    refund_result_info['data']["withhold_serial_no"] = withhold_serial_no
    refund_result_info['data']["channel"] = channel
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=refund_result_info))
    LogUtil.log_info(f"退款成功数据同步dcs成功，url:{url},request：{serial_no}，resp：{resp}")
    return serial_no


def asset_grant_success_to_dcs(item_no):
    url = gc.DCS_URL + dcs_asset_withdraw_success_url
    asset_info = deepcopy(global_asset)
    asset = get_asset_from_asset(item_no)
    trans = get_trans_from_asset_tran(item_no)
    loan_record = get_loan_record_from_asset(item_no)
    borrower = get_borrower_from_asset_card(item_no)
    asset_info["data"]['asset'] = asset[0]
    asset_info["key"] = item_no + get_random_str(3)
    if asset[0]['loan_channel'] != 'noloan':
        asset_info["data"]['loan_record'] = loan_record[0]
    asset_info["data"]['trans'].extend(trans)
    asset_info["data"]['borrower'] = borrower[0]

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=asset_info))
    LogUtil.log_info(f"小单资产同步dcs成功，url:{url}, request：{item_no}，resp：{resp}")
    # print(json.dumps(asset_info))
    return item_no
