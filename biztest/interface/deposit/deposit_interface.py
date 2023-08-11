#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

import common.global_const as gc
from biztest.util.http.http_util import Http as http
from biztest.util.tools.tools import get_guid


def trade_tally(order_no, trade_no, channel_code, pay_channel_code="qsq_cpcn_tq_quick", amount=500000):
    path = "/trade/tally"
    req = {
        "from_system": "dcs",
        "key": get_guid(),
        "type": "TallySync",
        "data": {
            "order_no": order_no,
            "trade_no": trade_no,
            "type": 1,
            "amount": amount,
            "memo": "资金归集记账",
            "channel_code": channel_code,
            "pay_channel_code": pay_channel_code,
            "in_account": None,
            "out_account": None,
            "callback_url": None
        }
    }
    url = gc.DEPOSIT_URL + path
    return http.http_post(url, req)


def trade_transfer(order_no, trade_no, in_account, out_account, amount=500000):
    path = "/trade/transfer"
    req = {
        "from_system": "dcs",
        "key": get_guid(),
        "type": "TransferSync",
        "data": {
            "order_no": order_no,
            "trade_no": trade_no,
            "type": 2,
            "amount": amount,
            "memo": "虚户间转账",
            "channel_code": None,
            "pay_channel_code": None,
            "in_account": in_account,
            "out_account": out_account,
            "callback_url": None
        }
    }
    url = gc.DEPOSIT_URL + path
    return http.http_post(url, req)


def trade_withdrawal(order_no, trade_no, out_account, amount=500000):
    path = "/trade/withdrawal"
    req = {
        "from_system": "dcs",
        "key": get_guid(),
        "type": "WithdrawSync",
        "data": {
            "order_no": order_no,
            "trade_no": trade_no,
            "type": 3,
            "amount": amount,
            "memo": "提现",
            "channel_code": None,
            "pay_channel_code": None,
            "in_account": None,
            "out_account": out_account,
            "callback_url": None
        }
    }
    url = gc.DEPOSIT_URL + path
    return http.http_post(url, req)


def trade_loan(order_no, trade_no, channel_code, element, amount=500000):
    path = "/trade/loan"
    req = {
        "from_system": "dcs",
        "key": get_guid(),
        "type": "LoanSync",
        "data": {
            "order_no": order_no,
            "trade_no": trade_no,
            "mem_acct_no": element['data']['bank_code_encrypt'],
            "mem_name": element['data']['user_name_encrypt'],
            "mem_cert_no": element['data']['id_number_encrypt'],
            "mem_mobile": element['data']['phone_number_encrypt'],
            "type": None,
            "amount": amount,
            "memo": "网银转账",
            "channel_code": channel_code,
            "pay_channel_code": None,
            "in_account": None,
            "out_account": None,
            "callback_url": None
        }
    }
    url = gc.DEPOSIT_URL + path
    return http.http_post(url, req)


def member_register(channel_code, element):
    path = "/member/register"
    req = {
        "from_system": "biz",
        "key": get_guid(),
        "type": "MemberRegister",
        "data": {
            "channel_code": channel_code,
            "mem_acct_no": element['data']['bank_code_encrypt'],
            "mem_name": element['data']['user_name_encrypt'],
            "mem_cert_no": element['data']['id_number_encrypt'],
            "mem_mobile": element['data']['phone_number_encrypt'],
            "memo": "新增白名单"
        }
    }
    url = gc.DEPOSIT_URL + path
    return http.http_post(url, req)


def huatong_tq_balance_notify(order_no, trade_no, pay_account, amount=500000):
    path = "/callback/huatong/ht_tengqiao?callbackType=BALANCE_NOTIFY"
    items = {
        "peerAccName": "商盟商务服务有限公司",
        "amount": amount,
        "recordTime": "2023-04-20 10:34:28",
        "seqNo": order_no,
        "peerBankName": "中国银联股份有限公司",
        "operateSubType":"1",
        "peerAccNo": pay_account,
        "peerBankNo": "905290000008",
        "operateType": "01",
        "serverTransId": trade_no
    }
    req = {
        "noticeType": "01",
        "items": json.dumps(items, ensure_ascii=False),
        "industryCode": "MC0321000001"
    }
    url = gc.DEPOSIT_URL + path
    headers = {"Content-Type": "application/json", "Authorization": "UTP01:MC0321000001:CALLBACK_FIX:1681964074688"}
    return http.http_post(url, req, headers)


def huatong_qjj_balance_notify(order_no, trade_no, pay_account="9911000008161031", amount=500000):
    path = "/callback/huatong/ht_qianjingjing?callbackType=BALANCE_NOTIFY"
    items = {
        "peerAccName": "商盟商务服务有限公司",
        "amount": amount,
        "recordTime": "2023-04-20 10:34:28",
        "seqNo": order_no,
        "peerBankName": "中国银联股份有限公司",
        "operateSubType":"1",
        "peerAccNo": pay_account,
        "peerBankNo": "905290000008",
        "operateType": "01",
        "serverTransId": trade_no
    }
    req = {
        "noticeType": "01",
        "items": json.dumps(items, ensure_ascii=False),
        "industryCode": "MC0321000001"
    }
    url = gc.DEPOSIT_URL + path
    headers = {"Content-Type": "application/json", "Authorization": "UTP01:MC0321000001:CALLBACK_FIX:1681964074688"}
    return http.http_post(url, req, headers)


if __name__ == "__main__":
    trade_tally("PH_tally_099000", "PH_tally_099000", "v_qs_phtest002_qs_qianjingjing", pay_channel_code="qsq_cpcn_tq_quick", amount=500000)
