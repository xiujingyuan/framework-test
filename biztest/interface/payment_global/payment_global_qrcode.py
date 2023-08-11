from biztest.config.payment.url_config import global_payment_base_url
from biztest.util.http.http_util import Http
from biztest.util.tools.tools import get_random_str


def cimb_payment_inquiry(channel_key, amount):
    url = global_payment_base_url + "/api/amberstar1/payment/cimb/verifydata/v1"
    request_body = {
        "header": {
            "requester_system": "SIBS",
            "request_reference_no": "SIBS40102915-1499-4120-a483-74a09777dc9e",
            "transaction_datetime": "2021-07-01T15:08:58.030+07:00"
        },
        "data": {
            "biller_id": "011556301315300",
            "reference1": channel_key,
            "reference2": "0912345600",
            "reference3": "",
            "transaction_id": "CIMB" + channel_key[5:],
            "transaction_datetime": "2021-07-01T15:09:00.000+07:00",
            "amount_paid": amount,
            "sender_account_name": "ร้ำลน จาฬปล้า"
        }
    }
    return request_body, Http.http_post(url, request_body)


def cimb_payment_confirm(channel_key, amount, result):
    url = global_payment_base_url + "/api/amberstar1/payment/cimb/notification/v1"
    request_body = {
        "header": {
            "requester_system": "SIBS",
            "request_reference_no": "SIBSba37bed3-4f04-4a5a-a27e-a21529bb5e40",
            "transaction_datetime": "2021-07-01T17:25:50.842+07:00"
        },
        "data": {
            "biller_id": "011556301315300",
            "reference1": channel_key,
            "reference2": "0912345600",
            "reference3": "",
            "biller_display_name": "",
            "result": result,
            "transaction_id": "CIMB" + channel_key[5:],
            "transaction_datetime": "2021-09-24T17:25:53.000+07:00",
            "amount_paid": amount,
            "sender_account_name": "ร้ำลน จาฬปล้า"
        }
    }
    return request_body, Http.http_post(url, request_body)


# scb 确认和通知的body是一模一样的
def scb_payment_inquiry_confirm(type, channel_key, amount):
    if type == "payment_inquiry":
        request = "verify"
        url = global_payment_base_url + "/api/amberstar1/payment/scb/verifydata/v1"
    else:
        request = "confirm"
        url = global_payment_base_url + "/api/amberstar1/payment/scb/notification/v1"
    request_body = {
        "request": request,
        "user": "scb",
        "password": "scb2021@123",
        "tranID": "scb" + channel_key,
        "tranDate": "2021-09-24T11:22:33",
        "channel": "ENET",
        "account": "4681016622",
        "amount": amount,
        "reference1": channel_key,
        "reference2": "0912345600",
        "reference3": "",
        "branchCode": "5037",
        "terminalID": "2550"
    }
    return request_body, Http.http_post(url, request_body)


#
def pandapay_inquiry_confirm(type, inner_key, amount=0):
    url = global_payment_base_url + "/pandapay/callback/pandapay_alibey_barcode"
    if type == "lookup":
        type = "inbound_payment.lookup"
    elif type == "payment_attempt":
        type = "inbound_payment.payment_attempt"
    else:
        type = "charge.paid"
    request_body = {
        "data": {
            "previous_attributes": {},
            "object": {
                "device_fingerprint": "zmcK8osGtfwP6oXYKUGTPj1yaS79hV7E",
                "amount": amount,
                "livemode": "false",
                "fee": 3132,
                "created_at": 1641388397,
                "refunds": [],
                "paid_at": 1641388587,
                "subscription_id": "",
                "currency": "MXN",
                "details": {
                    "phone": "9004227588",
                    "coupons": [],
                    "name": "Parthasaradhi",
                    "line_items": [],
                    "email": "test88@email.com",
                    "object": "details"
                },
                "id": "61d5996d0211a6172f5b591a",
                "customer_id": "cus_2r5gKtgQvExLc2str",
                "payment_method": {
                    "reference": inner_key,
                    "barcode_url": "https://s3.amazonaws.com/cash_payment_barcodes/sandbox_reference.png",
                    "expires_at": 1644019200,
                    "store_name": "OXXO",
                    "store": "10SLP50CKS",
                    "type": "oxxo",
                    "barcode": "99000003315514",
                    "auth_code": 356039729,
                    "object": "cash_payment"
                },
                "object": "charge",
                "status": "paid"
            }
        },
        "livemode": "false",
        "webhook_logs": [
            {
                "last_http_response_status": -1,
                "failed_attempts": 0,
                "id": "webhl_2r5gVqTosQEknM9XK",
                "url": "https://biz-gateway-proxy.starklotus.com/mex_payment1/pandapay/callback/pandapay_alibey_barcode",
                "object": "webhook_log",
                "last_attempted_at": 0
            }
        ],
        "webhook_status": "pending",
        "created_at": 1641388587,
        "id": "61d59a2b86a71f6f8a24d18d",
        "type": type,
        "object": "event"
    }
    return request_body, Http.http_post(url, request_body)


# mongopay的放款工具，0表示失败，非0表示成功
def mongopay_withdraw(channel_key, status):
    url = "https://openapi-san.mongopay.top/gateway/simulation"
    request_body = {
        "merchantCode": "S820210426024102000001",
        "orderNum": channel_key,
        "type": "CASH",
        "status": status
    }
    return request_body, Http.http_post(url, request_body)
