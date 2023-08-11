# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class RepayZhongbangZhongjiMock(Easymock):
    def zhongbang_zhongji_normal_repay(self,  repay_status=1):
        """
        众邦中际正常还款接口
        partner_repay_no字段需要与请求的一致
        这个接口不会校验返回的金额等，查询接口校验即可
        repay_status 还款状态
                0: 还款中 ----调用代扣查询接口
                1:还款成功 ----调用代扣查询接口
                2：还款失败 -----如果是2状态，直接就代扣失败
        """

        api = "/zhongbang/zhongbang_zhongji/NormRpyOnTm"
        mode = '''{
                  "code": 0,
                  "message": "message",
                  "data": {
                    "code": "000000",
                    "msg": "外层msg",
                    "result": {
                      "repay_status": "%s",
                      "fail_msg": "fail_msg",
                      "partner_repay_no": function({
                        _req
                      }) {
                        return _req.body.requestNo
                      },
                      "actual_repay_amount": 567.33,
                      "repay_principal": 479.71,
                      "repay_interest": 45.00,
                      "repay_penalty_amount": 0,
                      "repay_intefine": 0,
                      "repay_fee": 0
                    }
                  }
                }''' % (repay_status)
        self.update(api, mode)

    def zhongbang_zhongji_repay_query(self, msg='success', repay_status=1, repay_amt=438.01):
        """
        众邦中际还款结果查询接口
        repay_status 还款状态
            0: 还款中------重新查询
            1：还款成功
            2：还款失败
        """
        api = "/zhongbang/zhongbang_zhongji/NewRpyStsQry"
        mode = '''{
                  "code": 0,
                  "message": "message",
                  "data": {
                    "code": "000000",
                    "msg": "%s",
                    "result": {
                      "repay_status": "%s",
                      "fail_msg": "内层msg",
                      "partner_repay_no": function({
                        _req
                      }) {
                        return _req.body.repayRequestNo
                      },
                      "actual_repay_amount": "%s", //这个总金额是本+息，但是实际上代扣的金额还会加上费（代扣记录表中金额会加上费）
                      "repay_principal": "402.76", //不会校验这个本金和利息，只会校验总金额
                      "repay_interest": "34.5",
                      "repay_penalty_amount": 0,
                      "repay_intefine": 0,
                      "repay_fee": 0
                    }
                  }
                }''' % (msg, repay_status, repay_amt)
        self.update(api, mode)

    def zhongbang_zhongji_repay_trial(self, repay_principal=5000.0, repay_interest=30.0):
        """
        众邦中际试算接口
        此处mock试算金额的利息为30元，写死；
        code = 000000会继续调用接口：提前还款接口/normPrpymnt
        调用试算之后直接就会代扣失败的情况：
               code != 000000
               code = 000000， 本金不一致
               code = 000000， 利息超过当期利息
        """
        api = "/zhongbang/zhongbang_zhongji/NormPrpymntTrl"
        mode = {
                  "code": 0,
                  "message": "message",
                  "data": {
                    "code": "000000",
                    "msg": "外层msg",
                    "result": {
                      "actual_repay_amount": 6044.0,  # 这个金额不校验
                      "repay_principal": repay_principal,
                      "repay_interest": repay_interest,
                      "repay_penalty_amount": 0,
                      "repay_intefine": 0,
                      "repay_fee": 0
                    }
                  }
                }
        self.update(api, mode)

    def zhongbang_zhongji_repay_advance_payoff(self,  repay_status=1):
        """
        众邦中际提前结清接口
        repay_status 还款状态
            0: 还款中------调用代扣查询接口
            1:还款成功------调用代扣查询接口
            2：还款失败-------代扣失败
        该接口没有校验金额！！！
        """
        api = "/zhongbang/zhongbang_zhongji/normPrpymnt"
        mode = '''{
                  "code": 0,
                  "message": "message",
                  "data": {
                    "code": "000000",
                    "msg": "msg",
                    "result": {
                      "repay_status": "%s",
                      "fail_msg": "fail_msg",
                      "partner_repay_no": function({
                        _req
                      }) {
                        return _req.body.requestNo
                      },
                      "actual_repay_amount": 6030.51,
                      "repay_principal": 90,
                      "repay_interest": 10,
                      "repay_penalty_amount": 0,
                      "repay_intefine": 0,
                      "repay_fee": 0
                    }
                  }
                }''' % (repay_status)
        self.update(api, mode)

    def zhongbang_zhongji_withagreeshar(self):
            """
           众邦中际协议共享，这个接口不校验任何code状态，只要走预签约，它就会导致card_bind表中的绑卡状态是成功
            """
            api = "/zhongbang/zhongbang_zhongji/withAgreeShar"
            mode = '''{
                      "code": 0,
                      "message": "message",
                      "data": {
                        "code": "000000",  
                        "msg": "msg",
                        "result": {
                          "RetCd": "000000",
                          "RetInf": "111"
                        }
                      }
                    }'''
            self.update(api, mode)


if __name__ == "__main__":
    pass
