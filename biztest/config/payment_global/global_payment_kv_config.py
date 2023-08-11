import json

import common.global_const as gc


def update_kv_config(key, value):
    sql = "update keyvalue set keyvalue_value='%s' where keyvalue_key='%s'" % (
        json.dumps(value).encode('utf-8').decode('unicode_escape'), key)
    return gc.PAYMENT_DB.update(sql)


def add_user_center_card():
    sql1 = "INSERT INTO `card` (`card_num`, `card_account`, `card_account_mask`, `card_id_num`, `card_id_num_mask`, `card_username`, `card_username_mask`, `card_mobile`, `card_mobile_mask`, `card_bank_code`, `card_type`, `card_expiry_year`, `card_expiry_month`, `card_cvv`, `card_status`, `card_created_at`, `card_updated_at`, `card_auth_mode`, `card_email`, `card_email_mask`, `card_address`, `card_address_mask`, `card_user_uuid`)" \
           "VALUES('enc_03_3446721293687726080_025', 'enc_04_3446721036677554176_778', '', 'enc_02_2904999908740702208_297', '', 'enc_04_3132782998719045632_279', '', 'enc_01_2752562028249358336_117', '', 'T00003', '', '', '', '', 1, '2021-06-11 09:24:58', '2021-06-11 16:27:59', 'account', 'enc_05_2752999188760895488_191', '', 'enc_06_2752832664892874752_745', '', NULL)"
    sql2 = "INSERT INTO `binding` (`binding_card_num`, `binding_channel_name`, `binding_type`, `binding_status`, `binding_created_at`, `binding_updated_at`, `binding_info`, `binding_protocol_info`, `binding_register_name`, `binding_unknown_error`)" \
           "VALUES ('enc_03_3446721293687726080_025', 'gbpay_cymo1_verify', 4, 1, '2021-06-11 09:24:59', '2021-06-11 09:24:58', '', '', '', 0)"
    sql3 = "INSERT INTO `account` (`account_card_uuid`, `account_card_num`, `account_created_at`, `account_updated_at`, `account_auth_mode`)" \
           "VALUES ('6621061100000005511', 'enc_03_3446721293687726080_025', '2021-06-11 09:24:58', '2021-06-11 09:24:58', 'account')"
    fail_channel_error1 = gc.PAYMENT_DB.insert(sql1)
    fail_channel_error2 = gc.PAYMENT_DB.insert(sql2)
    fail_channel_error3 = gc.PAYMENT_DB.insert(sql3)
    return fail_channel_error1, fail_channel_error2, fail_channel_error3


def update_gbpay_verify(sign_company="cymo1", project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/gbpay/v2/transfers" % project_id
    else:
        url = "https://api.globalprimepay.com/v2/transfers"
    channel_name = "gbpay_%s_verify" % sign_company
    body = {
        "channel_name": channel_name,
        "type": "gbpay_verify",
        "app_id": "gbp0664",
        "private_key": "WIHZUxSiVJ8aZK2yHdxVMfpITU2VzxY3",
        "public_key": "BaelqsKoA1kluOfFSKtklPSZLRHYAbxM",
        "verify_url": url
    }
    update_kv_config(channel_name, body)


def update_gbpay_qrcode(sign_company="cymo1", project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "https://api.globalprimepay.com"
    channel_name = "gbpay_%s_qrcode" % sign_company
    body = {
        "channel_name": channel_name,
        "type": "gbpay_qrcode",
        "app_id": "gbp0664",
        "private_key": "WIHZUxSiVJ8aZK2yHdxVMfpITU2VzxY3",
        "public_key": "BaelqsKoA1kluOfFSKtklPSZLRHYAbxM",
        "customer_key": "fBUEy7WDsHzr7oh9Kh2d5trEG00qV+7e4ABoGV/xVWX8V+9s5vL+KUcrCkhAWlNPFQ+zXFYFaxyXip9XTKSD6eba7qQE7"
                        "+BUQAFAWXms8RYG6vRfI560S3yECng2zbRiW4g0cgCDJPKYoqeg45wO2ZmU32lSshAeq06qBD66xuTVWh++",
        "charge_query_url": "%s/v1/check_status_txn" % url,
        "charge_url": "%s/gbp/gateway/qrcode/text" % url,
        "callback_url": "https://biz-gateway-proxy.starklotus.com/tha_payment%s/gbpay/callback/backgroupurl/" % gc.ENV,
        "expire_time": 15,
        "expiry_period": "0"
    }
    update_kv_config(channel_name, body)


def update_gbpay_withhold(sign_company="cymo1", project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "https://api.globalprimepay.com"
    channel_name = "gbpay_%s_withhold" % sign_company
    body = {
        "channel_name": channel_name,
        "type": "gbpay_withhold",
        "private_key": "DGAIohUwt3s9jlVqO0a8VkBGObv1cPgh",
        "public_key": "TOyleflEUmC9ETulqjckJJmxX5IRazCA",
        "full_payment_token_url": "%s/v1/tokens" % url,
        "charge_url": "%s/v1/tokens/charge" % url,
        "charge_query_url": "%s/v1/check_status_txn" % url,
        "callback_url": "https://biz-gateway-proxy.starklotus.com/tha_payment%s/gbpay/callback/checkout/" % gc.ENV,
        "expire_time": 30
    }
    update_kv_config(channel_name, body)


def update_gbpay_checkout(sign_company="cymo1", project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "https://api.globalprimepay.com"
    channel_name = "gbpay_%s_checkout" % sign_company
    body = {
        "channel_name": channel_name,
        "type": "gbpay_checkout",
        "private_key": "DGAIohUwt3s9jlVqO0a8VkBGObv1cPgh",
        "public_key": "TOyleflEUmC9ETulqjckJJmxX5IRazCA",
        "full_payment_token_url": "%s/v1/tokens" % url,
        "charge_url": "%s/v1/tokens/charge" % url,
        "charge_query_url": "%s/v1/check_status_txn" % url,
        "secured_3d_url": "%s/v1/tokens/3d_secured" % url,
        "redirect_url": "http://www.baidu.com",
        "callback_url": "https://biz-gateway-proxy.starklotus.com/tha_payment%s/gbpay/callback/checkout/" % gc.ENV,
        "expire_time": 30
    }
    update_kv_config(channel_name, body)


def update_gbpay_withdraw(sign_company="cymo1", project_id=None):
    if project_id:
        withdraw_balance_url = \
            "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/withdraw/balance/v2/transfers" % project_id
        withdraw_query_url = \
            "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/withdraw/query/v2/transfers" % project_id
        withdraw_url = \
            "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/withdraw/v2/transfers" % project_id
    else:
        withdraw_balance_url = "https://api.globalprimepay.com/v2/transfers"
        withdraw_query_url = "https://api.globalprimepay.com/v2/transfers"
        withdraw_url = "https://api.globalprimepay.com/v2/transfers"
    channel_name = "gbpay_%s_withdraw" % sign_company
    body = {
        "channel_name": channel_name,
        "type": "gbpay_withdraw",
        "app_id": "gbp0664",
        "private_key": "WIHZUxSiVJ8aZK2yHdxVMfpITU2VzxY3",
        "public_key": "BaelqsKoA1kluOfFSKtklPSZLRHYAbxM",
        "withdraw_balance_query_url": withdraw_balance_url,
        "withdraw_query_url": withdraw_query_url,
        "withdraw_url": withdraw_url,
        "callback_url": "https://biz-gateway-proxy.starklotus.com/tha_payment1"
                        "/gbpay/callback/withdraw/",
        "description": "pay"
    }
    update_kv_config(channel_name, body)


def update_cashfree_withdraw(sign_company, project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "https://payout-gamma.cashfree.com"
    channel_name = "cashfree_%s_withdraw" % sign_company
    body = {
        "channel_name": channel_name,
        "type": "cashfree_withdraw",
        "client_id": "CF13250DZ8SGF4NLLYU2UU",
        "client_secret": "3babfc5e6141bd49c10dec05b8424881e6658198",
        "app_id": "12545b2ccda5062bb8fd9c88a54521",
        "secret_key": "dfa3aa07fdd6979206383689363f552d617a8c42",
        "authorize_url": "%s/payout/v1/authorize" % url,
        "verify_bank_account_url": "%s/payout/v1/validation/bankDetails" % url,
        "verify_upi_url": "%s/payout/v1/validation/upiDetails" % url,
        "register_url": "%s/payout/v1/addBeneficiary" % url,
        "register_query_url": "%s/payout/v1/getBeneId" % url,
        "register_query_by_id_url": "%s/payout/v1/getBeneficiary" % url,
        "withdraw_url": "%s/payout/v1/requestTransfer" % url,
        "withdraw_query_url": "%s/payout/v1/getTransferStatus" % url,
        "withdraw_balance_query_url": "%s/payout/v1/getBalance" % url
    }
    update_kv_config(channel_name, body)


def update_cashfree_verify(sign_company, project_id=None, name_match_switch=True, upi_unbind_account_switch=True):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "https://payout-api.cashfree.com"
    channel_name = "cashfree_%s_verify" % sign_company
    body = {
        "channel_name": channel_name,
        "type": "cashfree_verify",
        "client_id": "CF72858N7DDGWASGXEUQUU",
        "client_secret": "4dcd4f1fd21d5ca7f5f57102a614e1b58e2ba4e1",
        "authorize_url": "%s/payout/v1/authorize" % url,
        "verify_bank_account_url": "%s/payout/v1/validation/bankDetails" % url,
        "verify_upi_url": "%s/payout/v1/validation/upiDetails" % url,
        "name_match_switch": name_match_switch,
        "upi_unbind_account_switch": upi_unbind_account_switch,
        "name_similarity_rate": 0.8,
        "name_not_include": [
            "^006CREDIT \\d+$",
            "MB",
            "VALUED CUSTOMER",
            "IMPS CUSTOMER",
            "Cosmos",
            "APNB",
            "TJSB",
            "PJSB",
            "NO NAME",
            "BCB",
            "MBRR",
            "GPPB",
            "DNSB",
            "NIYO BLUE FUNDING AC",
            "KJSB",
            "Unregistered",
            "UNREGISTERED",
            "^[a-zA-Z]{1,2}$"
        ]
    }
    update_kv_config(channel_name, body)


def update_cashfree_sdk(sign_company, project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "https://test.cashfree.com"
    channel_name = "cashfree_%s_sdk" % sign_company
    body = {
        "channel_name": channel_name,
        "type": "cashfree_sdk",
        "client_id": "CF12545378PB6I0Q76QMI2",
        "client_secret": "5e17e03ea16b069bf5dec356208288af91006dcf",
        "app_id": "13261e0a7b38f955c0b25bfb016231",
        "secret_key": "5c335cffff372d900f8d3564fb2d4599c754d8c4",
        "expire_time": 15,
        "expiry_period": 2,
        "charge_url": "%s/api/v2/cftoken/order" % url,
        "charge_query_url": "%s/api/v1/order/info/status" % url,
        "callback_url": "https://biz-gateway-proxy.starklotus.com/tha_payment{0}/cashfree/callback/" % gc.ENV,
        "description": "yomoyo"
    }
    update_kv_config(channel_name, body)


def update_cashfree_ebank(sign_company, project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "https://test.cashfree.com"
    channel_name = "cashfree_%s_ebank" % sign_company
    body = {
        "channel_name": channel_name,
        "type": "cashfree_ebank",
        "client_id": "CF12545378PB6I0Q76QMI2",
        "client_secret": "5e17e03ea16b069bf5dec356208288af91006dcf",
        "app_id": "12545b2ccda5062bb8fd9c88a54521",
        "secret_key": "dfa3aa07fdd6979206383689363f552d617a8c42",
        "expire_time": 15,
        "expiry_period": "5",
        "charge_url": "%s/api/v1/order/create" % url,
        "charge_query_url": "%s/api/v1/order/info/status" % url,
        "callback_url": "https://biz-gateway-proxy.starklotus.com/tha_payment1/cashfree/callback/"
    }
    update_kv_config(channel_name, body)


def update_cashfree_reconci(sign_company, project_id=None):
    if project_id:
        url1 = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/api/v1/settlements" % project_id
        url2 = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/api/v1/settlement" % project_id
    else:
        url1 = "https://api.cashfree.com/api/v1/settlements"
        url2 = "https://api.cashfree.com/api/v1/settlement"
    channel_name = "cashfree_%s_ebank_reconci" % sign_company
    body = [
        {
            "id": 1,
            "next_id": 2,
            "recoci_type": "Settlement",
            "recon_advance_days": 0,
            "money_unit": "Y",
            "http_batch_config": {
                "url": url1,
                "method": "post",
                "request_data_type": "form",
                "response_data_type": "json",
                "params": {
                    "appId": "726948fc9c186a69a093f357f49627",
                    "secretKey": "f98c48a8ee9239c23a98dc080b27aeed520e12e9",
                    "count": 55,
                    "startDate": None,
                    "endDate": None,
                    "lastId": None
                },
                "dynamic_params": [
                    "lastId",
                    "startDate:startDate",
                    "endDate:endDate"
                ],
                "data_field": "settlements"
            },
            "field_map": {
                "settlementId:Long": "id:Long",
                "amount:Long": "totalTxAmount:BigDecimal",
                "adjustmentAmount:Long": "adjustment:BigDecimal",
                "settlementAmount:Long": "settlementAmount:BigDecimal",
                "settledAmount:Long": "amountSettled:BigDecimal",
                "settledAt:Date": "settledOn:Date"
            }
        },
        {
            "id": 2,
            "recoci_type": "Transaction",
            "paysvr_channel_name": True,
            "recon_advance_days": 0,
            "money_unit": "Y",
            "http_batch_config": {
                "url": url2,
                "method": "post",
                "request_data_type": "form",
                "response_data_type": "json",
                "params": {
                    "appId": "726948fc9c186a69a093f357f49627",
                    "secretKey": "f98c48a8ee9239c23a98dc080b27aeed520e12e9",
                    "count": 50,
                    "lastId": None,
                    "settlementId": None
                },
                "dynamic_params": [
                    "lastId",
                    "settlementId:id"
                ],
                "data_field": "transactions"
            },
            "field_map": {
                "channelKey:String": "orderId:String",
                "channelOrderNo:String": "orderId:String",
                "amount:Long": "txAmount:BigDecimal",
                "paymentMode:String": "paymentMode:String",
                "bankName:String": "bankName:String",
                "serviceCharge:Long": "serviceCharge:BigDecimal",
                "serviceTax:Long": "serviceTax:BigDecimal",
                "settlementAmount:Long": "settlementAmount:BigDecimal",
                "orderFinishedAt:Date": "txTime:Date",
                "date:Date": "txTime:Date"
            }
        }
    ]
    update_kv_config(channel_name, body)


def update_razorpay_withdraw(sign_company, project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "https://api.razorpay.com"
    channel_name = "razorpay_%s_withdraw" % sign_company

    body = {
        "channel_name": channel_name,
        "type": "razorpay_withdraw",
        "client_id": "rzp_test_X6qkUirAFaViOf",
        "client_secret": "iwVxYBt9dI0Ipp6bMj612c2E",
        "secret_key": "123456",
        "account_number": "2323230035394297",
        "verify_amount": "100",
        "create_contact_url": "%s/v1/contacts" % url,
        "create_fund_account_url": "%s/v1/fund_accounts" % url,
        "withdraw_url": "%s/v1/payouts" % url,
        "withdraw_query_url": "%s/v1/payouts" % url,
        "transaction_query_url": "%s/v1/transactions" % url
    }
    update_kv_config(channel_name, body)


def update_razorpay_ebank(sign_company="yomoyo", project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "https://api.razorpay.com"
    channel_name = "razorpay_%s_ebank" % sign_company
    body = {
        "channel_name": channel_name,
        "type": "razorpay_paymentlink",
        "client_id": "rzp_test_X6qkUirAFaViOf",
        "client_secret": "iwVxYBt9dI0Ipp6bMj612c2E",
        "secret_key": "123456",
        "expire_time": 33,
        "expiry_period": 1,
        "charge_url": "%s/v1/payment_links" % url,
        "charge_query_middle_url": "%s/v1/orders" % url,
        "charge_query_url": "%s/v1/orders" % url,
        "callback_url": "https://api.razorpay.com/razorpay/callback/",
        "payment_capture_url": "https://api.razorpay.com/v1/payments/%s/capture",
        "description": "test"
    }
    update_kv_config(channel_name, body)


def update_scb_sdk(sign_company="amberstar1", project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "https://api-sandbox.partners.scb/partners/sandbox"
    channel_name = "scb_%s_sdk" % sign_company
    charge_query_url = ("%s/v2/transactions/" % url) + "%s"
    body = {
        "channel_name": channel_name,
        "type": "scb_sdk",
        "transactionType": "PURCHASE",
        "transactionSubType": [
            "BP"
        ],
        "accountTo": "137613415414240",
        "merchantId": "512862849553666",
        "terminalId": "745531457571408",
        "description": "KN TEST ENV",
        "callback_url": None,
        "accept_language": "EN",
        "expire_time": 5,
        "expiry_period": 1,
        "app_key": "l7c73ac7f144fb4d22ac15371d9ba34666",
        "app_secret": "b277c9a19e794e8c9ab102c1bb488628",
        "token_url": "%s/v1/oauth/token" % url,
        "charge_url": "%s/v3/deeplink/transactions" % url,
        "charge_query_url": charge_query_url
    }
    update_kv_config(channel_name, body)


# 修改scb代付mock
def update_scb_withdraw(sign_company="amberstar1", project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "https://api-partners-uat.scb.co.th"
    channel_name = "scb_%s_withdraw" % sign_company
    body = {
        "channel_name": channel_name,
        "type": "scb_withdraw",
        "app_key": "l741773e508b6e4cccb339aa809cebc707",
        "app_secret": "3c98c871608840d39510aebb4289a1f3",
        "description": "desc_product",
        "business_purpose": "desc_product",
        "transactionType": "DR",
        "annotation": "annotation",
        "corporate_id": "asta993",
        "channel_code": "asta993",
        "corporate_name": "AMBER STAR CO.,LTD.",
        "payer_account_no": "4681016622",
        "payer_bank_code": "014",
        "payer_tax_id": "0115563013153",
        "product_name": "product_name",
        "token_url": "%s/partners/v1/oauth/token" % url,
        "withdraw_url": "%s/partners/v2/payment/transfer/credit/initiate" % url,
        "withdraw_confirm_url": "%s/partners/v2/payment/transfer/confirm" % url,
        "withdraw_query_url": "%s/partners/v1/payment/transfer/inquiry" % url,
        "withdraw_balance_url": "",
        "secret_key": "123456",
        "mock_balance": 0,
        "double_confirm": False,
        "next_query_time": 10
    }
    update_kv_config(channel_name, body)


# 修改用户中心mock
def update_user_center_config(project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "http://rpc-gateway-http.aidc-thailand.svc.cluster.local"
    keyvalue_key = "user_center_config"
    body = {
        "user_info_url": "%s/individual/getUserInfoByType" % url
    }
    update_kv_config(keyvalue_key, body)


def update_rapyd_qrcode(sign_company=None, project_id=None):
    if project_id:
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
    else:
        url = "https://sandboxapi.rapyd.net"
    channel_name = "rapyd_%s_qrcode" % sign_company
    body = {
        "channel_name": channel_name,
        "type": "rapyd_qrcode",
        "access_key": "0EF31D8F9C8BDC724331",
        "secret_key": "5bd6c148a9c8aea57d26e49fa504e43078f1492ed2a13b325efcb2701b61755ee14abefdca985f1f",
        "country": "TH",
        "currency": "THB",
        "language": "en",
        "expire_time": 15,
        "cardholder_preferred_currency": True,
        "server_url": "%s" % url,
        "charge_url": "%s/v1/payments" % url,
        "charge_query_url": "%s/v1/payments/" % url + "%s",
        "callback_url": "https://biz-gateway-proxy.starklotus.com/tha_payment{0}/rapyd/callback/rapyd_amberstar1_qrcode" % gc.ENV,
        "payment_method": "th_thaipromptpayqr_bank",
        "description": "thaipromptpayqr"
    }
    update_kv_config(channel_name, body)


# 修改通道额度
def update_channel_score_config(keyvalue_key, channel_name=None, kv_value=None):
    if kv_value:
        keyvalue_value = json.loads(kv_value)
    else:
        keyvalue_value = {
            "score_params": {
                "base_score": {
                    "enable": "true",
                    "max_score": 100,
                    "max_suc_amt": {
                        channel_name: 100000000,
                        "default": -1
                    }
                },
                "success_score": {
                    "enable": "false",
                    "max_score": 100
                },
                "fee_score": {
                    "enable": "false",
                    "max_score": 100
                },
                "provider_score": {
                    "enable": "true"
                },
                "bank_score": {
                    "enable": "false"
                }
            },
            "calc_formulas": "(A>MSA?0:S1)+S4"
        }
    update_kv_config(keyvalue_key, keyvalue_value)


def update_fusing_config(error_message_strategy={}):
    body = {
        "apply_to_async_task": [
            "withdraw"
        ],
        "error_message_strategy": error_message_strategy,
        "success_rate_strategy": {
            "default": {
                "avg_finished_seconds": 0,
                "query_time_minute": 60,
                "min_total_size": 2,
                "min_success_rate": 0.9,
                "restore_size": 3,
                "max_fusing_minute": 120
            }
        }
    }
    gc.NACOS.update_configs("paysvr-test1", "fusing_config", body)
