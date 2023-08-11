#!/usr/bin/python
# -*- coding: UTF-8 -*-
from foundation_test.config.contractsvr.contractsvr_interface_url_config import *
from foundation_test.util.http.http_util import Http

http = Http()


def sign_apply(apply_id):
    request_body = {
        "flow_key": "without_flow_key",
        "apply_id": apply_id,
        "version": 5,
        "callback_url": "",
        "data": [
        {
          "params": {
            "address": "测试地地址",
            "choose_payment_way": 1,
            "company_name": "萍乡唯渡贷后管理有限公司",
            "date": "2018年5月28日",
            "first_repayment_time": "【2019】年【05】月【28】日",
            "identity_encrypt": "enc_02_12425770_513",
            "limit_day": 30,
            "limit_month": 1,
            "mobile_encrypt": "enc_01_12756730_465",
            "name_encrypt": "enc_04_802170_835",
            "pay_all_service_charges_for_once_time": "【2019】年【06】月【28】日",
            "radio_render_limit_method_day": False,
            "radio_render_limit_method_month": True,
            "server_date": "【2019】年【05】月【28】日",
            "sign_User": {
              "identity": "140524197601010425",
              "mobile": "15720426854",
              "name": "张三"
            },
            "subject_sign": "sign_auto_yunzhi",
            "time_limit": 3
          },
          "tenant_key": "cos-old",
          "tmp_key": "qzb_marketing_service",
          "version": 5
        }
      ]
    }
    contractsvr_url = contractsvr_base_url + sign_apply_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(contractsvr_url, request_body, header)
    return resp


def warning_pool_size(pool, size):
    request_body = {
        "pool": pool,
        "size": size
    }
    contractsvr_url = contractsvr_base_url + warning_pool_url
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = http.http_post(contractsvr_url, request_body, header)
    return resp
