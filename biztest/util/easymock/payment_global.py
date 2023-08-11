import datetime
import random

from biztest.config.global_gbiz.global_gbiz_interface_params_config import payment_callback_url
from biztest.function.global_rbiz.rbiz_global_db_function import get_withhold_by_item_no, get_refund_request, \
    get_withdraw
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.easymock import Easymock
from biztest.function.global_gbiz.gbiz_global_db_function import get_withdraw_by_asset_item_no, \
    get_withdraw_order_by_item_no, get_withdraw_record_by_item_no
from biztest.util.tools.tools import get_date, get_sysconfig, get_tz, get_random_str, get_random_num, global_encry_data, \
    get_timestamp
from biztest.util.http.http_util import Http
from copy import deepcopy
import common.global_const as gc

env = gc.ENV
country = gc.COUNTRY
environment = gc.ENVIRONMENT
db = DataBase("global_payment%s_%s" % (env, country), environment)


class PaymentGlobalMock(Easymock):

    def update_withdraw_apply_success(self):
        api = "/withdraw/autoWithdraw"
        mode = '''{
            "code": 2,
            "message": "处理成功",
            "data": {"platform_code": "E20000",
                 "platform_message": "PROCESSING",
                 "channel_name": "test_channel_withdraw",
                 "channel_key": "@id",
                 "channel_code": "0000",
                 "channel_message": "成功",
                 "amount": function({_req}){return _req.body.amount},
                 "status": 2,
                 "trade_no": function({_req}){return _req.body.trade_no},
                 "finished_at": "1000-01-01 00:00:00"}}
            // 状态，0、新建，1、处理中，2、成功，3、失败'''
        self.update(api, mode)

    def update_withdraw_apply_fail(self):
        api = "/withdraw/autoWithdraw"
        mode = '''{
            "code": 1,
            "message": "风险交易: 疑似重复放款",
            "data": {
                "amount": function({_req}){return _req.body.amount},
                "platform_code": "KN_RISK_CONTROL",
                "platform_message": "Risk control intercepts, exceeding the number of trades",
                "channel_name": "route_no_channel",
                "channel_code": "KN_RISK_CONTROL",
                "channel_message": "Risk control intercepts, exceeding the number of trades",
                "created_at": "@now",
                "finished_at": "@now",
                "receiver_bank_code": "mock_test_0001",
                "channel_key": "@id", 
                "status": 3,
                "trade_no": function({_req}){return _req.body.trade_no}}}
            // 状态，0、新建，1、处理中，2、成功，3、失败'''
        self.update(api, mode)

    def update_withdraw_apply_process(self):
        api = "/withdraw/autoWithdraw"
        mode = '''{
            "code": 2,
            "message": "订单交易正在处理中！",
            "data": {
                "amount": function({_req}){return _req.body.amount},
                "platform_code": "E20002",
                "platform_message": "PROCESSING",
                "channel_name": "autotest_channel",
                "channel_code": "",
                "channel_message": "",
                "created_at": "@now",
                "finished_at": "",
                "receiver_bank_code": "mock_test_0001",
                "channel_key": "@id",
                "status": 0,
                "trade_no": function({_req}){return _req.body.trade_no}}}
            // 状态，0、新建，1、处理中，2、成功，3、失败'''
        self.update(api, mode)

    def update_withdraw_query_status(self, asset_info, merchant_status="process", receipt_status="process",
                                     retry=False, platform_code=None, platform_message=None, finish_at=None):
        api = "/withdraw/query"
        order_info = get_withdraw_order_by_item_no(asset_info['data']['asset']['item_no'] + 'w')
        record_info = get_withdraw_record_by_item_no(asset_info['data']['asset']['item_no'] + 'w')
        amount = order_info[0]["withdraw_order_amount"]
        if finish_at is None:
            finish_at = get_date(timezone=get_tz(gc.COUNTRY))
        data = {
            "code": 0,
            "message": "处理成功",
            "data": {"platform_code": "E20000",
                     "platform_message": "成功",
                     "channel_name": "test_channel",
                     "channel_code": "channel_code_000",
                     "channel_message": "channel_message_000",
                     "withdraw_type": order_info[0]["withdraw_order_withdraw_type"],
                     "amount": amount,
                     "channel_key": "%s",
                     "created_at": get_date(timezone=get_tz(gc.COUNTRY)),
                     "finished_at": finish_at,
                     "status": 2,
                     "trade_no": "",
                     "trade_details": []}}
        data["data"]["channel_key"] = record_info[-1]["withdraw_record_channel_key"]
        data["data"]["trade_no"] = record_info[-1]["withdraw_record_trade_no"]
        for record in record_info:
            temp = dict()
            temp["channel_name"] = "test_channel"
            temp["channel_key"] = record["withdraw_record_channel_key"]
            temp["channel_code"] = "channel_code_000"
            temp["channel_message"] = "channel_message_000"
            temp["trade_no"] = record["withdraw_record_trade_no"]
            temp["status"] = 3
            temp["finished_at"] = record["withdraw_record_finish_at"]
            temp["wd_number"] = "mock_test_222222222"
            temp["expire_time"] = get_date(month=1, timezone=get_tz())
            data["data"]["trade_details"].append(deepcopy(temp))
        if merchant_status == "success":
            data["data"]["status"] = 2
            data["code"] = 0
        elif merchant_status == "fail":
            data["data"]["status"] = 3
            data["code"] = 1
        else:
            data["data"]["status"] = 1
            data["code"] = 2
        if receipt_status == "success":
            data["data"]["platform_code"] = platform_code if platform_code is not None else "E20000"
            data["data"]["platform_message"] = platform_message if platform_message is not None else \
                "Transfer completed successfully"
            data["data"]["trade_details"][-1]["status"] = 2
        elif receipt_status == "fail" and retry is True:
            data["data"]["platform_code"] = platform_code if platform_code is not None else "rejected"
            data["data"]["platform_message"] = platform_message if platform_message is not None else \
                "Payout failed. Reinitiate transfer after 30 min."
            data["data"]["trade_details"][-1]["status"] = 3
        elif receipt_status == "fail" and retry is False:
            data["data"]["platform_code"] = platform_code if platform_code is not None else "KN_RISK_CONTROL"
            data["data"]["platform_message"] = platform_message if platform_message is not None else \
                "Risk control intercepts and exceeds trading limits"
            data["data"]["trade_details"][-1]["status"] = 3
        elif receipt_status == "process":
            data["data"]["platform_code"] = platform_code if platform_code is not None else "E20002"
            data["data"]["platform_message"] = platform_message if platform_message is not None else \
                "Transfer request pending at the bank"
            data["data"]["trade_details"][-1]["status"] = 1
        data["data"]["trade_details"][-1]["finished_at"] = get_date(timezone=get_tz())
        self.update(api, data)
        pass

    def update_phl_offline_withdraw_query_status(self, asset_info, merchant_status="process", receipt_status="process",
                                                 retry=False, platform_code=None, platform_message=None):
        api = "/withdraw/query"
        order_info = get_withdraw_order_by_item_no(asset_info['data']['asset']['item_no'] + 'w')
        record_info = get_withdraw_record_by_item_no(asset_info['data']['asset']['item_no'] + 'w')
        amount = order_info[0]["withdraw_order_amount"]
        data = {
            "code": 0,
            "message": "处理成功",
            "data": {"platform_code": "E20000",
                     "platform_message": "成功",
                     "channel_name": "test_channel",
                     "channel_code": "channel_code_000",
                     "channel_message": "channel_message_000",
                     "amount": amount,
                     "channel_key": "%s",
                     "created_at": get_date(timezone=get_tz()),
                     "finished_at": get_date(timezone=get_tz()),
                     "status": 2,
                     "trade_no": "",
                     "trade_details": []}}
        data["data"]["channel_key"] = record_info[-1]["withdraw_record_channel_key"]
        data["data"]["trade_no"] = record_info[-1]["withdraw_record_trade_no"]
        for record in record_info:
            temp = dict()
            temp["channel_name"] = "test_channel"
            temp["channel_key"] = record["withdraw_record_channel_key"]
            temp["channel_code"] = "channel_code_000"
            temp["channel_message"] = "channel_message_000"
            temp["trade_no"] = record["withdraw_record_trade_no"]
            temp["status"] = 3
            temp["finished_at"] = record["withdraw_record_finish_at"]
            temp["wd_number"] = "mock_test_222222222"
            temp["expire_time"] = get_date(month=1, timezone=get_tz())
            data["data"]["trade_details"].append(deepcopy(temp))
        if merchant_status == "success":
            data["data"]["status"] = 2
            data["code"] = 0
        elif merchant_status == "fail":
            data["data"]["status"] = 3
            data["code"] = 1
        else:
            data["data"]["status"] = 1
            data["code"] = 2
        if receipt_status == "success":
            data["data"]["platform_code"] = platform_code if platform_code is not None else "E20000"
            data["data"]["platform_message"] = platform_message if platform_message is not None else \
                "Transfer completed successfully"
            data["data"]["trade_details"][-1]["status"] = 2
        elif receipt_status == "fail" and retry is True:
            data["data"]["platform_code"] = platform_code if platform_code is not None else "rejected"
            data["data"]["platform_message"] = platform_message if platform_message is not None else \
                "Payout failed. Reinitiate transfer after 30 min."
            data["data"]["trade_details"][-1]["status"] = 3
        elif receipt_status == "fail" and retry is False:
            data["data"]["platform_code"] = platform_code if platform_code is not None else "KN_RISK_CONTROL"
            data["data"]["platform_message"] = platform_message if platform_message is not None else \
                "Risk control intercepts and exceeds trading limits"
            data["data"]["trade_details"][-1]["status"] = 3
        elif receipt_status == "process":
            data["data"]["platform_code"] = platform_code if platform_code is not None else "E1000"
            data["data"]["platform_message"] = platform_message if platform_message is not None else \
                "测试线下支付放款中，当作成功处理"
            data["data"]["trade_details"][-1]["status"] = 1
        data["data"]["trade_details"][-1]["finished_at"] = get_date(timezone=get_tz())
        self.update(api, data)
        pass

    def update_phl_offline_withdraw_status_exception(self, asset_info, merchant_status="process",
                                                     receipt_status="process",
                                                     retry=False, platform_code=None, platform_message=None):
        api = "/withdraw/query"
        order_info = get_withdraw_order_by_item_no(asset_info['data']['asset']['item_no'] + 'w')
        record_info = get_withdraw_record_by_item_no(asset_info['data']['asset']['item_no'] + 'w')
        amount = order_info[0]["withdraw_order_amount"]
        data = {
            "code": 0,
            "message": "处理成功",
            "data": {"platform_code": "E20000",
                     "platform_message": "成功",
                     "channel_name": "test_channel",
                     "channel_code": "channel_code_000",
                     "channel_message": "channel_message_000",
                     "amount": amount,
                     "channel_key": "%s",
                     "created_at": get_date(timezone=get_tz()),
                     "finished_at": get_date(timezone=get_tz()),
                     "status": 2,
                     "trade_no": "",
                     "trade_details": []}}
        data["data"]["channel_key"] = record_info[-1]["withdraw_record_channel_key"]
        data["data"]["trade_no"] = record_info[-1]["withdraw_record_trade_no"]
        for record in record_info:
            temp = dict()
            temp["channel_name"] = "test_channel"
            temp["channel_key"] = record["withdraw_record_channel_key"]
            temp["channel_code"] = "channel_code_000"
            temp["channel_message"] = "channel_message_000"
            temp["trade_no"] = record["withdraw_record_trade_no"]
            temp["status"] = 3
            temp["finished_at"] = record["withdraw_record_finish_at"]
            temp["wd_number"] = get_random_str()
            temp["expire_time"] = record["withdraw_record_finish_at"]
            data["data"]["trade_details"].append(deepcopy(temp))
        if merchant_status == "success":
            data["data"]["status"] = 2
            data["code"] = 0
        elif merchant_status == "fail":
            data["data"]["status"] = 3
            data["code"] = 1
        else:
            data["data"]["status"] = 1
            data["code"] = 2
        if receipt_status == "success":
            data["data"]["platform_code"] = platform_code if platform_code is not None else "E20000"
            data["data"]["platform_message"] = platform_message if platform_message is not None else \
                "Transfer completed successfully"
            data["data"]["trade_details"][-1]["status"] = 2
        elif receipt_status == "fail" and retry is True:
            data["data"]["platform_code"] = platform_code if platform_code is not None else "rejected"
            data["data"]["platform_message"] = platform_message if platform_message is not None else \
                "Payout failed. Reinitiate transfer after 30 min."
            data["data"]["trade_details"][-1]["status"] = 3
        elif receipt_status == "fail" and retry is False:
            data["data"]["platform_code"] = platform_code if platform_code is not None else "KN_RISK_CONTROL"
            data["data"]["platform_message"] = platform_message if platform_message is not None else \
                "Risk control intercepts and exceeds trading limits"
            data["data"]["trade_details"][-1]["status"] = 3
        elif receipt_status == "process":
            data["data"]["platform_code"] = platform_code if platform_code is not None else "E1000"
            data["data"]["platform_message"] = platform_message if platform_message is not None else \
                "测试线下支付放款中，当作成功处理"
            data["data"]["trade_details"][-1]["status"] = 1
        data["data"]["trade_details"][-1]["finished_at"] = get_date(timezone=get_tz())
        self.update(api, data)
        pass

    def update_withdraw_query_not_exist(self):
        api = "/withdraw/query"
        mode = '''{"code": 3, "message": "交易不存在", "data": null}
        // 状态，0、新建，1、处理中，2、成功，3、失败'''
        self.update(api, mode)

    def update_withdraw_query_risk_fail(self, asset_info):
        api = "/withdraw/query"
        amount = asset_info["data"]["asset"]["amount"]
        channel_key = get_withdraw_by_asset_item_no(asset_info['data']['asset']['item_no'])[0]['withdraw_channel_key']
        trade_no = get_withdraw_by_asset_item_no(asset_info['data']['asset']['item_no'])[0]['withdraw_merchant_key']
        mode = {
            "code": 1,
            "message": "交易失败",
            "data": {
                "platform_code": "E20011",
                "platform_message": "风控拦截，超过交易次数",
                "channel_name": "cashfree_yomoyo1_withdraw",
                "channel_code": "KN_RISK_CONTROL",
                "channel_message": "",
                "amount": amount,
                "channel_key": channel_key,
                "created_at": get_date(),
                "finished_at": get_date(),
                "receiver_bank_code": "BKID0006012",
                "status": 3,
                "trade_no": trade_no
            }
        }
        self.update(api, mode)

    def update_withdraw_balance_enough(self):
        api = "/withdraw/balance"
        mode = {
            "code": 0,
            "message": "余额查询成功",
            "data": {
                "total": 19979478,
                "available": 19979478,
                "data": [{
                    "total": 19979478,
                    "available": 19979478,
                    "channel_name": "cashfree_yomoyo1_withdraw"
                }]
            }
        }
        self.update(api, mode)
        pass

    def update_withdraw_balance_not_enouth(self):
        api = "/withdraw/balance"
        mode = {
            "code": 0,
            "message": "余额查询成功",
            "data": {
                "total": 10,
                "available": 10,
                "data": [{
                    "total": 10,
                    "available": 10,
                    "channel_name": "cashfree_yomoyo1_withdraw"
                }]
            }
        }
        self.update(api, mode)
        pass

    def update_withdraw_balance_random(self, amount=0):
        if amount == 0:
            amount = random.randint(0, 100000000)
        api = "/withdraw/balance"
        mode = {
            "code": 0,
            "message": "处理成功",
            "data": {"total": amount,
                     "available": amount}}
        self.update(api, mode)
        pass

    # rbiz global
    def update_withhold_autopay_ebank_url_success(self, withhold_amount=758400):
        api = "/withhold/autoPay"
        mode = {
            "code": 2,
            "message": "交易进行中",
            "data": {
                "platform_code": "E20002",
                "platform_message": "created",
                "channel_name": "razorpay_yomoyo5_ebank",
                "channel_code": "created",
                "channel_message": "created",
                "channel_key": "EBANK_" + get_random_num(),
                "need_bind": 0,
                "need_sms": 0,
                "amount": withhold_amount,
                "status": 1,
                "created_at": get_date(),
                "finished_at": "1000-01-01 00:00:00",
                "balance_not_enough": 0,
                "payment_type": "ebank",
                "payment_mode": "",
                "payment_option": "",
                "payment_gateway": "",
                "payment_data": {
                    "redirect_url": "https://rzp.io/i/nQR3ymulq",
                    "expire_time": get_date(minute=15)
                }
            }
        }
        self.update(api, mode)
        pass

    def update_withhold_autopay_ebank_account_success(self, withhold_amount=758400):
        api = "/withhold/autoPay"
        mode = {
            "code": 2,
            "message": "交易进行中",
            "data": {
                "platform_code": "E20002",
                "platform_message": "created",
                "channel_name": "qpay_kn_ebank",
                "channel_code": "created",
                "channel_message": "created",
                "channel_key": "ACCOUNT_" + get_random_num(),
                "need_bind": 0,
                "need_sms": 0,
                "amount": withhold_amount,
                "status": 1,
                "created_at": get_date(),
                "finished_at": "1000-01-01 00:00:00",
                "balance_not_enough": 0,
                "payment_type": "ebank",
                "payment_mode": "",
                "payment_option": "",
                "payment_gateway": "",
                "payment_data": {
                    "expire_time": "2022-10-09 17:26:07",
                    "bank_name": "HDFC",
                    "bank_account": "50200068003498",
                    "bank_code": "HDFC0000944",
                    "bank_user_name": "SHAURYA RAJ VERMA"
                }
            }
        }
        self.update(api, mode)
        pass

    def update_withhold_autopay_ebank_upi_success(self, withhold_amount=758400):
        api = "/withhold/autoPay"
        mode = {
            "code": 2,
            "message": "交易进行中",
            "data": {
                "platform_code": "E20002",
                "platform_message": "created",
                "channel_name": "qpay_kn_ebank",
                "channel_code": "created",
                "channel_message": "created",
                "channel_key": "UPI_" + get_random_num(),
                "need_bind": 0,
                "need_sms": 0,
                "amount": withhold_amount,
                "status": 1,
                "created_at": get_date(),
                "finished_at": "1000-01-01 00:00:00",
                "balance_not_enough": 0,
                "payment_type": "ebank",
                "payment_mode": "",
                "payment_option": "",
                "payment_gateway": "",
                "payment_data": {
                    "expire_time": get_date(hour=2),
                    "bank_name": "HDFC",
                    "vpa_account": "50200068003498",
                    "bank_code": "HDFC0000944",
                    "bank_user_name": "SHAURYA RAJ VERMA"
                }
            }
        }
        self.update(api, mode)
        pass

    def update_withhold_autopay_sdk_success(self, withhold_amount=758400, channel_key=get_random_str(10)):
        api = "/withhold/autoPay"
        mode = {
            "code": 2,
            "message": "交易进行中",
            "data": {
                "platform_code": "E20000",
                "platform_message": "Token generated",
                "channel_name": "cashfree_yomoyo5_sdk",
                "channel_code": "OK",
                "channel_message": "Token generated",
                "channel_key": "SDK_" + channel_key,
                "need_bind": 0,
                "need_sms": 0,
                "amount": withhold_amount,
                "status": 1,
                "created_at": get_date(),
                "finished_at": "1000-01-01 00:00:00",
                "balance_not_enough": 0,
                "payment_type": "sdk",
                "payment_mode": "",
                "payment_option": "",
                "payment_gateway": "",
                "payment_data": {
                    "sdk": "cashfree",
                    "app_id": channel_key,
                    "token": "d69JCN4MzUIJiOicGbhJCLiQ1VKJiOiAXe0Jye.N7QfiEjM4IjY0QmZ4EDZmVjI6ICdsF2cfJCL0YzMxYTMwEjNxojIwhXZiwiIS5USiojI5NmblJnc1NkclRmcvJCL0gTN3ojI05Wdv1WQyVGZy9mIsISM0cDN5IDOykDM5MzMwEjMxQjWJJkUiojIklkclRmcvJye.37RmNWVKJzBltozk3LFv6uIoCSknAaEAD6WfyFC11Gu4seMUx1c6EHMNPuqdrMBh-Q",
                    "notify_url": "https://biz-gateway-proxy.starklotus.com/ind_payment1/cashfree/callback/cashfree_yomoyo5_sdk",
                    "expire_time": get_date(minute=15)
                }
            }
        }
        self.update(api, mode)
        pass

    def update_withhold_autopay_qrcode_success(self, withhold_amount=758400, channel_key=get_random_str(10)):
        api = "/withhold/autoPay"
        mode = {
            "code": 2,
            "message": "交易进行中",
            "data": {
                "platform_code": "E20002",
                "platform_message": "PROCESSING",
                "channel_name": "payso_copperstone_qrcode",
                "channel_code": "KN_REQUEST_SUCCESS",
                "channel_message": "KN_REQUEST_SUCCESS",
                "channel_key": "QRCODE_" + channel_key,
                "need_bind": 0,
                "need_sms": 0,
                "amount": withhold_amount,
                "status": 1,
                "created_at": get_date(),
                "finished_at": "1000-01-01 00:00:00",
                "balance_not_enough": 0,
                "payment_type": "qrcode",
                "payment_mode": "",
                "payment_option": "",
                "payment_gateway": "",
                "payment_data": {
                    "image_dat": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA8IAAAEUAASUVORK5CYII=",
                    "expire_time": get_date(minute=15)
                }
            }
        }
        self.update(api, mode)
        pass

    def update_withhold_autopay_paycode_success(self, withhold_amount=758400, channel_key=get_random_str(10)):
        api = "/withhold/autoPay"
        mode = {
            "code": 2,
            "message": "交易进行中",
            "data": {
                "platform_code": "E20002",
                "platform_message": "PROCESSING",
                "channel_name": "payso_copperstone_paycode",
                "channel_code": "KN_REQUEST_SUCCESS",
                "channel_message": "KN_REQUEST_SUCCESS",
                "channel_key": "PAYCODE_" + channel_key,
                "need_bind": 0,
                "need_sms": 0,
                "amount": withhold_amount,
                "status": 1,
                "created_at": get_date(),
                "finished_at": "1000-01-01 00:00:00",
                "balance_not_enough": 0,
                "payment_type": "paycode",
                "payment_mode": "",
                "payment_option": "",
                "payment_gateway": "",
                "payment_data": {
                    "wh_number": "PSP331000008101",
                    "image_dat": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA8IAAAEUAASUVORK5CYII=",
                    "expire_time": get_date(minute=15)
                }
            }
        }
        self.update(api, mode)
        pass

    def update_withhold_autopay_barcode_success(self, withhold_amount=758400, channel_key=get_random_str(10)):
        api = "/withhold/autoPay"
        mode = {
            "code": 2,
            "message": "交易进行中",
            "data": {
                "platform_code": "E20002",
                "platform_message": "PROCESSING",
                "channel_name": "payso_copperstone_barcode",
                "channel_code": "KN_REQUEST_SUCCESS",
                "channel_message": "KN_REQUEST_SUCCESS",
                "channel_key": "BARCODE_" + channel_key,
                "need_bind": 0,
                "need_sms": 0,
                "amount": withhold_amount,
                "status": 1,
                "created_at": get_date(),
                "finished_at": "1000-01-01 00:00:00",
                "balance_not_enough": 0,
                "payment_type": "barcode",
                "payment_mode": "",
                "payment_option": "",
                "payment_gateway": "",
                "payment_data": {
                    "barcode_url": "https://s3.amazonaws.com/cash_payment_barcodes/sandbox_reference.png",
                    "wh_number": "PSP331000008101",
                    "image_dat": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA8IAAAEUAASUVORK5CYII=",
                    "expire_time": get_date(minute=15)
                }
            }
        }
        self.update(api, mode)
        pass

    def update_withhold_auto_qrcode_success(self):
        api = "/withhold/autoPay"
        mode = '''{
                       "code": 2,
                       "message": "处理成功",
                       "data": {"platform_code": "E20000",
                            "platform_message": "成功",
                            "channel_name": "auto_test_channel",
                            "channel_key": "@id",
                            "channel_code": "0000",
                            "channel_message": "自动化成功",
                            "amount": function({_req}){return _req.body.amount},
                            "status": 2,
                            "payment_type": "qrcode",
                            "payment_option": "" ,
                            "payment_data":{"image_dat":"@id","expire_time":"@now"},
                            "finished_at": "@now"}}
                       // 状态，0、新建，1、处理中，2、成功，3、失败'''
        self.update(api, mode)
        pass

    def update_withhold_auto_checkout_success(self):
        api = "/withhold/autoPay"
        html = ""
        mode = '''{
                       "code": 2,
                       "message": "处理成功",
                       "data": {"platform_code": "E20000",
                            "platform_message": "成功",
                            "channel_name": "auto_test_channel",
                            "channel_key": "@id",
                            "channel_code": "0000",
                            "channel_message": "自动化成功",
                            "amount": function({_req}){return _req.body.amount},
                            "status": 2,
                            "payment_type": "checkout",
                            "payment_option": "" ,
                            "payment_data": %s,
                            "finished_at": "@now"}}
                       // 状态，0、新建，1、处理中，2、成功，3、失败''' % html
        self.update(api, mode)
        pass

    def update_withhold_auto_withhold_success(self, withhold_amount=758400, code=2):
        api = "/withhold/autoPay"
        mode = {
            "code": code,
            "message": "交易进行中",
            "data": {
                "platform_code": "E20002",
                "platform_message": "auto test mock data platform msg",
                "channel_name": "gbpay_cymo4_withhold",
                "channel_code": "KN_NO_CHANNEL_CODE",
                "channel_message": "auto test mock data channel msg",
                "need_bind": 0,
                "need_sms": 0,
                "amount": withhold_amount,
                "channel_key": "withhold" + get_random_str(10),
                "status": 1,
                "created_at": get_date(),
                "finished_at": "1000-01-01 00:00:00",
                "balance_not_enough": 0,
                "payment_type": "withhold",
                "payment_option": "withhold",
                "payment_data": {
                    "expire_time": (datetime.datetime.now() + datetime.timedelta(minutes=15)).strftime(
                        "%Y-%m-%d %H:%M:%S")
                }
            }
        }
        self.update(api, mode)
        pass

    def update_withhold_auto_paycode_success(self, wh_number, expire_time):
        api = "/withhold/autoPay"
        mode = '''{
                       "code": 2,
                       "message": "处理成功",
                       "data": {"platform_code": "E20000",
                            "platform_message": "成功",
                            "channel_name": "auto_test_channel",
                            "channel_key": "@id",
                            "channel_code": "0000",
                            "channel_message": function({_req}){return _req.body.user_uuid},
                            "amount": function({_req}){return _req.body.amount},
                            "status": 2,
                            "payment_type": "paycode",
                            "payment_option": "" ,
                            "payment_data":{"wh_number":"%s","expire_time":"%s"},
                            "finished_at": "@now"}}
                       // 状态，0、新建，1、处理中，2、成功，3、失败''' % (wh_number, expire_time)
        self.update(api, mode)
        pass

    def update_withhold_auto_paycode_fail(self):
        api = "/withhold/autoPay"
        mode = '''{
                       "code": 2,
                       "message": "处理成功",
                       "data": {"platform_code": "E20000",
                            "platform_message": "成功",
                            "channel_name": "auto_test_channel",
                            "channel_key": "@id",
                            "channel_code": "0000",
                            "channel_message": function({_req}){return _req.body.user_uuid},
                            "amount": function({_req}){return _req.body.amount},
                            "status": 1,
                            "payment_type": "paycode",
                            "payment_option": "" ,
                            "payment_data":{"wh_number":"@id","expire_time":"%s"},
                            "finished_at": "@now"}}
                       // 状态，0、新建，1、处理中，2、成功，3、失败''' % get_date(day=7)
        self.update(api, mode)
        pass

    def update_withhold_submitUtr(self, code=True):
        api = "/withhold/submitUtr"
        mode = {
            "code": 0 if code is True else 1,
            "message": "成功" if code is True else "失败",
            "data": None
        }
        self.update(api, mode)
        pass

    def update_query_channel_reconci_data(self, count=0, amount=0, finish_at=None):
        if finish_at is None:
            finish_at = get_date()
        api = "/reconci/queryChannelReconciData"
        mode = {
            "code": 0,
            "message": "交易进行中",
            "data": []
        }
        remitter_bank_account = get_random_num()
        temp = {
            "channel_name": "Rbiz",
            "channel_key": "AUTO_C609273620394387877",
            "channel_order_no": "1000234567788884",
            "amount": 6042,
            "status": "2",
            "finished_at": "2022-09-28 12:00:00",
            "created_at": "2022-09-28 11:00:00",
            "bank_account": "6213941307516331",
            "bank_code": "ICBC",
            "bank_user_name": "XXX",
            "remitter_bank_account": "6213941307516332",
            "remitter_bank_code": "ICBC",
            "remitterbank_user_name": "XXX_1"

        }
        for i in range(0, count):
            temp["channel_key"] = "AUTO_" + get_random_num()
            temp["channel_order_no"] = get_random_num()
            temp["amount"] = amount
            temp["created_at"] = get_date(hour=-1)
            temp["finished_at"] = finish_at
            temp["remitter_bank_account"] = remitter_bank_account
            mode["data"].append(deepcopy(temp))
        self.update(api, mode)
        return mode

    def set_db_withdraw_status(self, merchant_key, status):
        if status == "success":
            status = 2
        elif status == "fail":
            status = 3
        elif status == "process":
            status = 1
        else:
            status = 1
        sql = "update withdraw set withdraw_status=%s, withdraw_finished_at='%s' where withdraw_merchant_key='%s'" % \
              (status, get_date(timezone=get_tz()), merchant_key)
        db.do_sql(sql)
        pass

    def set_db_withdraw_receipt_status(self, merchant_key, status, num=0, retry=False, terminated=False):
        if status == "success":
            status = 2
            channel = "cashfree_yomoyo1_withdraw"
            code = "SUCCESS"
            msg = "Details of transfer with transferId a927a2ecfdc64601bc76c1ede05f37a1"
        elif status == "fail" and retry is False and terminated is False:
            status = 3
            channel = "route_no_channel"
            code = "KN_RISK_CONTROL"
            msg = ""
        elif status == "fail" and retry is True and terminated is False:
            status = 3
            channel = "cashfree_yomoyo1_withdraw"
            code = "rejected"
            msg = "Payout failed. Reinitiate transfer after 30 min."
        elif status == "fail" and retry is False and terminated is True:
            status = 3
            channel = "cashfree_yomoyo1_withdraw"
            code = "rejected"
            msg = "autotest failed"
        else:
            status = 1
            channel = "cashfree_yomoyo1_withdraw"
            code = "processing"
            msg = ""

        sql1 = "select * from withdraw_receipt " \
               "where withdraw_receipt_merchant_key='%s' order by withdraw_receipt_id desc" % merchant_key
        resp = db.do_sql(sql1)
        if len(resp) == 0:
            return
        withdraw_receipt_id = resp[num]["withdraw_receipt_id"]
        sql2 = "update withdraw_receipt set " \
               "withdraw_receipt_status=%s, withdraw_receipt_finished_at='%s', withdraw_receipt_channel_name='%s', " \
               "withdraw_receipt_channel_resp_code='%s', withdraw_receipt_channel_resp_message='%s' " \
               "where withdraw_receipt_id='%s'" % (
                   status, get_date(timezone=get_tz()), channel, code, msg, withdraw_receipt_id)
        db.do_sql(sql2)
        pass

    def set_db_withdraw_not_exit(self, merchant_key):
        sql = "delete from withdraw where withdraw_merchant_key='%s'" % merchant_key
        db.do_sql(sql)
        pass

    def set_withdraw_callback_success(self, item_no):
        withdraw_order = get_withdraw_order_by_item_no(item_no + "w")
        withdraw_record = get_withdraw_record_by_item_no(item_no + "w")
        trade_no = withdraw_record[-1]["withdraw_record_trade_no"]
        amount = withdraw_order[0]["withdraw_order_amount"]
        url = gc.GRANT_URL + payment_callback_url
        data = {
            "from_system": "paysvr",
            "type": "withdraw",
            "key": get_random_str(15),
            "data": {
                "sign": "",
                "platform_code": "E20000",
                "platform_message": "OK",
                "channel_name": "razorpay_yomoyo_withdraw",
                "channel_code": "success",
                "channel_message": "OK",
                "finished_at": get_date(timezone=get_tz()),
                "channel_key": trade_no,
                "amount": amount,
                "status": 2,
                "merchant_key": item_no + "w",
                "trade_no": trade_no
            }
        }
        return Http.http_post(url, data)

    def set_withdraw_callback_reverse(self, item_no):
        withdraw_order = get_withdraw_order_by_item_no(item_no + "w")
        withdraw_record = get_withdraw_record_by_item_no(item_no + "w")
        trade_no = withdraw_record[-1]["withdraw_record_trade_no"]
        amount = withdraw_order[0]["withdraw_order_amount"]
        url = gc.GRANT_URL + payment_callback_url
        data = {
            "from_system": "paysvr",
            "type": "withdraw",
            "key": get_random_str(15),
            "data": {
                "status": 3,
                "channel_code": "KN_REVERSE_ORDER",
                "channel_message": "Refund",
                "platform_code": "E20001",
                "platform_message": "FAILED",
                "finished_at": get_date(timezone=get_tz()),
                "channel_key": trade_no,
                "amount": amount,
                "merchant_key": item_no + "w",
                "trade_no": trade_no,
                "sign": "",
                "channel_name": "razorpay_yomoyo_withdraw"
            }
        }
        return Http.http_post(url, data)

    def update_asset_offline_repay_info(self, account_number, side_account_number):
        api = "/asset/offline-repay-info"
        mode = {
            "code": 0,
            "message": "成功",
            "data": {
                "receive_card_no": "enc_03_2845502923004715008_044",
                "url_type": "QR_CODE",
                "url": "http://xxx.thabankcode.card1.qrcode.png",
                "repay_card_bank_name": "KIATNAKIN BANK",
                "repay_card_no": "enc_03_2845502923004715008_044",
            }
        }
        self.update(api, mode)
        pass

    def update_flow_query_withhold(self, amount, trade_date=None):
        if trade_date is None:
            trade_date = get_date(timezone=get_tz(gc.COUNTRY))
        api = "/flow-query/get-account-statement"
        trade_no = get_timestamp()
        account_number = get_random_num()
        side_account_number = get_random_num()
        mode = {
            "code": 0,
            "message": "成功",
            "data": [{
                "id": trade_no,
                "trade_no": trade_no,
                "trade_date": trade_date,
                "account_number": account_number,
                "side_account_number": side_account_number,
                "in_amount": amount,
                "out_amount": 0,
                "balance": 0,
                "loan_type": 1,
                "currency": "THA"
            }]
        }
        self.update(api, mode)
        return mode

    def update_withhold_query_success(self, item_no, pay_status=2, channel_name="auto_india_channel", amount=0,
                                      finished_at=get_date()):
        api = "/withhold/query"
        if amount == 0:
            withhold = get_withhold_by_item_no(item_no)
            amount = withhold[-1]["withhold_amount"]
        mode = {
            "code": 0,
            "message": "处理成功",
            "data": {"platform_code": "E20000",
                     "platform_message": "成功",
                     "channel_name": channel_name,
                     "channel_key": get_random_str(num=20),
                     "channel_code": "0000",
                     "channel_message": "成功",
                     "amount": amount,
                     "status": pay_status,
                     "finished_at": finished_at,
                     "payment_mode": "AUTOTEST"}}
        self.update(api, mode)
        pass

    def update_withold_auto_register_success(self, code=0, account_status="active"):
        api = "/withhold/autoRegister"
        mode = '''{
                       "code": %s,
                       "message": "开户成功",
                       "data": {
                            "platform_code": "E20000",
                            "platform_message": "auto mock error message",
                            "channel_name": "auto_test_collect_channel",
                            "channel_code": "0000",
                            "channel_message": "自动化开虚户成功",
                            "account_status": "%s",
                            "clabe": "",
                            "receiver_name": "YOMOYO BLOSSOM TECHNOLOGY PRIVATE LIMIT",
                            "receiver_vpa": "enc_03_3810939474465529856_444",
                            "receiver_vpa_qrcode": "data:image/png;base64,iVBORw0KGgozgoAAAAASUVORK5CYII=",
                            "receiver_bank": "" ,
                            "receiver_account": "" ,
                            "receiver_ifsc":""}}
                       // 状态，0、新建，1、处理中，2、成功，3、失败''' % (code, account_status)
        self.update(api, mode)
        pass

    def update_withold_auto_register_success_for_mex(self, code=0, account_status="active"):
        api = "/withhold/autoRegister"
        mode = '''{
                       "code": %s,
                       "message": "开户成功",
                       "data": {
                            "platform_code": "E20000",
                            "platform_message": "auto mock error message",
                            "channel_name": "auto_test_collect_channel",
                            "channel_code": "0000",
                            "channel_message": "自动化开虚户成功",
                            "account_status": "%s",
                            "clabe": "@id",
                            "expire_time": "%s",
                            "receiver_name": null,
                            "receiver_vpa": "",
                            "receiver_vpa_qrcode": null,
                            "receiver_bank": null,
                            "receiver_account": null,
                            "receiver_ifsc":null}}
                       // 状态，0、新建，1、处理中，2、成功，3、失败''' % (code, account_status, get_date())
        self.update(api, mode)
        pass

    def mock_global_withhold_refund(self, serial_no, pay_status=1):
        refund_request = get_refund_request(refund_request_withhold_serial_no=serial_no)[-1]
        api = "/withhold/refund"
        mode = {
            "code": 0,
            "message": "接收成功",
            "data": {
                "platform_code": "BF00232",
                "platform_message": "refund_apply_platform" + str(pay_status),
                "channel_name": "refund_apply_channel",
                "channel_key": "refund_" + get_random_str(10),
                "channel_code": "5123",
                "channel_message": "refund_apply_message" + str(pay_status),
                "amount": refund_request["refund_request_amount"],
                "status": pay_status,
                "finished_at": "1000-01-01 00:00:00"
            }
        }
        self.update(api, mode)
        pass

    def mock_global_withhold_refund_query(self, serial_no, pay_status=2):
        refund_request = get_refund_request(refund_request_withhold_serial_no=serial_no)[-1]
        api = "/withhold/refundQuery"
        mode = {
            "code": 0 if pay_status == 2 else 1,
            "message": "Transaction successful",
            "data": {
                "platform_code": "BF00232",
                "platform_message": "refund_query_platform_" + str(pay_status),
                "channel_name": "refund_query_channel",
                "merchant_key": refund_request["refund_request_serial_no"],
                "channel_key": "refund_" + get_random_str(10),
                "channel_code": "BF00232",
                "channel_message": "refund_query_message_" + str(pay_status),
                "amount": refund_request["refund_request_amount"],
                "status": pay_status,
                "finished_at": get_date(timezone=get_tz())
            }
        }
        self.update(api, mode)
        pass

    def mock_global_withdraw_query_for_rbiz(self, serial_no, status=2):
        refund_request = get_refund_request(refund_request_withhold_serial_no=serial_no)[-1]
        withdraw = get_withdraw(withdraw_ref_no=refund_request["refund_request_serial_no"])[-1]
        api = "/withdraw/query"
        mode = {
            "code": 0 if status == 2 else 1,
            "message": "交易",
            "data": {
                "platform_code": "E20000",
                "platform_message": "SUCCESS",
                "channel_name": "test_channel_withdraw",
                "channel_code": "KN_UNKNOWN_ERROR",
                "channel_message": "KN_UNKNOWN_ERROR",
                "amount": withdraw["withdraw_amount"],
                "channel_key": "withdraw_" + get_random_str(10),
                "created_at": get_date(timezone=get_tz()),
                "finished_at": get_date(timezone=get_tz()),
                "receiver_bank_code": "T00007",
                "status": status,
                "trade_no": "trade_no_" + get_random_str(10),
                "withdraw_type": "online",
                "trade_details": [
                    {
                        "channel_name": "test_channel_withdraw",
                        "channel_key": "SKX6000000002",
                        "channel_code": "KN_UNKNOWN_ERROR",
                        "channel_message": "KN_UNKNOWN_ERROR",
                        "trade_no": "trade_no_" + get_random_str(10),
                        "amount": withdraw["withdraw_amount"],
                        "status": status,
                        "finished_at": get_date(timezone=get_tz())
                    }
                ]
            }
        }
        self.update(api, mode)

    def mock_close_order_success(self):
        api = "/withhold/closeOrder"
        mode = {
            "code": 0,
            "message": "关闭订单成功",
            "data": {
                "platform_code": "E20010",
                "platform_message": "Order closed",
                "channel_name": "cashfree_whitekeys_sdk",
                "channel_code": "KN_MANUAL_CLOSE_ORDER",
                "channel_message": "ACTIVE"
            }
        }
        self.update(api, mode)

    def mock_close_order_fail(self):
        api = "/withhold/closeOrder"
        mode = {
            "code": 1,
            "message": "订单已经成为终态，关闭订单失败",
            "data": None
        }
        self.update(api, mode)

    def mock_close_order_500(self):
        api = "/withhold/closeOrder"
        mode = {"_res": {"status": 500}}
        self.update(api, mode)

    def mock_fox_delay_entry(self, asset_tran_list, period_list, percent):
        api = "/ph/fox/delay/entry"
        mode_temp = {"amount": 0, "period": 0}
        mode = {"code": 0,
                "data": {
                    "allow_defer": True,
                    "amount": 0,
                    "day": 7,
                    "detail": []},
                "message": "Success"
                }
        min_period = min(period_list)
        for i in period_list:
            detail = deepcopy(mode_temp)
            detail["period"] = i
            for asset_tran in asset_tran_list:
                if asset_tran["asset_tran_period"] == i:
                    if i == min_period and asset_tran["asset_tran_type"] == "fin_service":
                        detail["amount"] += asset_tran["asset_tran_total_amount"] * percent
                        mode["data"]["amount"] += asset_tran["asset_tran_total_amount"] * percent
                    if asset_tran["asset_tran_type"] == "repayinterest":
                        detail["amount"] += asset_tran["asset_tran_total_amount"]
                        mode["data"]["amount"] += asset_tran["asset_tran_total_amount"]
                    if asset_tran["asset_tran_type"] == "lateinterest":
                        detail["amount"] += asset_tran["asset_tran_balance_amount"]
                        mode["data"]["amount"] += asset_tran["asset_tran_balance_amount"]
            mode["data"]["detail"].append(detail)
        self.update(api, mode)
