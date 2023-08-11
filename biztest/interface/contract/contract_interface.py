#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import requests
from biztest.config.contract.contract_interface_params_config import contract_monitor_check_url, \
    before_import_url, import_url, withdraw_success_url, diversion_url, before_register_url, change_channel_url, \
    before_apply_url, payoff_asset_url, fox_sign_url, before_import_void_url, bind_success_url, contract_query_url, sign_url_url
from biztest.util.asserts.assert_util import Assert
from biztest.util.http.http_util import Http as http
from biztest.util.tools.tools import get_guid, get_date
import common.global_const as gc
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no


def monitor_check(timeout=60):
    result = None
    for i in range(timeout):
        url = gc.CONTRACT_URL + contract_monitor_check_url
        try:
            headers = {"Content-Type": "application/json", "Connection": "close"}
            resp = requests.get(url, headers=headers, timeout=10)
            print(resp.status_code)
            if resp.status_code == 200:
                print('monitor check passed')
                result = True
                break
            else:
                result = False
                time.sleep(1)
        except Exception as e:
            print(e)
            result = False
    return result


def bind_success_sign(four_element, sign_company):
    """
    绑卡成功签合同接口
    """
    request_body = {
        "from_system": "paysvr",
        "key": get_guid(),
        "type": "verify",
        "data": {
            "status": 0,
            "sign": "073f6ec2ca75b3cdb85340323bb8f49b",
            "merchant_key": "7979f368bd08fdbf5fa13f0728373a4f",
            "finished_at": "2021-03-11 11:18:32",
            "card_num_encrypt": four_element['data']['bank_code_encrypt'],
            "id_num_encrypt": four_element['data']['id_number_encrypt'],
            "username_encrypt": four_element['data']['user_name_encrypt'],
            "mobile_encrypt": four_element['data']['phone_number_encrypt'],
            "channel_name": "umf_my_protocol",
            "channel_sign_company": sign_company,
            "channel_key": "7979f368bd08fdbf5fa13f0728373a4f",
            "channel_code": "0000",
            "channel_message": "交易成功。",
            "platform_code": "E20000",
            "platform_message": "交易成功"
        }
    }
    contract_url = gc.CONTRACT_URL + bind_success_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contract_url, request_body, header)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


def before_import_sign(item_no, four_element, sub_type, from_app="草莓"):
    """
    进件前签合同接口
    :param item_no:
    :param four_element:
    :param sub_type
    :param from_app
    :return:
    """
    request_body = {
        "data": {
            "date": get_date(fmt="%Y-%m-%d"),
            "identity_encrypt": four_element['data']['id_number_encrypt'],
            "item_no": item_no,
            "mobile_encrypt": four_element['data']['phone_number_encrypt'],
            "name_encrypt": four_element['data']['user_name_encrypt'],
            "sub_type": sub_type,
            "from_app": from_app,
            "address": "上海市长宁区金钟路52号",
            "address_encrypt": "enc_06_3288794171926120448_492"
        },
        "from_system": "DSQ",
        "key": get_guid(),
        "type": "BeforeImport"
    }
    contract_url = gc.CONTRACT_URL + before_import_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contract_url, request_body, header)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


def import_sign(asset_info):
    """
    进件签合同接口
    :param asset_info:
    :return:
    """
    request_body = {
      "type": "AssetImport",
      "key": get_guid(),
      "data": asset_info['data'],
      "from_system": "BIZ"
    }
    contract_url = gc.CONTRACT_URL + import_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contract_url, request_body, header)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


def withdraw_success_sign(asset_info):
    """
    放款成功签合同接口
    :param asset_info:
    :return:
    """
    asset_info['data']['asset']['asset_item_no'] = asset_info['data']['asset']['item_no']
    request_body = {
      "type": "AssetImport",
      "key": get_guid(),
      "data": asset_info['data'],
      "from_system": "BIZ"
    }
    contract_url = gc.CONTRACT_URL + withdraw_success_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contract_url, request_body, header)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


def diversion_sign(apply_code, new_system_name, cover=True):
    """
    导流签合同接口
    :param apply_code:
    :param new_system_name:
    :param cover:
    :return:
    """
    request_body = {
        "applyCode": apply_code,
        "newSystemName": new_system_name,
        "cover": cover
    }
    contract_url = gc.CONTRACT_URL + diversion_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contract_url, request_body, header)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


def before_register_sign(channel, from_system_name, item_no, four_element):
    """
    开户前签合同接口
    :param channel:
    :param from_system_name:
    :param item_no:
    :param four_element:
    :return:
    """
    request_body = {
        "data": {
            "date": get_date(fmt="%Y-%m-%d"),
            "item_no": item_no,
            "identity_encrypt": four_element['data']['id_number_encrypt'],
            "mobile_encrypt": four_element['data']['phone_number_encrypt'],
            "name_encrypt": four_element['data']['user_name_encrypt'],
            "channel": channel,
            "from_system_name": from_system_name
        },
        "from_system": "DSQ",
        "key": get_guid(),
        "type": "BeforeRegister"
    }
    contract_url = gc.CONTRACT_URL + before_register_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contract_url, request_body, header)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


def change_channel(item_no, old_channel, new_channel):
    """
    切资方接口
    :param item_no:
    :param old_channel:
    :param new_channel:
    :return:
    """
    request_body = {
      "apply_code": item_no,
      "loan_channel": new_channel,
      "route_channel": new_channel,
      "old_channel": old_channel,
      "version": time.time(),
      "need_register": 1
    }
    contract_url = gc.CONTRACT_URL + change_channel_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contract_url, request_body, header)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


def before_apply_sign(asset_info):
    """
    进件资方前签合同接口
    """
    # asset_info['data']['asset']['asset_item_no'] = asset_info['data']['asset']['item_no']
    # asset_info = get_asset_import_data_by_item_no(item_no)['data']
    # asset_info['asset']['asset_item_no'] = asset_info['asset']['item_no']
    request_body = {
        "type": "AssetApplyTrailSuccess",
        "key": get_guid(),
        "data": {
          "asset" : {
            "asset_item_no" : asset_info['data']['asset']['item_no'],
            "type" : "paydayloan",
            "sub_type" : "multiple",
            "period_type" : "month",
            "period_count" : asset_info['data']['asset']['period_count'],
            "product_category" : "360",
            "cmdb_product_number" : "lzyh_12_1m_20210203",
            "grant_at" : "2021-08-27 12:07:10",
            "effect_at" : "1000-01-01 00:00:00",
            "actual_grant_at" : "1000-01-01 00:00:00",
            "due_at" : "2022-08-27 00:00:00",
            "payoff_at" : "2022-08-27 00:00:00",
            "from_system" : "strawberry",
            "status" : "sale",
            "principal_amount" : 400000,
            "granted_principal_amount" : 0,
            "loan_channel" : asset_info['data']['asset']['loan_channel'],
            "alias_name" : "S2021082737140602037",
            "interest_amount" : 16436,
            "fee_amount" : 44448,
            "balance_amount" : 0,
            "repaid_amount" : 0,
            "total_amount" : 460884,
            "version" : 1630037229652,
            "interest_rate" : 7.500,
            "charge_type" : 1,
            "ref_order_no" : "",
            "ref_order_amount" : None,
            "ref_order_type" : asset_info['data']['asset']['source_type'],
            "withholding_amount" : 0,
            "sub_order_type" : "",
            "overdue_guarantee_amount" : 0,
            "info" : "",
            "owner" : "KN",
            "risk_level" : "0",
            "product_name" : "",
            "from_app" : asset_info['data']['asset']['from_app'],
            "from_system_name" : ""
          },
        "loan_record": {
            "asset_item_no": "S2021082737140602037",
            "amount": 400000,
            "withholding_amount": 0,
            "channel": "zhongke_lanzhou",
            "status": 1,
            "identifier": "ID508279870299796290",
            "trade_no": "RN508279871464226125",
            "due_bill_no": "",
            "commission_amount": None,
            "pre_fee_amount": None,
            "service_fee_amount": None,
            "is_deleted": None,
            "finish_at": "1000-01-01 00:00:00",
            "trans_property": None,
            "pre_interest": None,
            "commission_amt_interest": None,
            "grant_at": "1000-01-01 00:00:00",
            "push_at": "1000-01-01 00:00:00"
        },
        "dtransactions": [{
            "asset_item_no": "S2021082737140602037",
            "type": "repayprincipal",
            "description": "本金",
            "amount": 32203,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 32203,
            "status": "nofinish",
            "due_at": "2021-09-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 1,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "principal"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayprincipal",
            "description": "本金",
            "amount": 32404,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 32404,
            "status": "nofinish",
            "due_at": "2021-10-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 2,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "principal"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayprincipal",
            "description": "本金",
            "amount": 32607,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 32607,
            "status": "nofinish",
            "due_at": "2021-11-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 3,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "principal"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayprincipal",
            "description": "本金",
            "amount": 32811,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 32811,
            "status": "nofinish",
            "due_at": "2021-12-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 4,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "principal"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayprincipal",
            "description": "本金",
            "amount": 33016,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 33016,
            "status": "nofinish",
            "due_at": "2022-01-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 5,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "principal"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayprincipal",
            "description": "本金",
            "amount": 33222,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 33222,
            "status": "nofinish",
            "due_at": "2022-02-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 6,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "principal"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayprincipal",
            "description": "本金",
            "amount": 33430,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 33430,
            "status": "nofinish",
            "due_at": "2022-03-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 7,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "principal"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayprincipal",
            "description": "本金",
            "amount": 33639,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 33639,
            "status": "nofinish",
            "due_at": "2022-04-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 8,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "principal"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayprincipal",
            "description": "本金",
            "amount": 33849,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 33849,
            "status": "nofinish",
            "due_at": "2022-05-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 9,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "principal"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayprincipal",
            "description": "本金",
            "amount": 34060,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 34060,
            "status": "nofinish",
            "due_at": "2022-06-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 10,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "principal"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayprincipal",
            "description": "本金",
            "amount": 34273,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 34273,
            "status": "nofinish",
            "due_at": "2022-07-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 11,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "principal"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayprincipal",
            "description": "本金",
            "amount": 34486,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 34486,
            "status": "nofinish",
            "due_at": "2022-08-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 12,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "principal"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayinterest",
            "description": "利息",
            "amount": 2500,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2500,
            "status": "nofinish",
            "due_at": "2021-09-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 1,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 11,
            "trade_at": "2021-08-27 12:07:10",
            "category": "interest"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayinterest",
            "description": "利息",
            "amount": 2299,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2299,
            "status": "nofinish",
            "due_at": "2021-10-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 2,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 11,
            "trade_at": "2021-08-27 12:07:10",
            "category": "interest"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayinterest",
            "description": "利息",
            "amount": 2096,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2096,
            "status": "nofinish",
            "due_at": "2021-11-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 3,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 11,
            "trade_at": "2021-08-27 12:07:10",
            "category": "interest"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayinterest",
            "description": "利息",
            "amount": 1892,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1892,
            "status": "nofinish",
            "due_at": "2021-12-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 4,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 11,
            "trade_at": "2021-08-27 12:07:10",
            "category": "interest"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayinterest",
            "description": "利息",
            "amount": 1687,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1687,
            "status": "nofinish",
            "due_at": "2022-01-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 5,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 11,
            "trade_at": "2021-08-27 12:07:10",
            "category": "interest"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayinterest",
            "description": "利息",
            "amount": 1481,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1481,
            "status": "nofinish",
            "due_at": "2022-02-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 6,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 11,
            "trade_at": "2021-08-27 12:07:10",
            "category": "interest"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayinterest",
            "description": "利息",
            "amount": 1273,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1273,
            "status": "nofinish",
            "due_at": "2022-03-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 7,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 11,
            "trade_at": "2021-08-27 12:07:10",
            "category": "interest"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayinterest",
            "description": "利息",
            "amount": 1064,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1064,
            "status": "nofinish",
            "due_at": "2022-04-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 8,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 11,
            "trade_at": "2021-08-27 12:07:10",
            "category": "interest"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayinterest",
            "description": "利息",
            "amount": 854,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 854,
            "status": "nofinish",
            "due_at": "2022-05-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 9,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 11,
            "trade_at": "2021-08-27 12:07:10",
            "category": "interest"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayinterest",
            "description": "利息",
            "amount": 643,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 643,
            "status": "nofinish",
            "due_at": "2022-06-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 10,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 11,
            "trade_at": "2021-08-27 12:07:10",
            "category": "interest"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayinterest",
            "description": "利息",
            "amount": 430,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 430,
            "status": "nofinish",
            "due_at": "2022-07-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 11,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 11,
            "trade_at": "2021-08-27 12:07:10",
            "category": "interest"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "repayinterest",
            "description": "利息",
            "amount": 217,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 217,
            "status": "nofinish",
            "due_at": "2022-08-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 12,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 11,
            "trade_at": "2021-08-27 12:07:10",
            "category": "interest"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "grant",
            "description": "放款",
            "amount": 400000,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 400000,
            "status": "nofinish",
            "due_at": "2021-08-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 0,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 1,
            "trade_at": "2021-08-27 12:07:10",
            "category": "grant"
        }],
        "fees": [{
            "asset_item_no": "S2021082737140602037",
            "type": "reserve",
            "description": "风险保障金",
            "amount": 2070,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2070,
            "status": "nofinish",
            "due_at": "2021-09-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 1,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "reserve",
            "description": "风险保障金",
            "amount": 2070,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2070,
            "status": "nofinish",
            "due_at": "2021-10-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 2,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "reserve",
            "description": "风险保障金",
            "amount": 2070,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2070,
            "status": "nofinish",
            "due_at": "2021-11-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 3,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "reserve",
            "description": "风险保障金",
            "amount": 2070,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2070,
            "status": "nofinish",
            "due_at": "2021-12-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 4,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "reserve",
            "description": "风险保障金",
            "amount": 2070,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2070,
            "status": "nofinish",
            "due_at": "2022-01-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 5,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "reserve",
            "description": "风险保障金",
            "amount": 2070,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2070,
            "status": "nofinish",
            "due_at": "2022-02-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 6,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "reserve",
            "description": "风险保障金",
            "amount": 2070,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2070,
            "status": "nofinish",
            "due_at": "2022-03-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 7,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "reserve",
            "description": "风险保障金",
            "amount": 2070,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2070,
            "status": "nofinish",
            "due_at": "2022-04-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 8,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "reserve",
            "description": "风险保障金",
            "amount": 2070,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2070,
            "status": "nofinish",
            "due_at": "2022-05-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 9,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "reserve",
            "description": "风险保障金",
            "amount": 2070,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2070,
            "status": "nofinish",
            "due_at": "2022-06-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 10,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "reserve",
            "description": "风险保障金",
            "amount": 2070,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2070,
            "status": "nofinish",
            "due_at": "2022-07-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 11,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "reserve",
            "description": "风险保障金",
            "amount": 2070,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 2070,
            "status": "nofinish",
            "due_at": "2022-08-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 12,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "guarantee",
            "description": "保障金",
            "amount": 181,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 181,
            "status": "nofinish",
            "due_at": "2021-09-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 1,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "guarantee",
            "description": "保障金",
            "amount": 181,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 181,
            "status": "nofinish",
            "due_at": "2021-10-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 2,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "guarantee",
            "description": "保障金",
            "amount": 181,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 181,
            "status": "nofinish",
            "due_at": "2021-11-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 3,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "guarantee",
            "description": "保障金",
            "amount": 181,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 181,
            "status": "nofinish",
            "due_at": "2021-12-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 4,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "guarantee",
            "description": "保障金",
            "amount": 181,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 181,
            "status": "nofinish",
            "due_at": "2022-01-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 5,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "guarantee",
            "description": "保障金",
            "amount": 181,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 181,
            "status": "nofinish",
            "due_at": "2022-02-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 6,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "guarantee",
            "description": "保障金",
            "amount": 181,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 181,
            "status": "nofinish",
            "due_at": "2022-03-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 7,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "guarantee",
            "description": "保障金",
            "amount": 181,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 181,
            "status": "nofinish",
            "due_at": "2022-04-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 8,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "guarantee",
            "description": "保障金",
            "amount": 181,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 181,
            "status": "nofinish",
            "due_at": "2022-05-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 9,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "guarantee",
            "description": "保障金",
            "amount": 181,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 181,
            "status": "nofinish",
            "due_at": "2022-06-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 10,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "guarantee",
            "description": "保障金",
            "amount": 181,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 181,
            "status": "nofinish",
            "due_at": "2022-07-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 11,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "guarantee",
            "description": "保障金",
            "amount": 181,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 181,
            "status": "nofinish",
            "due_at": "2022-08-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 12,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "consult",
            "description": "咨询服务费",
            "amount": 1453,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1453,
            "status": "nofinish",
            "due_at": "2021-09-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 1,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "consult",
            "description": "咨询服务费",
            "amount": 1453,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1453,
            "status": "nofinish",
            "due_at": "2021-10-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 2,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "consult",
            "description": "咨询服务费",
            "amount": 1453,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1453,
            "status": "nofinish",
            "due_at": "2021-11-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 3,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "consult",
            "description": "咨询服务费",
            "amount": 1453,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1453,
            "status": "nofinish",
            "due_at": "2021-12-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 4,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "consult",
            "description": "咨询服务费",
            "amount": 1453,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1453,
            "status": "nofinish",
            "due_at": "2022-01-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 5,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "consult",
            "description": "咨询服务费",
            "amount": 1453,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1453,
            "status": "nofinish",
            "due_at": "2022-02-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 6,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "consult",
            "description": "咨询服务费",
            "amount": 1453,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1453,
            "status": "nofinish",
            "due_at": "2022-03-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 7,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "consult",
            "description": "咨询服务费",
            "amount": 1453,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1453,
            "status": "nofinish",
            "due_at": "2022-04-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 8,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "consult",
            "description": "咨询服务费",
            "amount": 1453,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1453,
            "status": "nofinish",
            "due_at": "2022-05-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 9,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "consult",
            "description": "咨询服务费",
            "amount": 1453,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1453,
            "status": "nofinish",
            "due_at": "2022-06-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 10,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "consult",
            "description": "咨询服务费",
            "amount": 1453,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1453,
            "status": "nofinish",
            "due_at": "2022-07-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 11,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }, {
            "asset_item_no": "S2021082737140602037",
            "type": "consult",
            "description": "咨询服务费",
            "amount": 1453,
            "decrease_amount": 0,
            "repaid_amount": 0,
            "balance_amount": 0,
            "total_amount": 1453,
            "status": "nofinish",
            "due_at": "2022-08-27 00:00:00",
            "finish_at": "1000-01-01 00:00:00",
            "period": 12,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 21,
            "trade_at": "2021-08-27 12:07:10",
            "category": "fee"
        }],
        "cards_info": {
            "repay_card": {
                "account_num_encrypt": "enc_03_3203321852693317632_406",
                "account_type": "debit",
                "bank_code": "ccb",
                "bankname": "中国建设银行",
                "credentials_num_encrypt": "enc_02_3203317862383488000_189",
                "credentials_type": "0",
                "individual_idnum_encrypt": "enc_02_3203317862383488000_189",
                "phone_encrypt": "enc_01_17193434410_210",
                "username_encrypt": "enc_04_3966207350_992"
            },
            "receive_card": {
                "account_name_encrypt": "enc_04_3966207350_992",
                "bank": "中国建设银行",
                "bank_code": "ccb",
                "name": "中国建设银行",
                "num_encrypt": "enc_03_3203321852693317632_406",
                "owner_id_encrypt": "enc_02_3203317862383488000_189",
                "owner_name_encrypt": "enc_04_3966207350_992",
                "type": "individual",
                "phone_encrypt": "enc_01_17193434410_210",
                "factor_by": 4
            }
        }
        },
        "from_system": "BIZ"
    }
    contract_url = gc.CONTRACT_URL + before_apply_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contract_url, request_body, header)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


def payoff_asset_sign(item_no, period):
    """
    资产逾期结清签合同接口
    """
    request_body = {
      "asset_item_no": item_no,
      "settle_periods": [
        {
          "period": period,
          "finish_at": "2022-11-01 11:23:34"
        }
      ]
    }
    contract_url = gc.CONTRACT_URL + payoff_asset_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contract_url, request_body, header)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


def fox_sign(item_no, sign_type):
    """
    贷后法催签合同接口
    """
    request_body = {
        "type": "FoxContractSign",
        "key": get_guid(),
        "from_system": "fox",
        "data": {
            "item_no": item_no,
            "type": sign_type
        }
    }
    contract_url = gc.CONTRACT_URL + fox_sign_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contract_url, request_body, header)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


def before_import_void(id_num):
    """
    进件前合同作废接口
    """
    request_body = {
        "data": {
            "identity_encrypt": id_num,
            "from_app": "草莓"
        },
        "from_system": "DSQ",
        "key": get_guid(),
        "type": "BeforeImportVoid"
    }

    contract_url = gc.CONTRACT_URL + before_import_void_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contract_url, request_body, header)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


def contract_query(item_no, type_list=None):
    """
    查询合同
    """
    request_body = {
        "type": None,
        "types": [x for x in type_list] if type_list else None,
        "item_no": item_no,
        "item_nos": None,
        "need_sign": True
    }
    contract_url = gc.CONTRACT_URL + contract_query_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contract_url, request_body, header)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


def sign_url(url):
    """
    加签
    """
    params = {
        "url": url
    }
    contract_url = gc.CONTRACT_URL + sign_url_url
    header = {"Content-Type": "application/json"}
    resp = http.http_get(contract_url, params=params)
    Assert.assert_equal(0, resp['code'], resp)
    return resp


if __name__ == '__main__':
    gc.init_env(1, "china", "dev")
    # before_apply_sign("20201628764985442175")
    payoff_asset_sign("20201619588929798999_noloan", 4)