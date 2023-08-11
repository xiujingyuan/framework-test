# -*- coding: utf-8 -*-
from biztest.config.payment.url_config import payment_staging_base_url, \
    sign_company, global_payment_base_url, \
    global_rbiz_callback, global_gbiz_callback, global_rbiz_redirect, \
    global_sign_company_yomoyo, global_rbiz_merchant_name, global_amount, global_gbiz_merchant_name, \
    global_dsq_merchant_name
from biztest.function.rbiz.database_operation import *
from biztest.util.http.http_util import Http


"""
通用
"""


def get_timestamp():
    """
    获取20位的随机数
    :return:
    """
    return '2020' + str(datetime.now().timestamp()).replace('.', '')


"""
支付系统的主要接口
"""


def auto_withhold(four_element, channel_name, amount=100, operator="USER", sign_company="tq"):
    """
    代扣路由接口-指定代扣通道
    :param four_element:
    :param channel_name:
    :param amount:
    :param operator:
    :return:
    """
    channel_name = channel_name
    amount = amount
    operator = operator
    card_num_encrypt = four_element["bank_code_encrypt"]
    id_num_encrypt = four_element["id_number_encrypt"]
    username_encrypt = four_element["user_name_encrypt"]
    mobile_encrypt = four_element["phone_number_encrypt"]

    # 地址参数化，新增config
    url = payment_staging_base_url + "/withhold/autoPay"
    request_body = {
        "merchant_name": global_dsq_merchant_name,
        "merchant_key": get_guid(),
        "channel_name": channel_name,
        "amount": amount,
        "operator": operator,
        "card_num_encrypt": card_num_encrypt,
        "id_num_encrypt": id_num_encrypt,
        "username_encrypt": username_encrypt,
        "mobile_encrypt": mobile_encrypt,
        "callback": None,
        "service_fee": None,
        "role": "borrower",
        "device": "pc",
        "from": global_dsq_merchant_name,
        "need_sync": True,
        "sign_company": sign_company
    }
    resp = Http.http_post(url, request_body)
    return resp
    # try:
    #     resp = parse_resp_body(
    #         requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
    #     return resp
    # except Exception as e:
    #     raise Exception("代扣异常")


def auto_bind_withhold(**kwargs):
    """
    绑卡+代扣（传入绑卡参数+签约主体，实现绑卡成功后并使用该通道进行代扣）
       :param kwargs: dict包含代扣通道、四要素
       :return: json
           example:
    """
    channel_name = kwargs["channel_name"]
    verify_seq = kwargs["verify_seq"]
    amount = kwargs["amount"]
    operator = kwargs["operator"]
    card_num_encrypt = kwargs["card_num_encrypt"]
    id_num_encrypt = kwargs["id_num_encrypt"]
    username_encrypt = kwargs["username_encrypt"]
    mobile_encrypt = kwargs["mobile_encrypt"]

    # 地址参数化，新增config
    url = payment_staging_base_url + "/withhold/autoPay"
    request_body = {
        "merchant_name": global_dsq_merchant_name,
        "merchant_key": get_guid(),
        "sign_company": sign_company,
        "channel_name": channel_name,
        "verify_code": "111111",
        "verify_seq": verify_seq,
        "amount": amount,
        "operator": operator,
        "card_num_encrypt": card_num_encrypt,
        "id_num_encrypt": id_num_encrypt,
        "username_encrypt": username_encrypt,
        "mobile_encrypt": mobile_encrypt,
        "callback": None,
        "service_fee": None,
        "role": None,
        "device": None,
        "from": None,
        "need_sync": True
    }
    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        return resp
    except Exception as e:
        raise Exception("代扣异常")


def run_task_by_order_no(**kwargs):
    """
    按照order_no执行task
    :param kwargs:
    :return:
    """
    order_no = kwargs["order_no"]
    url = payment_staging_base_url + "task/runTaskByOrderNo"
    request_body = {
        "order_no": order_no
    }
    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        return resp
    except Exception as e:
        raise Exception("执行task异常")


def withhold_bindsms(four_element, channel_name):
    """
    指定通道获取验证码
    :param four_element:
    :param channel_name:
    :return:
    """
    channel_name = channel_name
    card_num_encrypt = four_element["bank_code_encrypt"]
    id_num_encrypt = four_element["id_number_encrypt"]
    username_encrypt = four_element["user_name_encrypt"]
    mobile_encrypt = four_element["phone_number_encrypt"]

    url = payment_staging_base_url + "/withhold/bindSms"
    request_body = {
        "merchant_name": global_dsq_merchant_name,
        "merchant_key": get_random_num(),
        "channel_name": channel_name,
        "card_num_encrypt": card_num_encrypt,
        "id_num_encrypt": id_num_encrypt,
        "username_encrypt": username_encrypt,
        "mobile_encrypt": mobile_encrypt,
        "type": None,
        "role": None,
        "device": None,
        "redirect_url": None,
        "from": None,
        "callback_url": None,
        "sign": "6ed19d604b0533ea2af0b9608c55e3adb"
    }
    resp = Http.http_post(url, request_body)
    return resp
    # try:
    #     resp = parse_resp_body(
    #         requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
    #     return resp
    # except Exception as e:
    #     raise Exception("获取验证码异常")


def withhold_bind(four_element, channel_name, verify_code, verify_seq):
    """
    协议支付绑卡确认：只绑卡不代扣
    :param four_element:
    :param channel_name:
    :param verify_code:
    :param verify_seq:
    :return:
    """
    channel_name = channel_name
    verify_code = verify_code
    verify_seq = verify_seq
    card_num_encrypt = four_element["bank_code_encrypt"]
    id_num_encrypt = four_element["id_number_encrypt"]
    username_encrypt = four_element["user_name_encrypt"]
    mobile_encrypt = four_element["phone_number_encrypt"]

    url = payment_staging_base_url + "/withhold/bind"
    request_body = {
        "merchant_name": global_dsq_merchant_name,
        "merchant_key": get_guid(),
        "channel_name": channel_name,
        "verify_code": verify_code,
        "verify_seq": verify_seq,
        "card_num_encrypt": card_num_encrypt,
        "id_num_encrypt": id_num_encrypt,
        "username_encrypt": username_encrypt,
        "mobile_encrypt": mobile_encrypt,
        "callback": None,
        "service_fee": None,
        "role": None,
        "device": None,
        "from": None,
        "need_sync": True
    }
    resp = Http.http_post(url, request_body)
    return resp
    # try:
    #     resp = parse_resp_body(
    #         requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
    #     return resp
    # except Exception as e:
    #     raise Exception("绑卡异常")


def withhold_autobindsms(**kwargs):
    """
    协议支付签约短信路由：传入签约主体，自动选择短信通道
    :param kwargs: 签约主体+四要素
    :return: 通道
    """
    card_num_encrypt = kwargs["card_num_encrypt"]
    id_num_encrypt = kwargs["id_num_encrypt"]
    username_encrypt = kwargs["username_encrypt"]
    mobile_encrypt = kwargs["mobile_encrypt"]

    url = payment_staging_base_url + "/withhold/autoBindSms"
    request_body = {
        "merchant_key": get_guid(),
        "merchant_name": global_dsq_merchant_name,
        "sign_company": sign_company,
        "card_num_encrypt": card_num_encrypt,
        "id_num_encrypt": id_num_encrypt,
        "username_encrypt": username_encrypt,
        "mobile_encrypt": mobile_encrypt
    }
    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        return resp
    except Exception as e:
        raise Exception("短信路由异常")


def auto_private_withdraw(channel, four_element):
    """
    【对私】代付路由接口-指定代付通道
       :param kwargs: dict
       :return: json
           example:
    """
    account = channel
    amount = 1
    receiver_type = 1
    receiver_name_encrypt = four_element["user_name_encrypt"]
    receiver_account_encrypt = four_element["bank_code_encrypt"]
    receiver_identity_encrypt = four_element["id_number_encrypt"]

    url = payment_staging_base_url + "/withdraw/autoWithdraw"
    request_body = {
        "merchant_name": global_dsq_merchant_name,
        "merchant_key": get_guid(),
        "trade_no": get_guid(),
        "project_code": get_guid(),
        "account": account,
        "receiver_type": receiver_type,
        # "sign_company": "tq",
        "amount": amount,
        "reason": "10",  # 便于中金直接代付成功
        "receiver_name_encrypt": receiver_name_encrypt,
        "receiver_account_encrypt": receiver_account_encrypt,
        "receiver_identity_encrypt": receiver_identity_encrypt,
        "receiver_bank_code": "",
        "receiver_bank_branch": None,
        "receiver_bank_subbranch": None,
        "receiver_bank_province": None,
        "receiver_bank_city": None,
        "redirect": "xxx",
        "callback": "http://cbiz1.jichu-test.kuainiujinke.com/api/lm/callback?id=20076&auth_token=07953c2623f426259057b9562951a354&time=1577179422",
        "sign": "e6af62c9bf3576fd3da6e73c1016320c"
    }
    resp = Http.http_post(url, request_body)
    return resp
    # try:
    #     resp = parse_resp_body(
    #         requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
    #     return resp
    # except Exception as e:
    #     raise Exception("对私代付异常")


def auto_public_withdraw(**kwargs):
    """
    【对公】代付路由接口-指定代付通道
       :param kwargs: dict
       :return: json
           example:
    """
    account = kwargs["account"]
    amount = kwargs["amount"]
    receiver_type = kwargs["receiver_type"]
    receiver_name_encrypt = kwargs["receiver_name_encrypt"]
    receiver_account_encrypt = kwargs["receiver_account_encrypt"]
    receiver_identity_encrypt = kwargs["receiver_identity_encrypt"]
    receiver_bank_code = kwargs["receiver_bank_code"]
    receiver_bank_branch = kwargs["receiver_bank_branch"]
    receiver_bank_subbranch = kwargs["receiver_bank_subbranch"]
    receiver_bank_province = kwargs["receiver_bank_province"]
    receiver_bank_city = kwargs["receiver_bank_city"]

    url = payment_staging_base_url + "/withdraw/autoWithdraw"
    request_body = {
        "merchant_name": global_dsq_merchant_name,
        "merchant_key": get_guid(),
        "trade_no": get_guid(),
        "project_code": get_guid(),
        "account": account,
        "receiver_type": receiver_type,
        # "sign_company": "tq",
        "amount": amount,
        "reason": "10",  # 便于中金直接代付成功
        "receiver_name_encrypt": receiver_name_encrypt,
        "receiver_account_encrypt": receiver_account_encrypt,
        "receiver_identity_encrypt": receiver_identity_encrypt,
        "receiver_bank_code": receiver_bank_code,
        "receiver_bank_branch": receiver_bank_branch,
        "receiver_bank_subbranch": receiver_bank_subbranch,
        "receiver_bank_province": receiver_bank_province,
        "receiver_bank_city": receiver_bank_city,
        "redirect": "xxx",
        "callback": "http://cbiz1.jichu-test.kuainiujinke.com/api/lm/callback?id=20076&auth_token=07953c2623f426259057b9562951a354&time=1577179422",
        "sign": "e6af62c9bf3576fd3da6e73c1016320c"
    }
    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        return resp
    except Exception as e:
        raise Exception("对公代付异常")

#
# def global_bind(**kwargs):
#     """
#         指定通道获取验证码
#         :param kwargs:
#         :return:
#     """
#     sign_company = kwargs["sign_company"]
#     bank_account_encrypt = kwargs["bank_account_encrypt"]
#     user_name_encrypt = kwargs["user_name_encrypt"]
#     mobile_encrypt = kwargs["mobile_encrypt"]
#     email_encrypt = kwargs["email_encrypt"]
#     address_encrypt = kwargs["address_encrypt"]
#     ifsc = kwargs["ifsc"]
#     # card_uuid = kwargs["card_uuid"]
#     merchant_key = kwargs["merchant_key"]
#
#     url = global_payment_base_url + "/card/bind"
#     request_body = {
#         "merchant_name": global_dsq_merchant_name,
#         # "merchant_key": get_guid(),
#         "merchant_key": merchant_key,
#         "sign_company": sign_company,
#         # "card_uuid": card_uuid, 不用传系统自动生成
#         "bank_account_encrypt": bank_account_encrypt,
#         "card_num_encrypt": "",
#         "upi_encrypt": "",
#         "id_num_encrypt": None,  # 海外不需要传身份证
#         "user_name_encrypt": user_name_encrypt,
#         "mobile_encrypt": mobile_encrypt,
#         "email_encrypt": email_encrypt,
#         "address_encrypt": address_encrypt,
#         "card_type": "",
#         "card_expiry_year": "",
#         "card_expiry_month": "",
#         "card_cvv": "",
#         "ifsc": ifsc
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("绑卡验证异常")
#
#
# def global_autobind(merchant_key, sign_company, bank_account_encrypt, upi_encrypt, ifsc, user_name_encrypt,
#                     mobile_encrypt, email_encrypt, address_encrypt):
#     """
#         指定通道获取验证码
#         :param kwargs:
#         :return:
#     """
#
#     url = global_payment_base_url + "/card/autoBind"
#     request_body = {
#         "merchant_name": global_dsq_merchant_name,
#         "merchant_key": merchant_key,
#         "sign_company": sign_company,
#         "bank_account_encrypt": bank_account_encrypt,
#         "user_name_encrypt": user_name_encrypt,
#         "mobile_encrypt": mobile_encrypt,
#         "email_encrypt": email_encrypt,
#         "address_encrypt": address_encrypt,
#         "ifsc": ifsc,
#         "id_num_encrypt": None,  # 海外不需要传身份证
#         "card_num_encrypt": None,
#         "upi_encrypt": upi_encrypt,
#         "card_type": "",
#         "card_expiry_year": "",
#         "card_expiry_month": "",
#         "card_cvv": ""
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("绑卡路由异常")
#
#
# def global_withhold_autoSubscribe(merchant_key, card_uuid, card_num_encrypt, user_name_encrypt, mobile_encrypt,
#                                   email_encrypt, address_encrypt, ifsc):
#     """
#         指定通道获取验证码
#         :param kwargs:
#         :return:
#     """
#     url = global_payment_base_url + "/withhold/autoSubscribe"
#     request_body = {
#         "merchant_name": global_dsq_merchant_name,
#         "merchant_key": merchant_key,
#         "sign_company": global_sign_company_yomoyo,
#         "card_uuid": card_uuid,
#         "card_num_encrypt": card_num_encrypt,
#         "ifsc": ifsc,
#         "user_name_encrypt": user_name_encrypt,
#         "mobile_encrypt": mobile_encrypt,
#         "email_encrypt": email_encrypt,
#         "address_encrypt": address_encrypt,
#         "redirect_url": global_rbiz_redirect,
#         "callback_url": "",
#         "card_type": "DC",
#         "card_expiry_year": None,
#         "card_expiry_month": None,
#         "card_cvv": None,
#         "id_num_encrypt": None
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("订阅路由异常")
#
#
# def global_bindCheck(**kwargs):
#     """
#         绑卡检查
#         :param kwargs:
#         :return:
#     """
#     sign_company = kwargs["sign_company"]
#     card_uuid = kwargs["card_uuid"]
#
#     url = global_payment_base_url + "/card/bindCheck"
#     request_body = {
#         "merchant_name": global_dsq_merchant_name,
#         "sign_company": sign_company,
#         "card_uuid": card_uuid
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("绑卡结果查询异常")
#
#
# def global_withhold_query(**kwargs):
#     """
#         代扣结果查询
#         :param kwargs:
#         :return:
#     """
#     merchant_key = kwargs["merchant_key"]
#
#     url = global_payment_base_url + "/withhold/query"
#     request_body = {
#         "merchant_name": global_rbiz_merchant_name,
#         "merchant_key": merchant_key
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("代扣结果查询异常")
#
#
# def global_withdraw_query(merchant_key):
#     """
#         放款结果查询
#         :param kwargs:
#         :return:
#     """
#
#     url = global_payment_base_url + "/withdraw/query"
#     request_body = {
#         "merchant_name": global_gbiz_merchant_name,
#         "merchant_key": merchant_key
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("放款结果查询异常")
#
#
# def global_withhold_autopay(merchant_key, sign_company, card_uuid, operator, payment_type, payment_option=None, payment_mode=None):
#     """
#     海外项目代扣:用于非SDK的场景：即只需要传payment_type这种代扣
#        :param
#        :return: json
#            example:
#     """
#
#     # 地址参数化，新增config
#     url = global_payment_base_url + "/withhold/autoPay"
#     request_body = {
#         "merchant_name": global_rbiz_merchant_name,
#         "merchant_key": merchant_key,
#         "amount": global_amount,
#         "sign_company": sign_company,
#         "card_uuid": card_uuid,
#         "operator": operator,  # operator不传默认是主动还款
#         "redirect": global_rbiz_redirect,
#         "callback": global_rbiz_callback,
#         "reason": "f-还款",
#         "payment_type": payment_type,
#         "payment_option": payment_option,
#         "payment_mode": payment_mode,
#         "device_info": None,
#         "sdk_info": None
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("海外代扣异常")
#
#
# def global_withhold_autopay_sdk(merchant_key, sign_company, card_uuid, operator, payment_type, payment_option):
#     """
#     海外项目代扣
#        :param
#        :return: json
#            example:
#     """
#
#     # 地址参数化，新增config
#     url = global_payment_base_url + "/withhold/autoPay"
#     request_body = {
#         "merchant_name": global_rbiz_merchant_name,
#         "merchant_key": merchant_key,
#         "amount": global_amount,
#         "sign_company": sign_company,
#         "card_uuid": card_uuid,
#         "operator": operator,  # operator不传默认是主动还款
#         "redirect": global_rbiz_redirect,
#         "callback": global_rbiz_callback,
#         "reason": "f-还款",
#         "payment_type": payment_type,
#         "payment_option": payment_option,  # payment_type=sdk时必传
#         "device_info":  # payment_type=sdk时必传
#             {
#                 "system_name": "android",
#                 "system_version": "7.0"
#             }
#         ,
#         "sdk_info": [  # payment_type=sdk时必传
#             {
#                 "name": "cashfree",
#                 "version": "1.0"
#             }
#         ]
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("海外代扣异常")
#
#
# def global_withhold_autopay_no_carduuid(merchant_key, sign_company, user_name_encrypt, mobile_encrypt, email_encrypt,
#                                         operator, payment_type, payment_option=None, payment_mode=None):
#     """
#     海外项目代扣：无卡支付场景
#        :param
#        :return: json
#            example:
#     """
#
#     # 地址参数化，新增config
#     url = global_payment_base_url + "/withhold/autoPay"
#     request_body = {
#         "merchant_name": global_rbiz_merchant_name,
#         "merchant_key": merchant_key,
#         "amount": global_amount,
#         "sign_company": sign_company,
#         "card_uuid": None,
#         "user_name_encrypt": user_name_encrypt,  # 无卡支付必传姓名、手机号、邮箱
#         "mobile_encrypt": mobile_encrypt,
#         "email_encrypt": email_encrypt,
#         "id_num_encrypt": None,
#         "address_encrypt": None,
#         "operator": operator,  # operator不传默认是主动还款
#         "redirect": global_rbiz_redirect,
#         "callback": global_rbiz_callback,
#         "reason": "f-还款",
#         "payment_type": payment_type,
#         "payment_option": payment_option,  # payment_type=sdk时必传payment_option
#         "payment_mode": payment_mode,
#         "device_info": None,
#         "sdk_info": None,
#         "need_sync": True
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("无卡支付代扣异常")
#
#
# def global_autoWithdraw(**kwargs):
#     """
#     海外项目放款
#        :param
#        :return: json
#            example:
#     """
#     amount = kwargs["amount"]
#     sign_company = kwargs["sign_company"]
#     card_uuid = kwargs["card_uuid"]
#     merchant_key = kwargs["merchant_key"]
#     merchant_name = kwargs["merchant_name"]
#     # 地址参数化，新增config
#     url = global_payment_base_url + "/withdraw/autoWithdraw"
#     request_body = {
#         "merchant_name": merchant_name,
#         "merchant_key": merchant_key,
#         "trade_no": get_guid(),
#         "amount": amount,
#         "sign_company": sign_company,
#         "card_uuid": card_uuid,
#         "reason": "f-放款",
#         "callback": global_gbiz_callback
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("海外放款异常")
#
#
# def global_autoWithdraw_new(amount, sign_company, card_uuid, merchant_key):
#     """
#     海外项目放款
#        :param
#        :return: json
#            example:
#     """
#     url = global_payment_base_url + "/withdraw/autoWithdraw"
#     request_body = {
#         "merchant_name": global_gbiz_merchant_name,
#         "merchant_key": merchant_key,
#         "trade_no": get_guid(),
#         "amount": amount,
#         "sign_company": sign_company,
#         "card_uuid": card_uuid,
#         "reason": "f-放款",
#         "callback": global_gbiz_callback
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("海外放款异常")
#
#
# def global_Withdraw_balance(sign_company):
#     """
#     海外项目放款余额查询
#        :param
#        :return: json
#            example:
#     """
#     # 地址参数化，新增config
#     url = global_payment_base_url + "/withdraw/balance"
#     request_body = {
#         "merchant_name": "gbiz",
#         "sign_company": sign_company
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("海外放款账户余额查询异常")
#
#
# def global_transfer_balance(channel_name):
#     """
#     海外项目转账余额查询
#        :param
#        :return: json
#            example:
#     """
#     # 地址参数化，新增config
#     url = global_payment_base_url + "/transfer/balance"
#     request_body = {
#         "merchant_name": "dcs",
#         "channel_name": channel_name
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("海外转账账户余额查询异常")
#
#
# def global_encrypt(**kwargs):
#     """
#         海外项目加密
#         :param kwargs:
#         :return:
#     """
#     plain1 = kwargs["plain1"]
#     plain2 = kwargs["plain2"]
#     plain3 = kwargs["plain3"]
#
#     url = "http://encryptor-test.k8s-ingress-nginx.kuainiujinke.com/encrypt/"
#     request_body = [
#         {
#             "type": 1,  # 手机号
#             "plain": plain1
#         },
#         # {
#         #     "type": 2,  # 身份证
#         #     "plain": "plain2"
#         # },
#         {
#             "type": 3,  # 卡号
#             "plain": plain2
#         },
#         {
#             "type": 4,  # 名字
#             "plain": plain3
#         }
#     ]
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("海外加密异常异常")
#
#
# def global_bindResult(**kwargs):
#     """
#         绑卡结果查询
#         :param kwargs:
#         :return:
#     """
#     merchant_key = kwargs["merchant_key"]
#
#     url = global_payment_base_url + "/card/bindResult"
#     request_body = {
#         "merchant_name": global_dsq_merchant_name,
#         "merchant_key": merchant_key
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("绑卡结果查询异常")
#
#
# def global_subscribeResult(**kwargs):
#     """
#         订阅结果查询
#         :param kwargs:
#         :return:
#     """
#     merchant_key = kwargs["merchant_key"]
#
#     url = global_payment_base_url + "/withhold/subscribeResult"
#     request_body = {
#         "merchant_name": global_dsq_merchant_name,
#         "merchant_key": merchant_key
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("订阅结果查询异常")
#
#
#
# def global_withhold_autoRegister(merchant_key, sign_company, card_uuid, account_no, user_uuid, individual_uuid,
#                                  user_name_encrypt, mobile_encrypt, email_encrypt):
#     """
#         开虚户
#         :param kwargs:
#         :return:
#     """
#     url = global_payment_base_url + "/withhold/autoRegister"
#     request_body = {
#         "merchant_name": global_dsq_merchant_name,
#         "merchant_key": merchant_key,
#         "sign_company": sign_company,
#         "card_uuid": card_uuid,
#         "account_no": account_no,
#         "user_uuid": user_uuid,
#         "individual_uuid": individual_uuid,
#         "user_name_encrypt": user_name_encrypt,
#         "mobile_encrypt": mobile_encrypt,
#         "email_encrypt": email_encrypt
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("开户异常")
#
#
# def global_withhold_unRegister(merchant_key, account_no):
#     """
#         开虚户
#         :param kwargs:
#         :return:
#     """
#     url = global_payment_base_url + "/withhold/unRegister"
#     request_body = {
#         "merchant_name": global_dsq_merchant_name,
#         "merchant_key": merchant_key,
#         "account_no": account_no
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("注销异常")
#
#
# def global_withhold_closeOrder(merchant_key):
#     """
#         开虚户
#         :param kwargs:
#         :return:
#     """
#     url = global_payment_base_url + "/withhold/closeOrder"
#     request_body = {
#         "merchant_name": global_rbiz_merchant_name,
#         "merchant_key": merchant_key
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("手动关闭代扣异常")
#
#
# def global_yinni_flinpay_paycode_withholdcallback(channel_key):
#     """
#     印尼代扣成功模拟
#        :param
#        :return: json
#            example:
#     """
#     url = "https://openapi.sanbox.flinpay.com/gateway/simulation"
#     request_body = {
#         "merchantCode": "S820200426155245000001",  # 这个是KV配置的
#         "orderNum": channel_key,
#         "type": "PAY",
#         "status": 1
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("印尼代扣回调异常")
#
#
# def global_transfer_transfer(merchant_key, trade_no, channel_name, in_account_no):
#     """
#         清分转账
#         :param kwargs:
#         :return:
#     """
#     url = global_payment_base_url + "/transfer/transfer"
#     request_body = {
#         "merchant_name": global_dsq_merchant_name,
#         "merchant_key": merchant_key,
#         "trade_no": trade_no,
#         "amount": global_amount,
#         "channel_name": channel_name,
#         "in_account_no": in_account_no,
#         "reason": "清分转账",
#         "callback": global_gbiz_callback
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("清分转账异常")
#
#
# def global_transfer_query(merchant_key):
#     """
#         清分转账
#         :param kwargs:
#         :return:
#     """
#     url = global_payment_base_url + "/transfer/query"
#     request_body = {
#         "merchant_name": global_dsq_merchant_name,
#         "merchant_key": merchant_key
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("清分转账结果查询异常")
#
#
# def global_fee_query(merchant_key, fee_type):
#     """
#         清结算-单笔成本查询
#         :param kwargs:
#         :return:
#     """
#     url = global_payment_base_url + "/fee/query"
#     request_body = {
#         "merchant_name": "Rbiz",
#         "merchant_key": merchant_key,
#         "fee_type": fee_type
#     }
#     try:
#         resp = parse_resp_body(
#             requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
#         return resp
#     except Exception as e:
#         raise Exception("单笔成本查询异常")
#
#
# def global_job_run_reconci(channel_name):
#     """
#         结算单下载
#         :param kwargs:
#         :return:
#     """
#     url = global_payment_base_url + "/job/run?jobType=reconciTaskJob&param={\"recon_date\":\"2020-06-09\",\"channel_name\":\"%s\"}" % channel_name
#
#     try:
#         resp = parse_resp_body(
#             requests.request(method='get', url=url))
#         return resp
#     except Exception as e:
#         raise Exception("结算单下载异常")
#
#
# def global_job_runtask(task_priority):
#     """
#         结算单下载
#         :param kwargs:
#         :return:
#     """
#     url = global_payment_base_url + "/job/run?jobType=paysvrTaskJob&param={\"delay_minute\":0,\"select_limit\":200,\"morethan_hour\":20,\"priority\":%s}" % task_priority
#
#     try:
#         resp = parse_resp_body(
#             requests.request(method='get', url=url))
#         return resp
#     except Exception as e:
#         raise Exception("结算单下载异常")


