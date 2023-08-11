# -*- coding: utf-8 -*-
import json

import common.global_const as gc
from biztest.config.payment.url_config import global_rbiz_callback, global_gbiz_callback, global_rbiz_redirect, \
    global_sign_company_yomoyo, global_dsq_merchant_name, global_amount, xendit_ebank_resp_payment_mode
from biztest.function.global_payment.global_payment_db_operation import get_task, get_sendmsg, \
    update_task_by_task_order_no, update_task_by_task_id
from biztest.util.asserts.assert_util import Assert
from biztest.util.http.http_util import Http
from biztest.util.tools.tools import get_random_str, get_random_num, get_date, get_item_no


# 泰国绑卡-传四要素
def auto_bind_tha(sign_company, element, ifsc="test", bank_account_encrypt=None, upi_encrypt=None,
                  card_num_encrypt=None):
    url = gc.PAYMENT_URL + "/card/autoBind"
    request_body = {
        "merchant_name": "dsq",
        "merchant_key": "AutoBind_" + get_random_str(),
        "sign_company": sign_company,

        "id_num_encrypt": element["data"]["id_number_encrypt"],
        "user_name_encrypt": element["data"]["user_name_encrypt"],
        "mobile_encrypt": element["data"]["mobile_encrypt"],
        "email_encrypt": element["data"]["email_encrypt"],
        "address_encrypt": element["data"]["address_encrypt"],

        "bank_account_encrypt": bank_account_encrypt,
        "ifsc": ifsc,
        "card_num_encrypt": card_num_encrypt,
        "upi_encrypt": upi_encrypt,
        "card_type": "",
        "card_expiry_year": "",
        "card_expiry_month": "",
        "card_cvv": ""
    }
    return request_body, Http.http_post(url, request_body)


# 印度/巴基斯坦绑卡-传uuid
def auto_bind(sign_company, card_uuid="181622481700782080", user_uuid="181622481700782080"):
    url = gc.PAYMENT_URL + "/card/autoBind"
    request_body = {
        "merchant_name": "dsq",
        "merchant_key": "AutoBind_" + get_random_str(),
        "sign_company": sign_company,
        "card_uuid": card_uuid,
        "user_uuid": user_uuid,
        "callback_url": ""
    }
    return request_body, Http.http_post(url, request_body)


# 绑卡结果查询
def global_bindResult(merchant_key):
    url = gc.PAYMENT_URL + "/card/bindResult"
    request_body = {
        "merchant_name": "dsq",
        "merchant_key": merchant_key
    }
    return request_body, Http.http_post(url, request_body)


def global_bindCheck(sign_company, card_uuid):
    url = gc.PAYMENT_URL + "/card/bindCheck"
    request_body = {
        "merchant_name": global_dsq_merchant_name,
        "sign_company": sign_company,
        "card_uuid": card_uuid
    }
    return request_body, Http.http_post(url, request_body)


# 代扣
def auto_pay(sign_company=None, payment_type="", payment_option="", payment_mode="", card_uuid="181622481700782080",
             user_uuid="181622481700782080",
             card_num="", operator="USER", channel_name=None, amount=global_amount):
    """
    海外项目代扣
       :param
       :return: json
           example:
    """
    url = gc.PAYMENT_URL + "/withhold/autoPay"
    request_body = {
        "merchant_name": "rbiz",
        "merchant_key": "Auto_WH_" + get_item_no()[6:],
        "amount": amount,
        "sign_company": sign_company,
        "channel_name": channel_name,
        "card_uuid": card_uuid,
        "user_uuid": user_uuid,
        "operator": operator,
        "redirect": global_rbiz_redirect,
        "callback": global_rbiz_callback,
        "reason": "f-还款",
        "card_num_encrypt": card_num,
        "card_cvv": "111",
        "card_expiry_year": "12",
        "card_expiry_month": "05",
        "payment_type": payment_type,
        "payment_option": payment_option,
        "payment_mode": payment_mode,
        "user_ip": "27.55.70.41",
        "device_info":
            {
                "system_name": "android",
                "system_version": "7.0"
            },
        "sdk_info": [
            {
                "name": "cashfree",
                "version": "1.0"
            }
        ]
    }
    return request_body, Http.http_post(url, request_body)


def global_withhold_query(merchant_key):
    url = gc.PAYMENT_URL + "/withhold/query"
    request_body = {
        "merchant_name": "rbiz",
        "merchant_key": merchant_key
    }
    return request_body, Http.http_post(url, request_body)


def global_withhold_close_order(merchant_key):
    url = gc.PAYMENT_URL + "/withhold/closeOrder"
    request_body = {
        "merchant_name": "rbiz",
        "merchant_key": merchant_key
    }
    return request_body, Http.http_post(url, request_body)


def global_withdraw_balance(sign_company):
    url = gc.PAYMENT_URL + "/withdraw/balance"
    request_body = {
        "merchant_name": "gbiz",
        "sign_company": sign_company
    }
    return request_body, Http.http_post(url, request_body)


def auto_withdraw(sign_company, card_uuid="181622481700782080", user_uuid="181622481700782080", channel_name="", amount=global_amount):
    url = gc.PAYMENT_URL + "/withdraw/autoWithdraw"
    request_body = {
        "merchant_name": "gbiz",
        "merchant_key": "Auto_WD_" + get_item_no()[6:],
        "trade_no": "Trade_" + get_item_no()[6:],
        "amount": amount,
        "sign_company": sign_company,
        "channel_name": channel_name,
        "user_uuid": user_uuid,
        "card_uuid": card_uuid,
        "reason": "f-放款",
        "callback": global_gbiz_callback
    }
    return request_body, Http.http_post(url, request_body)


def global_autoWithdraw_retry(sign_company, card_uuid, user_uuid="181622481700782080", channel_name="",
                              amount=global_amount,
                              merchant_key=""):
    url = gc.PAYMENT_URL + "/withdraw/autoWithdraw"
    request_body = {
        "merchant_name": "gbiz",
        "merchant_key": merchant_key,
        "trade_no": "Trade_" + get_item_no()[6:],
        "amount": amount,
        "sign_company": sign_company,
        "channel_name": channel_name,
        "user_uuid": user_uuid,
        "card_uuid": card_uuid,
        "reason": "f-放款",
        "callback": global_gbiz_callback
    }
    return request_body, Http.http_post(url, request_body)


def global_withdraw_query(merchant_key):
    url = gc.PAYMENT_URL + "/withdraw/query"
    request_body = {
        "merchant_name": "gbiz",
        "merchant_key": merchant_key
    }
    return request_body, Http.http_post(url, request_body)


def gbpay_qrcode_payment_callback(channel, amount, referno, gbpno):
    url = gc.PAYMENT_URL + "/gbpay/callback/payment/%s" % channel
    request_body = {
        "amount": amount,
        "referenceNo": referno,
        "gbpReferenceNo": gbpno
    }
    return request_body, Http.http_post(url, request_body)


def gbpay_qrcode_charge_callback(channel, amount, referno, resultCode="00"):
    url = gc.PAYMENT_URL + "/gbpay/callback/backgroupurl/%s" % channel
    request_body = {
        "amount": amount,
        "referenceNo": referno,
        "gbpReferenceNo": get_random_str(),
        "currencyCode": "764",
        "resultCode": resultCode,
        "totalAmount": amount,
        "fee": 4.028,
        "vat": 0.28196,
        "thbAmount": amount,
        "date": "09122020",
        "time": "170232",
        "paymentType": "Q"
    }
    return request_body, Http.http_post(url, request_body)


def gbpay_checkout_charge_callback(channel, amount, referno):
    url = gc.PAYMENT_URL + "/gbpay/callback/backgroupurl/%s" % channel
    request_body = {
        "totalAmount": "0",
        "amount": amount,
        "referenceNo": referno,
        "amountPerMonth": "0",
        "fee": "0.032",
        "resultCode": "00",
        "vat": "0.00224",
        "gbpReferenceNo": get_random_str(),
        "thbAmount": "0",
        "cardNo": "498765XXXXXX8769",
        "currencyCode": "764",
        "paymentType": "C"
    }
    return request_body, Http.http_post(url, request_body)


def run_task_by_order_no(order_no, except_json=None):
    update_task_by_task_order_no(order_no, task_next_run_at=get_date(day=-1))
    url = gc.PAYMENT_URL + "/task/runTaskByOrderNo"
    request_body = {
        "orderNo": order_no
    }
    resp = Http.http_post(url, request_body)
    if except_json is not None:
        Assert.assert_match_json(except_json, resp, "task运行不正确，task结果：%s" % str(resp))


def run_msg_by_order_no(order_no, except_json=None):
    url = gc.PAYMENT_URL + "/task/runSendMsgByOrderNo"
    request_body = {
        "orderNo": order_no
    }
    resp = Http.http_post(url, request_body)
    if except_json is not None:
        Assert.assert_match_json(except_json, resp, "msg运行不正确，msg结果：%s" % str(resp))


def run_task_by_task_id(task_id, except_json=None):
    update_task_by_task_id(task_id, task_next_run_at=get_date(day=-1))
    url = gc.PAYMENT_URL + "/task/runTaskById"
    request_body = {
        "id": task_id
    }
    resp = Http.http_post(url, request_body)
    if except_json is not None:
        Assert.assert_match_json(except_json, resp, "task运行不正确，task结果：%s" % str(resp))


def run_msg_by_msg_id(msg_id, except_json=None):
    url = gc.PAYMENT_URL + "/task/runSendMsgById"
    request_body = {
        "id": msg_id
    }
    resp = Http.http_post(url, request_body)
    if except_json is not None:
        Assert.assert_match_json(except_json, resp, "msg运行不正确，msg结果：%s" % str(resp))


def run_task(order_no, task_type, except_json=None):
    update_task_by_task_order_no(order_no, task_next_run_at=get_date(day=-1))
    task_list = get_task(task_order_no=order_no, task_status="open")
    task_id = 0
    for task in task_list:
        if task["task_type"] == task_type:
            task_id = task["task_id"]
            break
    if task_id == 0:
        raise Exception("no task found, task_order_no:%s, task_type:%s" % (order_no, task_type))
    run_task_by_task_id(task_id, except_json)


def run_msg(order_no, msg_type, except_json=None):
    msg_list = get_sendmsg(sendmsg_order_no=order_no, sendmsg_status="open")
    msg_id = 0
    for msg in msg_list:
        if msg["task_type"] == msg_type:
            msg_id = msg["task_id"]
            break
    if msg_id == 0:
        raise Exception("no task found, msg_order_no:%s, msg_type:%s" % (order_no, msg_type))
    run_task_by_task_id(msg_id, except_json)


def global_withhold_autoSubscribe(merchant_key, card_uuid, card_num_encrypt, user_name_encrypt, mobile_encrypt,
                                  email_encrypt, address_encrypt, ifsc):
    url = gc.PAYMENT_URL + "/withhold/autoSubscribe"
    request_body = {
        "merchant_name": global_dsq_merchant_name,
        "merchant_key": merchant_key,
        "sign_company": global_sign_company_yomoyo,
        "card_uuid": card_uuid,
        "card_num_encrypt": card_num_encrypt,
        "ifsc": ifsc,
        "user_name_encrypt": user_name_encrypt,
        "mobile_encrypt": mobile_encrypt,
        "email_encrypt": email_encrypt,
        "address_encrypt": address_encrypt,
        "redirect_url": global_rbiz_redirect,
        "callback_url": "",
        "card_type": "DC",
        "card_expiry_year": None,
        "card_expiry_month": None,
        "card_cvv": None,
        "id_num_encrypt": None
    }
    return request_body, Http.http_post(url, request_body)


def global_withhold_subscribeResult(merchant_key):
    url = gc.PAYMENT_URL + "/withhold/subscribeResult"
    request_body = {
        "merchant_name": global_dsq_merchant_name,
        "merchant_key": merchant_key
    }
    return request_body, Http.http_post(url, request_body)


def global_withhold_autoRegister(sign_company, user_uuid="181622481700782080", amount=""):
    url = gc.PAYMENT_URL + "/withhold/autoRegister"
    request_body = {
        "merchant_name": "dsq",
        "merchant_key": "AutoReg_" + get_random_str(),
        "sign_company": sign_company,
        "user_uuid": user_uuid,
        "account_no": "item_no%s" % get_random_num(),
        "amount": amount
    }
    return request_body, Http.http_post(url, request_body)


def global_withhold_unRegister(account_no):
    url = gc.PAYMENT_URL + "/withhold/unRegister"
    request_body = {
        "merchant_name": "dsq",
        "merchant_key": "UnReg_" + get_random_str(),
        "account_no": account_no
    }
    return request_body, Http.http_post(url, request_body)


def global_transfer_transfer(channel_name, in_account_no):
    url = gc.PAYMENT_URL + "/transfer/transfer"
    request_body = {
        "merchant_name": "dcs",
        "merchant_key": "Trans_%s" % get_random_str(),
        "trade_no": "Trade_%s" % get_random_str(),
        "amount": "121212",
        "channel_name": channel_name,
        "in_account_no": in_account_no,
        "reason": "清分转账",
        "callback": global_gbiz_callback
    }
    return request_body, Http.http_post(url, request_body)


def global_transfer_query(merchant_key):
    url = gc.PAYMENT_URL + "/transfer/query"
    request_body = {
        "merchant_name": "dcs",
        "merchant_key": merchant_key
    }
    return request_body, Http.http_post(url, request_body)


def global_transfer_balance(channel_name):
    url = gc.PAYMENT_URL + "/transfer/balance"
    request_body = {
        "merchant_name": "dcs",
        "channel_name": channel_name
    }
    return request_body, Http.http_post(url, request_body)


def global_fee_query(fee_type):
    url = gc.PAYMENT_URL + "/fee/query"
    request_body = {
        "merchant_name": "Rbiz",
        "merchant_key": "Fee_%s" % get_random_str(),
        "fee_type": fee_type
    }
    return request_body, Http.http_post(url, request_body)


def global_run_job(job_type, job_params):
    job_url = gc.PAYMENT_URL + "/job/run?jobType=%s" % job_type
    job_url = job_url + "&param=%s" % json.dumps(job_params)
    return Http.http_get(job_url)


# 刷下缓存
def clear_cache():
    cach_url = gc.PAYMENT_URL + "/manual/clearCache/route"
    return Http.http_get(cach_url)


# pandapay放款回调
def pandapay_withdraw_callback(channel, channel_key, status):
    url = gc.PAYMENT_URL + "/pandapay/callback/%s" % channel
    request_body = {
        "causaDevolucion": "自动化回调",
        "empresa": "TRANSFER_TO",
        "estado": status,
        "folioOrigen": channel_key,
        "id": int(get_random_num()[:6])
    }
    return request_body, Http.http_post(url, request_body)


def xendit_paycode_callback(channel, amount, ChannelKey, ChannelInnerKey="pcode-991099b0-cb2a-4a40-bcf3-0c5deb4d7036"):
    url = gc.PAYMENT_URL + "/xendit/callback/%s" % channel
    request_body = {
        "amount": global_amount / 100,
        "business_id": "619f2789bcee1cbe0f0e3e68",
        "channel_code": xendit_ebank_resp_payment_mode,
        "country_code": "PH",
        "currency": "PHP",
        "event": "payment_code.payment",
        "created": "2021-12-10T06:09:10.135001333Z",
        "payment_code": "CPPERSDSDB5PPH",
        "id": "pymt-af548f2c-bf9f-4f4c-8d24-996e53744fe4",
        "reference_id": ChannelKey,
        "remarks": "payment simulation",
        "payment_code_id": ChannelInnerKey,
        "status": "COMPLETED"  # COMPLETED=支付成功
    }
    return request_body, Http.http_post(url, request_body)


def xendit_ebank_callback(channel, amount, ChannelKey, ChannelInnerKey="pcode-991099b0-cb2a-4a40-bcf3-0c5deb4d7036"):
    url = gc.PAYMENT_URL + "/xendit/callback/%s" % channel
    request_body = {
        "data": {
            "id": ChannelInnerKey,
            "basket": None,
            "status": "SUCCEEDED",
            "actions": {
                "qr_checkout_string": None,
                "mobile_web_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=ce087b3d-b943-45ab-abc9-1c99009342d2",
                "desktop_web_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=ce087b3d-b943-45ab-abc9-1c99009342d2",
                "mobile_deeplink_checkout_url": None
            },
            "created": "2021-12-13T03:02:49.446671Z",
            "updated": "2021-12-13T03:02:49.487718Z",
            "currency": "PHP",
            "metadata": {
                "description": "test description"
            },
            "voided_at": None,
            "capture_now": True,
            "customer_id": None,
            "void_status": None,
            "callback_url": "https://biz-gateway-proxy.starklotus.com/phl_mayment1/xendit/callback/xendit_copperstone_ebank",
            "channel_code": xendit_ebank_resp_payment_mode,
            "failure_code": "fail mssage test",
            "reference_id": ChannelKey,
            "charge_amount": global_amount / 100,
            "capture_amount": global_amount / 100,
            "checkout_method": "ONE_TIME_PAYMENT",
            "refunded_amount": None,
            "payment_method_id": None,
            "channel_properties": {
                "failure_redirect_url": "http://www.baidu.com",
                "success_redirect_url": "http://www.baidu.com"
            },
            "is_redirect_required": True
        },
        "event": "ewallet.capture",
        "created": "2021-12-13T03:16:00.261180109Z",
        "business_id": "619f2789bcee1cbe0f0e3e68"
    }
    return request_body, Http.http_post(url, request_body)


def xendit_withdraw_callback(channel, amount, ChannelKey, ChannelInnerKey="disb-6a49375d-fc0b-4992-b46c-e04cede8388e"):
    url = gc.PAYMENT_URL + "/xendit/callback/%s" % channel
    request_body = {
        "id": ChannelInnerKey,
        "account_number": "09053005108",
        "amount": amount,
        "connector_reference": "SIMULATED_CONNECTOR_REFERENCE_1671604090578_8634",
        "channel_code": "PH_GCASH",
        "currency": "PHP",
        "description": ChannelKey,
        "entity": "xendit",
        "idempotency_key": ChannelKey,
        "reference_id": ChannelKey,
        "status": "COMPLETED",  # 只处理COMPLETED成功的回调
        # "failure_code": "INSUFFICIENT_BALANCE", # 代付成功的回调没有该字段
        "created": "2022-12-21T06:28:08.404Z",
        "updated": "2022-12-21T06:28:12.271Z",
        "account_name": "BENGNAN ADELYN ANGID"
    }
    return request_body, Http.http_post(url, request_body)


def easypaisa_paycode_inquiry(consumer_number):
    url = gc.PAYMENT_URL + "/easypaisa/easypaisa_goldlion_paycode/inquiry"
    req_data = {
        "username": "goldliontest",
        "password": "goldliontest_dev",
        "Consumer_number": consumer_number,
        "Bank_Mnemonic": "QISTPAY1"
    }
    resp = Http.http_post(url, req_data)
    return resp


def easypaisa_paycode_payment(consumer_number, amount):
    url = gc.PAYMENT_URL + "/easypaisa/easypaisa_goldlion_paycode/payment"
    req_data = {
        "username": "goldliontest",
        "password": "goldliontest_dev",
        "consumer_number": consumer_number,
        "tran_auth_id": "476022",
        "transaction_amount": amount,
        "tran_date": get_date(fmt="%Y%m%d"),
        "tran_time": get_date(fmt="%H%M%S"),
        "reserved": "111",
        "bank_nnemonic": "QISTPAY1"
    }
    resp = Http.http_post(url, req_data)
    return resp


def onelink_paycode_inquiry(consumer_number):
    url = gc.PAYMENT_URL + "/onelink/onelink_goldlion_paycode/inquiry"
    req_data = {
        "username": "olgoldlion",
        "password": "olgoldlion2023@123",
        "Consumer_number": consumer_number,
        "Bank_Mnemonic": "QISTPAY1"
    }
    resp = Http.http_post(url, req_data)
    return resp


def onelink_paycode_payment(consumer_number, amount):
    url = gc.PAYMENT_URL + "/onelink/onelink_goldlion_paycode/payment"
    req_data = {
        "username": "olgoldlion",
        "password": "olgoldlion2023@123",
        "Consumer_number": consumer_number,
        "Tran_Auth_Id": "476022",
        "Transaction_Amount": amount,
        "Tran_Date": get_date(fmt="%Y%m%d"),
        "Tran_Time": get_date(fmt="%H%M%S"),
        "Reserved": "111",
        "Bank_Nnemonic": "QISTPAY1"
    }
    resp = Http.http_post(url, req_data)
    return resp


def its_ebank_payment(consumer_number, amount):
    url = gc.PAYMENT_URL + "/swich/callback/its_goldlion_ebank"
    req_data = {
        "Status": "success",
        "Checksum": "",
        "Amount": amount,
        "PaymentType": "EasyPaisa",
        "CustomerTransactionId": consumer_number,
        "OrderId": "SW01496",
        "ChannelId": "8"
    }
    resp = Http.http_post(url, req_data)
    return resp


def paycools_paycode_inquiry(channel_key, amount):
    url = gc.PAYMENT_URL + "/paycools/callback/paycools_copperstone_wp"
    req_data = {
        "amount": amount,
        "createTime": get_date(),
        "eventName": "payment.verification",
        "mchOrderId": channel_key,
        "mobile": "",
        "referenceNumber": "PC0005O10000003",
        "sign": "62a002c4bbc2aeaf83448a03d87c834fa5937b82"
    }
    resp = Http.http_post(url, req_data)
    return resp


def paycools_paycode_confirm(channel_key, amount):
    url = gc.PAYMENT_URL + "/paycools/callback/paycools_copperstone_wp"
    req_data = {
        "amount": amount,
        "channelCode": "7ELEVEN_STATIC_VA",
        "codeMchOrderId": "PCP000000100000802",
        "createTime": "2023-02-14 17:12:33",
        "eventName": "payment.success",
        "mchOrderId": channel_key,
        "paymentCode": "PC0005O10000165",
        "returnTime": get_date(),
        "sign": "a8b934877cb12d3747baf406cda4d586d4b7fae1",
        "transactionId": "C1184676365953162412",
        "transactionStatus": "COMPLETE"
    }
    resp = Http.http_post(url, req_data)
    return resp


def paycools_qrcode_callback(channel_key, amount):
    url = gc.PAYMENT_URL + "/paycools/callback/paycools_copperstone_qrcode"
    req_data = {
        "amount": amount,
        "channelCode": "QRPH_HYBRID_QR",
        "createTime": "2023-02-14 17:29:29",
        "eventName": "qrcode.payment.success",
        "mchOrderId": channel_key,
        "remark": "PayCools Qrcode Payment",
        "returnTime": get_date(),
        "sign": "2430e2be9f3fd55a41bf47aa32d83201debbb3fa",
        "transactionId": "C1184676366969324811",
        "transactionStatus": "COMPLETE"
    }
    resp = Http.http_post(url, req_data)
    return resp


def paycools_ebank_callback(channel_key, amount):
    url = gc.PAYMENT_URL + "/paycools/callback/paycools_copperstone_ebank"
    req_data = {
        "amount": amount,
        "channelCode": "GCASH_URL",
        "createTime": "2023-02-17 15:02:18",
        "eventName": "h5.payment.success",
        "mchOrderId": channel_key,
        "remark": "PH_e_1676944197",
        "returnTime": get_date(),
        "sign": "3807b8bacf3b00a68a8f7a28f014e6e2b92be758",
        "transactionId": "C1184676617337849410",
        "transactionStatus": "COMPLETE"
    }
    resp = Http.http_post(url, req_data)
    return resp


def paycools_collect_callback(channel_key, account_no, amount):
    url = gc.PAYMENT_URL + "/paycools/callback/paycools_copperstone_collect"
    req_data = {
        "amount": amount,
        "channelCode": "INSTA_TRANSFER_ACC",
        "createTime": "2023-02-17 14:32:33",
        "eventName": "transfer.payment.success",
        "mchOrderId": channel_key,
        "paymentAccount": account_no,
        "remark": "Allbank Virtual Payment",
        "returnTime": get_date(),
        "sign": "7df9bfb39d9b3f155b4006ecb48d9ca03712c227",
        "transactionId": "C1184676615553454214",
        "transactionStatus": "COMPLETE"
    }
    resp = Http.http_post(url, req_data)
    return resp


if __name__ == '__main__':
    # 成本推送
    global_run_job("pushCostJob", {})
    # 成本试算
    global_run_job("providerCostJob", {"start2":"2023-05-04","end2":"2023-05-04","cycle_date":"2023-04-27 01:00:00","time_type":"createdAt","channel_name_list":["paycools_copperstone_withdraw"],"force_update":True,"page_size":2})
    # 熔断恢复
    global_run_job("fusingRestoreJob", {})
    # 成功率熔断
    global_run_job("fusingSuccessRateJob", {})
