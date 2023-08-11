# -*- coding: utf-8 -*-
from copy import deepcopy

import requests

from biztest.config.rbiz.params_config import asset_grant, capital_asset
from biztest.config.rbiz.url_config import *
from biztest.function.biz.biz_db_function import wait_biz_asset_appear, get_biz_asset_info_by_item_no, \
    get_central_task_id_by_type, wait_central_task_close_by_id

from biztest.function.gbiz.gbiz_db_function import *
from biztest.function.rbiz.rbiz_db_function import get_asset_extend_val_by_item_no, get_repay_card_by_item_no, \
    get_withhold_by_serial_no, get_sendmsg_list_by_order_no_and_type
from biztest.interface.rbiz.biz_central_interface import run_task_in_biz_central_by_task_id, run_msg_in_biz_central, \
    run_biz_central_task_by_count
from biztest.util.http.http_util import Http
from biztest.util.log.log_util import *
from biztest.util.tools.tools import *
import common.global_const as gc


def monitor_check(timeout=120):
    result = None
    for i in range(timeout):
        url = gc.REPAY_URL + rbiz_monitor_check_url
        try:
            headers = {"Content-Type": "application/json", "Connection": "close"}
            resp = requests.get(url, headers=headers, timeout=10)
            LogUtil.log_info(resp.status_code)
            if resp.status_code == 200:
                LogUtil.log_info('monitor check passed')
                result = True
                break
            else:
                LogUtil.log_info('monitor check failed')
                result = False
                time.sleep(1)
        except:
            result = False
    # 随机sleep10秒，怕并发导致服务挂了
    time.sleep(random.randint(1, 10))
    return result


"""
还款系统的主要接口
"""


def combo_active_repay(**kwargs):
    """
    主动合并代扣接口
    :param kwargs:包括用户信息，资产编号，金额，优惠券信息，协议支付验证码，优先级
    :return: 返回一个json包括code,message，data等信息
             example:
                {
                    "code": 0,
                    "message": "交易处理中",
                    "data": {
                        "type": "BIND_SMS",
                        "project_list": [
                            {
                                "status": 2,
                                "memo": "处理中",
                                "project_num": "yixin_xintuo20191119144856679_1",
                                "order_no": "AUTO_C311199812053599861",
                                "error_code": "E20017"
                            }
                        ]
                }

    """
    card_num_encrypt = kwargs["card_num_encrypt"]
    card_user_id_encrypt = kwargs["card_user_id_encrypt"]
    card_user_name_encrypt = kwargs["card_user_name_encrypt"]
    card_user_phone_encrypt = kwargs["card_user_phone_encrypt"]
    project_num_loan_channel = kwargs["project_num_loan_channel"]
    project_num_no_loan = kwargs["project_num_no_loan"]
    project_num_loan_channel_priority = kwargs["project_num_loan_channel_priority"]
    project_num_no_loan_priority = kwargs["project_num_no_loan_priority"]
    project_num_loan_channel_amount = kwargs["project_num_loan_channel_amount"]
    project_num_no_loan_amount = kwargs["project_num_no_loan_amount"]
    total_amount = kwargs["total_amount"]
    coupon_num = kwargs["coupon_num"] if "coupon_num" in kwargs else None
    coupon_amount = kwargs["coupon_amount"] if "coupon_amount" in kwargs else None
    order_no = kwargs["order_no"] if "order_no" in kwargs else ""
    verify_code = kwargs["verify_code"] if "verify_code" in kwargs else ""
    verify_seq = kwargs["verify_seq"] if "verify_seq" in kwargs else ""
    key = kwargs["key"] if "key" in kwargs else get_guid()

    url = gc.REPAY_URL + combo_active_path
    request_body = {
        "type": "PaydayloanUserActiveRepay",
        "key": key,
        "from_system": "DSQ",
        "data": {
            "card_num_encrypt": card_num_encrypt,
            "card_user_id_encrypt": card_user_id_encrypt,
            "card_user_name_encrypt": card_user_name_encrypt,
            "card_user_phone_encrypt": card_user_phone_encrypt,
            "total_amount": int(total_amount),
            "project_list": [
                {
                    "project_num": project_num_loan_channel,
                    "amount": int(project_num_loan_channel_amount),
                    "priority": project_num_loan_channel_priority,
                    "coupon_num": None,
                    "coupon_amount": None
                },
                {
                    "project_num": project_num_no_loan,
                    "amount": int(project_num_no_loan_amount),
                    "priority": project_num_no_loan_priority,
                    "coupon_num": coupon_num,
                    "coupon_amount": coupon_amount
                }
            ],
            "order_no": order_no,
            "verify_code": verify_code,
            "verify_seq": verify_seq
        }
    }
    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        LogUtil.log_info(
            f"主动代扣发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
        return resp, request_body
    except Exception as e:
        raise Exception(f"主动合并代扣失败:{e}")


def simple_active_repay(item_no, **kwargs):
    """
    简易版主动合并代扣接口，四要素从asset_individual表取值
    :param item_no: 资产编号
    :param kwargs:包括用户信息，资产编号，金额，优惠券信息，协议支付验证码，优先级
    :return: 返回一个json包括code,message，data等信息
    """
    asset_extend = get_asset_extend_val_by_item_no(item_no)
    project_num_no_loan = kwargs.get("project_num_no_loan", "repay_with_noloan")
    if project_num_no_loan is 'repay_with_noloan':
        project_num_no_loan = asset_extend[0]['asset_extend_val'] if asset_extend else item_no + "_quanyi"
    card_info = get_repay_card_by_item_no(item_no)

    card_num_encrypt = kwargs.get("card_num_encrypt", card_info[0]['card_acc_num_encrypt'])
    card_user_id_encrypt = kwargs.get("card_user_id_encrypt", card_info[0]['card_acc_id_num_encrypt'])
    card_user_name_encrypt = kwargs.get("card_user_name_encrypt", card_info[0]['card_acc_name_encrypt'])
    card_user_phone_encrypt = kwargs.get("card_user_phone_encrypt", card_info[0]['card_acc_tel_encrypt'])
    project_num_loan_channel = item_no
    project_num_loan_channel_amount = int(kwargs["project_num_loan_channel_amount"])

    coupon_num = kwargs["coupon_num"] if "coupon_num" in kwargs else None
    coupon_amount = kwargs["coupon_amount"] if "coupon_amount" in kwargs else None
    order_no = kwargs["order_no"] if "order_no" in kwargs else ""
    verify_code = kwargs["verify_code"] if "verify_code" in kwargs else ""
    verify_seq = kwargs["verify_seq"] if "verify_seq" in kwargs else ""
    key = kwargs["key"] if "key" in kwargs else get_guid()

    url = gc.REPAY_URL + combo_active_path

    request_body = {
        "type": "PaydayloanUserActiveRepay",
        "key": key,
        "from_system": "DSQ",
        "data": {
            "card_num_encrypt": card_num_encrypt,
            "card_user_id_encrypt": card_user_id_encrypt,
            "card_user_name_encrypt": card_user_name_encrypt,
            "card_user_phone_encrypt": card_user_phone_encrypt,
            "project_list": [
                {
                    "project_num": project_num_loan_channel,
                    "amount": int(project_num_loan_channel_amount),
                    "priority": 2,
                    "coupon_num": None,
                    "coupon_amount": None
                }
            ],
            "order_no": order_no,
            "verify_code": verify_code,
            "verify_seq": verify_seq
        }
    }
    if project_num_no_loan is not None:
        project_num_no_loan_amount = int(kwargs["project_num_no_loan_amount"])
        request_body['data']['project_list'].append({
            "project_num": project_num_no_loan,
            "amount": int(project_num_no_loan_amount),
            "priority": 1,
            "coupon_num": coupon_num,
            "coupon_amount": coupon_amount
        })
    total_amount = project_num_loan_channel_amount
    total_amount = total_amount if project_num_no_loan is None else total_amount + project_num_no_loan_amount
    request_body['data']['total_amount'] = int(total_amount)

    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        LogUtil.log_info(
            f"主动代扣发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，"
            f"resp：{json.dumps(resp['content'], ensure_ascii=False)}")
        return resp, request_body
    except Exception as e:
        raise Exception(f"主动合并代扣失败:{e}")


def combo_active_repay_without_no_loan(**kwargs):
    """
    主动合并代扣接口
    :param kwargs:包括用户信息，资产编号
    :return:
    """
    card_num_encrypt = kwargs["card_num_encrypt"]
    card_user_id_encrypt = kwargs["card_user_id_encrypt"]
    card_user_name_encrypt = kwargs["card_user_name_encrypt"]
    card_user_phone_encrypt = kwargs["card_user_phone_encrypt"]
    project_num_loan_channel = kwargs["project_num_loan_channel"]
    project_num_loan_channel_amount = kwargs["project_num_loan_channel_amount"]
    order_no = kwargs["order_no"] if "order_no" in kwargs else ""
    verify_code = kwargs["verify_code"] if "verify_code" in kwargs else ""
    verify_seq = kwargs["verify_seq"] if "verify_seq" in kwargs else ""
    key = kwargs["key"] if "key" in kwargs else get_guid()

    url = gc.REPAY_URL + combo_active_path
    request_body = {
        "type": "PaydayloanUserActiveRepay",
        "key": key,
        "from_system": "DSQ",
        "data": {
            "card_num_encrypt": card_num_encrypt,
            "card_user_id_encrypt": card_user_id_encrypt,
            "card_user_name_encrypt": card_user_name_encrypt,
            "card_user_phone_encrypt": card_user_phone_encrypt,
            "total_amount": int(project_num_loan_channel_amount),
            "project_list": [
                {
                    "project_num": project_num_loan_channel,
                    "amount": int(project_num_loan_channel_amount),
                    "priority": 1,
                    "coupon_num": None,
                    "coupon_amount": None
                }
            ],
            "order_no": order_no,
            "verify_code": verify_code,
            "verify_seq": verify_seq
        }
    }
    try:
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
        LogUtil.log_info(
            f"主动代扣发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
        return resp, request_body
    except Exception as e:
        raise Exception(f"主动合并代扣失败:{e}")


def bind_sms(order_no):
    """
    获取短信验证码
    :param order_no:代扣记录的serial_no
    :return:返回一个json包含code,message,验证码
            example:
                {
                "code": 0,
                "message": "绑卡短信发送成功！",
                "data": {
                    "verify_seq": "1235880123367493"
                }
            }
    """
    url = gc.REPAY_URL + bind_sms_path
    request_body = {
        "key": "sms" + get_guid(),
        "from_system": "DSQ",
        "type": "SendBindSms",
        "data": {
            "order_no": order_no
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
    LogUtil.log_info(f"获取短信验证码发起成功，url:{url},request：{request_body}，resp：{resp}")
    return resp['content']['data']['verify_seq']


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
        f"刷罚息发起成功，url:{url},request：{json.dumps(request_body, ensure_ascii=False)}，resp：{json.dumps(resp['content'], ensure_ascii=False)}")
    return resp


def asset_void_withhold(env, **kwargs):
    """
    资产取消接口
    :param env: 测试环境
    :param kwargs: dict包含个人信息，本金金额，协议支付验证码，回调gbiz地址，代扣记录序列号,资产编号
    :return:json包含code,message,data
        example:
            {
            "code": 2,
            "message": "交易处理中",
            "data": {
                "trade_no": "10023775",
                "order_no": "asset_void311199571530689944",
                "type": "BIND_SMS"
            }
        }
    """
    url = gc.REPAY_URL + asset_void_withhold_path

    card_num_encrypt = kwargs["card_num_encrypt"]
    id_num_encrypt = kwargs["id_num_encrypt"]
    username_encrypt = kwargs["username_encrypt"]
    mobile_encrypt = kwargs["mobile_encrypt"]
    amount = kwargs["amount"]
    order_no = kwargs["order_no"] if "order_no" in kwargs else ""
    verify_code = kwargs["verify_code"] if "verify_code" in kwargs else ""
    verify_seq = kwargs["verify_seq"] if "verify_seq" in kwargs else ""
    callback = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/repay{0}/withhold-callback".format(env)
    ref_no = kwargs["ref_no"]

    request_body = {
        "from_system": "GBIZ",
        "key": get_guid(),
        "type": "AssetVoidWithhold",
        "data": {
            "ref_no": ref_no,
            "trade_type": "asset_void",
            "owner": "qsq",
            "amount": amount,
            "mobile_encrypt": mobile_encrypt,
            "id_num_encrypt": id_num_encrypt,
            "username_encrypt": username_encrypt,
            "card_num_encrypt": card_num_encrypt,
            "callback": callback,
            "withhold_type": "AUTO",
            "user_active": False,
            "order_no": order_no,
            "verify_code": verify_code,
            "verify_seq": verify_seq
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
    LogUtil.log_info(f"资产取消发起成功，url:{url},request：{request_body}，resp：{resp}")
    return resp, request_body


def fox_manual_withhold(**kwargs):
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
    url = gc.REPAY_URL + fox_manual_withhold_path

    customer_bank_card_encrypt = kwargs['customer_bank_card_encrypt']
    customer_mobile_encrypt = kwargs['customer_mobile_encrypt']
    asset_period = kwargs['asset_period'] if kwargs['asset_period'] else None
    asset_item_no = kwargs['asset_item_no']
    amount = kwargs["amount"]

    request_body = {
        "type": "FoxManualWithhold",
        "key": get_guid(),
        "from_system": "Fox",
        "data": {
            "asset_item_no": asset_item_no,
            "amount": amount,
            "serial_no": "FOX_{}".format(get_guid()),
            "customer_bank_card_encrypt": customer_bank_card_encrypt,
            "customer_mobile_encrypt": customer_mobile_encrypt,
            "customer_bank_code": "ICBC",
            "operator": "管理员",
            "asset_period": asset_period
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
    LogUtil.log_info(f"贷后手动代扣发起成功，url:{url},request：{request_body}，resp：{resp}")
    return resp, request_body


def manual_withhold(**kwargs):
    """
    biz页面的手动代扣接口
    :param kwargs: dict包含个人信息,代扣金额,资产编号,代扣期次
    :return: json
        example:
            {
                "code": 2,
                "message": "交易处理中",
                "data": null
            }
    """
    url = gc.REPAY_URL + manual_withhold_path

    project_num = kwargs["project_num"]
    amount = kwargs["amount"]
    card_num_encrypt = kwargs["card_num_encrypt"]
    card_user_id_encrypt = kwargs["card_user_id_encrypt"]
    card_user_name_encrypt = kwargs["card_user_name_encrypt"]
    card_user_phone_encrypt = kwargs["card_user_phone_encrypt"]
    period = kwargs["period"] if kwargs["period"] else ""
    no_loan_no = kwargs.get("no_loan_no", "")
    no_loan_amount = kwargs.get("no_loan_amount", "")

    request_body = {
        "type": "WebManualWithhold",
        "from_system": "Biz",
        "key": "m" + get_guid(),
        "data": {
            "project_num": project_num,
            "amount": amount,
            "ref_asset_item_no": no_loan_no,
            "ref_asset_amount": no_loan_amount,
            "serial_no": "{}_1".format(get_guid()),
            "card_num_encrypt": card_num_encrypt,
            "card_user_id_encrypt": card_user_id_encrypt,
            "card_user_name_encrypt": card_user_name_encrypt,
            "card_user_phone_encrypt": card_user_phone_encrypt,
            "operator": "管理员",
            "from_system": "Biz",
            "period": period
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=request_body))
    LogUtil.log_info(f"Biz页面的手动代扣发起成功，url:{url},request：{request_body}，resp：{resp}")
    return resp, request_body


def paysvr_callback(merchant_key, transaction_status, channel_name="baidu_tq3_quick", channel_message="交易失败"):
    withhold = get_withhold_by_serial_no(merchant_key)
    withhold_channel = withhold[0]["withhold_channel"]
    if withhold_channel is None or withhold_channel == "":
        withhold_channel = channel_name
    url = gc.REPAY_URL + paysvr_callback_path
    req_body = {
        "merchant_key": merchant_key,
        "channel_name": withhold_channel,
        "channel_message": channel_message,
        "channel_key": merchant_key,
        "finished_at": get_date(),
        "transaction_status": transaction_status,
        "sign": "6401cd046b5ae44ef208b8ea82d398ab",
        "from_system": "paysvr"
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=req_body))
    LogUtil.log_info(f"Paysvr回调发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def paysvr_trade_callback(merchant_key, transaction_status, channel_name="baofoo_tq4_protocol"):
    url = gc.REPAY_URL + paysvr_trade_callback_path
    req_body = {
        "merchant_key": merchant_key,
        "channel_name": channel_name,
        "channel_key": merchant_key,
        "finished_at": get_date(),
        "transaction_status": transaction_status,
        "sign": "6401cd046b5ae44ef208b8ea82d398ab",
        "from_system": "paysvr"
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=req_body))
    LogUtil.log_info(f"Paysvr trade回调发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def mozhi_beiyin_callback(merchant_key, due_bill_no, amount, transaction_status="SUCCESS", channel="BEIYIN"):
    url = gc.REPAY_URL + mozhi_callback_path
    req_body = {
        "userId": "412724199006262123",
        "outOrderNo": "TMZ-" + due_bill_no,
        "transNo": merchant_key,
        "repayStatus": transaction_status,
        "failCode": "6",
        "repayResult": transaction_status,
        "repayResultList": [
            {
                "outOrderNo": due_bill_no,
                "status": transaction_status,
                "amount": amount,
                "authorizeChannel": channel,
                "repayItems": [
                    {
                        "termNo": 1,
                        "termAmount": amount,
                        "termPrincipal": 0,
                        "termInterest": 0,
                        "termPrinPenalty": 0,
                        "termInterPenalty": 0,
                        "termFee": 0,
                        "termInsuranceAmount": 0
                    }
                ]
            }
        ],
        "repaySource": "MZ"
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=req_body))
    LogUtil.log_info(f"墨智北银回调发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def weishenma_daxinganling_callback(merchant_key, item_no, amount, transaction_status="success"):
    url = gc.REPAY_URL + weishenma_callback_path
    req_body = {
        "state": transaction_status,
        "shddh": item_no,
        "sign": get_random_num(),
        "repay_money": str(amount),
        "repay_method": "withhold",
        "repay_type": "2",
        "repay_qx": 1,
        "serial_number": "CK" + item_no,
        "trade_endtime": "20200721204208",
        "repay_remark": merchant_key
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}, json=req_body))
    LogUtil.log_info(f"微神马回调发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def project_repay_query(project_num, project_type="paydayloan"):
    url = gc.REPAY_URL + project_repay_query_path.format(project_num, project_type)
    resp = parse_resp_body(requests.request(method='get', url=url))
    LogUtil.log_info(f"Dsq发起查询成功，url:{url},resp：{json.dumps(resp['content'])}")
    return resp


def repay_combo_query_key(req_key):
    url = gc.REPAY_URL + combo_query_key_path
    req_body = {
        "type": "PaydayloanUserActiveRepay",
        "key": req_key,
        "from_system": "DSQ"
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"DSQ查询代扣发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp, req_body, url


def repay_combo_query_order(order_no):
    url = gc.REPAY_URL + combo_query_order_path
    req_body = {
        "type": "PaydayloanUserActiveRepay",
        "order_no": order_no,
        "from_system": "DSQ"
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"DSQ查询代扣发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp, req_body, url


def trade_withhold(ref_no, trade_type, owner, amount):
    url = gc.REPAY_URL + trade_withhold_path
    req_key = get_guid()
    req_body = {
        "from_system": "dsq",
        "key": req_key,
        "type": "TradeOrderApply",
        "sync_datetime": None,
        "busi_key": f"comobo_{get_guid()}",
        "data": {
            "lockKey": f"comobo_{get_guid()}_third",
            "ref_no": ref_no,
            "trade_type": trade_type,
            "owner": owner,
            "withhold_type": "active",
            "amount": amount,
            "mobile_encrypt": "enc_01_4078360_712",
            "id_num_encrypt": "enc_02_4078420_505",
            "username_encrypt": "enc_04_4078410_417",
            "card_num_encrypt": "enc_03_2566873927553386496_624",
            "card_code": "ABC",
            "callback": None,
            "coupon_num": None,
            "coupon_amount": None
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    resp.update({"req_key": req_key})
    LogUtil.log_info(f"订单代扣发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def query_withhold(item_no):
    url = gc.REPAY_URL + query_withhold_path
    req_body = {
        "withhold_asset_item_no": item_no
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"query_withhold发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp, req_body, url


def query_withhold_by_one(item_no, serial_no):
    url = gc.REPAY_URL + query_withhold_by_one_path.format(item_no, serial_no)
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"}))
    LogUtil.log_info(f"query_withhold_by_one 发起成功，url:{url},resp：{resp}")
    return resp, url


def asset_repay_period(asset_item_no, period, recharge_serial_no):
    url = gc.REPAY_URL + asset_repay_period_path
    req_body = {
        "from_system": "Biz",
        "type": "AssetRepayPeriod",
        "key": get_guid(),
        "data": {
            "asset_item_no": asset_item_no,
            "period": period,
            "operator_id": "157",
            "operator_name": "ff",
            "recharge_serial_no": recharge_serial_no
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"asset_repay_period 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp, req_body, url


def asset_repay(item_no, amount, period):
    url = gc.REPAY_URL + asset_repay_path
    req_body = {
        "from_system": "Biz",
        "type": "AssetRepay",
        "key": get_guid(),
        "data": {
            "project_num": item_no,
            "date": None,
            "merchant_id": None,
            "serial_no": None,
            "repay_periods": [
                {
                    "period": period,
                    "amount": amount
                }
            ]
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"asset_repay 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp, req_body, url


def asset_settle_period(item_no, period):
    url = gc.REPAY_URL + asset_settle_period_path
    req_body = {
        "from_system": "BIZ",
        "key": get_guid(),
        "type": "AssetSettlePeriod",
        "data": {
            "asset_item_no": item_no,
            "period": period
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    return resp, req_body, url


def asset_tran_decrease(item_no, amount, period, type):
    url = gc.REPAY_URL + asset_tran_decrease_path
    req_body = {
        "key": get_guid(),
        "type": "DecreaseLateInterest",
        "from_system": "Fox",
        "data": {
            "asset_item_no": item_no,
            "period": period,
            "amount": amount,
            "type": type
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"asset_tran_decrease 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp, req_body, url


def asset_tran_decrease_late_fee(item_no, amount, period):
    url = gc.REPAY_URL + asset_tran_decrease_late_fee_path
    req_body = {
        "from_system": "BIZ",
        "key": get_guid(),
        "type": "AssetDecreaseLateFee",
        "data": {
            "asset_item_no": item_no,
            "period": period,
            "amount": amount,
            "type": None,
            "comment": "fox减免资产费用成功",
            "operator_id": None,
            "operator_name": None,
            "fromSystem": None,
            "send_change_mq": True
        },
        "sync_datetime": get_timestamp_by_now(),
        "busi_key": None
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"asset_tran_decrease 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp, req_body, url


def asset_repay_reverse(item_no, channel_key):
    url = gc.REPAY_URL + asset_repay_reverse_path
    req_body = {
        "from_system": "Biz",
        "key": get_guid(),
        "type": "AssetRepayReverse",
        "data": {
            "asset_item_no": item_no,
            "serial_no": channel_key,
            "operator_id": "1",
            "operator_name": "wq",
            "comment": "还款逆操作"
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    return resp


def account_recharge(amount, user_id_num_encrypt, item_no, card_num_encrypt):
    url = gc.REPAY_URL + account_recharge_path
    req_body = {
        "key": get_guid(),
        "type": "AccountRecharge",
        "from_system": "Biz",
        "data": {
            "user_id_num_encrypt": user_id_num_encrypt,
            "amount": amount,
            "serial_no": "Autotest" + item_no,
            "merchant_id": "4",
            "asset_item_no": item_no,
            "date": get_date(),
            "card_num_encrypt": card_num_encrypt,
            "comment": "API充值测试",
            "withhold_recharge": False,
            "operator_id": 1,
            "operator_name": "ff"
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    return resp, req_body, url


def fox_manual_withhold_query(item_no, serial_no):
    url = gc.REPAY_URL + fox_manual_withhold_query_path
    req_body = {
        "serial_no": serial_no,
        "asset_item_no": item_no,
        "from_system": "dsq"
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    return resp, req_body, url


def account_balance_clear(item_no, id_num):
    url = gc.REPAY_URL + account_balance_clear_path
    req_body = {
        "key": get_guid(),
        "type": "AccountClear",
        "from_system": "BIZ",
        "data": {
            "asset_item_no": item_no,
            "user_id_num_encrypt": id_num,
            "operator_id": 1,
            "operator_name": "自动化测试"
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    return resp, req_body, url


def asset_provision_settle(item_no, period=None):
    # 拨备结清资产
    url = gc.REPAY_URL + asset_provision_settle_path
    req_body = {
        "from_system": "FOX",
        "key": get_guid(),
        "type": "provisionSettleAsset",
        "data": {
            "amount": "",
            "comment": "auto test",
            "item_no": item_no,
            "operate_name": "zss",
            "period": period,
            "provision_type": "arbitration"
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"拨备结清发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp, req_body, url


def sync_withhold_card(id_num, user_name, bank_num, tel, from_system='strawberry'):
    url = gc.REPAY_URL + sync_withhold_card_path

    req_body = {
        "from_system": from_system,
        "key": get_guid(),
        "type": "withholdCard",
        "data": {
            "withholdCards": [
                {
                    "withhold_card_user_idnum_encrypt": id_num,
                    "withhold_card_user_name_encrypt": user_name,
                    "withhold_card_card_num_encrypt": bank_num,
                    "withhold_card_user_phone_encrypt": tel,
                    "withhold_card_bank_code": "PSBC",
                    "withhold_card_bind_time": get_date(),
                    "withhold_card_priority": 1,
                    "withhold_card_memo": "自动化测试",
                    "withhold_card_from_app": "syl"
                }
            ]
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"同步代扣卡发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp, req_body


def withhold_refund(merchant_key, refund_amount, serial_no_list=[], item_no_list=[]):
    url = gc.REPAY_URL + withhold_refund_path
    req_key = get_guid()
    req_body = {
        "type": "RepeatedWithholdRefund",
        "key": req_key,
        "from_system": "biz",
        "data": {
            "refund_withhold_serial_no": merchant_key,
            "operator": "朱莎莎",
            "amount": refund_amount,
            "repay_withhold_serial_no": serial_no_list,
            "detail_list": item_no_list
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    resp.update({"req_key": req_key})
    LogUtil.log_info(f"代扣退款发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def mozhi_withhold_apply(due_bill_no, withhold_amount, card_num, period=1):
    url = gc.REPAY_URL + mozhi_apply_path
    req_key = get_guid()
    req_body = {
        "payAmount": withhold_amount,
        "bankCardNo": card_num,
        "loanTransNo": due_bill_no,
        "transNo": due_bill_no + "_KUAINIU_PAY",
        "repayTerms": [
            {
                "term": period,
                "amount": withhold_amount
            }
        ]
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    resp.update({"req_key": req_key})
    LogUtil.log_info(f"墨智代偿后切我方代扣发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def mozhi_withhold_query(due_bill_no):
    url = gc.REPAY_URL + mozhi_query_path
    req_key = get_guid()
    req_body = {
        "loanTransNo": due_bill_no,
        "transNo": due_bill_no + "_KUAINIU_PAY"
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    resp.update({"req_key": req_key})
    LogUtil.log_info(f"墨智代偿后切我方代扣查询成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def fix_status_asset_change_mq_sync(item_no, operate_type="asset"):
    url = gc.REPAY_URL + asset_change_mq
    req_body = {
        "type": "AssetChangeMQ",
        "key": get_guid(),
        "from_system": "BIZ",
        "data": {
            "owner": "KN",
            "action": "fix_status",
            "item_no": item_no,
            "user_id_num_encrypt": "",
            "operate_type": operate_type,
            "recharge_log_id_list": [],
            "repay_log_id_list": [],
            "tran_log_id_list": []
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"重新同步发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def fk_asset_info(item_no, source='bc'):
    url = gc.REPAY_URL + fk_asset_info_path
    req_body = {
        "apply_code": item_no,
        "apply_source": source
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"fk_asset_info 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def four_factor_withhold(**kwargs):
    url = gc.REPAY_URL + four_factor_withhold_path
    card_num_encrypt = kwargs["card_num_encrypt"]
    id_num_encrypt = kwargs["card_user_id_encrypt"]
    username_encrypt = kwargs["card_user_name_encrypt"]
    mobile_encrypt = kwargs["card_user_phone_encrypt"]
    amount = kwargs["amount"]
    req_key = get_guid()
    req_body = {
        "from_system": "BIZ",
        "key": get_guid(),
        "type": "WithholdWithoutProject",
        "data": {
            "amount": amount,
            "operator": "自动化测试",
            "card_num_encrypt": card_num_encrypt,
            "card_user_id_encrypt": id_num_encrypt,
            "card_user_name_encrypt": username_encrypt,
            "card_user_phone_encrypt": mobile_encrypt
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    resp.update({"req_key": req_key})
    LogUtil.log_info(f"四要素代扣发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def asset_grant_success_to_rbiz(item_no, source_type=None, sub_order_type=None):
    url = gc.REPAY_URL + asset_withdraw_success
    asset_info = deepcopy(asset_grant)
    biz_asset = get_biz_asset_info_by_item_no(item_no)
    # version取biz表中的数字+10
    version = int(biz_asset[0]["asset_version"]) + 10
    asset = get_asset_from_asset_and_asset_extend(item_no, version, source_type)
    drans = get_dtransactions_grant_from_asset_tran(item_no)
    drans_princial_and_interest = get_dtransactions_principal_and_interest_from_asset_tran(item_no)
    fees = get_fees_from_asset_tran(item_no)
    loan_record = get_loan_record_from_asset(item_no)
    repay_card = get_repay_card_from_asset_card(item_no)
    receive_card = get_receive_card_from_asset_card(item_no)
    asset_info["data"]['asset'] = asset[0]
    asset_info["data"]["asset"]["sub_order_type"] = sub_order_type if sub_order_type is not None else ""
    asset_info["key"] = item_no + get_random_str(3)
    asset_info["data"]['loan_record'] = loan_record[0]
    asset_info["data"]['dtransactions'].extend(drans)
    asset_info["data"]['dtransactions'].extend(drans_princial_and_interest)
    asset_info["data"]['fees'].extend(fees)
    asset_info["data"]['cards_info']['repay_card'] = repay_card[0]
    asset_info["data"]['cards_info']['receive_card'] = receive_card[0]
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=asset_info))
    LogUtil.log_info(f"放款成功资产同步rbiz成功，url:{url}, request：{item_no}，resp：{resp}")
    return item_no


# biz-central和biz-contract接收进件成功消息
def asset_import_success_to_rbiz_by_api(item_no):
    asset_import_body = get_asset_import_data_from_sendmsg_by_item_no(item_no)
    biz_central_url = gc.BIZ_CENTRAL_URL + "/asset/import"
    contract_url = gc.CONTRACT_URL + "/asset/import"
    resp = parse_resp_body(
        requests.request(method='post', url=biz_central_url, headers={"content-type": "application/json"},
                         json=asset_import_body))
    LogUtil.log_info(f"进件消息同步biz-central成功，url:{biz_central_url}, request：{item_no}，resp：{resp}")
    resp = parse_resp_body(
        requests.request(method='post', url=contract_url, headers={"content-type": "application/json"},
                         json=asset_import_body))
    LogUtil.log_info(f"进件消息同步biz-contract成功，url:{contract_url}, request：{item_no}，resp：{resp}")
    task_list = get_central_task_id_by_type(item_no, "AssetImport")
    if task_list is not None and len(task_list) > 0:
        run_task_in_biz_central_by_task_id(task_list[0]["task_id"])
        wait_central_task_close_by_id(task_list[0]["task_id"])


# biz-central接收放款成功消息
def asset_withdraw_success_to_biz_by_api(item_no):
    msg_info = get_sendmsg_list_by_order_no_and_type(item_no, "AssetWithdrawSuccess")
    if msg_info:
        asset_withdraw_body = json.loads(msg_info[0]['sendmsg_content'])["body"]
        biz_central_url = gc.BIZ_CENTRAL_URL + "/asset/withdrawSuccess"

        resp = parse_resp_body(
            requests.request(method='post', url=biz_central_url, headers={"content-type": "application/json"},
                             json=asset_withdraw_body))
        LogUtil.log_info(f"放款成功资产同步biz-central成功，url:{biz_central_url}, request：{item_no}，resp：{resp}")
        # 小单发送权责分配消息
        if asset_withdraw_body["data"]["asset"]["loan_channel"] == "noloan":
            biz_dcs_url = gc.DCS_URL + "/accrual/allocated-new"
            resp = parse_resp_body(
                requests.request(method='post', url=biz_dcs_url, headers={"content-type": "application/json"},
                                 json=asset_withdraw_body))
            LogUtil.log_info(f"小单放款成功资产同步dcs成功，url:{biz_dcs_url}, request：{item_no}，resp：{resp}")
        task_list = get_central_task_id_by_type(item_no, "AssetWithdrawSuccess")
        if task_list is not None and len(task_list) > 0:
            run_task_in_biz_central_by_task_id(task_list[0]["task_id"])
            wait_central_task_close_by_id(task_list[0]["task_id"])


# biz-central和dcs接收账成功消息--充值
def asset_recharge_success_account_to_biz_by_api(order_no):
    msg_info = get_sendmsg_list_by_order_no_and_type(order_no, "account_change_account_update")
    if msg_info:
        for msg in msg_info:
            msg_body = json.loads(msg['sendmsg_content'])["body"]
            biz_central_url = gc.BIZ_CENTRAL_URL + "/account/import"
            dcs_url = gc.DCS_URL + "/paydayloan/repay/notify"
            resp = parse_resp_body(
                requests.request(method='post', url=biz_central_url, headers={"content-type": "application/json"},
                                 json=msg_body))
            LogUtil.log_info(f"账充值信息同步biz-central成功，url:{biz_central_url}, request：{order_no}，resp：{resp}")
            resp = parse_resp_body(
                requests.request(method='post', url=dcs_url, headers={"content-type": "application/json"},
                                 json=msg_body))
            LogUtil.log_info(f"账充值信息同步dcs成功，url:{dcs_url}, request：{order_no}，resp：{resp}")
            run_biz_central_task_by_count(order_no, 5)


# biz-central和dcs接收账成功消息--还款
def asset_repay_success_account_to_biz_by_api(order_no):
    msg_info = get_sendmsg_list_by_order_no_and_type(order_no, "account_change_tran_repay")
    if msg_info:
        for msg in msg_info:
            msg_body = json.loads(msg['sendmsg_content'])["body"]
            biz_central_url = gc.BIZ_CENTRAL_URL + "/account/import"
            dcs_url = gc.DCS_URL + "/paydayloan/repay/notify"
            resp = parse_resp_body(
                requests.request(method='post', url=biz_central_url, headers={"content-type": "application/json"},
                                 json=msg_body))
            LogUtil.log_info(f"账还款信息同步biz-central成功，url:{biz_central_url}, request：{order_no}，resp：{resp}")
            resp = parse_resp_body(
                requests.request(method='post', url=dcs_url, headers={"content-type": "application/json"},
                                 json=msg_body))
            LogUtil.log_info(f"账还款信息同步dcs成功，url:{dcs_url}, request：{order_no}，resp：{resp}")
            run_biz_central_task_by_count(order_no, 5)


# biz-central和dcs接收账成功消息--还款
def asset_repay_success_asset_change_to_biz_by_api(order_no, msg_type="asset_change_tran_repay"):
    msg_info = get_sendmsg_list_by_order_no_and_type(order_no, msg_type)
    if msg_info:
        for msg in msg_info:
            msg_body = json.loads(msg['sendmsg_content'])["body"]
            biz_central_url = gc.BIZ_CENTRAL_URL + "/asset/change"
            resp = parse_resp_body(
                requests.request(method='post', url=biz_central_url, headers={"content-type": "application/json"},
                                 json=msg_body))
            LogUtil.log_info(f"资产变更消息同步biz-central成功，url:{biz_central_url}, request：{order_no}，resp：{resp}")
            task_list = get_central_task_id_by_type(order_no, "AssetChange")
            if task_list is not None and len(task_list) > 0:
                run_task_in_biz_central_by_task_id(task_list[0]["task_id"])
                wait_central_task_close_by_id(task_list[0]["task_id"])
            run_msg_in_biz_central(order_no)
            task_list = get_central_task_id_by_type(order_no, "UserRepay")
            if task_list is not None and len(task_list) > 0:
                run_task_in_biz_central_by_task_id(task_list[0]["task_id"])
                wait_central_task_close_by_id(task_list[0]["task_id"])


# 代扣记录同步--还款
def asset_withhold_success_to_biz_by_api(order_no):
    msg_info = get_sendmsg_list_by_order_no_and_type(order_no, "WithholdResultImport")
    for msg in msg_info:
        msg_body = json.loads(msg['sendmsg_content'])["body"]
        biz_central_url = gc.BIZ_CENTRAL_URL + "/withhold/withholdResultImport"
        resp = parse_resp_body(
            requests.request(method='post', url=biz_central_url, headers={"content-type": "application/json"},
                             json=msg_body))
        LogUtil.log_info(f"代扣信息同步biz-central成功，url:{biz_central_url}, request：{order_no}，resp：{resp}")
        task_list = get_central_task_id_by_type(order_no, "WithholdResultImport")
        if task_list is not None and len(task_list) > 0:
            run_task_in_biz_central_by_task_id(task_list[0]["task_id"])
            wait_central_task_close_by_id(task_list[0]["task_id"], 10)
        run_biz_central_task_by_count(order_no)


def capital_asset_success_to_rbiz(item_no):
    url = gc.REPAY_URL + capital_asset_success
    url_central = gc.BIZ_CENTRAL_URL + capital_asset_central
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
    resp_biz = parse_resp_body(
        requests.request(method='post', url=url_central, headers={"content-type": "application/json"},
                         json=capital_asset_info))
    LogUtil.log_info(f"资方还款计划同步rbiz成功，url:{url},request：{item_no}，resp：{resp}")
    LogUtil.log_info(f"资方还款计划同步biz成功，url:{url_central},request：{item_no}，resp_biz：{resp_biz}")
    return item_no


# 提供给fox使用的接口 ---start

def fox_deadline_asset_query(due_date=get_date_before_today(day=1, fmt="%Y-%m-%d")):
    url = gc.REPAY_URL + fox_deadline_asset_query_path
    req_body = {
        "due_date": due_date,
        "page_size": 1000
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"fox_deadline_asset_query发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def asset_overdue_view_for_fox(item_no):
    url = gc.BIZ_URL + asset_overdue_view_for_fox_path.format(item_no)
    resp = parse_resp_body(requests.request(method='get', url=url))
    LogUtil.log_info(f"asset_overdue_view_for_fox查询成功，url:{url},resp：{resp}")
    return resp


def fox_query_card_list(id_num):
    url = gc.REPAY_URL + fox_query_card_list_path
    req_body = {
        "from_app_name": "Fox",
        "user_id_num_encrypt": id_num
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"fox_query_card_list 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def asset_bill_decrease(item_no, decrease_amount):
    url = gc.REPAY_URL + asset_bill_decrease_path
    req_body = {
        "from_system": "CRM",
        "key": get_guid(),
        "type": "BillDecrease",
        "data": {
            "asset_item_no": item_no,
            "bill_balance_amount": decrease_amount,
            "operator": "自动化测试"
        }
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"asset_bill_decrease 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def asset_buyback(item_no, loan_channel, prin_amt=700000, buyback_prin_amt=606452, buyback_int_amt=4882):
    url = gc.REPAY_URL + asset_buyback_path
    req_body = {
        "type": "asset_buyback_notify",
        "key": loan_channel + get_random_str(),
        "from_system": "BIZ",
        "data": {
            "asset_item_no": item_no,
            "period_count": 12,
            "granted_principal_amount": prin_amt,
            "start_period": 4,
            "buyback_total_principal_amount": buyback_prin_amt,
            "buyback_total_interest_amount": buyback_int_amt,
            "buyback_start_date": get_date(fmt="%Y-%m-%d") + " 00:00:00",
            "buyback_category": "buyback",
            "channel": loan_channel,
            "needSettleReduce": False
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"asset_buyback 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def change_asset_due_at_by_test_platform(item_no, month=0, day=0):
    url = "http://auto-vue.k8s-ingress-nginx.kuainiujinke.com/api/repay/repay_tools/change_asset"
    req_body = {
        "env": str(gc.ENV),
        "item_no": item_no,
        "item_no_rights": "",
        "advance_day": day,
        "advance_month": month,
        "refresh_late": False,
        "mock_name": "rbiz_manual_test"
    }

    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(f"change_asset_due_at_by_test_platform 发起成功，url:{url},request：{req_body}，resp：{resp}")
    return resp


def run_job_by_api(job_type, job_params):
    job_url = gc.REPAY_URL + "/job/run"
    params = {"jobType": job_type,
              "param": json.dumps(job_params)}
    return Http.http_get(job_url, params=params)


def run_withholdAutoV1_by_api(item_no=None, loan_channel=None):
    job_type = "withholdAutoV1"
    job_params = {
        "selectColumns": "distinct t1.asset_tran_asset_item_no, t1.asset_tran_period, "
                         "DATE_FORMAT(t1.asset_tran_due_at,'%Y-%m-%d') asset_tran_due_at",
        "fromTable": "asset a",
        "joinSql": [
            "inner join asset_tran t1 on a.asset_item_no = t1.asset_tran_asset_item_no"
        ],
        "whereSql": [
            "and t1.asset_tran_status = 'nofinish' and t1.asset_tran_due_at >= date_sub(current_date, interval 1 day) "
            "and t1.asset_tran_due_at < date_add(current_date, interval 1 day)",
            "and t1.asset_tran_type not like 'late%' and t1.asset_tran_type != 'credit_fee'",
            "and a.asset_type = 'paydayloan' and a.asset_status in('repay','late')",
            "and a.asset_from_system <> 'hxyl'",
            "and not exists(select 1 from asset_operation_auth where asset_item_no = asset_operation_auth_asset_item_no"
            " and asset_operation_auth_action in ('withhold','createWithholdAutoTask'))"
        ],
        "retry": True,
        "stepSeconds": 2,
        "noLoanExeTime": "0:00",
        "loanExeTime": "0:00",
        "step": 150
    }
    if item_no is not None:
        job_params["whereSql"].append("and a.asset_item_no = '%s'" % item_no)
    if loan_channel is not None:
        job_params["whereSql"].append("and a.asset_loan_channel = '%s'" % loan_channel)
    run_job_by_api(job_type, job_params)


def run_refreshLateFeeV1_by_api(item_no=None):
    job_type = "refreshLateFeeV1"
    job_params = {
        "startDate": get_date(year=-1),
        "joinSql": [
            "left join asset_late_fee_refresh_log as c on a.asset_item_no = c.asset_late_fee_refresh_log_asset_item_no "
            "and c.asset_late_fee_refresh_log_update_at >= current_date and asset_late_fee_refresh_log_item_type = 'asset'"
        ],
        "whereSql": [
            "and a.asset_from_system != 'hxyl'",
            "and a.asset_status= 'repay'",
            "and c.`asset_late_fee_refresh_log_asset_item_no` is null",
            "and t.asset_tran_amount > t.asset_tran_repaid_amount",
            "and  a.asset_sub_type not in('kkj','dkhk')",
            "and a.asset_product_category not in('7','14')",
            " and a.asset_owner not like 'STB%'"
        ],
        "refreshAll": False
    }
    if item_no is not None:
        job_params["whereSql"].append("and a.asset_item_no like '%%%s%%'" % item_no)
    run_job_by_api(job_type, job_params)
