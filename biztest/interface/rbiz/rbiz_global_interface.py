# -*- coding: utf-8 -*-
import json
import time
from copy import deepcopy

import requests

from biztest.config.global_rbiz.global_rbiz_interface_params_config import global_asset
from biztest.config.rbiz.params_config import capital_asset

from biztest.config.rbiz.url_config import *
from biztest.function.global_gbiz.gbiz_global_db_function import get_asset_from_asset, get_trans_from_asset_tran, \
    get_loan_record_from_asset, get_borrower_from_asset_card, get_asset_info_by_item_no, \
    get_capital_transaction_principal_from_asset_tran, get_capital_transaction_fees_from_asset_tran
from biztest.function.global_rbiz.rbiz_global_db_function import get_refund_request, get_withdraw
from biztest.interface.rbiz.rbiz_global_config import rbiz_asset_import_url
from biztest.util.http.http_util import Http
from biztest.util.log.log_util import LogUtil
from biztest.util.tools.tools import get_guid, parse_resp_body, get_date_timestamp, get_date, get_random_str, \
    get_timestamp_by_now, get_tz
import common.global_const as gc

"""
小语种还款系统的主要接口
"""


def monitor_check(timeout=60):
    result = None
    for i in range(timeout):
        url = gc.REPAY_URL + rbiz_monitor_check_url
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
        except:
            result = False
    return result


def combo_active_repay(**kwargs):
    """
    主动合并代扣接口
    """
    card_uuid = kwargs["card_uuid"]
    individual_uuid = kwargs.get("individual_uuid", "")
    email = kwargs.get("email", "")
    id_num = kwargs["id_num"]
    user_id = kwargs["user_id"]
    user_name = kwargs.get("user_name", "")
    mobile = kwargs["mobile"]
    repay_type = kwargs.get("repay_type", None)
    coupon_num = kwargs.get("coupon_num", None)
    coupon_amount = kwargs.get("coupon_amount", None)
    project_num_loan_channel = kwargs.get("project_num_loan_channel", None)
    project_num_loan_channel_amount = kwargs.get("project_num_loan_channel_amount", None)
    total_amount = project_num_loan_channel_amount
    redirect_url = kwargs.get("redirect_url", "https://www.baidu.com")
    payment_option = kwargs.get("payment_option", "")
    payment_type = kwargs.get("payment_type", "ebank")
    payment_mode = kwargs.get("payment_mode", "")
    card_num_encrypt = kwargs.get("card_num_encrypt", "")

    url = gc.REPAY_URL + combo_active_path
    request_body = {
        "from_system": "DSQ",
        "key": get_guid(),
        "type": "CombineWithholdTaskHandler",
        "data": {
            "from_app": "testapp",
            "card_uuid": card_uuid,
            "individual_uuid": individual_uuid,
            "id_num": id_num,
            "user_id": user_id,
            "user_name": user_name,
            "mobile": mobile,
            "email": email,
            "redirect_url": redirect_url,
            "repay_type": repay_type,
            "total_amount": total_amount,
            "project_list": [
                {
                    "priority": 1,
                    "project_num": project_num_loan_channel,
                    "amount": project_num_loan_channel_amount,
                    "coupon_list": [
                        {"coupon_num": coupon_num,
                         "coupon_amount": coupon_amount,
                         "coupon_type": "cash"}] if coupon_num is not None else None
                }
            ],
            "order_no": "",
            "verify_code": "",
            "verify_seq": "",
            "payment_type": payment_type,
            "payment_option": payment_option,
            "payment_mode": payment_mode,
            "card_cvv": "111",
            "card_num_encrypt": card_num_encrypt,
            "card_expiry_year": "29",
            "card_expiry_month": "05",
            "device_info": {
                "system_name": "android",
                "system_version": "10"
            },
            "sdk_info": [
                {
                    "name": "test",
                    "version": "1.0.1"
                }
            ]
        }
    }

    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        LogUtil.log_info(
            f"主动代扣发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
        return resp, request_body
    except Exception as e:
        raise Exception("主动合并代扣失败")


def combo_active_repay_with_no_loan(**kwargs):
    """
    主动合并代扣接口
    """
    card_uuid = kwargs["card_uuid"]
    id_num = kwargs["id_num"]
    user_id = kwargs["user_id"]
    mobile = kwargs["mobile"]
    repay_type = kwargs.get("repay_type", None)
    coupon_num = kwargs.get("coupon_num", None)
    coupon_amount = kwargs.get("coupon_amount", None)
    project_num_loan_channel = kwargs.get("project_num_loan_channel", None)
    project_num_loan_channel_amount = kwargs.get("project_num_loan_channel_amount", None)
    project_num_no_loan = kwargs.get("project_num_no_loan", project_num_loan_channel + "x")
    project_num_no_loan_amount = kwargs.get("project_num_no_loan_amount", None)
    total_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
    payment_type = kwargs.get("payment_type", "checkout")
    payment_option = kwargs.get("payment_option", "")
    coupon_list = [{"coupon_num": coupon_num,
                    "coupon_amount": coupon_amount,
                    "coupon_type": "cash"}] if coupon_num is not None else None

    url = gc.REPAY_URL + combo_active_path
    request_body = {
        "from_system": "DSQ",
        "key": get_guid(),
        "type": "CombineWithholdTaskHandler",
        "data": {
            "card_uuid": card_uuid,
            "mobile": mobile,
            "id_num": id_num,
            "user_id": user_id,
            "total_amount": total_amount,
            "redirect_url": "https://www.baidu.com",
            "repay_type": repay_type,
            "project_list": [
                {
                    "priority": 2,
                    "project_num": project_num_loan_channel,
                    "amount": project_num_loan_channel_amount,
                    "coupon_list": coupon_list
                },
                {
                    "priority": 1,
                    "project_num": project_num_no_loan,
                    "amount": project_num_no_loan_amount
                }
            ],
            "order_no": "",
            "verify_code": "",
            "verify_seq": "",
            "payment_type": payment_type,
            "payment_option": payment_option,
            "payment_mode": "",
            "device_info": {
                "system_name": "android",
                "system_version": "10"
            },
            "sdk_info": [
                {
                    "name": "test",
                    "version": "1.0.1"
                }
            ]
        }
    }

    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        LogUtil.log_info(
            f"主动代扣发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
        return resp, request_body
    except Exception as e:
        raise Exception("主动合并代扣失败")


def transaction_confirm(order_no, transaction_no=None):
    url = gc.REPAY_URL + transaction_confirm_path
    if transaction_no is None:
        transaction_no = get_random_str(10)
    request_body = {
        "from_system": "dcq",
        "key": get_guid(),
        "type": "TransactionConfirm",
        "data": {
            "order_no": order_no,
            "transaction_no": transaction_no
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
    LogUtil.log_info(
        f"transaction confirm发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def refresh_late_fee(asset_item_no):
    """
    逾期资产刷新罚息的接口
    :param asset_item_no: 资产编号
    :return:返回一个json，包含code,message,data=null
                example:
                    {
                    "code": 0,
                    "message": "处理成功",
                    "data": null
                }
    """
    url = gc.REPAY_URL + refresh_late_fee_path
    request_body = {
        "from_system": "Biz",
        "type": "RbizRefreshLateInterest",
        "key": get_guid(),
        "data": {
            "asset_item_no": asset_item_no
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
    LogUtil.log_info(
        f"refresh late发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def paysvr_callback(merchant_key, pay_amount, is_success=2, channel_name="auto_thailand_channel",
                    finished_at=None, original_merchant_key=None):
    if finished_at is None:
        finished_at = get_date(timezone=get_tz(gc.COUNTRY))
    url = gc.REPAY_URL + paysvr_callback_path
    req_body = {
        "from_system": "paysvr",
        "key": get_guid(),
        "type": "withhold",
        "data": {
            "amount": pay_amount,
            "merchant_key": merchant_key,
            "channel_key": merchant_key + "_C",
            "status": is_success,
            "finished_at": finished_at,
            "platform_message": "Transaction Successful",
            "platform_code": "E20000",
            "channel_name": channel_name,
            "channel_code": "KN_REQUEST_SUCCESS",
            "channel_message": "KN_REQUEST_SUCCESS",
            "payment_type": "ebank",
            "payment_mode": "",
            "original_merchant_key": original_merchant_key
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    url = gc.REPAY_URL + "/task/run?orderNo=" + str(merchant_key)
    Http.http_get(url, headers={"Content-Type": "application/json"})
    LogUtil.log_info(
        f"paysvr callback发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp, req_body


def paysvr_trade_callback(merchant_key, pay_amount, is_success=2, channel_name="cashfree_yomoyo_ebank",
                          finished_at=None):
    if finished_at is None:
        finished_at = get_date(timezone=get_tz(gc.COUNTRY))
    url = gc.REPAY_URL + paysvr_trade_callback_path
    req_body = {
        "from_system": "paysvr",
        "key": get_guid(),
        "type": "withhold",
        "data": {
            "amount": pay_amount,
            "merchant_key": merchant_key,
            "channel_key": merchant_key + "_C",
            "status": is_success,
            "finished_at": finished_at,
            "platform_message": "Transaction Successful",
            "platform_code": "E20000",
            "channel_name": channel_name,
            "channel_code": "KN_REQUEST_SUCCESS",
            "channel_message": "KN_REQUEST_SUCCESS",
            "payment_type": "ebank",
            "payment_mode": "",
            "original_merchant_key": ""
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"paysvr trade callback发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp, req_body


def paysvr_smart_collect_callback(account_no, pay_amount, finished_at=None):
    if finished_at is None:
        finished_at = get_date(timezone=get_tz(gc.COUNTRY))
    url = gc.REPAY_URL + global_paysvr_smart_collect_path
    req_body = {
        "from_system": "paysvr",
        "key": get_guid() + "cl",
        "type": "withhold",
        "data": {
            "amount": pay_amount,
            "merchant_key": get_random_str(),
            "channel_key": get_random_str(),
            "status": 2,
            "finished_at": finished_at,
            "channel_name": "pandapay_test_collect",
            "channel_code": "KN_COLLECT_SUCCESS",
            "channel_message": "KN_COLLECT_SUCCESS",
            "platform_message": "Transaction Successful",
            "platform_code": "E20000",
            "card_uuid": "",
            "account_no": account_no,
            "payment_type": "collect",
            "payment_mode": "",
            "original_merchant_key": ""
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=req_body))
    LogUtil.log_info(
        f"paysvr smart collect callback发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，"
        f"resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp, req_body


def paysvr_query_tolerance_result(serial_no, pay_amount=100000):
    url = gc.REPAY_URL + global_paysvr_query_tolerance_result_path.format(serial_no, pay_amount)
    resp = parse_resp_body(
        requests.request(method='get', url=url, headers={"content-type": "application/json"}))
    LogUtil.log_info(
        f"paysvr query tolerance result发起成功，url:{url}, resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def repay_trial(item_no, period=None):
    url = gc.REPAY_URL + repay_trial_path
    req_body = {
        "asset_item_no": item_no,
        "period": period
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=req_body))
    LogUtil.log_info(
        f"repay-trial发起成功，url:{url}, resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def repay_offline_withhold_apply(**kwargs):
    """
    泰国线下还款
    """
    item_no = kwargs.get("item_no", None)
    amount = kwargs.get("amount", None)

    url = gc.REPAY_URL + offline_withhold_apply
    request_body = {
        "from_system": "dsq",
        "key": get_guid(),
        "type": "OfflineWithhold",
        "data": {
            "item_no": item_no,
            "amount": amount
        }
    }

    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        LogUtil.log_info(
            f"线下还款申请发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
        return resp, request_body
    except Exception as e:
        raise Exception("线下还款申请发起失败")


def repay_offline_withhold_confirm(**kwargs):
    """
    泰国线下还款确认
    """
    item_no = kwargs.get("item_no", None)
    amount = kwargs.get("amount", None)
    merchant_key = kwargs.get("merchant_key", None)
    request_no = kwargs.get("request_no", None)
    bank_code = kwargs.get("bank_code", None)
    card_no = kwargs.get("card_no", None)
    transaction_no = kwargs.get("transaction_no", None)

    url = gc.REPAY_URL + offline_withhold_confirm
    request_body = {
        "from_system": "dsq",
        "key": get_guid(),
        "type": "OfflineWithholdConfirm",
        "data": {
            "card_no": card_no,
            "transaction_no": transaction_no,
            "item_no": item_no,
            "amount": amount,
            "request_no": request_no,
            "order_no": merchant_key,
            "bank_code": bank_code,
            "payment_serial_no": [
                "https://2c6b8dad.oss-ap-southeast-1.aliyuncs.com/ocrphoto/ocr-photo-76220300798197760-1594278724708.jpg",
                "https://dxcloud-sh-eday-test.oss-cn-shanghai.aliyuncs.com/ocrphoto/ocr-photo-67029869719977984-1594797535339.jpg",
                "https://dxcloud-sh-eday-test.oss-cn-shanghai.aliyuncs.com/ocrphoto/ocr-photo-79443516488417280-1595235059113.jpg",
                "https://dxcloud-sh-eday-test.oss-cn-shanghai.aliyuncs.com/ocrphoto/ocr-photo-79443516488417280-1595235329992.jpg"]
        }
    }

    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        LogUtil.log_info(
            f"线下还款确认发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
        return resp, request_body
    except Exception as e:
        raise Exception("线下还款申请发起失败")


def repay_offline_withhold_deal(**kwargs):
    """
    线下还款人工处理
    :param kwargs:
    :return:
    """
    url = gc.REPAY_URL + offline_withhold_deal
    request_body = {
        "from_system": "biz",
        "key": get_guid(),
        "type": "OfflineWithholdDeal",
        "data": {
            "card_no": "enc_03_3573347754854320128_693",
            "serial_no": kwargs.get("serial_no", ""),
            "item_no": kwargs.get("item_no", ""),
            "request_no": kwargs.get("request_no", ""),
            "amount": 100,
            "status": kwargs.get("status"),
            "comment": "成功" if kwargs.get("status") == "success" else "失败",
            "trade_id": kwargs.get("trade_id", "")
        }
    }
    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        LogUtil.log_info(
            f"线下还款人工处理发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，"
            f"resp：{json.dumps(resp['content'], ensure_ascii=False)}")
        return resp
    except Exception as e:
        raise Exception("线下还款人工处理发起失败")


def project_repay_query(project_num, project_type="paydayloan"):
    url = gc.REPAY_URL + global_project_repay_query_path.format(project_num, project_type)
    resp = parse_resp_body(requests.request(method='get', url=url))
    return resp, url


def available_refund_query(item_no, from_system="biz"):
    url = gc.REPAY_URL + global_refund_query_path.format(item_no, from_system)
    resp = parse_resp_body(requests.request(method='get', url=url))
    return resp, url


def combo_query_key(key):
    url = gc.REPAY_URL + combo_query_key_path
    req_body = {
        "type": "PaydayloanUserActiveRepay",
        "key": key,
        "from_system": "DSQ"
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    return resp, req_body, url


def combo_active_repay_sdk(**kwargs):
    """
    主动合并代扣接口
    :param kwargs:包括用户信息，资产编号，金额，优惠券信息，协议支付验证码，优先级
    :return: 返回一个json包括code,message，data等信息
             example:
                {
                    "code": 0,
                    "message": "交易处理中",
                    "data": {
                        "type": "URL",
                        "content": "支付页面地址",
                        "project_list": [
                            {
                                "status": 2,
                                "memo": "交易处理中",
                                "project_num": "qnn20191580725153431066",
                                "order_no": "YX_HM402062311114552733",
                                "error_code": "E20017"
                            }
                        ]
                    }
                }
    """
    card_uuid = kwargs["card_uuid"]
    id_num = kwargs["id_num"]
    user_id = kwargs["user_id"]
    mobile = kwargs["mobile"]
    project_num_loan_channel = kwargs.get("project_num_loan_channel", None)
    project_num_no_loan = kwargs.get("project_num_no_loan", None)
    project_num_loan_channel_priority = kwargs.get("project_num_loan_channel_priority", None)
    project_num_no_loan_priority = kwargs.get("project_num_no_loan_priority", None)
    project_num_loan_channel_amount = kwargs.get("project_num_loan_channel_amount", None)
    project_num_no_loan_amount = kwargs.get("project_num_no_loan_amount", None)
    total_amount = kwargs["total_amount"]
    coupon_num = kwargs["coupon_num"] if "coupon_num" in kwargs else None
    coupon_amount = kwargs["coupon_amount"] if "coupon_amount" in kwargs else None
    order_no = kwargs["order_no"] if "order_no" in kwargs else ""
    verify_code = kwargs["verify_code"] if "verify_code" in kwargs else ""
    verify_seq = kwargs["verify_seq"] if "verify_seq" in kwargs else ""

    url = gc.REPAY_URL + combo_active_path
    request_body = {
        "from_system": "DSQ",
        "key": get_guid(),
        "type": "CombineWithholdTaskHandler",
        "data": {
            "card_uuid": card_uuid,
            "mobile": mobile,
            "id_num": id_num,
            "user_id": user_id,
            "total_amount": total_amount,
            "order_no": order_no,
            "verify_code": verify_code,
            "verify_seq": verify_seq,
            "user_ip": "10.10.10.127",
            "redirect_url": "http://xxxxxxxxx/",
            "project_list": [
                {
                    "priority": 1,
                    "project_num": project_num_loan_channel,
                    "amount": project_num_loan_channel_amount,
                    "coupon_num": coupon_num,
                    "coupon_amount": coupon_amount
                }
            ],
            "payment_type": "sdk",
            "payment_option": "upi",
            "device_info": {
                "system_name": "android",
                "system_version": "10"
            },
            "sdk_info": [
                {
                    "name": "cashfree",
                    "version": "1.0.1"
                }
            ]
        }
    }

    if project_num_loan_channel and project_num_no_loan is None:
        request_body['data']['project_list'][0]['priority'] = project_num_loan_channel_priority
        request_body['data']['project_list'][0]['project_num'] = project_num_loan_channel
        request_body['data']['project_list'][0]['amount'] = project_num_loan_channel_amount
    elif project_num_no_loan and project_num_loan_channel is None:
        request_body['data']['project_list'][0]['priority'] = project_num_no_loan_priority
        request_body['data']['project_list'][0]['project_num'] = project_num_no_loan
        request_body['data']['project_list'][0]['amount'] = project_num_no_loan_amount
    elif project_num_no_loan and project_num_loan_channel:
        request_body['data']['project_list'].append({
            "priority": 1,
            "project_num": "ZZ_zjf_3qi_65268xiaodan",
            "amount": 80027,
            "coupon_num": "",
            "coupon_amount": ""
        })
        request_body['data']['project_list'][0]['priority'] = project_num_loan_channel_priority
        request_body['data']['project_list'][0]['project_num'] = project_num_loan_channel
        request_body['data']['project_list'][0]['amount'] = project_num_loan_channel_amount
        request_body['data']['project_list'][1]['priority'] = project_num_no_loan_priority
        request_body['data']['project_list'][1]['project_num'] = project_num_no_loan
        request_body['data']['project_list'][1]['amount'] = project_num_no_loan_amount

    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        LogUtil.log_info(
            f"SDK代扣发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
        return resp, request_body
    except Exception as e:
        raise Exception("主动合并代扣失败")


def trade_withhold(item_no, trade_type, delay_amount, payment_type="", payment_option="", payment_mode="",
                   period_list=None, delay_days=7, four_element=None):
    url = gc.REPAY_URL + trade_withhold_path
    req_key = get_guid()
    req_body = {
        "from_system": "eday",
        "key": req_key,
        "type": "TradeOrderApply",
        "data": {
            "from_app": "testapp",
            "owner": "test",
            "ref_no": get_guid(),
            "trade_type": trade_type,
            "payment_type": payment_type,
            "payment_option": payment_option,
            "payment_mode": payment_mode,
            "amount": delay_amount,
            "user_id": four_element['data']['id_number'],
            "card_uuid": four_element['data']['card_num'],
            "user_ip": "10.10.10.10",
            "redirect_url": "http://xxxxxxxxx/",
            "delay_assets": [],
        }
    }
    for period in period_list:
        if period != max(period_list):
            delay_asset_temp = {
                "item_no": item_no,
                "period": period,
                "delay_days": delay_days,
                "delay_amount": delay_amount // len(period_list),
                "total_amount": delay_amount // len(period_list)
            }
        else:
            delay_asset_temp = {
                "item_no": item_no,
                "period": period,
                "delay_days": delay_days,
                "delay_amount": (delay_amount // len(period_list)) + (delay_amount % len(period_list)),
                "total_amount": (delay_amount // len(period_list)) + (delay_amount % len(period_list)),
            }
        req_body["data"]["delay_assets"].append(delay_asset_temp)
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"订单代扣发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def tran_decrease(item_no, decrease_type, amount, period=1):
    url = gc.REPAY_URL + asset_tran_decrease_path
    req_body = {
        "from_system": "biz",
        "type": "FoxDecreaseLateInterest",
        "key": get_guid(),
        "data": {
            "operator_name": "autotest",
            "amount": amount,
            "period": period,
            "asset_item_no": item_no,
            "operator_id": "",
            "type": decrease_type
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"tran减免成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def fox_withhold(**kwargs):
    """
    贷后手动代扣接口
    :param kwargs: dict包含个人信息,代扣金额,资产编号,代扣期次
    :return: json
        example:
            {
                "code": 2,
                "message": "交易处理中",
                "data": null
            }
    """
    url = gc.REPAY_URL + fox_withhold_path
    item_no = kwargs['item_no']
    amount = kwargs['amount']
    user_id = kwargs["four_element"]['data']['id_number']
    payment_type = kwargs.get("payment_type", None)
    payment_mode = kwargs.get("payment_mode", None)
    payment_option = kwargs.get("payment_option", None)

    request_body = {
        "from_system": "fox",
        "key": "fox" + item_no,
        "type": "FoxManualWithhold",
        "data": {
            "item_no": item_no,
            "payment_type": payment_type,
            "payment_option": payment_option,
            "payment_mode": payment_mode,
            "amount": amount,
            "user_id": user_id,
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
    LogUtil.log_info(
        f"fox代扣发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp, request_body


def fox_withhold_query(req_key):
    url = gc.REPAY_URL + fox_withhold_query_path.format(req_key)
    resp = parse_resp_body(requests.request(method='get', url=url))
    LogUtil.log_info(
        f"fox_withhold_query发起成功，url:{url}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp, url


def fox_overdue_view(item_no):
    url = gc.REPAY_URL + fox_overdue_view_for_fox_path.format(item_no)
    resp = parse_resp_body(requests.request(method='get', url=url))
    LogUtil.log_info(
        f"fox_overdue_view发起成功，url:{url}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp, url


def fox_deadline_asset_query(due_date=get_date(fmt="%Y-%m-%d")):
    url = gc.REPAY_URL + fox_deadline_asset_query_path
    req_body = {
        "due_date": due_date,
        "page_size": 10000
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"fox_deadline_asset_query发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp, url


def fox_query_asset_repay():
    url = gc.REPAY_URL + fox_query_asset_repay_path
    req_body = {
        "end_date": get_date(fmt="%Y-%m-%d"),
        "start_date": get_date(fmt="%Y-%m-%d"),
        "page_size": 1000,
        "page_index": 1
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"fox查询资产还款成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp, url


def fox_query_asset_repay_detail(item_no, repay_date=get_date(fmt="%Y-%m-%d")):
    url = gc.REPAY_URL + fox_query_asset_repay_detail_path.format(item_no, repay_date)
    resp = parse_resp_body(requests.request(method='get', url=url))
    LogUtil.log_info(
        f"fox查询资产还款详情，url:{url}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp, url


def fox_query_new_overdue():
    url = gc.REPAY_URL + fox_query_new_overdue_path.format(get_date(fmt="%Y-%m-%d"), get_date(fmt="%Y-%m-%d"))
    resp = parse_resp_body(requests.request(method='get', url=url))
    LogUtil.log_info(
        f"fox查询新过期资产，url:{url}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp, url


def fox_query_withhold_records(id_num):
    url = gc.REPAY_URL + fox_query_withhold_records_path
    req_body = {
        "from_system": "fox",
        "type": "QueryWithhold",
        "key": get_guid(),
        "data": {
            "id_num": id_num,
            "start_date": "2020-08-19",
            "end_date": "2021-08-20"
        }
    }
    resp = parse_resp_body(requests.request(method='post', json=req_body, url=url))
    return resp, url


def fox_cancel_and_decrease(item_no, amount=100, period=1):
    url = gc.REPAY_URL + fox_cancel_and_decrease_path
    req_body = {
        "key": get_guid(),
        "type": "CancelAndDecrease",
        "from_system": "Fox",
        "data": {
            "asset_item_no": item_no,
            "period": period,
            "amount": amount,
            "comment": "罚息减免",
            "operator_id": 1,
            "operator_name": "autotest"
        }
    }
    resp = parse_resp_body(requests.request(method='post', json=req_body, url=url))
    LogUtil.log_info(
        f"关单&减免发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def withhold_refund_online(item_no, withhold_serial_no, refund_amount, refund_card_uuid, refund_channel,
                           refund_type="ONLINE"):
    url = gc.REPAY_URL + global_refund_online_path
    req_key = get_guid()
    req_body = {
        "from_system": "biz",
        "key": req_key,
        "type": "OnlineRepeatRefund",
        "data": {
            "item_no": item_no,
            "refund_withhold_serial_no": withhold_serial_no,
            "refund_amount": refund_amount,
            "refund_card_uuid": refund_card_uuid,
            "refund_channel": refund_channel,
            "refund_type": refund_type,
            "operator": "auto_test"
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"线上代扣退款发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def withhold_refund_offline(item_no, withhold_serial_no, refund_amount, refund_card_uuid, refund_channel):
    url = gc.REPAY_URL + global_refund_offline_path
    req_key = get_guid()
    req_body = {
        "from_system": "biz",
        "key": req_key,
        "type": "OfflineRepeatRefund",
        "data": {
            "item_no": item_no,
            "refund_withhold_serial_no": withhold_serial_no,
            "refund_amount": refund_amount,
            "refund_card_uuid": refund_card_uuid,
            "refund_channel": refund_channel,
            "refund_type": "OFFLINE",
            "operator": "auto_test"
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"线下代扣退款发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def trade_refund(merchant_key, refund_amount, refund_type=2, channel_name="razorpay_yomoyo_collect"):
    url = gc.REPAY_URL + trade_refund_path
    req_body = {
        "from_system": "dsq",
        "key": get_guid(),
        "type": "TradeOrderRefundApply",
        "data": {
            "trade_no": merchant_key,
            "amount": refund_amount,
            "refund_type": refund_type,
            "refund_channel": channel_name
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"paysvr_refund_callback发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp, req_body


def force_refund(merchant_key, refund_amount, item_no_list=[], channel_name="baofoo_tq5"):
    url = gc.REPAY_URL + force_refund_path
    req_key = get_guid()
    req_body = {
        "type": "ForceWithholdRefund",
        "key": req_key,
        "from_system": "biz",
        "data": {
            "withhold_result_serial_no": merchant_key,
            "operator": "朱莎莎",
            "amount": refund_amount,
            "refund_type": 2,
            "refund_channel": channel_name,
            "detail_list": item_no_list
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"代扣退款发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def refund_callback(serial_no, pay_status=2):
    refund_request = get_refund_request(refund_request_withhold_serial_no=serial_no)[-1]
    url = gc.REPAY_URL + globak_refund_callback_path
    req_body = {"from_system": "paysvr",
                "key": get_random_str(),
                "type": "refund",
                "data": {
                    "amount": refund_request["refund_request_amount"],
                    "status": pay_status,
                    "merchant_key": refund_request["refund_request_serial_no"],
                    "finished_at": get_date(timezone=get_tz()),
                    "channel_name": "refund_callback_channel",
                    "channel_key": "refund_" + get_random_str(10),
                    "channel_code": "callback_code",
                    "channel_message": "callback_message"
                }}
    resp = parse_resp_body(requests.request(method='post', url=url,
                                            headers={"content-type": "application/json"}, json=req_body))
    LogUtil.log_info(f"退款回调成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，"
                     f"resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def refund_withdraw_callback(serial_no, pay_status=2):
    refund_request = get_refund_request(refund_request_withhold_serial_no=serial_no)[-1]
    withdraw = get_withdraw(withdraw_ref_no=refund_request["refund_request_serial_no"])[-1]
    url = gc.REPAY_URL + globak_withdraw_callback_path
    req_body = {"from_system": "paysvr",
                "key": get_random_str(),
                "type": "withdraw",
                "data": {
                    "platform_code": "E20000",
                    "platform_message": "SUCCESS",
                    "channel_name": "test_channel_withdraw",
                    "channel_code": "KN_UNKNOWN_ERROR",
                    "channel_message": "KN_UNKNOWN_ERROR",
                    "finished_at": get_date(timezone=get_tz()),
                    "channel_key": "withdraw_" + get_random_str(10),
                    "amount": withdraw["withdraw_amount"],
                    "status": pay_status,
                    "merchant_key": withdraw["withdraw_serial_no"],
                    "trade_no": "trade_no_" + get_random_str(10),
                    "wd_number": None,
                    "expire_time": None
                }}
    resp = parse_resp_body(requests.request(method='post', url=url,
                                            headers={"content-type": "application/json"}, json=req_body))
    LogUtil.log_info(f"退款回调成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，"
                     f"resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def withhold_cancel(request_key, cancel_reason="退出支付"):
    url = gc.REPAY_URL + withhold_cancel_path
    req_body = {
        "from_system": "DSQ",
        "key": get_guid(),
        "type": "WithholdCancel",
        "data": {
            "req_key": request_key,
            "cancel_reason": cancel_reason
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"cancel-withhold发起成功，url:{url}, resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def fix_status_asset_change_mq_sync(item_no):
    url = gc.REPAY_URL + asset_change_mq
    req_body = {
        "type": "AssetChangeMQ",
        "key": get_guid(),
        "from_system": "BIZ",
        "data": {
            "item_no": item_no,
            "operate_type": "asset",
            "action": "fix_status"
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"重新同步发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def asset_grant_success_to_rbiz(item_no):
    url = gc.REPAY_URL + rbiz_asset_import_url
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
    LogUtil.log_info(f"放款成功资产同步rbiz成功，url:{url}, request：{item_no}，resp：{resp}")
    return item_no


def capital_asset_success_to_rbiz(item_no):
    url = gc.REPAY_URL + capital_asset_success
    capital_asset_info = deepcopy(capital_asset)
    asset = get_asset_info_by_item_no(item_no)
    capital_trans_principal = get_capital_transaction_principal_from_asset_tran(item_no)
    capital_trans_fees = get_capital_transaction_fees_from_asset_tran(item_no)
    capital_asset_info["channel"] = asset[0]['asset_loan_channel']
    capital_asset_info["item_no"] = item_no
    capital_asset_info["period_count"] = asset[0]['asset_period_count']
    capital_asset_info["due_at"] = asset[0]['asset_due_at']
    capital_asset_info["granted_amount"] = asset[0]['asset_principal_amount']
    capital_asset_info["cmdb_no"] = asset[0]['asset_cmdb_product_number']
    capital_asset_info['capital_transactions'].extend(capital_trans_principal)
    capital_asset_info["capital_transactions"].extend(capital_trans_fees)
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=capital_asset_info))
    LogUtil.log_info(f"资方还款计划同步rbiz成功，url:{url},request：{item_no}，resp：{resp}")
    return item_no


def withhold_order_query(item_no):
    url = gc.REPAY_URL + withhold_order_query_path
    req_body = {
        "from_system": "dsq",
        "key": get_random_str(),
        "type": "string",
        "data": {
            "item_no": item_no
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"查询资产还款记录发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp, req_body


def void_asset_from_mq(item_no, loan_channel):
    url = gc.REPAY_URL + asset_void_from_mq
    req_body = {
        "version": get_timestamp_by_now(),
        "status": "sale",
        "apply_code": item_no,
        "message": "取消放款,资产冲正",
        "channel": loan_channel,
        "cancel_type": "ASSET_REVERSAL",
        "grant_time": get_date()
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"资产冲正发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，"
        f"resp：{json.dumps(resp['content'], ensure_ascii=False)}")


def cancel_asset_from_mq(item_no, loan_channel):
    url = gc.REPAY_URL + asset_cancel_from_mq
    req_body = {"key": get_guid(),
                "type": "AssetGrantCancelNotifyMQ",
                "from_system": "gbiz",
                "data": {"version": get_timestamp_by_now(),
                         "apply_code": item_no,
                         "message": "取消放款，作废资产",
                         "status": "void",
                         "channel": loan_channel}}
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"资产取消发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，"
        f"resp：{json.dumps(resp['content'], ensure_ascii=False)}")


def asset_tolerance_settle(item_no, amount=0):
    url = gc.REPAY_URL + asset_tolerance_settle_path
    req_body = {
        "key": get_guid(),
        "from_system": "biz",
        "type": "ToleranceSettleAsset",
        "data": {
            "item_no": item_no
        }
    }
    if amount != 0:
        req_body["data"]["tolerance_amount"] = amount
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"资产拨备结清发起成功，url:{url},request：{json.dumps(req_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")


def asset_settle_debt(item_no, serial_no):
    url = gc.REPAY_URL + asset_settle_debt_path
    req_body = {
        "from_system": "BIZ",
        "key": get_guid(),
        "type": "AssetSettleDebt",
        "data": {
            "asset_item_no": item_no,
            "recharge_serial_no": serial_no,
            "operator_name": "自动化测试"
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"asset_settle_debt 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def asset_account_recharge(amount, id_num, serial_no, item_no, ):
    url = gc.REPAY_URL + account_recharge_path
    req_body = {
        "from_system": "BIZ",
        "key": get_guid(),
        "type": "AccountRecharge",
        "data": {
            "amount": amount,
            "date": get_date(),
            "comment": "",
            "user_id_num": None,
            "user_id_num_encrypt": id_num,
            "serial_no": serial_no,
            "merchant_id": None,
            "asset_item_no": item_no,
            "card_num": None,
            "operator_id": 0,
            "operator_name": "autotest",
            "send_change_mq": True,
            "withhold_recharge": False
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"account recharge 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def asset_repay_reverse(item_no, serial_no):
    url = gc.REPAY_URL + asset_repay_reverse_path
    req_body = {
        "from_system": "BIZ",
        "key": get_guid(),
        "type": "AssetRepayReverse",
        "data": {
            "type": "asset",
            "asset_item_no": item_no,
            "serial_no": serial_no,
            "operator_id": "1",
            "operator_name": "autotest",
            "comment": "还款逆操作"
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"asset_repay_reverse 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def asset_void_withhold(item_no, amount, payment_type="qrcode", payment_option="", payment_mode="", four_element=None):
    url = gc.REPAY_URL + asset_void_withhold_path
    req_body = {
        "from_system": "eday",
        "key": get_guid(),
        "type": "AssetVoidWithhold",
        "data": {
            "from_app": "testapp",
            "owner": "test",
            "ref_no": item_no,
            "trade_type": "asset_void",
            "payment_type": payment_type,
            "payment_option": payment_option,
            "payment_mode": payment_mode,
            "amount": amount,
            "user_id": four_element['data']['id_number'],
            "card_uuid": four_element['data']['card_num'],
            "user_ip": "10.10.10.10",
            "callback": "http://www.baidu.com",
            "redirect_url": "http://xxxxxxxxx/"
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"asset-void-withhold 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def run_job_by_api(job_type, job_params):
    job_url = gc.REPAY_URL + "/job/run"
    # job_url = "https://biz-gateway-proxy.starklotus.com/tha_repay1" + "/job/run"
    params = {"jobType": job_type,
              "param": json.dumps(job_params)}
    return Http.http_get(job_url, params=params)


def run_refreshLateFeeV1_by_api(item_no=None):
    job_type = "refreshLateFeeV1"
    job_params = {
        "startDate": get_date(year=-5, month=-1),
        "joinSql": [
            "inner join asset a on t.asset_tran_asset_item_no = a.asset_item_no",
            "left join asset_late_fee_refresh_log as c on "
            "a.asset_item_no = c.asset_late_fee_refresh_log_asset_item_no and "
            "c.asset_late_fee_refresh_log_update_at >= current_date and "
            "asset_late_fee_refresh_log_item_type = 'asset'"
        ],
        "whereSql": [
            "and a.asset_status= 'repay'",
            "and c.`asset_late_fee_refresh_log_asset_item_no` is null",
            "and t.asset_tran_amount > t.asset_tran_repaid_amount"
        ],
        "refreshAll": False
    }
    if item_no is not None:
        job_params["whereSql"].append("and a.asset_item_no like '%%%s%%'" % item_no)
    run_job_by_api(job_type, job_params)


def run_refreshLateFeeByDayBatch_by_api(item_no=None):
    job_type = "refreshLateFeeByDayBatch"
    job_params = {
        "startDate": get_date(year=-5, month=-1),
        "joinSql": [
            "inner join asset a on t.asset_tran_asset_item_no = a.asset_item_no",
            "left join asset_late_fee_refresh_log as c on "
            "a.asset_item_no = c.asset_late_fee_refresh_log_asset_item_no and "
            "c.asset_late_fee_refresh_log_update_at >= current_date and "
            "asset_late_fee_refresh_log_item_type = 'asset'"
        ],
        "whereSql": [
            "and a.asset_status= 'repay'",
            "and c.`asset_late_fee_refresh_log_asset_item_no` is null",
            "and t.asset_tran_amount > t.asset_tran_repaid_amount"
        ],
        "refreshAll": False
    }
    if item_no is not None:
        job_params["whereSql"].append("and a.asset_item_no like '%%%s%%'" % item_no)
    run_job_by_api(job_type, job_params)


def run_assetDecreaseDueAtOnDay_by_api():
    job_type = "assetDecreaseDueAtOnDay"
    job_params = {}
    run_job_by_api(job_type, job_params)


def run_decreasedLateInterestUndoJob_by_api():
    job_type = "decreasedLateInterestUndoJob"
    job_params = {}
    run_job_by_api(job_type, job_params)


def run_assetTolerancePayoffJob_by_api(itemNos=None, toleranceAmount=0, byPeriod=False, term=1000):
    job_type = "assetTolerancePayoffJob"
    job_params = dict()
    if itemNos is not None:
        job_params["itemNos"] = itemNos
    if toleranceAmount != 0:
        job_params["toleranceAmount"] = toleranceAmount
    job_params["byPeriod"] = byPeriod
    job_params["term"] = term
    run_job_by_api(job_type, job_params)


"""
{"itemNos": ["P2023032409923290322"],
"term": 1,
"byPeriod": true,
"toleranceAmount": 6000}
"""


def run_withholdTimeout_by_api():
    job_type = "withholdTimeout"
    job_params = {"limit": 1000}
    run_job_by_api(job_type, job_params)


def run_accountStatementSync_by_api(start=None, end=None):
    job_type = "accountStatementSync"
    job_params = {"startDate": start,
                  "endDate": end}
    run_job_by_api(job_type, job_params)


def run_initStatusAccountStatementMatchWithholdRecord_by_api():
    job_type = "initStatusAccountStatementMatchWithholdRecord"
    job_params = {"limit": 200}
    run_job_by_api(job_type, job_params)


def run_assetRelateHistoryMove_by_api(asset_id=None, month=1, limit=10):
    job_type = "assetRelateHistoryMove"
    job_params = {
        "assetId": asset_id,
        "beforeMonth": month,
        "limit": limit
    }
    run_job_by_api(job_type, job_params)


def run_withholdRelateHistoryMove_by_api(month=6, limit=2):
    job_type = "withholdRelateHistoryMove"
    job_params = {"beforeMonth": month,
                  "limit": limit,
                  "step": 3,
                  "withholdStatus": ["fail", "cancel"]}
    run_job_by_api(job_type, job_params)


def run_manualSyncAsset_by_api(item_no_list=None):
    job_type = "manualSyncAsset"
    job_params = {"assetItemNo": item_no_list}
    run_job_by_api(job_type, job_params)


def run_taskDbJob_by_api(priority=1, limit=2):
    job_type = "taskDbJob"
    job_params = {"priority": priority, "delayMinute": 0, "limit": limit, "withInHour": 24}
    run_job_by_api(job_type, job_params)


def run_DbMutipleThreadRunTaskJob_by_api(priority=1, limit=1000):
    job_type = "DbMutipleThreadRunTaskJob"
    job_params = {"delay_minute": 2, "select_limit": limit, "morethan_hour": 24, "priority": priority}
    run_job_by_api(job_type, job_params)


def run_reopenTimeoutTaskJob_by_api():
    job_type = "reopenTimeoutTaskJob"
    job_params = {"withInHour": 24, "delayMinute": 35}
    run_job_by_api(job_type, job_params)


def run_reopenTimeoutSendMsgJob_by_api():
    job_type = "reopenTimeoutSendMsgJob"
    job_params = {"withInHour": 24, "delayMinute": 35}
    run_job_by_api(job_type, job_params)


def run_FoxAdvancePushJob_by_api():
    job_type = "FoxAdvancePushJob"
    job_params = {"assetType": "paydayloan"}
    run_job_by_api(job_type, job_params)


if __name__ == "__main__":
    run_taskDbJob_by_api()
    # run_assetTolerancePayoffJob_by_api(toleranceAmount=1000, term=10000000, byPeriod=True)
    # run_refreshLateFeeV1_by_api("P2022041216720998154")
    # run_manualSyncAsset_by_api(["P2022041216720998154"])
    # run_accountStatementSync_by_api(get_date(day=-2, fmt="%Y-%m-%d"),
    #                                 get_date(day=0, fmt="%Y-%m-%d"))
    # run_initStatusAccountStatementMatchWithholdRecord_by_api()
    # Http.http_post("http://capital-api-7.k8s-ingress-nginx.kuainiujinke.com/flow-query/get-transactions",
    #                {
    #                    "from_system": "Rbiz",
    #                    "key": get_random_str(),
    #                    "type": "getAccountStatement",
    #                    "data": {
    #                        "currency": None,
    #                        "date": "2022-10-12",
    #                        "end_date": "2022-10-12",
    #                        "account": "abc",
    #                        "side_account": None,
    #                        "loan_type": None,
    #                        "trade_no": None
    #                    },
    #                    "sync_datetime": None,
    #                    "busi_key": None
    #                }
    #                )
