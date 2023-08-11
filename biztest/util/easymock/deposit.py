# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
import random


class DepositMock(Easymock):
    # 白名单注册接口#############################################################
    def update_memeber_register_success(self):
        api = "/member/register"
        mode = {"code": 0, "message": "请求成功", "data": None}
        self.update(api, mode)

    def update_memeber_register_fail(self):
        api = "/member/register"
        mode = {"code": 1, "message": "资金渠道不存在，请查证！", "data": None}
        self.update(api, mode)

    # 白名单注册查询接口#############################################################
    def update_member_query_success(self):
        api = "/member/query"
        mode = '{"code":0,"message":"请求成功","data":{' \
               '"status":0,' \
               '"mem_acct_no":function({_req}){return _req.body.data.mem_acct_no},' \
               '"mem_name":function({_req}){return _req.body.data.mem_name},' \
               '"mem_cert_no":function({_req}){return _req.body.data.mem_cert_no},' \
               '"mem_mobile":function({_req}){return _req.body.data.mem_mobile},}}'
        self.update(api, mode)

    def update_member_query_fail(self):
        api = "/member/query"
        mode = {"code": 0, "message": "0TB320307615白名单账户已存在", "data": {"status": 1}}
        self.update(api, mode)

    def update_member_query_process(self):
        api = "/member/query"
        mode = {"code": 0, "message": "该用户正在添加中", "data": {"status": 2}}
        self.update(api, mode)

    def update_member_query_no_member(self):
        api = "/member/query"
        mode = {"code": 0, "message": "未找到该用户记录", "data": {"status": 3}}
        self.update(api, mode)

    # 放款接口#############################################################
    def update_trade_loan_success(self):
        api = "/trade/loan"
        mode = '{"code":0,"message":"收单成功","data":{"order_no":function({_req}){return _req.body.data.order_no}}}'
        self.update(api, mode)

    def update_trade_loan_fail(self):
        api = "/trade/loan"
        mode = '{"code":1,"message":"四要素验证不通过","data":{"order_no":function({_req}){return _req.body.data.order_no}}}'
        self.update(api, mode)

    def update_trade_loan_risk_trade(self):
        api = "/trade/loan"
        mode = '{"code":1,"message":"疑似风险交易","data":{"order_no":function({_req}){return _req.body.data.order_no}}}'
        self.update(api, mode)

    # 放款查询接口#############################################################
    def update_trade_query(self, order_no, trade_no, amount, type):
        api = "/trade/query"
        if type == "success":
            status, memo = 2, "交易成功"
        elif type == "fail":
            status, memo = 3, "交易失败"
        elif type == "final_fail":
            status, memo = 3, "核心出金处理错误"
        else:
            status, memo = 2, "交易成功"
        mode = """{
            "code": 0,
            "message": "订单查询成功",
            "data": {
                "order_no": "%s",
                "status": %s,
                "type": 2,
                "finished_at": function(){var timestamp=new Date().getTime();return timestamp;},
                "trades": [
                    {
                        "trade_no": "%s",
                        "status": %s,
                        "finished_at": function(){var timestamp=new Date().getTime();return timestamp;},
                        "memo": "交易成功",
                        "amount": %s
                    }
                ],
                "amount": %s,
                "memo": "%s"
            }
        }""" % (order_no, status, trade_no, status, amount, amount, memo)
        self.update(api, mode)

    def update_trade_query_success(self, item_no, amount, card_no, id_no):
        api = "/trade/query"
        mode = '{"code":0,"message":"","data":{"order_no":function({_req}){return _req.body.data.order_no},\
                "status":2,"finished_at":function(){var timestamp=new Date().getTime();return timestamp;},\
                "trades":[{"trade_no":"%s","status":2,\
                "finished_at":function(){var timestamp=new Date().getTime();return timestamp;},\
                "memo":"交易成功","amount":%s00}],\
                "amount":%s00,"memo":"交易成功","channel_code":"tongrongmiyang",\
                "mem_acct_no":"%s", \
                "mem_name":"enc_04_1294450_000",\
                "mem_cert_no":"%s",\
                "mem_mobile":"enc_01_2630683215241152512_009"}}//status：0-收单1-交易中2-交易成功3-交易失败6-订单不存在' \
               % (item_no, amount, amount, card_no, id_no)
        self.update(api, mode)

    def update_trade_query_failed_final(self, item_no, amount, card_no, id_no):
        api = "/trade/query"
        mode = '{"code":0,"message":"","data":{"order_no":function({_req}){return _req.body.data.order_no},\
                "status":3,"finished_at":function(){var timestamp=new Date().getTime();return timestamp;},\
                "trades":[{"trade_no":"%s","status":3,\
                "finished_at":function(){var timestamp=new Date().getTime();return timestamp;},\
                "memo":"此笔资产交易最终失败","amount":%s00}],\
                "amount":%s00,"memo":"此笔资产交易最终失败","channel_code":"tongrongmiyang",\
                "mem_acct_no":"%s",\
                "mem_name":"enc_04_1294450_000",\
                "mem_cert_no":"%s",\
                "mem_mobile":"enc_01_2630683215241152512_009"}}//status：0-收单1-交易中2-交易成功3-交易失败6-订单不存在'\
                % (item_no, amount, amount, card_no, id_no)
        self.update(api, mode)

    def update_trade_query_failed_retry(self, item_no, amount, card_no, id_no):
        api = "/trade/query"
        mode = '{"code":0,"message":"","data":{"order_no":function({_req}){return _req.body.data.order_no},\
                "status":3,"finished_at":function(){var timestamp=new Date().getTime();return timestamp;},\
                "trades":[{"trade_no":"%s","status":3,\
                "finished_at":function(){var timestamp=new Date().getTime();return timestamp;},\
                "memo":"对手行状态异常，不能发起此交易。","amount":%s00}],\
                "amount":%s00,"memo":"对手行状态异常，不能发起此交易。","channel_code":"tongrongmiyang",\
                "mem_acct_no":"%s",\
                "mem_name":"enc_04_1294450_000",\
                "mem_cert_no":"%s",\
                "mem_mobile":"enc_01_2630683215241152512_009"}}//status：0-收单1-交易中2-交易成功3-交易失败6-订单不存在'\
                % (item_no, amount, amount, card_no, id_no)
        self.update(api, mode)

    def update_trade_query_failed_delay(self, fourelement):
        api = "/trade/query"
        mode = '{"code":0,"message":"","data":{"order_no":function({_req}){return _req.body.data.order_no},\
                "status":3,"finished_at":function(){var timestamp=new Date().getTime();return timestamp;},\
                "trades":[{"trade_no":"xxxxxxxxxxxxxxxxxxxx","status":3,\
                "finished_at":function(){var timestamp=new Date().getTime();return timestamp;},\
                "memo":"账户可提现余额不足","amount":400000}],\
                "amount":400000,"memo":"账户可提现余额不足","channel_code":"tongrongmiyang",\
                "mem_acct_no":"%s",\
                "mem_name":"enc_04_1294450_000",\
                "mem_cert_no":"%s",\
                "mem_mobile":"enc_01_2630683215241152512_009"}}//status：0-收单1-交易中2-交易成功3-交易失败6-订单不存在'\
                % (fourelement['data']['bank_code_encrypt'], fourelement['data']['id_number_encrypt'])
        self.update(api, mode)

    def update_trade_query_failed_terminate(self, fourelement):
        api = "/trade/query"
        mode = '{"code":0,"message":"","data":{"order_no":function({_req}){return _req.body.data.order_no},\
                "status":3,"finished_at":function(){var timestamp=new Date().getTime();return timestamp;},\
                "trades":[{"trade_no":"xxxxxxxxxxxxxxxxxxxx","status":3,\
                "finished_at":function(){var timestamp=new Date().getTime();return timestamp;},\
                "memo":"疑似风险交易","amount":400000}],\
                "amount":400000,"memo":"疑似风险交易","channel_code":"tongrongmiyang",\
                "mem_acct_no":"%s",\
                "mem_name":"enc_04_1294450_000",\
                "mem_cert_no":"%s",\
                "mem_mobile":"enc_01_2630683215241152512_009"}}//status：0-收单1-交易中2-交易成功3-交易失败6-订单不存在'\
                % (fourelement['data']['bank_code_encrypt'], fourelement['data']['id_number_encrypt'])
        self.update(api, mode)

    def update_trade_query_failed_other_msg(self, item_no, amount, card_no, id_no):
        api = "/trade/query"
        mode = '{"code":0,"message":"","data":{"order_no":function({_req}){return _req.body.data.order_no},\
                "status":3,"finished_at":function(){var timestamp=new Date().getTime();return timestamp;},\
                "trades":[{"trade_no":"%s","status":3,\
                "finished_at":function(){var timestamp=new Date().getTime();return timestamp;},\
                "memo":"test1234","amount":%s00}],\
                "amount":%s00,"memo":"test1234","channel_code":"tongrongmiyang",\
                "mem_acct_no":"%s",\
                "mem_name":"enc_04_1294450_000",\
                "mem_cert_no":"%s",\
                "mem_mobile":"enc_01_2630683215241152512_009"}}//status：0-收单1-交易中2-交易成功3-交易失败6-订单不存在'\
                % (item_no, amount, amount, card_no, id_no)
        self.update(api, mode)

    def update_trade_query_not_exist(self):
        api = "/trade/query"
        mode = '{"code":0,"message":"","data":{"order_no":function({_req}){return _req.body.data.order_no},\
                "status":6,"amount":0,"memo":"订单不存在"}}//status：0-收单1-交易中2-交易成功3-交易失败6-订单不存在'
        self.update(api, mode)

    def update_trade_query_process(self):
        api = "/trade/query"
        mode = '{"code":0,"message":"交易中","data":{"order_no":function({_req}){return _req.body.data.order_no},\
                "status":1,"amount":0}}//status：0-收单1-交易中2-交易成功3-交易失败6-订单不存在'
        self.update(api, mode)

    def update_trade_query_error_code(self):
        api = "/trade/query"
        mode = '{"code":%s,"message":"交易中","data":{"order_no":function({_req}){return _req.body.data.order_no},\
                "status":1,"amount":0}}//status：0-收单1-交易中2-交易成功3-交易失败6-订单不存在' % random.choice([1, 2])
        self.update(api, mode)

    # 额度查询接口#############################################################
    def update_balance_enough(self):
        api = "/account/query-balance"
        mode = {
              "code": 0,
              "message": "查询成功",
              "data": {
                "channel_code": "tongrongmiyang",
                "use_balance": 300000000
              }
            }
        self.update(api, mode)

    def update_balance_not_enough(self):
        api = "/account/query-balance"
        mode = {
              "code": 0,
              "message": "查询成功",
              "data": {
                "channel_code": "tongrongmiyang",
                "use_balance": 10
              }
            }
        self.update(api, mode)

    # 转账接口#############################################################
    def update_transfer_success(self):
        api = "/trade/transfer"
        mode = '{"code":0,"message":"收单成功","data":{"order_no":function({_req}){return _req.body.data.itemNo}}}'
        self.update(api, mode)

    def update_transfer_failed(self):
        api = "/trade/transfer"
        mode = '{"code":1,"message":"收单成功","data":{"order_no":function({_req}){return _req.body.data.itemNo}}}'
        self.update(api, mode)

    # 转账查询接口#############################################################
    def update_transfer_query_success(self):
        api = "/trade/query"
        mode = '''{
            "code": 0,
            "message": "订单查询成功",
            "data": {
                "order_no": function({_req}) {return _req.body.data.order_no},
                "status": 2,
                "type": 2,
                "finished_at": function() {var timestamp = new Date().getTime();return timestamp;},
                "trades": [{
                    "trade_no": function({_req}) {return _req.body.data.itemNo},
                    "status": 2,
                    "finished_at": function() {var timestamp = new Date().getTime();return timestamp;},
                    "memo": "交易成功",
                    "amount": function({_req}) {return _req.body.data.amount}
                    }],
                "amount": function({_req}) {return _req.body.data.amount},
                "memo": "交易成功"
                }
            } //status：0-收单1-交易中2-交易成功3-交易失败6-订单不存在'''
        self.update(api, mode)

    def update_transfer_query_failed(self):
        api = "/trade/query"
        mode = '''{
            "code": 0,
            "message": "订单查询成功",
            "data": {
                "order_no": function({_req}) {return _req.body.data.order_no},
                "status": 3,
                "type": 2,
                "finished_at": function() {var timestamp = new Date().getTime();return timestamp;},
                "trades": [{
                    "trade_no": function({_req}) {return _req.body.data.itemNo},
                    "status": 3,
                    "finished_at": function() {var timestamp = new Date().getTime();return timestamp;},
                    "memo": "交易成功",
                    "amount": function({_req}) {return _req.body.data.amount}
                    }],
                "amount": function({_req}) {return _req.body.data.amount},
                "memo": "交易成功"
                }
            } //status：0-收单1-交易中2-交易成功3-交易失败6-订单不存在'''
        self.update(api, mode)

    def update_transfer_query_failed_retry(self):
        api = "/trade/query"
        mode = '''{
            "code": 0,
            "message": "订单查询成功",
            "data": {
                "order_no": function({_req}) {return _req.body.data.order_no},
                "status": 1,
                "type": 2,
                "finished_at": function() {var timestamp = new Date().getTime();return timestamp;},
                "trades": [{
                    "trade_no": function({_req}) {return _req.body.data.itemNo},
                    "status": 1,
                    "finished_at": function() {var timestamp = new Date().getTime();return timestamp;},
                    "memo": "交易成功",
                    "amount": function({_req}) {return _req.body.data.amount}
                    }],
                "amount": function({_req}) {return _req.body.data.amount},
                "memo": "交易成功"
                }
            } //status：0-收单1-交易中2-交易成功3-交易失败6-订单不存在'''
        self.update(api, mode)

    def update_transfer_query_process(self):
        api = "/trade/query"
        mode = '{"code":0,"message":"交易中","data":{"order_no":function({_req}){return _req.body.data.itemNo},' \
               '"status":1,"amount":0}}'
        self.update(api, mode)


if __name__ == "__main__":
    jining = DepositMock('carltonliu', 'lx19891115', "5dddb8bdd1784d36471d5f78")
    jining.update_transfer_query_success()
    # jining.update_trade_loan_risk_trade()
    # jining.update_trade_query_not_exist()
    # jining.update_trade_query_process()
    # mode = "{\n  \"code\": 0,\n  \"message\": \"收单成功\",\n  \"data\": {\n    \"order_no\": function({\n      _req\n
    # }) {\n      return _req.body.data.itemNo\n    }\n  }\n}"
    # print(mode)
    # mode = mode.replace(' ', '')
    # mode = mode.replace('\n', '')
    # print(str(mode))
    print(random.choice([0, 1]))
