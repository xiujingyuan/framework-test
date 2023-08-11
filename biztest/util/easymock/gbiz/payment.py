# -*- coding: utf-8 -*-
from copy import deepcopy

from biztest.function.gbiz.gbiz_db_function import get_withdraw_record_by_item_no, get_withdraw_order_by_item_no
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import get_date


class PaymentMock(Easymock):
    def query_protocol_channels_need_bind(self, bind_status='-1', protocol_info='', sign_company='hq'):
        api = "/channel/queryProtocolChannels"
        mode = {
                  "code": 0,
                  "message": "查询代扣可用通道成功",
                  "data": [{
                    "data": [
                      {
                        "channel_name": "baofoo_tq_protocol",
                        "product_type": "protocol",
                        "bind_status": bind_status,
                        "protocol_info": protocol_info
                      }
                    ],
                    "sign_company": sign_company
                  }]
                }
        self.update(api, mode)

    def query_protocol_channels_need_bind_for_zhongbang_zhongji(self):
        api = "/channel/queryProtocolChannels"
        mode = '''{
                "code": 0,
                "message": "查询代扣可用通道成功",
                "data": [
                    {
                        "data": [
                            {
                                "channel_name": "baofoo_tq_protocol",
                                "product_type": "protocol",
                                "bind_status": "-1"
                            },
                            {
                                "channel_name": "hq_cpcn_tq_quick",
                                "product_type": "quick",
                                "bind_status": "-1"
                              }
                        ],
                        "sign_company": "qjhy"
                    }
                ]
            }'''
        self.update(api, mode)

    def query_protocol_channels_need_bind_for_zhongbang_zhongji_rl(self):
        api = "/channel/queryProtocolChannels"
        mode = {
            "code": 0,
            "message": "查询代扣可用通道成功",
            "data": [
                {
                    "data": [
                        {
                            "channel_name": "baofoo_hy_protocol",
                            "product_type": "protocol",
                            "bind_status": "-1"
                        }
                    ],
                    "sign_company": "hy"
                }
            ]
        }
        self.update(api, mode)


    def query_protocol_channels_get_protocol_info(self):
        '''
        新增加字段protocol_info，目前只有众邦中际在用这个协议号
        '''
        api = "/channel/queryProtocolChannels"
        mode = '''{
                    "code": 0,
                    "message": "查询代扣可用通道成功",
                    "data": [
                        {
                            "data": [
                                {
                                    "channel_name": "baofoo_tq_protocol",
                                    "product_type": "protocol",
                                    "bind_status": "1",
                                    "protocol_info": "T@id"
                                },
                                {
                                    "channel_name": "hq_cpcn_tq_quick",
                                    "product_type": "quick",
                                    "bind_status": "-1"
                              }
                            ],
                            "sign_company": "qjhy"
                        }
                    ]
                }'''
        self.update(api, mode)

    def query_protocol_channels_not_need_bind(self, bind_status="-1"):
        api = "/channel/queryProtocolChannels"
        mode = {
                  "code": 0,
                  "message": "查询代扣可用通道成功",
                  "data": [{
                    "data": [{
                        "channel_name": "hq_baidu_tq3_quick",
                        "product_type": "quick",
                        "bind_status": "1"
                      },
                      {
                        "channel_name": "hq_cpcn_tq_quick",
                        "product_type": "quick",
                        "bind_status": bind_status
                      }
                    ],
                    "sign_company": "hq"
                  }]
                }
        self.update(api, mode)

    def bind_success(self, four_element):
        api = "/withhold/bind"
        mode = '''{
            "code": 0,
            "message": "绑卡成功",
            "data": {
                "code": "E20000",
                "msg": "交易成功",
                "channel_message": "交易成功",
                "channel_name": function({_req}){return _req.body.channel_name},
                "card_status": 4,
                "bank_name": "中国农业银行",
                "bank_code": "ABC",
                "card_num_encrypt": "%s",
                "id_num_encrypt": "%s",
                "username_encrypt": "%s",
                "mobile_encrypt": "%s",
                "protocol_info": "xy@id",
            }
        }''' % (four_element['data']['bank_code_encrypt'],
                four_element['data']['id_number_encrypt'],
                four_element['data']['user_name_encrypt'],
                four_element['data']['phone_number_encrypt'])
        self.update(api, mode)

    def bind_fail(self):
        api = "/withhold/bind"
        mode = '''{
            "code": 1,
            "message": "绑卡失败",
            "data": {
                "channel_code": "3999",
                "channel_msg": "验证码错误或过期",
                "code": "E20020",
                "msg": "短信验证码输入有误",
                "channel_message": "短信验证码输入有误",
                "channel_name": function({_req}){return _req.body.channel_name},
                "card_status": 4,
                "bank_name": "中国农业银行",
                "bank_code": "ABC",
                "channel_error": "验证码错误或过期"
            }
        }'''
        self.update(api, mode)

    def auto_bind_sms_success(self):
        api = "/withhold/autoBindSms"
        mode = {
            "code": 0,
            "message": "绑卡申请成功",
            "data": {
                "channel_code": "0000",
                "channel_msg": "交易成功。",
                "code": "E20000",
                "msg": "交易成功",
                "channel_message": "交易成功",
                "channel_name": "hq_baidu_tq3_quick",
                "verify_seq": "@id"
            }
        }
        self.update(api, mode)

    def auto_bind_sms_fail(self):
        api = "/withhold/autoBindSms"
        mode = {
            "code": 1,
            "message": "绑卡申请失败",
            "data": {
                "channel_code": "00202005",
                "channel_msg": "银行卡号输入有误,错误码00070004",
                "code": "E20107",
                "msg": "无效卡号，请核对后重新输入",
                "channel_message": "无效卡号，请核对后重新输入",
                "channel_name": "hq_baidu_tq3_quick"
            }
        }
        self.update(api, mode)

    def update_withdraw_balance_enough(self, amount=200000000):
        api = "/withdraw/balance"
        mode = {
            "code": 0,
            "message": "",
            "data": {
                "total": amount,
                "available": amount
            }
        }
        self.update(api, mode)

    def update_withdraw_apply_success(self):
        api = "/withdraw/autoWithdraw"
        mode = '''{
            "code": 2,
            "message": "订单交易正在处理中！",
            "data": {
                "account": function({_req}){return _req.body.account},
                "amount": function({_req}){return _req.body.amount},
                "code": "E99997",
                "msg": "操作处理中",
                "channel_message": "操作处理中",
                "receiver_type": 3,
                "receiver_name": "通融小贷",
                "receiver_name_encrypt": function({_req}){return _req.body.receiver_name_encrypt},
                "receiver_account": "53079",
                "receiver_account_encrypt": function({_req}){return _req.body.receiver_account_encrypt},
                "receiver_identity": "0000000000000",
                "receiver_identity_encrypt": function({_req}){return _req.body.receiver_identity_encrypt},
                "receiver_bank_code": "JNBANK",
                "channel_key": "1947bb99a4ca4fa686c462b0949f6c98",
                "withdraw_receipt_list": [
                    {
                        "status": 0,
                        "channel_name": function({_req}){return _req.body.account},
                        "channel_key": "1947bb99a4ca4fa686c462b0949f6c98",
                        "finished_at": "1000-01-01 00:00:00",
                        "trade_no": function({_req}){return _req.body.trade_no}
                    }
                ]
            }
        }'''
        self.update(api, mode)

    def update_withdraw_apply_risk_fail(self):
        api = "/withdraw/autoWithdraw"
        mode = '''{
            "code": 1,
            "message": "风控拦截，疑似重复代付",
            "data": null
            }
            '''
        self.update(api, mode)

    def update_withdraw_apply_fail(self):
        api = "/withdraw/autoWithdraw"
        mode = '''{
            "code": 2,
            "message": "脱敏服务异常",
            "data": null
            }
            '''
        self.update(api, mode)

    def update_withdraw_query_status(self, merchent_key, merchant_status="process", receipt_status="process",
                                     retry=False, platform_code=None, platform_message=None):
        api = "/withdraw/query"
        order_info = get_withdraw_order_by_item_no(merchent_key)
        record_info = get_withdraw_record_by_item_no(merchent_key)
        amount = order_info[0]["withdraw_order_amount"]
        data = {
            "code": 0,
            "message": "处理成功",
            "data": {
                "account": "test_channel",
                "amount": amount,
                "status": 2,
                "channel_code": "0000",
                "channel_msg": "成功",
                "code": "E20000",
                "msg": "成功",
                "error_code": None,
                "channel_message": "成功",
                "channel_key": "%s",
                "created_at": get_date(),
                "finished_at": get_date(),
                "withdraw_receipt_list": []}}
        data["data"]["channel_key"] = record_info[-1]["withdraw_record_channel_key"]
        for record in record_info:
            temp = dict()
            temp["channel_name"] = "test_channel"
            temp["channel_key"] = record["withdraw_record_channel_key"]
            temp["channel_resp_code"] = record["withdraw_record_resp_code"]
            temp["channel_resp_message"] = record["withdraw_record_resp_message"]
            temp["trade_no"] = record["withdraw_record_trade_no"]
            temp["status"] = 3
            temp["finished_at"] = record["withdraw_record_finish_at"]
            data["data"]["withdraw_receipt_list"].append(deepcopy(temp))
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
            data["data"]["code"] = platform_code if platform_code is not None else "E20000"
            data["data"]["msg"] = platform_message if platform_message is not None else "自动化测试成功"
            data["data"]["withdraw_receipt_list"][-1]["status"] = 2
        elif receipt_status == "fail" and retry is True:
            data["data"]["code"] = platform_code if platform_code is not None else "FAILED"
            data["data"]["msg"] = platform_message if platform_message is not None else "放款失败"
            data["data"]["withdraw_receipt_list"][-1]["status"] = 3
        elif receipt_status == "fail" and retry is False:
            data["data"]["code"] = platform_code if platform_code is not None else "KN_RISK_CONTROL"
            data["data"]["msg"] = platform_message if platform_message is not None else ""
            data["data"]["withdraw_receipt_list"][-1]["status"] = 3
        elif receipt_status == "process":
            data["data"]["code"] = platform_code if platform_code is not None else ""
            data["data"]["msg"] = platform_message if platform_message is not None else ""
            data["data"]["withdraw_receipt_list"][-1]["status"] = 1
        elif receipt_status == "fail_terminated":
            data["data"]["code"] = platform_code if platform_code is not None else "E20167"
            data["data"]["msg"] = platform_message if platform_message is not None else "风控拦截，疑似重复代付"
            data["data"]["withdraw_receipt_list"][-1]["status"] = 3
        data["data"]["withdraw_receipt_list"][-1]["finished_at"] = get_date()
        self.update(api, data)
