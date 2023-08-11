# -*- coding: utf-8 -*-
import time
from datetime import datetime

from biztest.config.payment.url_config import global_cashfree_available_amount_lubi, global_withhold_failed_msg, \
    global_withhold_no_exist_msg, global_withhold_successed_msg, global_withdraw_failed_reason, \
    global_withdraw_no_exist_msg, global_withdraw_failed_message, global_withdraw_query_fail_001, global_paymentMode, \
    global_razorpay_ebank_channel_key, global_razorpay_ebank_fail_message, \
    global_razorpay_ebank_payment_mode, global_razorpay_verifyid, global_cashfree_subscribe_id, \
    global_cashfree_subscribe_url, global_cashfree_subscribe_paymentId, global_autoSubscribe_withhold_failcode, \
    global_autoSubscribe_withhold_successcode, global_autoSubscribe_withhold_message, global_razorpay_collect_inner_no, \
    global_cashfree_total_amount_lubi, global_cashfree_withdraw_fail_001, global_cashfree_withdraw_fail_002, \
    global_cashfree_withdraw_bene_id, global_cashfree_ebank_channel_key, cashfree_ebank_settlement_id, \
    global_ebank_payurl, global_cashfree_sdk_token
from biztest.interface.payment.payment_interface import get_timestamp
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import get_date


class CashfreeMock(Easymock):
    def update_cashfree_account_bind_success(self, name="test"):
        api = "/payout/v1/validation/bankDetails"
        # cashfree绑卡更新为成功：status=SUCCESS且data.accountExists=YES
        mode = {"status": "SUCCESS",
                "subCode": "200",  # 不要改，有断言用到
                "message": "Bank Account details verified successfully.",  # 不要改，有断言用到
                "data": {"nameAtBank": name,
                         "accountExists": "YES",
                         "amountDeposited": "0",
                         "refId": "@id"}}
        self.update(api, mode)

    def update_cashfree_account_bind_not_exist(self):
        # cashfree返回鉴权成功但是打款又失败了，这种属于鉴权失败：status=SUCCESS且accountExists=NO
        api = "/payout/v1/validation/bankDetails"
        mode = {"status": "SUCCESS",
                "subCode": "200",
                "message": "Invalid account number or ifsc provided",
                "data": {"accountExists": "NO"}}
        self.update(api, mode)

    def update_cashfree_account_bind_error(self):
        # cashfree绑卡更新为失败
        api = "/payout/v1/validation/bankDetails"
        mode = {"status": "ERROR",
                "subCode": "422",
                "message": "Please provide a valid IFSC code"}
        self.update(api, mode)

    def update_cashfree_upi_bind_success(self, name="test"):
        # cashfree_upi绑卡更新为成功
        api = "/payout/v1/validation/upiDetails"
        mode = {"status": "SUCCESS",
                "subCode": "200",
                "message": "VPA verification successful",
                "data": {"nameAtBank": name,
                         "accountExists": "YES"}}
        self.update(api, mode)

    def update_cashfree_upi_bind_not_exist(self):
        # cashfree_upi绑卡失败，账户不存在
        api = "/payout/v1/validation/upiDetails"
        mode = {"status": "SUCCESS",
                "subCode": "200",
                "message": "VPA verification successful",
                "data": {"accountExists": "NO"}}
        self.update(api, mode)

    def update_cashfree_upi_bind_error(self):
        # cashfree upi绑卡失败，状态error
        api = "/payout/v1/validation/upiDetails"
        mode = {"status": "ERROR",
                "subCode": "520",
                "message": "Validation attempt failed"}
        self.update(api, mode)

    def update_cashfree_sdk_gettoken_success(self):
        api = "/api/v2/cftoken/order"
        mode = {
            "status": "OK",  # OK是成功，其他为失败
            "message": "Token generated",
            "cftoken": "sdk_token"
        }
        self.update(api, mode)

    def update_cashfree_sdk_gettoken_fail(self):
        api = "/api/v2/cftoken/order"
        mode = {
            "status": "FAILED",  # OK是成功，其他为失败
            "message": "Token generate failed",  # message有断言，不要改
            "cftoken": None
        }
        self.update(api, mode)

    def update_cashfree_ebank_process(self):
        # cashfree-ebank发起代扣成功，会返回网关支付链接
        api = "/api/v1/order/create"
        mode = {
            "status": "OK",
            "paymentLink": "https:\/\/payments-test.cashfree.com\/order\/#7bwlccyo9i0w80810uw0z"
        }
        self.update(api, mode)

    def update_cashfree_ebank_error(self):
        api = "/api/v1/order/create"
        # 发起代扣异常
        mode = {
            "status": "ERROR",
            "reason": "Order Id does not exist"
        }
        self.update(api, mode)

    def update_cashfree_withhold_query_success(self):
        # status=OK且 OrderStatus=PAID 且 txStatus=SUCCESS
        api = "/api/v1/order/info/status"
        mode = {
            "orderStatus": "PAID",
            "orderAmount": "6285.00",
            "status": "OK",
            "txStatus": "SUCCESS",
            "txTime": get_date(),
            "txMsg": "Transaction is Successful",
            "referenceId": "@id",
            "paymentMode": "UPI",
            "orderCurrency": "INR",
            "paymentDetails": {
                "payersVPA": "sunilsingh23893@okaxis",
                "utr": "033916679911"
            }
        }
        self.update(api, mode)

    def update_cashfree_withhold_query_no_pay_expired(self):
        api = "/api/v1/order/info/status"
        # OrderStatus=ACTIVE,没有txStatus节点时，超过有效期orderExpiryTime
        mode = {
            "orderStatus": "ACTIVE",
            "orderAmount": "0.01",
            "orderExpiryTime": get_date(day=-1),  # 订单过期时间必须比当前时间小，才会置为代扣失败
            "status": "OK"
        }
        self.update(api, mode)

    def update_cashfree_withhold_query_no_pay_no_expire(self):
        api = "/api/v1/order/info/status"
        # OrderStatus=ACTIVE,没有txStatus节点时，未超过有效期orderExpiryTime
        mode = {
            "orderStatus": "ACTIVE",
            "orderAmount": "0.01",
            "orderExpiryTime": get_date(day=1),  # 订单过期时间必须比当前时间小，才会置为代扣失败
            "status": "OK"
        }
        self.update(api, mode)

    def update_cashfree_withhold_query_not_exist(self):
        api = "/api/v1/order/info/status"
        # 查询返回交易不存在，置为代扣失败
        mode = {
            "status": "ERROR",
            "reason": "Order Id does not exist"
        }
        self.update(api, mode)

    def update_cashfree_withhold_query_fail_failed(self):
        api = "/api/v1/order/info/status"
        # orderStatus=ACTIVE 且 txStatus=FAILED，且 当前时间超过有效期orderExpiryTime+配置的5分钟
        mode = {
            "orderStatus": "ACTIVE",
            "orderAmount": "5035.00",
            "orderExpiryTime": get_date(day=-1),
            "status": "OK",
            "txStatus": "FAILED",
            "txTime": get_date(),
            "txMsg": "Transaction fail",
            "referenceId": "@id",
            "paymentMode": "UPI",
            "orderCurrency": "INR",
            "paymentDetails": {
                "payersVPA": "",
                "utr": ""
            }
        }
        self.update(api, mode)

    def update_cashfree_withhold_query_fail_user_dropped(self):
        api = "/api/v1/order/info/status"
        # orderStatus=ACTIVE 且 txStatus=USER_DROPPED，且 当前时间超过有效期orderExpiryTime+配置的5分钟
        mode = {
            "orderStatus": "ACTIVE",
            "orderAmount": "3808.50",
            "orderExpiryTime": get_date(day=-1),
            "status": "OK",
            "txStatus": "USER_DROPPED",
            "txTime": get_date(),
            "txMsg": "User dropped out of txn",
            "referenceId": "@id",
            "paymentMode": "UPI",
            "orderCurrency": "INR",
            "paymentDetails": {
                "payersVPA": "",
                "utr": ""
            }
        }
        self.update(api, mode)

    def update_cashfree_withhold_query_fail_pending(self):
        api = "/api/v1/order/info/status"
        # status=OK且OrderStatus=ACTIVE,txStatus=PENDING，且 当前时间超过有效期orderExpiryTime+配置的5分钟
        mode = {
            "orderStatus": "ACTIVE",
            "orderAmount": "5035.00",
            "orderExpiryTime": get_date(day=-1),
            "status": "OK",
            "txStatus": "PENDING",
            "txTime": get_date(),
            "txMsg": None,
            "referenceId": "@id",
            "paymentMode": "UPI",
            "orderCurrency": "INR",
            "paymentDetails": {
                "payersVPA": "",
                "utr": ""
            },
        }
        self.update(api, mode)

    def update_cashfree_withhold_query_process_no_exprie(self):
        api = "/api/v1/order/info/status"
        # status=OK且OrderStatus=ACTIVE,txStatus=PENDING且没有返回订单过期时间orderExpiryTime，置为代扣处理中
        mode = {
            "orderStatus": "ACTIVE",
            "orderAmount": "0.01",
            "status": "OK",
            "txStatus": "PENDING",
            "txTime": get_date(),
            "txMsg": None,
            "referenceId": "@id",
            "paymentMode": "UPI",
            "orderCurrency": "INR"
        }
        self.update(api, mode)

    def update_cashfree_withhold_query_process_failed(self):
        api = "/api/v1/order/info/status"
        # status=OK且OrderStatus=ACTIVE,txStatus=FAILED，且当前时间小于过期时间，置为代扣处理中
        mode = {
            "orderStatus": "ACTIVE",
            "orderAmount": "3805.50",
            "orderExpiryTime": get_date(day=1),
            "status": "OK",
            "txStatus": "FAILED",
            "txTime": get_date(),
            "txMsg": "Transaction fail",
            "referenceId": "@id",
            "paymentMode": "UPI",
            "orderCurrency": "INR",
            "paymentDetails": {
                "payersVPA": "",
                "utr": ""
            }
        }
        self.update(api, mode)

    def update_cashfree_withhold_query_process_user_dropped(self):
        api = "/api/v1/order/info/status"
        # status=OK且OrderStatus=ACTIVE,txStatus=USER_DROPPED，且当前时间小于过期时间，置为代扣处理中
        mode = {
            "orderStatus": "ACTIVE",
            "orderAmount": "3808.50",
            "orderExpiryTime": get_date(day=1),
            "status": "OK",
            "txStatus": "USER_DROPPED",
            "txTime": get_date(),
            "txMsg": "User dropped out of txn",
            "referenceId": "@id",
            "paymentMode": "UPI",
            "orderCurrency": "INR",
            "paymentDetails": {
                "payersVPA": "",
                "utr": ""
            }
        }
        self.update(api, mode)

    def update_cashfree_withhold_query_process_pending(self):
        api = "/api/v1/order/info/status"
        # status=OK且OrderStatus=ACTIVE,txStatus=PENDING且当前时间小于过期时间orderExpiryTime，置为代扣处理中
        mode = {
            "orderStatus": "ACTIVE",
            "orderAmount": "5035.00",
            "orderExpiryTime": get_date(day=1),
            "status": "OK",
            "txStatus": "PENDING",
            "txTime": get_date(),
            "txMsg": None,
            "referenceId": "@id",
            "paymentMode": "UPI",
            "orderCurrency": "INR",
            "paymentDetails": {
                "payersVPA": "",
                "utr": ""
            },
        }
        self.update(api, mode)

    def update_cashfree_withhold_query_process_other_error(self):
        api = "/api/v1/order/info/status"
        # OrderStatus=FLAGGED，txStatus=CANCELLED，组合码不配置在channel_error中
        mode = {
            "orderStatus": "FLAGGED",
            "orderAmount": "5035.00",
            "orderExpiryTime": "2025-03-08 01:14:14",
            "txStatus": "CANCELLED",
            "txTime": "2020-03-08 00:59:25",
            "txMsg": global_withhold_failed_msg,  # 这个msg会保存到withhold_receipt_channel_resp_message
            "referenceId": "100441924",
            "paymentMode": "UPI",
            "orderCurrency": "INR",
            "paymentDetails": {
                "payersVPA": "",
                "utr": ""
            },
            "status": "OK"
        }
        self.update(api, mode)

    def update_cashfree_withdraw_balance_success(self):
        api = "/payout/v1/getBalance"
        mode = {
            "status": "SUCCESS",
            "subCode": "200",
            "message": "Ledger balance for the account",
            "data": {
                "balance": global_cashfree_total_amount_lubi,
                "availableBalance": global_cashfree_available_amount_lubi  # 这个金额写死，便于查询返回参数的断言
            }
        }
        self.update(api, mode)

    def update_cashfree_withdraw_balance_fail(self):
        api = "/payout/v1/getBalance"
        mode = {
            "status": "ERROR",
            "subCode": "403",
            "message": "failed"
        }
        self.update(api, mode)

    def update_cashfree_query_Beneficiary_not_exit(self, card_num):
        # cashfree 查询受益人不存在
        api_id = "5fc8a34d8fda8700203d4120"
        api = "/payout/v1/getBeneficiary/" + str(card_num)
        mode = {"status": "ERROR",
                "subCode": "404",
                "message": "Beneficiary does not exist"}
        self.update_by_api_id(api_id, api, mode, "get")

    def update_cashfree_query_Beneficiary_exit(self, card_num):
        # cashfree 查询受益人存在
        api_id = "5fc8a34d8fda8700203d4120"
        api = "/payout/v1/getBeneficiary/" + str(card_num)
        mode = {
            "status": "SUCCESS",
            "subCode": "200",
            "message": "Details of beneficiary",
            "data": {
                "beneId": card_num,
                "name": "VIRAL DUDHAT",
                "email": "xnxbdb@gmail.com",
                "phone": "15250118972",
                "address1": "aaaa address",
                "address2": "",
                "city": "",
                "state": "",
                "pincode": "",
                "bankAccount": "",
                "ifsc": "",
                "status": "VERIFIED",
                "maskedCard": None,
                "vpa": "failure@upi",
                "addedOn": "2020-10-13 15:37:19"}}
        self.update_by_api_id(api_id, api, mode, "get")

    def update_cashfree_add_Beneficiary_success(self):
        # cashfree 添加受益人更新为成功
        api = "/payout/v1/addBeneficiary"
        mode = {
            "status": "SUCCESS",
            "subCode": "200",
            "message": "Beneficiary added successfully"
        }
        self.update(api, mode)

    def update_cashfree_add_Beneficiary_fail(self):
        # cashfree 添加受益人失败
        api = "/payout/v1/addBeneficiary"
        mode = {
            "status": "ERROR",
            "subCode": "400",
            "message": "failed"
        }
        self.update(api, mode)

    def update_cashfree_withdraw_success(self):
        # 放款请求成功
        api = "/payout/v1/requestTransfer"
        mode = {
            "status": "SUCCESS",
            "subCode": "200",
            "message": "Transfer completed successfully",
            "data": {
                "referenceId": "10023",
                "utr": "P16111765023806",
                "acknowledged": 1
            }
        }
        self.update(api, mode)

    def update_cashfree_withdraw_query_success(self):
        api = "/payout/v1/getTransferStatus"
        mode = {
            "status": "SUCCESS",
            "subCode": "200",
            "message": global_withdraw_query_fail_001,
            "data": {
                "transfer": {
                    "referenceId": 78932,
                    "bankAccount": "00011020001772",
                    "ifsc": "HDFC0000001",
                    "beneId": "enc_03_366369990_783_11112",
                    "amount": "1",
                    "status": "SUCCESS",
                    "utr": "1387420160907000256943",
                    "addedOn": "2020-02-15 18:42:56",
                    "processedOn": "2020-02-15 18:42:56",
                    "transferMode": "BANK",
                    "acknowledged": 1
                }
            }
        }
        self.update(api, mode)

    def update_cashfree_withdraw_query_reversed(self):
        # 外层status=SUCCESS且内部Status=REVERSED，为放款失败
        api = "/payout/v1/getTransferStatus"
        mode = {
            "status": "SUCCESS",
            "subCode": "200",
            "message": global_withdraw_query_fail_001,
            "data": {
                "transfer": {
                    "referenceId": 78932,
                    "bankAccount": "00011020001772",
                    "ifsc": "HDFC0000001",
                    "beneId": "enc_03_366369990_783_11112",
                    "amount": "1",
                    "status": "REVERSED",
                    "utr": "1387420160907000256943",
                    "addedOn": "2020-02-15 18:42:56",
                    "processedOn": "2020-02-15 18:42:56",
                    "transferMode": "BANK",
                    "acknowledged": 1
                }
            }
        }
        self.update(api, mode)

    def update_cashfree_withdraw_query_fail(self):
        # 外层status=SUCCESS且内部Status=FAILED，为放款失败
        api = "/payout/v1/getTransferStatus"
        mode = {
            "status": "SUCCESS",
            "subCode": "200",
            "message": "Details of transfer with transferId 1d7015aed440411e8dcebe8263680049",
            "data": {
                "transfer": {
                    "referenceId": 104870920,
                    "bankAccount": "64039780830",
                    "ifsc": "SBIN0040065",
                    "beneId": "enc_03_2772851618960901120_206",
                    "amount": "4000.00",
                    "status": global_cashfree_withdraw_fail_002,
                    "addedOn": "2020-03-10 12:32:21",
                    "processedOn": "2020-03-10 12:32:21",
                    "reason": global_withdraw_failed_reason,
                    "transferMode": "BANK"
                }
            }
        }
        self.update(api, mode)

    def update_cashfree_withdraw_query_fail_not_exists(self):
        # 放款查询返回交易不存在，代码写死置为放款失败
        api = "/payout/v1/getTransferStatus"
        mode = {
            "status": "ERROR",
            "subCode": "404",
            "message": global_withdraw_no_exist_msg
        }
        self.update(api, mode)

    def update_cashfree_withdraw_fail(self):
        # 放款请求失败
        api = "/payout/v1/requestTransfer"
        mode = {
            "status": "ERROR",
            "subCode": "400",  # subCode=400需要先在channel_error中配置为失败
            "message": global_withdraw_failed_message
        }
        self.update(api, mode)

    def update_cashfree_withdraw_query_out_status_error(self):
        api = "/payout/v1/getTransferStatus"
        # cashfree  status<>SUCCESS需要查询（若channel_code配置了状态则按照配置来）
        mode = {
            "status": "ERROR",
            "subCode": "406",  # 406不配置到到channel_code中，或者配置为处理中
            "message": "error"
        }
        self.update(api, mode)

    def update_cashfree_withdraw_query_pending(self):
        api = "/payout/v1/getTransferStatus"
        # cashfree通道返回status=SUCCESS且data.status=PENDING，置为放款处理中
        mode = {
            "status": "SUCCESS",
            "subCode": "200",
            "message": "Details of transfer with transferId 159381033b123",
            "data": {
                "transfer": {
                    "referenceId": 17073,
                    "bankAccount": "026291800001191",
                    "beneId": "ABCD_123",
                    "amount": "20.00",
                    "status": "PENDING",
                    "utr": "1387420170430008800069857",
                    "addedOn": "2020-03-25 05:51:22",
                    "processedOn": "2020-03-25 05:51:22",
                    "acknowledged": 1
                }
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_success_cashfree(self):
        # cashfree_订阅，创建订阅请求成功
        api = "/api/v2/subscriptions"
        mode = {
            "status": "OK",
            "message": "Subscription created successfully",
            "subReferenceId": global_cashfree_subscribe_id,  # 在订阅结果查询时需要用
            "authLink": global_cashfree_subscribe_url
        }
        self.update(api, mode)

    def update_autoSubscribe_resultquery_success_cashfree(self):
        # cashfree_订阅结果查询成功
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id  # global_cashfree_subscribe_id依赖于上一步的返回，如果这个8615在mock上被改了会导致断言失败
        mode = {
            "status": "OK",
            "message": "Subscription Details",
            "subscription": {
                "subscriptionId": "f2020032414154",
                "subReferenceId": 8611,
                "planId": "1100",
                "customerName": "JOHN DOE",
                "customerEmail": "wangxiaoming@google.com",
                "customerPhone": "15201959337",
                "mode": "",
                "cardNumber": None,
                "status": "ACTIVE",  # INITIALIZED、ACTIVE成功、CANCELLED 和 COMPLETED 订阅失败
                "addedOn": "2020-03-25 12:33:37",
                "scheduledOn": None,
                "currentCycle": 0
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_resultquery_process_cashfree(self):
        # cashfree_订阅结果查询处理中，addedOn设置一个很大的时间
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id  # global_cashfree_subscribe_id依赖于上一步的返回，如果这个8615在mock上被改了会导致断言失败
        mode = {
            "status": "OK",
            "message": "Subscription Details",
            "subscription": {
                "subscriptionId": "f2020032414154",
                "subReferenceId": 8615,
                "planId": "1100",
                "customerName": "JOHN DOE",
                "customerEmail": "wangxiaoming@google.com",
                "customerPhone": "15201959337",
                "mode": "",
                "cardNumber": None,
                "status": "INITIALIZED",  # INITIALIZED 等待用户授权中、 ACTIVE 成功、CANCELLED 和 COMPLETED 订阅失败
                "addedOn": "2050-03-25 12:33:37",
                # status= INITIALIZED 且当前时间大于创建时间addedOn + subscribe_query_expire_time，就会调用订阅取消接口
                "scheduledOn": None,
                "currentCycle": 0
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_resultquery_fail_cashfree_001(self):
        # cashfree_订阅结果查询到订阅失败status=CANCELLED，addedOn设置一个很大的时间
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id  # global_cashfree_subscribe_id依赖于上一步的返回，如果这个8615在mock上被改了会导致断言失败
        mode = {
            "status": "OK",
            "message": "Subscription Details",
            "subscription": {
                "subscriptionId": "f2020032414154",
                "subReferenceId": 8615,
                "planId": "1100",
                "customerName": "JOHN DOE",
                "customerEmail": "wangxiaoming@google.com",
                "customerPhone": "15201959337",
                "mode": "",
                "cardNumber": None,
                "status": "CANCELLED",  # INITIALIZED 等待用户授权中、 ACTIVE 成功、CANCELLED 和 COMPLETED 订阅失败
                "addedOn": "2050-03-25 12:33:37",
                # status= INITIALIZED 且当前时间大于创建时间addedOn + subscribe_query_expire_time，就会调用订阅取消接口
                "scheduledOn": None,
                "currentCycle": 0
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_resultquery_fail_cashfree_002(self):
        # cashfree_订阅结果查询到订阅失败status=COMPLETED，addedOn设置一个很大的时间
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id  # global_cashfree_subscribe_id依赖于上一步的返回，如果这个8615在mock上被改了会导致断言失败
        mode = {
            "status": "OK",
            "message": "Subscription Details",
            "subscription": {
                "subscriptionId": "f2020032414154",
                "subReferenceId": 8615,
                "planId": "1100",
                "customerName": "JOHN DOE",
                "customerEmail": "wangxiaoming@google.com",
                "customerPhone": "15201959337",
                "mode": "",
                "cardNumber": None,
                "status": "COMPLETED",  # INITIALIZED 等待用户授权中、 ACTIVE 成功、CANCELLED 和 COMPLETED 订阅失败
                "addedOn": "2050-03-25 12:33:37",
                # status= INITIALIZED 且当前时间大于创建时间addedOn + subscribe_query_expire_time，就会调用订阅取消接口
                "scheduledOn": None,
                "currentCycle": 0
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_resultquery_expire_cashfree(self):
        # cashfree_订阅结果查询，订阅超过配置配置时间，调用取消订阅接口置为订阅失败
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id  # global_cashfree_subscribe_id依赖于上一步的返回，如果这个8615在mock上被改了会导致断言失败
        mode = {
            "status": "OK",
            "message": "Subscription Details",
            "subscription": {
                "subscriptionId": "f2020032414154",
                "subReferenceId": 8615,
                "planId": "1100",
                "customerName": "JOHN DOE",
                "customerEmail": "wangxiaoming@google.com",
                "customerPhone": "15201959337",
                "mode": "",
                "cardNumber": None,
                "status": "INITIALIZED",  # INITIALIZED 等待用户授权中、 ACTIVE 成功
                "addedOn": "2020-03-25 12:33:37",  # 且当前时间大于创建时间addedOn + subscribe_query_expire_time，就会调用订阅取消接口
                "scheduledOn": None,
                "currentCycle": 0
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_cancel_sucess_cashfree(self):
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id + "/cancel"  # global_cashfree_subscribe_id依赖于上一步的返回，如果这个8615在mock上被改了会导致断言失败
        mode = {
            "status": "OK",
            "message": "Subscription Cancelled"
        }
        self.update(api, mode)

    def update_autoSubscribe_fail_cashfree(self):
        # cashfree_订阅请求，创建订阅直接失败即绑卡失败
        api = "/api/v2/subscriptions"
        mode = {
            "status": "ERROR",
            "message": "Subscription created failed",
            "subReferenceId": 8615,
            "authLink": None
        }
        self.update(api, mode)

    def update_autoSubscribe_withhold_error_cashfree(self):
        # cashfree_订阅代扣请求异常
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id + "/charge"  # global_cashfree_subscribe_id是订阅绑卡时返回的id
        mode = {
            "status": "ERROR",  # OK 请求成功，ERROR 请求失败
            "message": "SUCCESSFUL",
            "subCode": 404,
            "payment": {
                "paymentId": global_cashfree_subscribe_paymentId,  # 下一步代扣查询要用
                "referenceId": 285180,
                "amount": "90",
                "status": "ERROR",  # SUCCESS、FAILED、PENDING
                "addedOn": "2020-03-24 15:31:43"
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_withhold_process_cashfree(self):
        # cashfree_订阅代扣请求处理中：status=OK&status=PENDING
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id + "/charge"  # global_cashfree_subscribe_id是订阅绑卡时返回的id
        mode = {
            "status": "OK",  # OK 请求成功，ERROR 请求失败
            "message": "SUCCESSFUL",
            "subCode": 404,
            "payment": {
                "paymentId": global_cashfree_subscribe_paymentId,  # 下一步代扣查询要用
                "referenceId": 285180,
                "amount": "90",
                "status": "PENDING",  # SUCCESS、FAILED、PENDING
                "addedOn": "2020-03-24 15:31:43"
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_withhold_fail_cashfree(self):
        # cashfree_订阅代扣请求，status=OK&status=FAILED直接代扣失败
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id + "/charge"  # global_cashfree_subscribe_id是订阅绑卡时返回的id
        mode = {
            "status": "OK",  # OK 请求成功，ERROR 请求失败
            "message": global_autoSubscribe_withhold_message,
            "subCode": 404,
            "payment": {
                "paymentId": global_cashfree_subscribe_paymentId,  # 下一步代扣查询要用
                "referenceId": 285180,
                "amount": "90",
                "status": global_autoSubscribe_withhold_failcode,  # SUCCESS、FAILED、PENDING
                "addedOn": "2020-03-24 15:31:43"
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_withhold_success_cashfree(self):
        # cashfree_订阅代扣请求，status=OK&status=SUCCESS直接代扣成功
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id + "/charge"  # global_cashfree_subscribe_id是订阅绑卡时返回的id
        mode = {
            "status": "OK",  # OK 请求成功，ERROR 请求失败
            "message": global_autoSubscribe_withhold_message,
            "subCode": 404,
            "payment": {
                "paymentId": global_cashfree_subscribe_paymentId,  # 下一步代扣查询要用
                "referenceId": 285180,
                "amount": "90",
                "status": global_autoSubscribe_withhold_successcode,  # SUCCESS、FAILED、PENDING
                "addedOn": "2020-03-24 15:31:43"
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_withhold_query_success_cashfree(self):
        # cashfree_订阅代扣查询，status=OK&status=SUCCESS查询到代扣成功
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id + "/payments/" + global_cashfree_subscribe_paymentId  # 8615是订阅绑卡时返回的id，8134是上异步订阅请求返回的paymentId
        mode = {
            "status": "OK",  # OK 请求成功，ERROR 请求失败
            "message": global_autoSubscribe_withhold_message,
            "subCode": 404,
            "payment": {
                "paymentId": global_cashfree_subscribe_paymentId,
                "cycle": 1,
                "referenceId": 286113,
                "amount": "110.00",
                "status": global_autoSubscribe_withhold_successcode,  # SUCCESS、FAILED、PENDING、undefined
                "addedOn": "2020-03-24 15:31:43"
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_withhold_query_fail_cashfree(self):
        # cashfree_订阅代扣查询，status=OK&status=SUCCESS查询到代扣成功
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id + "/payments/" + global_cashfree_subscribe_paymentId  # 8615是订阅绑卡时返回的id，8134是上异步订阅请求返回的paymentId
        mode = {
            "status": "OK",  # OK 请求成功，ERROR 请求失败
            "message": global_autoSubscribe_withhold_message,
            "subCode": 404,
            "payment": {
                "paymentId": global_cashfree_subscribe_paymentId,
                "cycle": 1,
                "referenceId": 286113,
                "amount": "110.00",
                "status": global_autoSubscribe_withhold_failcode,  # SUCCESS、FAILED、PENDING、undefined
                "addedOn": "2020-03-24 15:31:43"
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_withhold_query_process_cashfree(self):
        # cashfree_订阅代扣查询
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id + "/payments/" + global_cashfree_subscribe_paymentId  # 8615是订阅绑卡时返回的id，8134是上异步订阅请求返回的paymentId
        mode = {
            "status": "OK",  # OK 请求成功，ERROR 请求失败
            "message": global_autoSubscribe_withhold_message,
            "subCode": 404,
            "payment": {
                "paymentId": global_cashfree_subscribe_paymentId,
                "cycle": 1,
                "referenceId": 286113,
                "amount": "110.00",
                "status": "PENDING",  # SUCCESS、FAILED、PENDING、undefined
                "addedOn": "2020-03-24 15:31:43"
            }
        }
        self.update(api, mode)

    def update_autoSubscribe_withhold_query_error_cashfree(self):
        # cashfree_订阅代扣查询
        api = "/api/v2/subscriptions/" + global_cashfree_subscribe_id + "/payments/" + global_cashfree_subscribe_paymentId  # 8615是订阅绑卡时返回的id，8134是上异步订阅请求返回的paymentId
        mode = {
            "status": "ERROR",  # OK 请求成功，ERROR 请求失败
            "message": global_autoSubscribe_withhold_message,
            "subCode": 404,
            "payment": {
                "paymentId": global_cashfree_subscribe_paymentId,
                "cycle": 1,
                "referenceId": 286113,
                "amount": "110.00",
                "status": "undefined",  # SUCCESS、FAILED、PENDING、undefined
                "addedOn": "2020-03-24 15:31:43"
            }
        }
        self.update(api, mode)

    def update_cashfree_reconic_total_havadata(self):
        # 总账单：注意settlements节点下的值不要改，改了会导致脚本失败
        api = "/api/v1/settlements"
        mode = {
            "status": "OK",
            "message": "1 settlements fetched",
            "lastId": 262907,
            "settlements": [
                {
                    "id": 262907,
                    "totalTxAmount": "7129.00",  # =明细中txAmount之和，不要改
                    "settlementAmount": "7105.40",  # =明细中settlementAmount之和，不要改
                    "adjustment": "0.00",
                    "amountSettled": "7105.40",
                    "transactionFrom": get_date(fmt="%Y-%m-%d"),
                    "transactionTill": get_date(fmt="%Y-%m-%d"),
                    "utr": "N164200403470096",
                    "settledOn": "2020-06-12 10:32:04"
                }
            ]
        }
        self.update(api, mode)

    def update_cashfree_reconic_total_nodata(self):
        # 总账单
        api = "/api/v1/settlements"
        mode = {
            "status": "OK",
            "message": "No data fetched",
            "settlements": [
            ]
        }
        self.update(api, mode)

    def update_cashfree_reconic_detail_havedata(self, data_id=1):
        # 单笔账单明细：注意transactions节点下的值不要改，改了会导致脚本失败
        api = "/api/v1/settlement"
        mode = {
            "status": "OK",
            "message": "2 settlements fetched",
            "transactions": [
                {
                    "id": data_id*1000000 + 1,
                    "referenceId": "145600992",
                    "orderId": "RBIZ4121488104" + str(data_id*1000000 + 1),  # 不要改
                    "txAmount": "1510.50",  # 不要改
                    "paymentMode": "UPI",
                    "bankName": "android_intent",
                    "serviceCharge": "5.00",  # 不要改
                    "serviceTax": "0.90",  # 不要改
                    "settlementAmount": "1504.60",  # 不要改
                    "txTime": "2020-06-11 00:33:07"
                },
                {
                    "id": data_id*1000000 + 2,
                    "referenceId": "145602033",
                    "orderId": "RBIZ4121488104" + str(data_id*1000000 + 2),  # 不要改
                    "txAmount": "2054.00",  # 不要改
                    "paymentMode": "UPI",
                    "bankName": "android_intent",
                    "serviceCharge": "5.00",  # 不要改
                    "serviceTax": "0.90",  # 不要改
                    "settlementAmount": "2048.10",  # 不要改
                    "txTime": "2020-06-11 00:36:44"
                }
            ],
            "lastId": data_id*1000000 + 2
        }
        self.update(api, mode)

    def update_cashfree_reconic_detail_nodata(self):
        # 单笔账单明细
        api = "/api/v1/settlement"
        mode = {
            "status": "OK",
            "message": "No data fetched",
            "transactions": [
            ]
        }
        self.update(api, mode)


if __name__ == "__main__":
    pass
