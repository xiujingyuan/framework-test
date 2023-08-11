# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class RepayLanzhouMock(Easymock):
    def update_pre_tied_card(self, resp_code="9999"):
        api = "/lanzhou/haoyue/preTiedCard"
        mode = {
            "transDate": "2020-10-12",
            "transTime": "12:02:22",
            "respCode": resp_code,
            "respMsg": "交易接收成功"
        }
        self.update(api, mode)

    def update_tied_card(self, resp_code="9999"):
        api = "/lanzhou/haoyue/tiedCard"
        mode = {
            "transDate": "2020-10-12",
            "transTime": "12:02:22",
            "respCode": resp_code,
            "respMsg": "交易接收成功"
        }
        self.update(api, mode)

    def update_lanzhou_statement(self, is_compensate, loan_id, compensate_amount, period):
        api = '/lanzhou/statement'
        compensate_date = get_calc_date(datetime.now(), day=-1, fmt='%Y/%m/%d')
        repay_date = get_calc_date(datetime.now(), day=0, fmt='%Y/%m/%d')
        compensate_mode = {
            "code": 0,
            "message": "",
            "data": [
                {
                    "contractNo": "4g2x8cn0n8",
                    "serialNo": None,
                    "productCode": "KN-DEBX-ZKBC",
                    "amount": None,
                    "loanNo": loan_id,
                    "productTerm": None,
                    "status": None,
                    "finishAt": None,
                    "remark": "代偿",
                    "term": "{0}".format(period),
                    "totalAmount": None,
                    "principalAmount": None,
                    "interestAmount": None,
                    "serviceCharge": None,
                    "otherServiceCharge": None,
                    "guaranteeFee": None,
                    "overdueFine": None,
                    "liquidatedDamages": None,
                    "mitigateAmount": None,
                    "tradeType": "现金分期",
                    "realRepayAt": None,
                    "recordedAt": None,
                    "isAheadRepay": None,
                    "compensatoryAmount": "{0}".format(compensate_amount),
                    "compensatoryAt": compensate_date
                }
            ]
        }
        repay_mode = {
            "code": 0,
            "message": "",
            "data": [
                {
                    "contractNo": "6qldt83s9f",
                    "serialNo": "",
                    "productCode": "KN-DEBX-ZKBC",
                    "amount": None,
                    "loanNo": loan_id,
                    "productTerm": None,
                    "status": 1,
                    "finishAt": None,
                    "remark": "还款",
                    "term": "{0}".format(period),
                    "totalAmount": "694.06",
                    "principalAmount": "644.06",
                    "interestAmount": "50.00",
                    "serviceCharge": "0.00",
                    "otherServiceCharge": "0.00",
                    "guaranteeFee": "0.00",
                    "overdueFine": "0.00",
                    "liquidatedDamages": "0.00",
                    "mitigateAmount": "0.00",
                    "tradeType": "现金分期",
                    "realRepayAt": repay_date,
                    "recordedAt": repay_date,
                    "isAheadRepay": "0",
                    "compensatoryAmount": None,
                    "compensatoryAt": None
                }
            ]
        }
        self.update(api, compensate_mode if is_compensate else repay_mode)

    # S成功、F失败
    def update_tied_card_query(self, re_code="S", resp_code="9999"):
        api = "/lanzhou/haoyue/tiedCardQuery"
        mode = {
            "msgId": get_random_str(),
            "reCode": re_code,
            "bizRespCode": resp_code,
            "bizRespMsg": "签约查询自动化",
            "transDate": "2020-10-12",
            "transTime": "12:10:51",
            "respCode": "9999",
            "respMsg": "签约查询自动化"
        }
        self.update(api, mode)

    def update_repay_apply(self, resp_code="9999"):
        api = "/lanzhou/haoyue/offlineRepaymentApply"
        mode = {
            "transDate": get_date(fmt="%Y-%m-%d"),
            "transTime": "10:44:25",
            "respCode": resp_code,
            "respMsg": "自动化测试"
        }
        self.update(api, mode)

    # // 交易处理成功
    # respCode = 9999 + state:4
    # // 交易处理失败
    # respCode = 9000 / 9999 + 2 / 5
    # // 交易处理中
    # respCode = 0100 / 1100 / 1300
    # // 交易请求成功
    # respCode = 0000
    # // 交易请求失败respCode = 1000 / 1200
    # // 重试
    # respCode = 未知code
    # // state: 1 - 代扣成功；2 - 代扣失败；3 - 还款中；4 - 还款成功；5 - 还款失败
    def update_repay_query(self, resp_code="9999", state=1, rpyBondComAmt=1.81, rpyBankAmt=348.88, repayDate=None):
        api = "/lanzhou/haoyue/repaymentQuery"
        repayDate = repayDate if repayDate is not None else get_date(fmt="%Y-%m-%d")
        mode = '''{
          "transDate": "%s",
          "transTime": "10:20:30",
          "respCode": %s,
          "respMsg": "自动化测试查询结果",
          "serialno": function({
            _req
          }) {
            return _req.body.serialno
          },
          "rpyBondComAmt": %s,
          "rpyChannelAmt": 0,
          "rpyBankAmt": %s,
          "state": %s,
          "rpyDate": "%s"
        }''' % (get_date(fmt="%Y-%m-%d"), resp_code, rpyBondComAmt, rpyBankAmt, state, repayDate)
        self.update(api, mode)

    def update_repay_trail(self, resp_code="9999"):
        api = "/lanzhou/haoyue/repaymentTrial"
        mode = {
            "transDate": get_date(fmt="%Y-%m-%d"),
            "transTime": "10:44:25",
            "respCode": resp_code,
            "respMsg": "自动化测试"
        }
        self.update(api, mode)

    def update_repay_trail_query(self, loan_id, resp_code="9999", paynormamt=4000.00, payInteamt=4.42,
                                 paytotalamt=4013.23):
        api = "/lanzhou/haoyue/repaymentTrialQuery"
        mode = {
            "transDate": get_date(fmt="%Y-%m-%d"),
            "transTime": "10:20:20",
            "respCode": resp_code,
            "respMsg": "自动化试算查询",
            "loanid": loan_id,
            "paynormamt": paynormamt,
            "payInteamt": payInteamt,
            "payEnteamt": 0.00,
            "fee": 0.00,
            "paytotalamt": paytotalamt,
            "paydate": get_date(fmt="%Y%m%d")
        }
        self.update(api, mode)

    def update_repay_trail_notice(self, loan_id, resp_code="9999"):
        api = "/lanzhou/haoyue/repaymentTrialNotice"
        mode = {
            "transDate": "2020-09-02",
            "transTime": "2020-09-02",
            "respCode": resp_code,
            "respMsg": "成功",
            "loanid": loan_id,
            "paynormamt": 809.20,
            "payInteamt": 20.00,
            "payEnteamt": 0.00,
            "fee": 0.00,
            "paytotalamt": 829.20,
            "paydate": "2020-09-03"
        }
        self.update(api, mode)


if __name__ == "__main__":
    pass
