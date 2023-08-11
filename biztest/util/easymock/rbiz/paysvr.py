# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import *
from biztest.config.rbiz.url_config import *
from biztest.config.rbiz.params_config import mock_query_protocol_channels_mode, mock_bind_sms_mode
from biztest.util.tools.tools import get_random_num


class PaysvrMock(Easymock):
    query_protocol_channels_mode = mock_query_protocol_channels_mode
    bind_sms_mode = mock_bind_sms_mode
    query_protocol_channels_path = mock_paysvr_query_protocol_channels_path
    bind_sms_path = mock_paysvr_bind_sms_path

    def update_query_protocol_channels_bind_sms(self):
        self.query_protocol_channels_mode['data'][0]['data'][0]['bind_status'] = "-1"
        self.query_protocol_channels_mode['data'][0]['data'][0]['protocol_info'] = None
        self.update(self.query_protocol_channels_path, self.query_protocol_channels_mode)

    def update_query_protocol_channels_not_bind_sms(self, channel_name='baofoo_tq4_protocol'):
        self.query_protocol_channels_mode['data'][0]['data'][0]['bind_status'] = "1"
        self.query_protocol_channels_mode['data'][0]['data'][0]['channel_name'] = channel_name
        self.update(self.query_protocol_channels_path, self.query_protocol_channels_mode)

    def update_bind_sms_success(self):
        self.update(self.bind_sms_path, self.bind_sms_mode)

    def update_auto_pay_withhold_success(self, channel_name='baidu_tq3_quick'):
        api = '/withhold/autoPay'
        mode = {
            "code": 0,
            "message": "交易成功",
            "data": {
                "channel_code": "2000",
                "channel_msg": "交易成功",
                "code": "E20000",
                "msg": "交易成功",
                "error_code": "E20000",
                "channel_message": "交易成功",
                "need_bind": 1,
                "need_sms": 0,
                "amount": 2401,
                "channel": channel_name,
                "channel_key": "@id",
                "created_at": "@now",
                "finished_at": "@now",
                "card_num_encrypt": "enc_03_2993609813722139648_151",
                "id_num_encrypt": "enc_02_2993585069627017216_601",
                "username_encrypt": "enc_04_283572470_136",
                "mobile_encrypt": "enc_01_36299261470_554",
                "balance_not_enough": 0,
                "withhold_receipt_list": [
                    {
                        "channel": channel_name,
                        "status": 2,
                        "channel_key": "@id",
                        "channel_code": "2000",
                        "channel_message": "交易成功"
                    }
                ]
            },
            "sign": "4a7cd37c07c0bb3f9df48d0a833e3922"
        }
        str_mode2 = json.dumps(mode)
        self.update(api, str(str_mode2))

    def update_auto_pay_withhold_fail(self, message='自动化失败'):
        # E20004 为余额不足的特殊code 不会切到我方代扣
        api = '/withhold/autoPay'
        mode = {
            "code": 1,
            "message": "交易失败",
            "data": {
                "channel_code": "64",
                "channel_msg": message,
                "code": "E21114",
                "msg": message,
                "error_code": "E21114",
                "channel_message": message,
                "need_bind": 0,
                "need_sms": 0,
                "amount": 100462,
                "channel": "cpcn_tq_withhold",
                "channel_key": "RBIZ" + get_random_num(),
                "created_at": "@now",
                "finished_at": "@now",
                "card_num_encrypt": "enc_03_37398880_862",
                "id_num_encrypt": "enc_02_37398840_853",
                "username_encrypt": "enc_04_446560_696",
                "mobile_encrypt": "enc_01_37398870_599",
                "balance_not_enough": 0,
                "withhold_receipt_list": [
                    {
                        "channel": "cpcn_tq_withhold",
                        "status": 3,
                        "channel_key": "RBIZ" + get_random_num(),
                        "channel_code": "64",
                        "channel_message": message
                    }
                ]
            },
            "sign": "ba3ffc19549e0e10d4c045a3fddb29f1"
        }
        str_mode2 = json.dumps(mode)
        self.update(api, str(str_mode2))

    def update_auto_pay_withhold_process(self, message='自动化处理中'):
        api = '/withhold/autoPay'
        mode = {
            "code": 2,
            "message": "交易处理中",
            "data": {
                "channel_code": "64",
                "channel_msg": message,
                "code": "E21114",
                "msg": message,
                "error_code": "E21114",
                "channel_message": message,
                "need_bind": 0,
                "need_sms": 0,
                "amount": 100462,
                "channel": "cpcn_tq_withhold",
                "channel_key": "RBIZ" + get_random_num(),
                "created_at": "@now",
                "finished_at": "@now",
                "card_num_encrypt": "enc_03_37398880_862",
                "id_num_encrypt": "enc_02_37398840_853",
                "username_encrypt": "enc_04_446560_696",
                "mobile_encrypt": "enc_01_37398870_599",
                "balance_not_enough": 0,
                "withhold_receipt_list": [
                    {
                        "channel": "cpcn_tq_withhold",
                        "status": 1,
                        "channel_key": "RBIZ" + get_random_num(),
                        "channel_code": "64",
                        "channel_message": message
                    }
                ]
            },
            "sign": "ba3ffc19549e0e10d4c045a3fddb29f1"
        }
        str_mode2 = json.dumps(mode)
        self.update(api, str(str_mode2))

    def update_withhold_refund(self, merchant_key, amount, pay_status="success"):
        api = "/withhold/refund"
        mode = {
            "code": 0,
            "message": "接收成功",
            "request": {
                "amount": amount,
                "state": pay_status,
                "sign": "f945285abf18f9a720a2c2019266d21a",
                "trade_type": "refund",
                "merchant_id": 4,
                "merchant_key": merchant_key,
                "channel_name": "baofoo_tq5",
                "channel_key": "@id",
                "channel_code": "5123",
                "channel_message": "自动化测试",
                "finished_at": "@datetime"
            }
        }
        str_mode2 = json.dumps(mode)
        self.update(api, str(str_mode2))

    def update_withhold_refund_query(self, amount, pay_status="success", merchant_key=""):
        api = "/withhold/refundQuery"
        mode = {
            "code": 1,
            "message": "auto test",
            "data": {
                "channel_code": "BF00232",
                "channel_message": "autotest" + str(pay_status),
                "code": "0000",
                "msg": "autotest msg",
                "error_code": "E20000",
                "trade_type": "refund",
                "merchant_id": 4,
                "merchant_key": merchant_key,
                "channel_name": "baofoo_tq5_withhold",
                "channel_key": "DSQ@id",
                "amount": amount,
                "finished_at": "@now",
                "state": pay_status
            },
            "sign": "743d003f1c7a08ca01f9cb4ce0261068"
        }
        str_mode2 = json.dumps(mode)
        self.update(api, str(str_mode2))

    def update_withhold_query(self, pay_status=2, channel_name='baidu_tq3_quick', msg='自动化测试'):
        api = mock_paysvr_transaction_query_path
        mode = {
            "code": 0,
            "message": msg,
            "data": {
                "channel_code": "BF00232",
                "channel_msg": msg,
                "code": "0000",
                "msg": "余额不足",
                "error_code": "E20000",
                "channel_message": msg,
                "need_bind": -1,
                "need_sms": -1,
                "amount": 26666,
                "channel": channel_name,
                "channel_key": "DSQ@id",
                "created_at": "@now",
                "finished_at": "@now",
                "balance_not_enough": 0,
                "withhold_receipt_list": [{
                    "channel": channel_name,
                    "status": pay_status,
                    "channel_key": "DSQ@id",
                    "channel_code": "BF00232",
                    "channel_message": msg
                }]
            },
            "sign": "743d003f1c7a08ca01f9cb4ce0261068"
        }
        str_mode2 = json.dumps(mode)
        self.update(api, str(str_mode2))

    def update_withdraw_query(self, amount, pay_status=2, receiver_name="", receiver_account="", receiver_id=""):
        api = "/withdraw/query"
        mode = {
            "code": 0,
            "message": "交易成功",
            "data": {
                "account": "qsq_cpcn_tq_quick",
                "amount": amount,
                "state": pay_status,
                "channel_code": "0000",
                "channel_msg": "代付成功",
                "code": "E20000",
                "msg": "代付成功",
                "error_code": "E20000",
                "channel_message": "代付成功",
                "channel_key": "withdraw@id",
                "created_at": "@now",
                "finished_at": "@now",
                "receiver_type": 1,
                "receiver_name_encrypt": receiver_name,
                "receiver_account_encrypt": receiver_account,
                "receiver_identity_encrypt": receiver_id,
                "receiver_bankcode": "ICBC",
                "withdraw_receipt_list": [{
                    "status": 2,
                    "channel_name": "qsq_cpcn_tq_quick",
                    "channel_key": "withdraw@id",
                    "finished_at": "@now",
                    "trade_no": "trade@id"
                }]
            },
            "sign": "ebfc13c604469cf8384aa8f3935e2be6"
        }
        str_mode2 = json.dumps(mode)
        self.update(api, str(str_mode2))

    def update_withhold_bind_query_success(self, channel_name='baofoo_tq4_protocol'):
        api = '/withhold/bindCheck'
        mode = {
            "code": 0,
            "message": "成功",
            "data": {
                "need_sms": 1,
                "need_bind": 1,
                "channel_name": channel_name
            }
        }
        str_mode2 = json.dumps(mode)
        self.update(api, str(str_mode2))
